from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from typing import Any

import httpx

from backend.config import settings
from backend.services.model_service import BaseModelService

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def log_event(event: str, **fields: Any) -> None:
    logger.info(json.dumps({"event": event, **fields}, default=str))


def _parse_generated_json(generated_text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(generated_text)
    except json.JSONDecodeError:
        start = generated_text.find("{")
        end = generated_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("Inference response did not contain JSON.") from None
        parsed = json.loads(generated_text[start : end + 1])

    if not isinstance(parsed, dict):
        raise ValueError("Inference response JSON must be an object.")

    return parsed


class HttpInferenceService(BaseModelService):
    async def generate(self, prompt: str, language: str = "auto") -> dict:
        if not settings.MODEL_ENDPOINT:
            raise RuntimeError("MODEL_ENDPOINT is not configured.")

        request_id = str(uuid.uuid4())
        endpoint = settings.MODEL_ENDPOINT.rstrip("/")
        url = f"{endpoint}/generate"
        headers = {"X-Request-ID": request_id}
        if settings.MODEL_API_KEY:
            headers["Authorization"] = f"Bearer {settings.MODEL_API_KEY}"

        payload = {
            "prompt": prompt,
            "request_id": request_id,
        }
        retry_attempts = max(settings.MODEL_RETRY_ATTEMPTS, 1)
        start_time = time.perf_counter()

        log_event(
            "inference_request_started",
            request_id=request_id,
            endpoint=endpoint,
            language=language,
            prompt_chars=len(prompt),
        )

        for attempt in range(1, retry_attempts + 1):
            try:
                timeout = httpx.Timeout(settings.MODEL_TIMEOUT_SECONDS)
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    response.raise_for_status()

                body = response.json()
                generated_text = body.get("generated_text", "")
                if not isinstance(generated_text, str) or not generated_text.strip():
                    raise ValueError("Inference service returned empty generated_text.")

                parsed = _parse_generated_json(generated_text)
                latency_ms = int((time.perf_counter() - start_time) * 1000)
                log_event(
                    "inference_request_finished",
                    request_id=request_id,
                    attempt=attempt,
                    latency_ms=latency_ms,
                    model=body.get("model"),
                    inference_latency_ms=body.get("latency_ms"),
                )
                return parsed

            except (httpx.TimeoutException, httpx.ConnectError, httpx.RemoteProtocolError, httpx.HTTPStatusError) as exc:
                should_retry = attempt < retry_attempts and not (
                    isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500
                )
                log_event(
                    "inference_request_error",
                    request_id=request_id,
                    attempt=attempt,
                    retrying=should_retry,
                    error=str(exc),
                )
                if not should_retry:
                    raise RuntimeError(
                        f"Inference service request failed after {attempt} attempt(s). "
                        f"request_id={request_id}"
                    ) from exc
                await asyncio.sleep(min(2 ** (attempt - 1), 5))

            except (json.JSONDecodeError, ValueError) as exc:
                log_event("inference_response_invalid", request_id=request_id, attempt=attempt, error=str(exc))
                raise RuntimeError(f"Inference service returned invalid output. request_id={request_id}") from exc

        raise RuntimeError(f"Inference service request failed. request_id={request_id}")

