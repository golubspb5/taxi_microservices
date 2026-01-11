import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_driver_presence_online():
    payload = {
        "status": "online",
        "location": {"x": 5, "y": 5}
    }
    response = client.put("/api/v1/drivers/me/presence", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["location"]["x"] == 5
    assert data["location"]["y"] == 5
