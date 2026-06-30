# API

## Backend API
- `POST /triage`
  - Request: `TriageRequest(message, language="auto", conversation_id?)`
  - Response: `TriageResponse(department, priority, emergency, confidence, advice, language)`

The backend currently uses `RunPodModelService` as a placeholder model provider.

## Inference Service API (Sprint 6 target)
- `POST /generate` (planned)
- `GET /health`

