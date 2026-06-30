"""
Normalize raw patient input before symptom matching.

Steps applied in order:
1. Unicode normalization (NFC) — fixes split Devanagari vowel signs
2. Chandrabindu / anusvara unification  साँ → सां
3. Lowercase English characters (Devanagari is case-free)
4. Collapse whitespace
5. Strip leading/trailing whitespace

Does NOT remove punctuation — periods can distinguish sentence boundaries
and exclamation marks carry severity signals.
"""

import re
import unicodedata


# Devanagari chandrabindu (U+0901) → anusvara (U+0902)
# Visually near-identical; unifying them prevents double-matching.
_CHANDRABINDU = "ँ"
_ANUSVARA = "ं"

# Common Hinglish spelling variants → canonical form
# Format: (pattern, replacement) — applied in order.
_HINGLISH_NORMALIZATIONS: list[tuple[str, str]] = [
    # saans / sans / saas → saans
    (r"\bsans\b", "saans"),
    (r"\bsaas\b", "saans"),
    # bukhar / bukhaar / bukhaar → bukhar
    (r"\bbukhaar\b", "bukhar"),
    # dard / derd → dard
    (r"\bderd\b", "dard"),
    # peeth / pith → peeth
    (r"\bpith\b", "peeth"),
    # daant / dant → daant
    (r"\bdant\b", "daant"),
    # khansi / khasi / khanshi → khansi
    (r"\bkhanshi\b", "khansi"),
    (r"\bkhasi\b", "khansi"),
    # ulti / ulta → ulti
    (r"\bulta\b", "ulti"),
    # chakkar / chaker → chakkar
    (r"\bchaker\b", "chakkar"),
    # petdard (run-together) → pet dard
    (r"\bpetdard\b", "pet dard"),
    # naak → naak (no change needed, just ensuring no typo variant)
    (r"\bnaakk\b", "naak"),
]

_HINGLISH_PATTERNS = [
    (re.compile(p, re.IGNORECASE), r)
    for p, r in _HINGLISH_NORMALIZATIONS
]

# Collapse multiple spaces/tabs/newlines into a single space
_WHITESPACE = re.compile(r"\s+")


def normalize(text: str) -> str:
    if not text:
        return ""

    # 1. Unicode NFC — recompose split characters (e.g. े + ा → composed forms)
    text = unicodedata.normalize("NFC", text)

    # 2. Unify chandrabindu → anusvara in Devanagari text
    text = text.replace(_CHANDRABINDU, _ANUSVARA)

    # 3. Lowercase (safe for Devanagari — codepoints are unaffected)
    text = text.lower()

    # 4. Hinglish spelling normalization
    for pattern, replacement in _HINGLISH_PATTERNS:
        text = pattern.sub(replacement, text)

    # 5. Collapse whitespace
    text = _WHITESPACE.sub(" ", text).strip()

    return text
