from __future__ import annotations

from contextlib import asynccontextmanager
import time
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.classifier import SkinConditionClassifier
from app.preprocessing import preprocess_lesion_image, validate_and_load_image
from app.schemas import DiagnosisResponse, SymptomInput
from app.triage import build_care_guidance, evaluate_triage


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the skin condition classifier once on application startup."""
    app.state.classifier = SkinConditionClassifier()
    yield


app = FastAPI(title="Tvacha Screening API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_classifier(request: Request) -> SkinConditionClassifier:
    classifier = getattr(request.app.state, "classifier", None)
    if classifier is None:
        classifier = SkinConditionClassifier()
        request.app.state.classifier = classifier
    return classifier


@app.get("/health")
def health_check(request: Request) -> dict[str, str | bool]:
    """Return service health and model readiness status."""
    classifier = getattr(request.app.state, "classifier", None)
    model_loaded = bool(classifier is not None and classifier.is_loaded)
    return {
        "status": "ok",
        "service": "tvacha-api",
        "model_loaded": model_loaded,
    }


@app.post("/predict", response_model=DiagnosisResponse)
async def predict_lesion(
    request: Request,
    image: UploadFile = File(...),
    symptoms: str = Form(...),
) -> DiagnosisResponse:
    """Run preliminary dermatological screening on an uploaded lesion image and symptoms."""
    try:
        symptom_input = SymptomInput.model_validate_json(symptoms)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    file_bytes = await image.read()
    try:
        pil_image = validate_and_load_image(file_bytes)
        tensor = preprocess_lesion_image(pil_image)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    classifier = _get_classifier(request)
    start_time = time.perf_counter()
    top_predictions = classifier.predict(tensor)
    triage = evaluate_triage(symptom_input, top_predictions)
    top_condition = top_predictions[0].condition_name if top_predictions else "Unspecified"
    guidance = build_care_guidance(top_condition, triage.urgency_level)
    inference_time_ms = max(1, int((time.perf_counter() - start_time) * 1000))

    return DiagnosisResponse(
        scan_id=str(uuid4()),
        top_predictions=top_predictions,
        triage=triage,
        guidance=guidance,
        inference_time_ms=inference_time_ms,
    )
