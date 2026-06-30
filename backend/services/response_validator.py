from typing import Dict, Any

from backend.schemas.response import TriageResponse


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default


def validate_and_normalize(model_output: Dict[str, Any], *, fallback: TriageResponse) -> TriageResponse:
    """Validate model JSON output and map into TriageResponse.

    If malformed/missing fields, fallback to deterministic heuristic values.
    """
    if not isinstance(model_output, dict):
        return fallback

    department = model_output.get("department", fallback.department)
    priority = model_output.get("priority", fallback.priority)

    emergency = model_output.get("emergency")
    if emergency is None:
        # Map from priority if emergency is not provided.
        emergency = str(priority).lower() == "emergency"

    confidence = _safe_float(model_output.get("confidence"), fallback.confidence)
    advice = model_output.get("advice", fallback.advice)
    reasoning = model_output.get("reasoning", fallback.reasoning)
    recommended_tests = model_output.get("recommended_tests", fallback.recommended_tests)

    # Basic type guards
    if not isinstance(department, str) or not department.strip():
        department = fallback.department
    if not isinstance(priority, str) or not priority.strip():
        priority = fallback.priority
    if not isinstance(advice, str) or not advice.strip():
        advice = fallback.advice
    if not isinstance(reasoning, list):
        reasoning = fallback.reasoning
    if not isinstance(recommended_tests, list):
        recommended_tests = fallback.recommended_tests

    if not isinstance(emergency, bool):
        emergency = bool(emergency)

    reasoning = [str(item).strip() for item in reasoning if str(item).strip()][:5]
    recommended_tests = [str(item).strip() for item in recommended_tests if str(item).strip()][:4]

    return TriageResponse(
        department=department,
        priority=priority,
        emergency=emergency,
        confidence=confidence,
        advice=advice,
        language=fallback.language,
        reasoning=reasoning or fallback.reasoning,
        recommended_tests=recommended_tests or fallback.recommended_tests,
    )

