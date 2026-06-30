from fastapi.testclient import TestClient

from backend.app import app


def test_backend_health_works_on_versioned_and_legacy_paths():
    client = TestClient(app)

    assert client.get("/health").json() == {"status": "healthy"}
    assert client.get("/api/v1/health").json() == {"status": "healthy"}
