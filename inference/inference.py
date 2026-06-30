from __future__ import annotations

import time

from config import MODEL_NAME
from load_model import model_manager
from schemas import GenerateResponse


def run_inference(prompt: str, request_id: str) -> GenerateResponse:
    start_time = time.perf_counter()
    generated_text = model_manager.generate(prompt)
    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return GenerateResponse(
        generated_text=generated_text,
        latency_ms=latency_ms,
        model=MODEL_NAME,
        request_id=request_id,
    )
