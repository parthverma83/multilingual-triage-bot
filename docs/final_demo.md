# Final Demo Plan (Sprint 7)

## Story
1. Patient enters symptoms via Streamlit.
2. Streamlit calls FastAPI `/triage`.
3. FastAPI calls inference service.
4. Model + structured prompting returns strict JSON.
5. Response validator normalizes to `TriageResponse`.
6. UI shows department, priority/emergency, confidence, and advice.

## Checklist
- End-to-end test cases (EN/HI/MR).
- Performance notes (warm start, batch size if applicable).
- Clear architecture diagram.

