from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    request_id: str | None = None


class GenerateResponse(BaseModel):
    generated_text: str
    latency_ms: int
    model: str
    request_id: str
