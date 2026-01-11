import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_trip():
    payload = {
        "start_x": 0,
        "start_y": 0,
        "end_x": 3,
        "end_y": 4
    }
    response = client.post("/api/v1/passenger/rides", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ride_id" in data
    assert "estimated_price" in data
    assert data["status"] == "pending"
