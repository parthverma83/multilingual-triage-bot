import os
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INFERENCE_DIR = PROJECT_ROOT / "inference"

for path in (PROJECT_ROOT, INFERENCE_DIR):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)

os.environ.setdefault("APP_NAME", "MedRoute AI")
os.environ.setdefault("APP_VERSION", "1.0.0")
os.environ.setdefault("MODEL_PROVIDER", "runpod")
os.environ.setdefault("MODEL_ENDPOINT", "http://inference.test")
os.environ.setdefault("MODEL_API_KEY", "")
os.environ.setdefault("MODEL_TIMEOUT_SECONDS", "1")
os.environ.setdefault("MODEL_RETRY_ATTEMPTS", "2")
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "3306")
os.environ.setdefault("MYSQL_USER", "root")
os.environ.setdefault("MYSQL_PASSWORD", "")
os.environ.setdefault("MYSQL_DATABASE", "triage_test")
os.environ.setdefault("SKIP_MODEL_LOAD", "true")


@pytest.fixture
def fallback_response():
    from backend.schemas.response import TriageResponse

    return TriageResponse(
        department="General Medicine",
        priority="Routine",
        emergency=False,
        confidence=0.4,
        advice="Please consult a clinician if symptoms persist.",
        language="en",
    )
