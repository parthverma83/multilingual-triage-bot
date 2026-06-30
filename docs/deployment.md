# Deployment Notes

## Sprint 6 - Deployment and Integration

### Local inference smoke test

Run the inference service without loading the model:

```bash
SKIP_MODEL_LOAD=true uvicorn server:app --host 0.0.0.0 --port 8001
```

Then check:

```bash
curl http://localhost:8001/health
```

### Docker build

Build from the repository root so the Dockerfile can copy the inference package:

```bash
docker build -f inference/Dockerfile -t triage-inference:latest .
```

The LoRA adapter is excluded by `.dockerignore` and should be mounted at `/models/sarvam_triage_lora` unless you intentionally choose to bake it into a private image.

### Docker Compose

Start backend and inference together:

```bash
SKIP_MODEL_LOAD=true docker compose up --build
```

Useful endpoints:

- Backend: `http://localhost:8000/health`
- Inference: `http://localhost:8001/health`

### RunPod

1. Push `triage-inference:latest` to your container registry.
2. Create a GPU-backed RunPod pod from that image.
3. Mount the LoRA adapter at `/models/sarvam_triage_lora`, or set `LORA_PATH` to the mounted adapter path.
4. Set `SKIP_MODEL_LOAD=false` or omit it.
5. Confirm `/health` returns `model_loaded: true`.
6. Point the backend `MODEL_ENDPOINT` to the RunPod inference URL.

### Backend inference settings

- `MODEL_ENDPOINT`: base URL for the inference service, for example `http://inference:8001` locally.
- `MODEL_API_KEY`: optional bearer token if the endpoint is protected.
- `MODEL_TIMEOUT_SECONDS`: request timeout, default `60`.
- `MODEL_RETRY_ATTEMPTS`: transient failure retry count, default `3`.

Every backend-to-inference call includes a request ID and every inference response returns it. Logs are emitted as JSON strings for easier tracing.
