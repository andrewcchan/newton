import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index route returns a 200 OK status."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Projectile Simulation" in response.get_data(as_text=True)

def test_simulate_route_success(client):
    """Test the /simulate route with valid data."""
    payload = {
        "velocity": 25,
        "angle": 45,
        "gravity": 9.8
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "x" in data and "y" in data and "hit" in data

def test_simulate_route_missing_data(client):
    """Test that missing data returns a 400 Bad Request."""
    payload = {"velocity": 25, "angle": 45}
    response = client.post("/simulate", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_simulate_route_invalid_data_type(client):
    """Test that invalid data types return a 400 Bad Request."""
    payload = {"velocity": "fast", "angle": 45, "gravity": 9.8}
    response = client.post("/simulate", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_simulate_route_negative_values(client):
    """Test that negative or out-of-range values return a 400."""
    payload = {"velocity": -10, "angle": 45, "gravity": 9.8}
    response = client.post("/simulate", json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()
