from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Tvacha Screening API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str | bool]:
    """Return service health and model readiness status."""
    return {
        "status": "ok",
        "service": "tvacha-api",
        "model_loaded": False,
    }
