"""
Symptom extraction pipeline.

Flow:
    raw text
        → text_normalizer.normalize()
        → substring match against SYMPTOM_MAP vocabulary
        → duration / severity extraction
        → body_part inference
        → structured result dict
"""

import re
from typing import Any

from backend.services.medical_dictionary import (
    SYMPTOM_MAP,
    SEVERITY_SEVERE,
    SEVERITY_MILD,
)
from backend.services.text_normalizer import normalize


# ── Pre-compile match patterns at import time ─────────────────────────────────
# For each symptom, build one compiled regex that ORs all its phrases.
# Using \b word-boundaries for Latin; lookaround for Devanagari since
# \b doesn't cross Unicode script boundaries reliably.

def _build_pattern(phrases: list[str]) -> re.Pattern:
    parts = []
    for phrase in phrases:
        if any("ऀ" <= ch <= "ॿ" for ch in phrase):
            escaped = re.escape(phrase)
            parts.append(f"(?<![\\u0900-\\u097F]){escaped}(?![\\u0900-\\u097F])")
        else:
            parts.append(r"\b" + re.escape(phrase) + r"\b")
    return re.compile("|".join(parts), re.IGNORECASE)


# Dict[canonical_id → compiled pattern matching all languages]
_SYMPTOM_PATTERNS: dict[str, re.Pattern] = {
    symptom_id: _build_pattern(
        entry.get("english", [])
        + entry.get("hindi", [])
        + entry.get("marathi", [])
        + entry.get("hinglish", [])
    )
    for symptom_id, entry in SYMPTOM_MAP.items()
}

_SEVERITY_SEVERE_RE = re.compile(
    "|".join(re.escape(w) for w in SEVERITY_SEVERE), re.IGNORECASE
)
_SEVERITY_MILD_RE = re.compile(
    "|".join(re.escape(w) for w in SEVERITY_MILD), re.IGNORECASE
)

_DURATION_RE = re.compile(
    r"\b(\d+)\s*(day|days|week|weeks|month|months|hour|hours|hr|hrs"
    r"|din|hafte|mahine|ghanta|ghante)\b",
    re.IGNORECASE,
)

# Body part keywords → canonical label (first match wins)
_BODY_PART_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(chest|seene|chhaati|छाती|सीने)\b", re.IGNORECASE), "chest"),
    (re.compile(r"\b(ear|kaan|कान)\b", re.IGNORECASE), "ear"),
    (re.compile(r"\b(head|sir|sar|डोके|सिर)\b", re.IGNORECASE), "head"),
    (re.compile(r"\b(eye|aankh|डोळे|आँख)\b", re.IGNORECASE), "eye"),
    (re.compile(r"\b(back|peeth|पीठ|पाठ)\b", re.IGNORECASE), "back"),
    (re.compile(r"\b(stomach|abdomen|pet|पेट|पोट)\b", re.IGNORECASE), "abdomen"),
    (re.compile(r"\b(throat|gala|घसा|गला)\b", re.IGNORECASE), "throat"),
    (re.compile(r"\b(knee|ghutna|गुडघा|घुटना)\b", re.IGNORECASE), "knee"),
]


# ── Public API ────────────────────────────────────────────────────────────────

def extract_symptoms(message: str) -> dict[str, Any]:
    if not message or not message.strip():
        return {"symptoms": [], "duration": None, "severity": None, "body_part": None}

    text = normalize(message)

    symptoms: list[str] = [
        symptom_id
        for symptom_id, pattern in _SYMPTOM_PATTERNS.items()
        if pattern.search(text)
    ]

    severity: str | None = None
    if _SEVERITY_SEVERE_RE.search(text):
        severity = "severe"
    elif _SEVERITY_MILD_RE.search(text):
        severity = "mild"

    duration: str | None = None
    m = _DURATION_RE.search(text)
    if m:
        duration = f"{m.group(1)} {m.group(2)}"

    body_part: str | None = None
    for pattern, label in _BODY_PART_RULES:
        if pattern.search(text):
            body_part = label
            break

    return {
        "symptoms": symptoms,
        "duration": duration,
        "severity": severity,
        "body_part": body_part,
    }
