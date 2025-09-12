from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_invalid_todo_title():
    response = client.post("/todos/", json={"title": "Hi"})
    assert response.status_code == 422
