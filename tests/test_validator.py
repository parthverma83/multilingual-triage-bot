from backend.services.response_validator import validate_and_normalize


def test_validator_fills_missing_defaults(fallback_response):
    result = validate_and_normalize({"department": "", "confidence": "bad"}, fallback=fallback_response)

    assert result.department == fallback_response.department
    assert result.priority == fallback_response.priority
    assert result.emergency is False
    assert result.confidence == fallback_response.confidence
    assert result.advice == fallback_response.advice
    assert result.language == fallback_response.language
    assert result.reasoning == fallback_response.reasoning
    assert result.recommended_tests == fallback_response.recommended_tests


def test_validator_maps_emergency_from_priority(fallback_response):
    result = validate_and_normalize(
        {
            "department": "Emergency Medicine",
            "priority": "Emergency",
            "confidence": "0.91",
            "advice": "Seek urgent medical care.",
            "reasoning": ["Chest pain reported"],
            "recommended_tests": ["ECG"],
        },
        fallback=fallback_response,
    )

    assert result.emergency is True
    assert result.confidence == 0.91
    assert result.reasoning == ["Chest pain reported"]
    assert result.recommended_tests == ["ECG"]
