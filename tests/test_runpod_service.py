import pytest

from backend.services import runpod_service
from backend.services.runpod_service import RunPodModelService


class FakeSettings:
    MODEL_ENDPOINT = "http://inference.test"
    MODEL_API_KEY = ""
    MODEL_TIMEOUT_SECONDS = 1.0
    MODEL_RETRY_ATTEMPTS = 2


@pytest.mark.asyncio
async def test_runpod_service_parses_generated_json(monkeypatch):
    async def handler(request):
        import httpx

        return httpx.Response(
            200,
            json={
                "generated_text": '{"department":"Cardiology","priority":"Emergency","emergency":true,"confidence":0.93,"advice":"Go to emergency care.","reasoning":["Chest pain reported"],"recommended_tests":["ECG","Troponin"]}',
                "latency_ms": 10,
                "model": "sarvam-triage-v1",
                "request_id": "req-1",
            },
        )

    import httpx

    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(runpod_service, "settings", FakeSettings())

    class MockedAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(runpod_service.httpx, "AsyncClient", MockedAsyncClient)

    result = await RunPodModelService().generate("prompt", language="en")

    assert result["department"] == "Cardiology"
    assert result["emergency"] is True
    assert result["reasoning"] == ["Chest pain reported"]
    assert result["recommended_tests"] == ["ECG", "Troponin"]


@pytest.mark.asyncio
async def test_runpod_service_rejects_malformed_response(monkeypatch):
    async def handler(request):
        import httpx

        return httpx.Response(
            200,
            json={
                "generated_text": "not json",
                "latency_ms": 10,
                "model": "sarvam-triage-v1",
                "request_id": "req-1",
            },
        )

    import httpx

    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(runpod_service, "settings", FakeSettings())

    class MockedAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            super().__init__(transport=transport, *args, **kwargs)

    monkeypatch.setattr(runpod_service.httpx, "AsyncClient", MockedAsyncClient)

    with pytest.raises(RuntimeError, match="invalid output"):
        await RunPodModelService().generate("prompt", language="en")


@pytest.mark.asyncio
async def test_runpod_service_handles_timeout(monkeypatch):
    class TimeoutClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, *args, **kwargs):
            raise runpod_service.httpx.TimeoutException("timed out")

    monkeypatch.setattr(runpod_service, "settings", FakeSettings())
    monkeypatch.setattr(runpod_service.httpx, "AsyncClient", lambda *args, **kwargs: TimeoutClient())

    with pytest.raises(RuntimeError, match="failed after"):
        await RunPodModelService().generate("prompt", language="en")
