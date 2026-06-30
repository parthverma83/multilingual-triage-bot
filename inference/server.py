from __future__ import annotations

import logging
import os
import json
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from config import ADAPTER_VERSION, BASE_MODEL, MODEL_NAME
from inference import run_inference
from load_model import model_manager
from schemas import GenerateRequest, GenerateResponse

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def log_event(event: str, **fields):
    logger.info(json.dumps({"event": event, **fields}, default=str))


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("SKIP_MODEL_LOAD", "").lower() in {"1", "true", "yes"}:
        log_event("model_load_skipped", reason="SKIP_MODEL_LOAD enabled")
    else:
        log_event("model_load_started", model=MODEL_NAME, base_model=BASE_MODEL)
        model_manager.load()
        log_event("model_loaded", model=MODEL_NAME, base_model=BASE_MODEL)
        log_event("warmup_started")
        model_manager.generate("Hello")
        log_event("warmup_complete")

    yield


app = FastAPI(
    title="Triage Inference Service",
    version="1.0.0",
    lifespan=lifespan,
)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.perf_counter()
        log_event("request_received", request_id=request_id, path=request.url.path, method=request.method)

        response = await call_next(request)
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        response.headers["X-Request-ID"] = request_id
        log_event(
            "request_finished",
            request_id=request_id,
            path=request.url.path,
            status_code=response.status_code,
            latency_ms=latency_ms,
        )
        return response


app.add_middleware(RequestIdMiddleware)

router = APIRouter()


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model_manager.loaded,
        "model": MODEL_NAME,
        "base_model": BASE_MODEL,
        "adapter_version": ADAPTER_VERSION,
    }



@router.post("/generate", response_model=GenerateResponse)
def generate(request: Request, payload: GenerateRequest):
    request_id = payload.request_id or request.state.request_id
    try:
        log_event("generation_started", request_id=request_id, prompt_chars=len(payload.prompt))
        response = run_inference(payload.prompt, request_id=request_id)
        log_event("generation_finished", request_id=request_id, latency_ms=response.latency_ms)
        return response
    except Exception as exc:
        log_event("generation_failed", request_id=request_id, error=str(exc))
        logger.exception(json.dumps({"event": "generation_exception", "request_id": request_id}))
        raise HTTPException(status_code=500, detail=f"Generation failed. request_id={request_id}") from exc


app.include_router(router)
app.include_router(router, prefix="/api/v1")
