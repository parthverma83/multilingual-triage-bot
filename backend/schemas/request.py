from pydantic import BaseModel


class TriageRequest(BaseModel):
    message: str
    language: str = "auto"
    conversation_id: str | None = None


