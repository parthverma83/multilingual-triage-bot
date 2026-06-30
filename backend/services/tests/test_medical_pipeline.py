"""
Multilingual medical pipeline tests.

Covers symptom extraction, emergency detection, and department routing
across English, Hindi, Marathi, and Hinglish inputs.

Run from project root:
    python -m pytest backend/services/tests/test_medical_pipeline.py -v
"""

import pytest

from backend.services.symptom_extractor import extract_symptoms
from backend.services.emergency_detector import detect_emergency
from backend.services.department_router import route_department


# ── Helpers ───────────────────────────────────────────────────────────────────

def pipeline(text: str) -> dict:
    extracted = extract_symptoms(text)
    emergency_info = detect_emergency(extracted, raw_text=text)
    department_info = route_department(extracted)
    return {
        "symptoms": extracted["symptoms"],
        "severity": extracted["severity"],
        "duration": extracted["duration"],
        "body_part": extracted["body_part"],
        "emergency": emergency_info["emergency"],
        "department": department_info["department"],
    }


# ── English scenarios ─────────────────────────────────────────────────────────

class TestEnglish:

    def test_chest_pain_emergency_cardiology(self):
        r = pipeline("I have chest pain radiating to my left arm")
        assert "chest_pain" in r["symptoms"]
        assert r["emergency"] is True
        assert r["department"] == "Cardiology"

    def test_fever_routine_general_medicine(self):
        r = pipeline("I have fever for 3 days with chills")
        assert "fever" in r["symptoms"]
        assert r["duration"] == "3 days"
        assert r["emergency"] is False
        assert r["department"] == "General Medicine"

    def test_ear_pain_ent(self):
        r = pipeline("My ear hurts and yellow fluid is coming out")
        assert r["department"] == "ENT"
        assert r["emergency"] is False

    def test_ear_discharge_ent(self):
        r = pipeline("There is yellow discharge from my ear")
        assert r["department"] == "ENT"

    def test_severe_abdominal_general_surgery(self):
        r = pipeline("I have severe abdominal pain on the lower right side")
        assert "abdominal_pain" in r["symptoms"]
        assert r["severity"] == "severe"
        assert r["department"] == "General Surgery"

    def test_pregnancy_bleeding_obstetrics(self):
        r = pipeline("I am 32 weeks pregnant and I am bleeding")
        assert "pregnancy" in r["symptoms"]
        assert r["emergency"] is True
        assert r["department"] == "Obstetrics & Gynecology"

    def test_shortness_of_breath_emergency(self):
        r = pipeline("I am having difficulty breathing and cannot breathe")
        assert r["emergency"] is True

    def test_stroke_symptoms_emergency_neurology(self):
        r = pipeline("My face is drooping and I cannot speak properly, arm weakness")
        assert r["emergency"] is True
        assert r["department"] == "Neurology"

    def test_seizure_emergency(self):
        r = pipeline("The patient is having a seizure and shaking uncontrollably")
        assert r["emergency"] is True

    def test_snake_bite_emergency(self):
        r = pipeline("A snake bit me on the leg 10 minutes ago")
        assert r["emergency"] is True

    def test_mild_headache_routine_neurology(self):
        r = pipeline("I have a mild headache since morning")
        assert r["severity"] == "mild"
        assert r["department"] == "Neurology"
        assert r["emergency"] is False

    def test_sore_throat_ent(self):
        r = pipeline("I have a sore throat and difficulty swallowing")
        assert r["department"] == "ENT"

    def test_urinary_burning_general_medicine(self):
        r = pipeline("I have burning sensation while urinating since 2 days")
        assert "urinary_symptoms" in r["symptoms"]
        assert r["duration"] == "2 days"

    def test_vomiting_nausea(self):
        r = pipeline("I am vomiting and feeling nauseous")
        assert "vomiting" in r["symptoms"]

    def test_road_accident_emergency(self):
        r = pipeline("I was in a road accident and my leg is bleeding heavily")
        assert r["emergency"] is True

    def test_labor_pain_emergency_obstetrics(self):
        r = pipeline("I am having labor pain and contractions")
        assert r["emergency"] is True
        assert r["department"] == "Obstetrics & Gynecology"


# ── Hindi (Devanagari) scenarios ──────────────────────────────────────────────

class TestHindi:

    def test_bukhar_general_medicine(self):
        r = pipeline("मुझे 3 दिनों से बुखार है")
        assert "fever" in r["symptoms"]
        assert r["department"] == "General Medicine"

    def test_seene_mein_dard_cardiology(self):
        r = pipeline("मुझे सीने में दर्द हो रहा है")
        assert "chest_pain" in r["symptoms"]
        assert r["emergency"] is True
        assert r["department"] == "Cardiology"

    def test_saans_nahi_aa_rahi_emergency(self):
        r = pipeline("सांस नहीं आ रही है")
        assert r["emergency"] is True

    def test_behosh_emergency(self):
        r = pipeline("वह बेहोश हो गया है")
        assert r["emergency"] is True

    def test_kaan_dard_ent(self):
        r = pipeline("कान में बहुत दर्द हो रहा है")
        assert r["department"] == "ENT"

    def test_pet_dard_general_medicine(self):
        r = pipeline("पेट में दर्द हो रहा है और उल्टी आ रही है")
        assert "abdominal_pain" in r["symptoms"]
        assert "vomiting" in r["symptoms"]

    def test_garbhavati_bleeding_obstetrics(self):
        r = pipeline("मैं गर्भवती हूँ और खून आ रहा है")
        assert "pregnancy" in r["symptoms"]
        assert r["emergency"] is True
        assert r["department"] == "Obstetrics & Gynecology"

    def test_sir_dard_neurology(self):
        r = pipeline("सिर में बहुत तेज दर्द हो रहा है")
        assert "headache" in r["symptoms"]
        assert r["department"] == "Neurology"

    def test_saanp_ne_kaata_emergency(self):
        r = pipeline("सांप ने काटा है")
        assert r["emergency"] is True


# ── Marathi scenarios ─────────────────────────────────────────────────────────

class TestMarathi:

    def test_taap_general_medicine(self):
        r = pipeline("मला 2 दिवसांपासून ताप आहे")
        assert "fever" in r["symptoms"]
        assert r["department"] == "General Medicine"

    def test_chhati_dukh_cardiology(self):
        r = pipeline("छातीत खूप दुखत आहे")
        assert r["department"] == "Cardiology"
        assert r["emergency"] is True

    def test_kan_dukh_ent(self):
        r = pipeline("कान दुखतो आणि त्यातून पाणी येत आहे")
        assert r["department"] == "ENT"

    def test_dhap_lagali_emergency(self):
        r = pipeline("धाप लागली आहे श्वास घेता येत नाही")
        assert r["emergency"] is True

    def test_garbhavati_marathi(self):
        r = pipeline("मी गर्भवती आहे आणि रक्तस्राव होत आहे")
        assert r["emergency"] is True
        assert r["department"] == "Obstetrics & Gynecology"

    def test_dokedukhi_neurology(self):
        r = pipeline("डोके खूप दुखते")
        assert "headache" in r["symptoms"]
        assert r["department"] == "Neurology"


# ── Hinglish (romanised) scenarios ────────────────────────────────────────────

class TestHinglish:

    def test_bukhar_hinglish(self):
        r = pipeline("mujhe 3 din se bukhar hai")
        assert "fever" in r["symptoms"]
        assert r["duration"] == "3 din"

    def test_seene_mein_dard_hinglish(self):
        r = pipeline("seene mein dard ho raha hai")
        assert "chest_pain" in r["symptoms"]
        assert r["emergency"] is True

    def test_saans_hinglish(self):
        r = pipeline("saans nahi aa rahi hai")
        assert r["emergency"] is True

    def test_kaan_dard_hinglish(self):
        r = pipeline("kaan dard ho raha hai")
        assert r["department"] == "ENT"

    def test_ulti_hinglish(self):
        r = pipeline("ulti ho rahi hai aur pet mein dard hai")
        assert "vomiting" in r["symptoms"]
        assert "abdominal_pain" in r["symptoms"]

    def test_pregnant_hinglish(self):
        r = pipeline("main pregnant hun aur bleeding ho rahi hai")
        assert "pregnancy" in r["symptoms"]
        assert r["emergency"] is True
        assert r["department"] == "Obstetrics & Gynecology"

    def test_saanp_hinglish(self):
        r = pipeline("saanp ne kaata hai")
        assert r["emergency"] is True


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:

    def test_empty_string(self):
        r = pipeline("")
        assert r["symptoms"] == []
        assert r["emergency"] is False
        assert r["department"] == "General Medicine"

    def test_gibberish(self):
        r = pipeline("asdfgh xyz 123")
        assert r["symptoms"] == []
        assert r["emergency"] is False

    def test_multiple_symptoms_returns_all(self):
        r = pipeline("I have fever, cough, and headache")
        assert "fever" in r["symptoms"]
        assert "cough" in r["symptoms"]
        assert "headache" in r["symptoms"]

    def test_severity_severe_detected(self):
        r = pipeline("I have severe chest pain")
        assert r["severity"] == "severe"
        assert r["emergency"] is True

    def test_severity_mild_detected(self):
        r = pipeline("I have a mild headache")
        assert r["severity"] == "mild"

    def test_duration_extracted(self):
        r = pipeline("I have had a cough for 5 days")
        assert r["duration"] == "5 days"

    def test_mixed_script(self):
        # Common in real patient messages
        r = pipeline("I have बुखार and chest pain")
        assert "fever" in r["symptoms"]
        assert "chest_pain" in r["symptoms"]
        assert r["emergency"] is True
