import io
import json

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


def _make_dummy_png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (256, 256), color=(180, 120, 100)).save(buf, format="PNG")
    return buf.getvalue()


def test_health_reports_model_loaded() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "tvacha-api"
    assert payload["model_loaded"] is True


def test_predict_routine_symptoms_returns_low_urgency() -> None:
    symptoms_payload = {
        "body_location": "forearm",
        "duration_days": 3,
        "itching": True,
        "pain": False,
        "bleeding": False,
        "fever": False,
        "rapid_spread": False,
    }
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            files={"image": ("lesion.png", _make_dummy_png_bytes(), "image/png")},
            data={"symptoms": json.dumps(symptoms_payload)},
        )

    assert response.status_code == 200
    body = response.json()
    assert len(body["top_predictions"]) == 3
    assert body["triage"]["urgency_level"] == "low"
    assert body["scan_id"]
    assert body["inference_time_ms"] >= 1
    assert "disclaimer" in body["guidance"]


def test_predict_bleeding_escalates_to_high_urgency() -> None:
    symptoms_payload = {
        "body_location": "cheek",
        "duration_days": 4,
        "itching": False,
        "pain": False,
        "bleeding": True,
        "fever": False,
        "rapid_spread": False,
    }
    with TestClient(app) as client:
        response = client.post(
            "/predict",
            files={"image": ("lesion.png", _make_dummy_png_bytes(), "image/png")},
            data={"symptoms": json.dumps(symptoms_payload)},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["triage"]["urgency_level"] == "high"
    assert "Active bleeding reported" in body["triage"]["red_flags_triggered"]
