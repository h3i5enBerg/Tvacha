from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import torch
import torch.nn as nn
from torchvision import models

from app.schemas import ConditionPrediction

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _ClinicalClass:
    name: str
    category: str


CLINICAL_CLASSES: tuple[_ClinicalClass, ...] = (
    _ClinicalClass("Eczema / Dermatitis", "Inflammatory"),
    _ClinicalClass("Fungal Infection (Tinea)", "Infectious"),
    _ClinicalClass("Psoriasis", "Inflammatory"),
    _ClinicalClass("Contact Dermatitis", "Inflammatory"),
    _ClinicalClass("Acne / Folliculitis", "Inflammatory"),
    _ClinicalClass("Benign Nevus / Pigmented Lesion", "Pigmented"),
    _ClinicalClass("Suspicious Lesion — Clinical Review", "Triage Alert"),
)

DEFAULT_HF_MODEL_ID = os.getenv(
    "TVACHA_HF_MODEL_ID",
    "Anwarkh1/Skin_Cancer-Image_Classification",
)


def _infer_category(label: str) -> str:
    """Map an arbitrary model label to one of the four clinical categories."""
    lower = label.lower()
    if any(k in lower for k in ("melanoma", "carcinoma", "malignant", "suspicious", "cancer", "bcc", "scc", "akiec")):
        return "Triage Alert"
    if any(k in lower for k in ("tinea", "fungal", "ringworm", "candida", "infectious", "herpes", "scabies")):
        return "Infectious"
    if any(k in lower for k in ("nevus", "naevus", "pigment", "keratosis", "lentigo", "bkl", "df", "vasc")):
        return "Pigmented"
    return "Inflammatory"


class SkinConditionClassifier:
    """Lightweight skin lesion classifier with HF primary and MobileNetV3 fallback."""

    def __init__(self, hf_model_id: str | None = None) -> None:
        self._device = torch.device("cpu")
        self._loaded = False
        self._backend_name = "uninitialized"
        self._hf_model: nn.Module | None = None
        self._hf_id2label: dict[int, str] = {}
        self._fallback_model: nn.Module | None = None

        target_hf_id = hf_model_id or DEFAULT_HF_MODEL_ID
        if not self._try_load_hf_model(target_hf_id):
            self._load_mobilenet_fallback()

    @property
    def is_loaded(self) -> bool:
        """Return True once a classification backbone is ready for inference."""
        return self._loaded

    @property
    def backend_name(self) -> str:
        """Return the active model backend identifier."""
        return self._backend_name

    def _try_load_hf_model(self, model_id: str) -> bool:
        """Attempt to load a Hugging Face vision classifier from local cache or hub."""
        try:
            from transformers import AutoModelForImageClassification  # type: ignore[import-not-found]
        except ImportError:
            logger.info("transformers not installed; using MobileNetV3 fallback.")
            return False

        allow_remote = os.getenv("TVACHA_ALLOW_HF_DOWNLOAD", "0") == "1"
        try:
            model = AutoModelForImageClassification.from_pretrained(
                model_id,
                local_files_only=not allow_remote,
            )
            model.eval()
            model.to(self._device)
            raw_id2label = getattr(model.config, "id2label", {}) or {}
            self._hf_id2label = {int(k): str(v) for k, v in raw_id2label.items()}
            self._hf_model = model
            self._backend_name = f"hf:{model_id}"
            self._loaded = True
            return True
        except Exception as exc:
            logger.info("HF model '%s' unavailable (%s); falling back to MobileNetV3.", model_id, exc)
            return False

    def _load_mobilenet_fallback(self) -> None:
        """Load deterministic MobileNetV3-Small mapped to 7 clinical categories."""
        try:
            backbone = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
        except Exception:
            torch.manual_seed(42)
            backbone = models.mobilenet_v3_small(weights=None)

        in_features = backbone.classifier[-1].in_features
        torch.manual_seed(42)
        backbone.classifier[-1] = nn.Linear(in_features, len(CLINICAL_CLASSES))
        backbone.eval()
        backbone.to(self._device)

        self._fallback_model = backbone
        self._backend_name = "torchvision:mobilenet_v3_small"
        self._loaded = True

    def predict(self, tensor: torch.Tensor) -> list[ConditionPrediction]:
        """Run inference on a (1, 3, 224, 224) tensor and return Top-3 predictions."""
        if not self._loaded:
            raise RuntimeError("SkinConditionClassifier is not loaded.")
        if tensor.ndim != 4 or tensor.shape[1:] != (3, 224, 224):
            raise ValueError(f"Expected tensor shape (N, 3, 224, 224), got {tuple(tensor.shape)}.")

        inputs = tensor.to(self._device, dtype=torch.float32)

        with torch.inference_mode():
            if self._hf_model is not None:
                logits = self._hf_model(pixel_values=inputs).logits
                probs = torch.softmax(logits[0], dim=-1)
                k = min(3, probs.shape[0])
                top_probs, top_indices = torch.topk(probs, k=k)
                return [
                    ConditionPrediction(
                        condition_name=(name := self._hf_id2label.get(int(idx), f"Condition {int(idx)}")),
                        confidence=round(float(prob), 4),
                        category=_infer_category(name),
                    )
                    for prob, idx in zip(top_probs.tolist(), top_indices.tolist())
                ]

            assert self._fallback_model is not None
            logits = self._fallback_model(inputs)
            probs = torch.softmax(logits[0], dim=-1)
            top_probs, top_indices = torch.topk(probs, k=3)
            return [
                ConditionPrediction(
                    condition_name=CLINICAL_CLASSES[int(idx)].name,
                    confidence=round(float(prob), 4),
                    category=CLINICAL_CLASSES[int(idx)].category,
                )
                for prob, idx in zip(top_probs.tolist(), top_indices.tolist())
            ]
