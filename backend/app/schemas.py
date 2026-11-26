from typing import Literal

from pydantic import BaseModel, Field


class SymptomInput(BaseModel):
    """Structured symptom context submitted alongside a lesion image."""

    body_location: str = Field(..., min_length=1)
    duration_days: int = Field(..., ge=0)
    itching: bool
    pain: bool
    bleeding: bool
    fever: bool
    rapid_spread: bool
    notes: str | None = None


class ConditionPrediction(BaseModel):
    """Single predicted dermatological condition with confidence score."""

    condition_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    category: str


class TriageResult(BaseModel):
    """Rule-based clinical urgency assessment combining predictions and symptoms."""

    urgency_level: Literal["low", "moderate", "high"]
    urgency_reason: str
    red_flags_triggered: list[str]


class CareGuidance(BaseModel):
    """Preliminary general and AYUSH supportive care guidance."""

    general_steps: list[str]
    ayush_supportive_care: list[str]
    when_to_see_doctor: str
    disclaimer: str


class DiagnosisResponse(BaseModel):
    """Top-level response payload for preliminary dermatological screening."""

    scan_id: str
    top_predictions: list[ConditionPrediction]
    triage: TriageResult
    guidance: CareGuidance
    inference_time_ms: int = Field(..., ge=0)
