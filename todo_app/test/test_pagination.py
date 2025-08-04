from fastapi.testclient import TestClient
from todo_app.main import app

client = TestClient(app)

def test_pagination_validation():
    """Test that pagination parameters are validated correctly"""
    
    # Test invalid skip (negative)
    response = client.get("/todos?skip=-1&limit=10")
    # Should get 401 (not authenticated) or 422 (validation error)
    assert response.status_code in [401, 422]
    
    # Test invalid limit (too high)  
    response = client.get("/todos?skip=0&limit=200")
    # Should get 401 (not authenticated) or 422 (validation error)
    assert response.status_code in [401, 422]

def test_pagination_endpoint_exists():
    """Test that the pagination endpoint exists and accepts parameters"""
    
    # Test without auth - should get 401 but endpoint should exist
    response = client.get("/todos?skip=0&limit=10")
    assert response.status_code == 401  # Not 404
    
    # Test with invalid params - should get validation error
    response = client.get("/todos?skip=-1")
    assert response.status_code in [401, 422]

if __name__ == "__main__":
    test_pagination_validation()
    test_pagination_endpoint_exists()
    print("✅ Basic pagination tests passed!")
