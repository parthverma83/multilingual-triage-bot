# Project TODO

## Sprint 4 — AI Inference Service (setup scaffold)
- [x] Create `triage-bot/inference/` folder structure (backend separate from inference)
- [x] Add `triage-bot/inference/requirements.txt` (standard Transformers + PEFT)
- [x] Add `triage-bot/inference/config.py` (BASE_MODEL + LORA_PATH)
- [x] Add placeholder `load_model.py`, `inference.py`, `server.py`, `Dockerfile`
- [x] Add `triage-bot/docs/` with architecture/api/deployment/final_demo docs
- [ ] Create a Python 3.11 venv and install `triage-bot/inference/requirements.txt`

## Sprint 5 — Model implementation
- [ ] Implement `triage-bot/inference/load_model.py`
- [ ] Implement `triage-bot/inference/inference.py`
- [ ] Smoke test inference locally on GPU (if available)

## Sprint 6 - Container + RunPod
- [x] Add GPU inference Dockerfile
- [x] Add `.dockerignore`
- [x] Add Docker Compose for backend + inference
- [x] Replace backend `RunPodModelService` to call inference service
- [x] Add request IDs and structured logs
- [ ] Build inference Docker image locally
- [ ] Deploy to RunPod
- [ ] Validate `/health` with model loaded on GPU

## Sprint 7 — Streamlit + End-to-end
- [ ] Connect Streamlit to FastAPI
- [ ] End-to-end testing
- [ ] Demo polish + final presentation prep

