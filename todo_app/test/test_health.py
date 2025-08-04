from fastapi.testclient import TestClient
from todo_app.main import app          # ← exact import path

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    # Just check we get a response
    data = response.json()
    assert data is not None
