"""
Static translation dictionary for all user-facing medical output.

Internal logic always uses canonical English identifiers.
This module translates them to the patient's language at response time.

Supported language codes (from language_detector.py):
    en  — English
    hi  — Hindi (Devanagari)
    mr  — Marathi (Devanagari)

For any unsupported code, English is returned unchanged.
"""

import re
from typing import Optional

# ── Departments ───────────────────────────────────────────────────────────────

DEPARTMENTS: dict[str, dict[str, str]] = {
    "Cardiology": {
        "en": "Cardiology",
        "hi": "हृदय रोग विभाग",
        "mr": "हृदयरोग विभाग",
    },
    "General Medicine": {
        "en": "General Medicine",
        "hi": "सामान्य चिकित्सा विभाग",
        "mr": "सर्वसाधारण औषध विभाग",
    },
    "Emergency Medicine": {
        "en": "Emergency Medicine",
        "hi": "आपातकालीन विभाग",
        "mr": "आपत्कालीन विभाग",
    },
    "ENT": {
        "en": "ENT (Ear, Nose & Throat)",
        "hi": "नाक-कान-गला विभाग",
        "mr": "कान-नाक-घसा विभाग",
    },
    "Obstetrics & Gynecology": {
        "en": "Obstetrics & Gynecology",
        "hi": "प्रसूती व स्त्रीरोग विभाग",
        "mr": "प्रसूती व स्त्रीरोग विभाग",
    },
    "Neurology": {
        "en": "Neurology",
        "hi": "तंत्रिका विज्ञान विभाग",
        "mr": "मेंदूरोग विभाग",
    },
    "General Surgery": {
        "en": "General Surgery",
        "hi": "सामान्य शल्य चिकित्सा विभाग",
        "mr": "सर्वसाधारण शस्त्रक्रिया विभाग",
    },
    "Orthopaedics": {
        "en": "Orthopaedics",
        "hi": "हड्डी रोग विभाग",
        "mr": "अस्थिरोग विभाग",
    },
    "Dermatology": {
        "en": "Dermatology",
        "hi": "त्वचा रोग विभाग",
        "mr": "त्वचारोग विभाग",
    },
    "Ophthalmology": {
        "en": "Ophthalmology",
        "hi": "नेत्र रोग विभाग",
        "mr": "नेत्ररोग विभाग",
    },
    "Urology": {
        "en": "Urology",
        "hi": "मूत्र रोग विभाग",
        "mr": "मूत्ररोग विभाग",
    },
    "Dental": {
        "en": "Dental",
        "hi": "दंत चिकित्सा विभाग",
        "mr": "दंत विभाग",
    },
}

# ── Priority ──────────────────────────────────────────────────────────────────

PRIORITIES: dict[str, dict[str, str]] = {
    "Emergency": {
        "en": "Emergency",
        "hi": "आपातकाल",
        "mr": "आपत्कालीन",
    },
    "Urgent": {
        "en": "Urgent",
        "hi": "तत्काल",
        "mr": "तातडीचे",
    },
    "Routine": {
        "en": "Routine",
        "hi": "सामान्य",
        "mr": "नियमित",
    },
}

# ── Emergency banner ──────────────────────────────────────────────────────────

EMERGENCY_BANNER: dict[str, str] = {
    "en": "🚨 EMERGENCY — Seek immediate medical attention",
    "hi": "🚨 आपातकाल — तुरंत चिकित्सकीय सहायता लें",
    "mr": "🚨 आपत्कालीन — त्वरित वैद्यकीय मदत घ्या",
}

# ── Advice ────────────────────────────────────────────────────────────────────

ADVICE: dict[str, dict[str, str]] = {
    "emergency": {
        "en": "Emergency detected. Please seek urgent medical care.",
        "hi": "आपातकालीन स्थिति है। कृपया तुरंत चिकित्सकीय सहायता लें।",
        "mr": "आपत्कालीन स्थिती आहे. कृपया त्वरित वैद्यकीय मदत घ्या.",
    },
    "routine": {
        "en": "Based on your symptoms, this looks like a routine medical concern.",
        "hi": "आपके लक्षणों के आधार पर, यह एक सामान्य चिकित्सा समस्या लगती है।",
        "mr": "तुमच्या लक्षणांच्या आधारे, हे एक सामान्य वैद्यकीय कारण वाटते.",
    },
}

# ── Recommended tests ─────────────────────────────────────────────────────────

TESTS: dict[str, dict[str, str]] = {
    "Vitals check": {
        "en": "Vitals check",
        "hi": "जीवन संकेत जांच",
        "mr": "जीवनचिन्ह तपासणी",
    },
    "ECG": {
        "en": "ECG",
        "hi": "ईसीजी",
        "mr": "ईसीजी",
    },
    "Troponin": {
        "en": "Troponin",
        "hi": "ट्रोपोनिन परीक्षण",
        "mr": "ट्रोपोनिन चाचणी",
    },
    "CBC": {
        "en": "CBC (Complete Blood Count)",
        "hi": "सीबीसी (पूर्ण रक्त गणना)",
        "mr": "सीबीसी (संपूर्ण रक्त मोजणी)",
    },
    "Blood pressure check": {
        "en": "Blood pressure check",
        "hi": "रक्तचाप जांच",
        "mr": "रक्तदाब तपासणी",
    },
    "Chest X-ray": {
        "en": "Chest X-ray",
        "hi": "छाती का एक्स-रे",
        "mr": "छातीचा एक्स-रे",
    },
    "Blood tests": {
        "en": "Blood tests",
        "hi": "रक्त परीक्षण",
        "mr": "रक्त चाचणी",
    },
    "Blood Sugar": {
        "en": "Blood Sugar",
        "hi": "रक्त शर्करा",
        "mr": "रक्तातील साखर",
    },
    "Neurological examination": {
        "en": "Neurological examination",
        "hi": "तंत्रिका संबंधी परीक्षण",
        "mr": "मज्जासंस्था तपासणी",
    },
    "ENT examination": {
        "en": "ENT examination",
        "hi": "नाक-कान-गला जांच",
        "mr": "कान-नाक-घसा तपासणी",
    },
    "Otoscopy": {
        "en": "Otoscopy",
        "hi": "कान की जांच",
        "mr": "कानाची तपासणी",
    },
    "Pregnancy test": {
        "en": "Pregnancy test",
        "hi": "गर्भावस्था परीक्षण",
        "mr": "गर्भधारणा चाचणी",
    },
    "Pelvic examination": {
        "en": "Pelvic examination",
        "hi": "श्रोणि परीक्षण",
        "mr": "श्रोणि तपासणी",
    },
    "Ultrasound": {
        "en": "Ultrasound",
        "hi": "अल्ट्रासाउंड",
        "mr": "अल्ट्रासाऊंड",
    },
    "Blood group": {
        "en": "Blood group",
        "hi": "रक्त समूह",
        "mr": "रक्तगट",
    },
    "X-ray": {
        "en": "X-ray",
        "hi": "एक्स-रे",
        "mr": "एक्स-रे",
    },
    "MRI": {
        "en": "MRI",
        "hi": "एमआरआई",
        "mr": "एमआरआय",
    },
    "Urine test": {
        "en": "Urine test",
        "hi": "मूत्र परीक्षण",
        "mr": "लघवी चाचणी",
    },
    "Skin biopsy": {
        "en": "Skin biopsy",
        "hi": "त्वचा बायोप्सी",
        "mr": "त्वचा बायोप्सी",
    },
    "Eye examination": {
        "en": "Eye examination",
        "hi": "नेत्र परीक्षण",
        "mr": "डोळ्यांची तपासणी",
    },
    "Anti-rabies vaccination": {
        "en": "Anti-rabies vaccination",
        "hi": "रेबीज रोधी टीका",
        "mr": "रेबीज विरोधी लस",
    },
    "Wound care": {
        "en": "Wound care",
        "hi": "घाव की देखभाल",
        "mr": "जखमेची काळजी",
    },
    "Anti-venom": {
        "en": "Anti-venom",
        "hi": "विष-विरोधी उपचार",
        "mr": "विष-विरोधी उपचार",
    },
    "Dental examination": {
        "en": "Dental examination",
        "hi": "दांत की जांच",
        "mr": "दात तपासणी",
    },
}

# ── Reasoning labels (canonical symptom_id → text) ────────────────────────────

REASONING: dict[str, dict[str, str]] = {
    # Symptom labels
    "Fever reported": {
        "en": "Fever reported",
        "hi": "बुखार की शिकायत",
        "mr": "ताप आल्याची तक्रार",
    },
    "Cough reported": {
        "en": "Cough reported",
        "hi": "खांसी की शिकायत",
        "mr": "खोकला असल्याची तक्रार",
    },
    "Chest pain reported": {
        "en": "Chest pain reported",
        "hi": "छाती में दर्द की शिकायत",
        "mr": "छातीत दुखण्याची तक्रार",
    },
    "Difficulty breathing reported": {
        "en": "Difficulty breathing reported",
        "hi": "सांस लेने में कठिनाई की शिकायत",
        "mr": "श्वास घेण्यास त्रास असल्याची तक्रार",
    },
    "Headache reported": {
        "en": "Headache reported",
        "hi": "सिर दर्द की शिकायत",
        "mr": "डोकेदुखीची तक्रार",
    },
    "Sore throat reported": {
        "en": "Sore throat reported",
        "hi": "गले में दर्द की शिकायत",
        "mr": "घसा दुखण्याची तक्रार",
    },
    "Ear pain reported": {
        "en": "Ear pain reported",
        "hi": "कान में दर्द की शिकायत",
        "mr": "कान दुखण्याची तक्रार",
    },
    "Abdominal pain reported": {
        "en": "Abdominal pain reported",
        "hi": "पेट दर्द की शिकायत",
        "mr": "पोटदुखीची तक्रार",
    },
    "Vomiting reported": {
        "en": "Vomiting reported",
        "hi": "उल्टी की शिकायत",
        "mr": "उलटी होण्याची तक्रार",
    },
    "Diarrhea reported": {
        "en": "Diarrhea reported",
        "hi": "दस्त की शिकायत",
        "mr": "जुलाबाची तक्रार",
    },
    "Bleeding reported": {
        "en": "Bleeding reported",
        "hi": "रक्तस्राव की शिकायत",
        "mr": "रक्तस्रावाची तक्रार",
    },
    "Loss of consciousness or fainting reported": {
        "en": "Loss of consciousness or fainting reported",
        "hi": "बेहोशी या मूर्छा की शिकायत",
        "mr": "शुद्ध हरपणे किंवा बेशुद्धीची तक्रार",
    },
    "Pregnancy-related concern reported": {
        "en": "Pregnancy-related concern reported",
        "hi": "गर्भावस्था से संबंधित समस्या",
        "mr": "गर्भधारणेशी संबंधित समस्या",
    },
    # Emergency reasons
    "Chest pain reported": {
        "en": "Chest pain reported",
        "hi": "छाती में दर्द — आपातकालीन लक्षण",
        "mr": "छातीत दुखणे — आपत्कालीन लक्षण",
    },
    "Difficulty breathing / shortness of breath": {
        "en": "Difficulty breathing / shortness of breath",
        "hi": "सांस लेने में कठिनाई",
        "mr": "श्वास घेण्यास त्रास",
    },
    "Loss of consciousness": {
        "en": "Loss of consciousness",
        "hi": "बेहोशी",
        "mr": "शुद्ध हरपणे",
    },
    "Possible stroke symptoms": {
        "en": "Possible stroke symptoms",
        "hi": "संभावित लकवे के लक्षण",
        "mr": "संभाव्य पक्षाघाताची लक्षणे",
    },
    "Seizure / convulsion": {
        "en": "Seizure / convulsion",
        "hi": "दौरा / मिर्गी",
        "mr": "झटका / फेफरे",
    },
    "Pregnancy with complication": {
        "en": "Pregnancy with complication",
        "hi": "गर्भावस्था में जटिलता",
        "mr": "गर्भधारणेत गुंतागुंत",
    },
    "Snake bite": {
        "en": "Snake bite",
        "hi": "सांप का काटना",
        "mr": "सापाने चावणे",
    },
    "Animal bite — rabies risk": {
        "en": "Animal bite — rabies risk",
        "hi": "जानवर का काटना — रेबीज का खतरा",
        "mr": "प्राण्याने चावणे — रेबीजचा धोका",
    },
    "Active labor": {
        "en": "Active labor",
        "hi": "प्रसव पीड़ा",
        "mr": "प्रसूती वेदना",
    },
    "Vaginal bleeding": {
        "en": "Vaginal bleeding",
        "hi": "योनि से रक्तस्राव",
        "mr": "योनीतून रक्तस्राव",
    },
    "Reduced fetal movement": {
        "en": "Reduced fetal movement",
        "hi": "गर्भ में हलचल कम",
        "mr": "बाळाची हालचाल कमी",
    },
    "Emergency phrase detected in text": {
        "en": "Emergency phrase detected in text",
        "hi": "पाठ में आपातकालीन स्थिति का उल्लेख",
        "mr": "मजकुरात आपत्कालीन स्थिती आढळली",
    },
    "Severe abdominal pain — escalated": {
        "en": "Severe abdominal pain — escalated",
        "hi": "गंभीर पेट दर्द — आपातकालीन",
        "mr": "तीव्र पोटदुखी — आपत्कालीन",
    },
    "Severe headache — escalated": {
        "en": "Severe headache — escalated",
        "hi": "गंभीर सिर दर्द — आपातकालीन",
        "mr": "तीव्र डोकेदुखी — आपत्कालीन",
    },
    "Severe back pain — escalated": {
        "en": "Severe back pain — escalated",
        "hi": "गंभीर पीठ दर्द — आपातकालीन",
        "mr": "तीव्र पाठदुखी — आपत्कालीन",
    },
}

# ── Duration + severity templates ─────────────────────────────────────────────

_DURATION_TEMPLATE: dict[str, str] = {
    "en": "Symptoms present for {duration}",
    "hi": "लक्षण {duration} से हैं",
    "mr": "लक्षणे {duration} पासून आहेत",
}

_SEVERITY_TEMPLATE: dict[str, str] = {
    "en": "{severity} severity reported",
    "hi": "{severity} गंभीरता की शिकायत",
    "mr": "{severity} तीव्रतेची तक्रार",
}

_SEVERITY_LABELS: dict[str, dict[str, str]] = {
    "severe": {"en": "Severe", "hi": "गंभीर", "mr": "तीव्र"},
    "moderate": {"en": "Moderate", "hi": "मध्यम", "mr": "मध्यम"},
    "mild": {"en": "Mild", "hi": "हल्की", "mr": "सौम्य"},
}

_ROUTED_TEMPLATE: dict[str, str] = {
    "en": "Routed to {department} based on symptom pattern",
    "hi": "{department} में भेजा गया — लक्षणों के आधार पर",
    "mr": "{department} — लक्षणांच्या आधारे",
}


# ── Public translation functions ──────────────────────────────────────────────

def _lang(code: Optional[str]) -> str:
    """Normalise language code; fall back to 'en'."""
    if code in ("hi", "mr"):
        return code
    return "en"


def translate_department(dept: str, lang: Optional[str]) -> str:
    l = _lang(lang)
    return DEPARTMENTS.get(dept, {}).get(l, dept)


def translate_priority(priority: str, lang: Optional[str]) -> str:
    l = _lang(lang)
    return PRIORITIES.get(priority, {}).get(l, priority)


def translate_emergency_banner(lang: Optional[str]) -> str:
    return EMERGENCY_BANNER.get(_lang(lang), EMERGENCY_BANNER["en"])


def translate_advice(advice: str, lang: Optional[str], *, emergency: bool = False) -> str:
    l = _lang(lang)
    if l == "en":
        return advice
    key = "emergency" if emergency else "routine"
    return ADVICE[key].get(l, advice)


def translate_test(test: str, lang: Optional[str]) -> str:
    l = _lang(lang)
    return TESTS.get(test, {}).get(l, test)


def translate_reasoning_item(item: str, lang: Optional[str]) -> str:
    """Translate a single reasoning string.

    Handles:
    - Static phrases (from REASONING dict)
    - Dynamic duration strings:  "Symptoms present for 3 days"
    - Dynamic severity strings:  "Severe severity reported"
    - Dynamic routing strings:   "Routed to Cardiology based on symptom pattern"
    """
    l = _lang(lang)
    if l == "en":
        return item

    # Static lookup
    if item in REASONING:
        return REASONING[item].get(l, item)

    # Dynamic: "Symptoms present for X"
    m = re.match(r"^Symptoms present for (.+)$", item)
    if m:
        return _DURATION_TEMPLATE[l].format(duration=m.group(1))

    # Dynamic: "X severity reported"
    m = re.match(r"^(\w+) severity reported$", item, re.IGNORECASE)
    if m:
        sev_en = m.group(1).lower()
        sev_translated = _SEVERITY_LABELS.get(sev_en, {}).get(l, m.group(1))
        return _SEVERITY_TEMPLATE[l].format(severity=sev_translated)

    # Dynamic: "Routed to X based on symptom pattern"
    m = re.match(r"^Routed to (.+) based on symptom pattern$", item)
    if m:
        dept_translated = translate_department(m.group(1), l)
        return _ROUTED_TEMPLATE[l].format(department=dept_translated)

    # Unknown — return as-is
    return item


def translate_response(response: dict, lang: Optional[str]) -> dict:
    """Translate all user-facing fields in a triage response dict in-place."""
    l = _lang(lang)
    if l == "en":
        return response

    is_emergency = bool(response.get("emergency"))

    if "department" in response:
        response["department"] = translate_department(response["department"], l)

    if "priority" in response:
        response["priority"] = translate_priority(response["priority"], l)

    if "advice" in response:
        response["advice"] = translate_advice(response["advice"], l, emergency=is_emergency)

    if "recommended_tests" in response and response["recommended_tests"]:
        response["recommended_tests"] = [
            translate_test(t, l) for t in response["recommended_tests"]
        ]

    if "reasoning" in response and response["reasoning"]:
        response["reasoning"] = [
            translate_reasoning_item(r, l) for r in response["reasoning"]
        ]

    return response
