from fastapi import FastAPI

from backend.api.routes import router








app = FastAPI(
    title="Multilingual Medical Triage API",
    version="1.0.0",
)

app.include_router(router)
app.include_router(router, prefix="/api/v1")


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Medical Triage Backend",
    }


