"""
Clinical rule engine — determines whether a case is an emergency.

Uses canonical symptom IDs from medical_dictionary.py and, as a second
pass, scans the raw text for EMERGENCY_PHRASES so high-risk phrases
that slipped through extraction still trigger the flag.
"""

import re
from typing import Any

from backend.services.medical_dictionary import EMERGENCY_PHRASES
from backend.services.text_normalizer import normalize


# Canonical symptom IDs that always indicate an emergency
_EMERGENCY_SYMPTOM_IDS: set[str] = {
    "chest_pain",
    "shortness_of_breath",
    "loss_of_consciousness",
    "stroke_symptoms",
    "seizure",
    "severe_bleeding",        # added as alias if ever extracted
    "bleeding",
    "anaphylaxis",            # covered by allergic_reaction + throat swelling
    "snake_bite",
    "dog_bite",               # potential rabies — urgent
    "labor_pain",
    "vaginal_bleeding",
    "reduced_fetal_movement",
}

# Human-readable labels for each emergency symptom
_EMERGENCY_LABELS: dict[str, str] = {
    "chest_pain":              "Chest pain reported",
    "shortness_of_breath":     "Difficulty breathing / shortness of breath",
    "loss_of_consciousness":   "Loss of consciousness",
    "stroke_symptoms":         "Possible stroke symptoms",
    "seizure":                 "Seizure / convulsion",
    "bleeding":                "Bleeding reported",
    "allergic_reaction":       "Possible severe allergic reaction",
    "snake_bite":              "Snake bite",
    "dog_bite":                "Animal bite — rabies risk",
    "labor_pain":              "Active labor",
    "vaginal_bleeding":        "Vaginal bleeding",
    "reduced_fetal_movement":  "Reduced fetal movement",
}

# Pre-compile emergency phrase scanner
_EMERGENCY_PHRASE_RE = re.compile(
    "|".join(re.escape(p) for p in EMERGENCY_PHRASES),
    re.IGNORECASE,
)


def detect_emergency(extracted: dict[str, Any], raw_text: str = "") -> dict[str, Any]:
    symptoms: list[str] = extracted.get("symptoms") or []
    severity: str | None = extracted.get("severity")

    reasons: list[str] = []
    emergency = False

    # Rule 1 — emergency symptom IDs
    for s in symptoms:
        if s in _EMERGENCY_SYMPTOM_IDS:
            emergency = True
            label = _EMERGENCY_LABELS.get(s, s.replace("_", " ").title())
            reasons.append(label)

    # Rule 2 — pregnancy + any bleeding or pain = emergency
    if "pregnancy" in symptoms and (
        "vaginal_bleeding" in symptoms
        or "bleeding" in symptoms
        or "abdominal_pain" in symptoms
        or "labor_pain" in symptoms
    ):
        emergency = True
        if "Pregnancy with complication" not in reasons:
            reasons.append("Pregnancy with complication")

    # Rule 3 — severe modifier on an otherwise-routine symptom escalates it
    if severity == "severe" and not emergency:
        for s in symptoms:
            if s in {"abdominal_pain", "headache", "back_pain"}:
                emergency = True
                reasons.append(f"Severe {s.replace('_', ' ')} — escalated")
                break

    # Rule 4 — raw text phrase scan catches anything missed by extraction
    if raw_text and not emergency:
        normalised = normalize(raw_text)
        if _EMERGENCY_PHRASE_RE.search(normalised):
            emergency = True
            reasons.append("Emergency phrase detected in text")

    return {"emergency": emergency, "reasons": reasons}
