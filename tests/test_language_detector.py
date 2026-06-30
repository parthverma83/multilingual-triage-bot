from backend.services.language_detector import detect_language


def test_english_chest_pain_stays_english():
    detected = detect_language("I have severe chest pain and difficulty breathing")

    assert detected["language"] == "en"
