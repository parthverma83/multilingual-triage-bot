import pytest

from backend.services.model_service import BaseModelService
from backend.services.triage_engine import TriageEngine


class FakeModelService(BaseModelService):
    async def generate(self, prompt: str, language: str = "auto") -> dict:
        return {
            "department": "General Medicine",
            "priority": "Routine",
            "emergency": False,
            "confidence": 0.82,
            "advice": "Monitor symptoms and consult a doctor if they worsen.",
        }


@pytest.mark.asyncio
async def test_triage_pipeline_produces_valid_response():
    engine = TriageEngine(model=FakeModelService())

    result = await engine.process("I have fever and headache for two days", language="en")

    assert result.department
    assert result.priority
    assert isinstance(result.emergency, bool)
    assert 0 <= result.confidence <= 1
    assert result.advice
    assert result.language
    assert result.reasoning
    assert result.recommended_tests


@pytest.mark.asyncio
async def test_triage_pipeline_forces_emergency_override():
    engine = TriageEngine(model=FakeModelService())

    result = await engine.process("I have severe chest pain and cannot breathe", language="en")

    assert result.emergency is True
    assert result.priority == "Emergency"
    assert "Vitals check" in result.recommended_tests
