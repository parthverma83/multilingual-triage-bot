from fastapi.testclient import TestClient

from backend.api import routes
from backend.app import app
from backend.services.model_service import BaseModelService
from backend.services.triage_engine import TriageEngine


class MockInferenceService(BaseModelService):
    async def generate(self, prompt: str, language: str = "auto") -> dict:
        return {
            "department": "General Medicine",
            "priority": "Routine",
            "emergency": False,
            "confidence": 0.77,
            "advice": "Take fluids and seek care if symptoms worsen.",
            "reasoning": ["Fever reported"],
            "recommended_tests": ["Vitals check", "CBC"],
        }


def test_end_to_end_triage_request_with_mocked_inference(monkeypatch):
    monkeypatch.setattr(routes, "engine", TriageEngine(model=MockInferenceService()))
    client = TestClient(app)

    response = client.post(
        "/api/v1/triage",
        json={
            "message": "I have fever and body pain",
            "language": "en",
            "conversation_id": "conv-test",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["department"]
    assert body["priority"]
    assert isinstance(body["emergency"], bool)
    assert "confidence" in body
    assert body["advice"]
    assert body["reasoning"]
    assert body["recommended_tests"]
