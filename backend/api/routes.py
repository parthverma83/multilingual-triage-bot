from fastapi import APIRouter

from backend.schemas.request import TriageRequest
from backend.services.http_inference_service import HttpInferenceService
from backend.services.triage_engine import TriageEngine


router = APIRouter()

engine = TriageEngine(model=HttpInferenceService())


@router.post("/triage")
async def triage(request: TriageRequest):
    return await engine.process(request.message, language=request.language)


@router.get("/health")
def health():
    return {"status": "healthy"}



