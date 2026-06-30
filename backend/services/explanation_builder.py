from __future__ import annotations

from typing import Any


SYMPTOM_LABELS = {
    "fever": "Fever reported",
    "cough": "Cough reported",
    "chest_pain": "Chest pain reported",
    "shortness_of_breath": "Difficulty breathing reported",
    "headache": "Headache reported",
    "sore_throat": "Sore throat reported",
    "ear_pain": "Ear pain reported",
    "abdominal_pain": "Abdominal pain reported",
    "vomiting": "Vomiting reported",
    "diarrhea": "Diarrhea reported",
    "bleeding": "Bleeding reported",
    "loss_of_consciousness": "Loss of consciousness or fainting reported",
    "pregnancy": "Pregnancy-related concern reported",
}


RECOMMENDED_TESTS_BY_DEPARTMENT = {
    "Cardiology": ["ECG", "Troponin"],
    "Neurology": ["Neurological examination", "Blood pressure check"],
    "ENT": ["ENT examination", "Otoscopy"],
    "General Medicine": ["Vitals check", "CBC"],
    "Gynecology": ["Pregnancy test", "Pelvic examination"],
    "Emergency Medicine": ["Vitals check", "ECG", "Blood tests"],
}


def build_reasoning(
    *,
    extracted: dict[str, Any],
    emergency_info: dict[str, Any],
    department_info: dict[str, Any],
) -> list[str]:
    symptoms = extracted.get("symptoms") or []
    reasons: list[str] = []

    for emergency_reason in emergency_info.get("reasons") or []:
        if emergency_reason not in reasons:
            reasons.append(str(emergency_reason))

    for symptom in symptoms:
        label = SYMPTOM_LABELS.get(symptom, str(symptom).replace("_", " ").title())
        if label not in reasons:
            reasons.append(label)

    duration = extracted.get("duration")
    if duration:
        reasons.append(f"Symptoms present for {duration}")

    severity = extracted.get("severity")
    if severity:
        reasons.append(f"{str(severity).title()} severity reported")

    department = department_info.get("department")
    if department and not reasons:
        reasons.append(f"Routed to {department} based on symptom pattern")

    return reasons[:5]


def recommended_tests_for_department(department: str, *, emergency: bool = False) -> list[str]:
    tests = list(RECOMMENDED_TESTS_BY_DEPARTMENT.get(department, RECOMMENDED_TESTS_BY_DEPARTMENT["General Medicine"]))
    if emergency and "Vitals check" not in tests:
        tests.insert(0, "Vitals check")
    return tests[:4]
