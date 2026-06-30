from fastapi.testclient import TestClient

import server


def test_inference_health_works_on_versioned_and_legacy_paths():
    client = TestClient(server.app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["model"] == "sarvam-triage-v1"
    assert body["base_model"]
    assert "model_loaded" in body


def test_generate_returns_expected_schema(monkeypatch):
    def fake_run_inference(prompt: str, request_id: str):
        from schemas import GenerateResponse

        return GenerateResponse(
            generated_text='{"department":"General Medicine","priority":"Routine","emergency":false,"confidence":0.8,"advice":"Rest and hydrate."}',
            latency_ms=12,
            model="sarvam-triage-v1",
            request_id=request_id,
        )

    monkeypatch.setattr(server, "run_inference", fake_run_inference)
    client = TestClient(server.app)

    response = client.post(
        "/api/v1/generate",
        json={"prompt": "Patient has fever", "request_id": "req-test-1"},
    )

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"generated_text", "latency_ms", "model", "request_id"}
    assert body["request_id"] == "req-test-1"
    assert response.headers["x-request-id"]
