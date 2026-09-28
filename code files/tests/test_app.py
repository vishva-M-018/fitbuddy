import os

os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200
