from fastapi.testclient import TestClient
from museums.main import app

client = TestClient(app)

def test_running_app():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my FastAPI application!"}
