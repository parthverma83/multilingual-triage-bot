# Architecture (Sprint 4)

## Goal
Separate business logic (backend) from model serving (inference).

## Folders
- `triage-bot/backend/`: triage pipeline orchestration + API.
- `triage-bot/inference/`: model loading + inference endpoint.
- `triage-bot/models/`: base model assets + LoRA adapter artifacts.

## Current Sprint Status
- Sprint 4.1–4.3: `triage-bot/inference/` created with placeholders + config + requirements.
- Sprint 5: implement `inference/load_model.py` and verify local inference.
- Sprint 6: add Docker wiring and deploy to RunPod.

