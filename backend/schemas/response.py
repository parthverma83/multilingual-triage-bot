from pydantic import BaseModel, Field


class TriageResponse(BaseModel):
    department: str
    priority: str
    emergency: bool
    confidence: float
    advice: str
    language: str
    reasoning: list[str] = Field(default_factory=list)
    recommended_tests: list[str] = Field(default_factory=list)


