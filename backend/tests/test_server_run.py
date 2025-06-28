import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_server_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_server_chat():
    data = {"message": "test"}
    response = client.post("/chat/", json=data)
    assert response.status_code == 200
    assert response.json()["response"].startswith(("안녕하세요", "상품명을 알려주시면")) 