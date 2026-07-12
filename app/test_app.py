import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_content(client):
    response = client.get("/")
    data = response.get_json()
    assert data["status"] == "running"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_metrics_count(client):
    response = client.get("/metrics-count")
    assert response.status_code == 200
    assert "requests_served" in response.get_json()
