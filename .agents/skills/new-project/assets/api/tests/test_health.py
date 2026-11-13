"""Health route."""

from fastapi.testclient import TestClient

from app.api.routes import create_app


def test_health() -> None:
    response = TestClient(create_app()).get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
