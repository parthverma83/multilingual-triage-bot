from typing import Dict, Any


def build_prompt(
    *,
    language: str,
    extracted: Dict[str, Any],
    emergency_info: Dict[str, Any],
    department_info: Dict[str, Any],
) -> str:
    symptoms = extracted.get("symptoms") or []
    duration = extracted.get("duration")
    severity = extracted.get("severity")
    department = department_info.get("department")

    emergency = emergency_info.get("emergency", False)

    # Force deterministic structured output from the model.
    # The response_validator will ensure schema correctness.
    return (
        "You are a medical triage assistant. "
        "Return ONLY valid JSON with the required schema. Do not include markdown.\n\n"
        f"Language: {language}\n\n"
        "Symptoms:\n"
        + ("\n".join([f"- {s}" for s in symptoms]) if symptoms else "- (not specified)" )
        + "\n\n"
        f"Duration: {duration if duration else 'unknown'}\n"
        f"Severity: {severity if severity else 'unknown'}\n"
        f"Possible Department: {department}\n"
        + ("Emergency Detected: true\n" if emergency else "Emergency Detected: false\n")
        + "\n"
        "Risk: "
        + ("Emergency" if emergency else "Routine")
        + "\n\n"
        "Return ONLY JSON. Example format:\n"
        "{\n"
        '  "department": "...",\n'
        '  "priority": "Routine|Urgent|Emergency",\n'
        '  "emergency": false,\n'
        '  "confidence": 0.0,\n'
        '  "advice": "...",\n'
        '  "reasoning": ["short reason 1", "short reason 2"],\n'
        '  "recommended_tests": ["test 1", "test 2"]\n'
        "}\n"
    )

