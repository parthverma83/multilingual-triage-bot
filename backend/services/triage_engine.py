import json
import logging

from backend.schemas.response import TriageResponse
from backend.services.model_service import BaseModelService
from backend.services.language_detector import detect_language
from backend.services.symptom_extractor import extract_symptoms
from backend.services.emergency_detector import detect_emergency
from backend.services.department_router import route_department
from backend.services.explanation_builder import build_reasoning, recommended_tests_for_department
from backend.services.prompt_builder import build_prompt
from backend.services.response_validator import validate_and_normalize
from backend.services.translations import translate_response

logger = logging.getLogger(__name__)


class TriageEngine:
    def __init__(self, model: BaseModelService):
        self.model = model

    async def process(self, message: str, language: str = "auto") -> TriageResponse:
        # Sprint 3 orchestrator: deterministic intelligence first, model second.
        # Language is detected/normalized regardless of frontend choice.
        detected = detect_language(message)
        detected_language = detected.get("language") or language
        normalized_text = detected.get("normalized_text") or message

        extracted = extract_symptoms(normalized_text)
        emergency_info = detect_emergency(extracted, raw_text=message)
        department_info = route_department(extracted)
        fallback_department = department_info.get("department", "General Medicine")
        fallback_emergency = bool(emergency_info.get("emergency"))
        fallback_reasoning = build_reasoning(
            extracted=extracted,
            emergency_info=emergency_info,
            department_info=department_info,
        )

        fallback_priority = "Emergency" if fallback_emergency else "Routine"
        fallback = TriageResponse(
            department=fallback_department,
            priority=fallback_priority,
            emergency=fallback_emergency,
            confidence=float(department_info.get("confidence", 0.4)),
            advice=(
                "Emergency detected. Please seek urgent medical care." if fallback_emergency
                else "Based on your symptoms, this looks like a routine medical concern."
            ),
            language=detected_language,
            reasoning=fallback_reasoning,
            recommended_tests=recommended_tests_for_department(fallback_department, emergency=fallback_emergency),
        )

        prompt = build_prompt(
            language=detected_language,
            extracted=extracted,
            emergency_info=emergency_info,
            department_info=department_info,
        )

        try:
            model_output = await self.model.generate(prompt=prompt, language=detected_language)
        except Exception as exc:
            logger.error(
                json.dumps(
                    {
                        "event": "model_generation_failed_using_fallback",
                        "error": str(exc),
                        "language": detected_language,
                    }
                )
            )
            model_output = {}

        # Placeholder RunPodModelService returns a non-triage dict; validator will fall back.
        validated = validate_and_normalize(model_output, fallback=fallback)

        # Deterministic enforcement: emergency flag/priority override model.
        if emergency_info.get("emergency"):
            validated.emergency = True
            validated.priority = "Emergency"
            if "Vitals check" not in validated.recommended_tests:
                validated.recommended_tests = ["Vitals check", *validated.recommended_tests]

        # Translate all user-facing fields to the patient's language.
        # Internal canonical values (English) are preserved up to this point
        # so routing logic and validation are unaffected.
        response_dict = validated.model_dump()
        translate_response(response_dict, detected_language)
        return validated.__class__(**response_dict)




