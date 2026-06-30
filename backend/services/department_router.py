from typing import Dict, Any, List


def route_department(extracted: Dict[str, Any]) -> Dict[str, Any]:
    symptoms: List[str] = extracted.get("symptoms") or []
    body_part = extracted.get("body_part")
    severity = extracted.get("severity")

    # Ordered from most-specific to least-specific — first match wins.

    # Obstetrics & Gynecology
    if "pregnancy" in symptoms or "labor_pain" in symptoms or "vaginal_bleeding" in symptoms:
        return {"department": "Obstetrics & Gynecology", "confidence": 0.9}

    # Cardiology
    if "chest_pain" in symptoms or "heart_palpitations" in symptoms or body_part == "chest":
        return {"department": "Cardiology", "confidence": 0.8}

    # Neurology
    if "stroke_symptoms" in symptoms or "seizure" in symptoms:
        return {"department": "Neurology", "confidence": 0.9}

    if "headache" in symptoms or "dizziness" in symptoms or body_part == "head":
        return {"department": "Neurology", "confidence": 0.75}

    # ENT
    if (
        "ear_pain" in symptoms
        or "ear_discharge" in symptoms
        or "hearing_loss" in symptoms
        or "sore_throat" in symptoms
        or body_part == "ear"
        or body_part == "throat"
    ):
        return {"department": "ENT", "confidence": 0.8}

    # Ophthalmology → mapped to General Medicine if no ophthalmology dept
    if "eye_symptoms" in symptoms or body_part == "eye":
        return {"department": "Ophthalmology", "confidence": 0.8}

    # General Surgery — severe or lower-right abdominal pain
    if "abdominal_pain" in symptoms and severity == "severe":
        return {"department": "General Surgery", "confidence": 0.75}

    # Orthopaedics
    if "fracture" in symptoms:
        return {"department": "Orthopaedics", "confidence": 0.85}

    if "joint_pain" in symptoms:
        return {"department": "Orthopaedics", "confidence": 0.7}

    # Dermatology
    if "rash" in symptoms or "burns" in symptoms or "skin_infection" in symptoms:
        return {"department": "Dermatology", "confidence": 0.75}

    # Urology
    if "urinary_symptoms" in symptoms:
        return {"department": "Urology", "confidence": 0.8}

    # Dental
    if "toothache" in symptoms:
        return {"department": "Dental", "confidence": 0.9}

    # General Medicine — everything else
    return {"department": "General Medicine", "confidence": 0.6}
