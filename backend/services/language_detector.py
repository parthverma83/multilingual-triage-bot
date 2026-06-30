import re
from typing import Dict, Any, Tuple


def _contains_any(text: str, needles: Tuple[str, ...]) -> bool:
    return any(n in text for n in needles)


def detect_language(text: str) -> Dict[str, Any]:
    """Lightweight language detection.

    Output fields:
      - language: canonical code used by the app/LLM prompts (en/hi/mr/auto)
      - normalized_text: cleaned text for rule-based processing
    """
    if not text or not text.strip():
        return {"language": "auto", "normalized_text": ""}

    # Normalize whitespace
    normalized = re.sub(r"\s+", " ", text.strip())

    # Unicode blocks heuristic
    # Devanagari block covers Hindi and Marathi
    if re.search(r"[\u0900-\u097F]", normalized):
        # Heuristic: Marathi often uses words like "आहे/आहेत/होत", "मला", "तुम्हाला"
        # Hindi often has "है/हैं", "मुझे"
        hi_markers = ("मुझे", "है", "हो रहा", "होता", "चाहिए", "दर्द")
        mr_markers = ("मला", "आहे", "येत", "ताप", "डोके", "दुखत")

        # If Marathi markers appear more, choose 'mr', else 'hi'
        score_hi = sum(1 for m in hi_markers if m in normalized)
        score_mr = sum(1 for m in mr_markers if m in normalized)
        language = "mr" if score_mr > score_hi else "hi"
        return {"language": language, "normalized_text": normalized}

    # Roman-script heuristics
    # Try to detect Hindi transliteration (common for chest pain etc.)
    hi_translit_markers = ("mujhe", "dard", "bukhar", "khansi", "saans")
    mr_translit_markers = ("mala", "taap", "dokyat", "dukht", "thand", "saans")
    if _contains_any(normalized.lower(), hi_translit_markers):
        return {"language": "hi", "normalized_text": normalized}
    if _contains_any(normalized.lower(), mr_translit_markers):
        return {"language": "mr", "normalized_text": normalized}

    # Default to English for roman script
    return {"language": "en", "normalized_text": normalized}

