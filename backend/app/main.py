from fastapi import FastAPI

app = FastAPI(
    title="Multilingual Medical Triage Bot"
)

@app.get("/")
def root():
    return {
        "message": "Triage Bot API Running"
    }
