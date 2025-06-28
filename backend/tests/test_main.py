import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch("backend.main.agent")
def test_chat(mock_agent):
    class DummyMsg:
        def __init__(self, content):
            self.content = content
    # agent.invoke가 실제 main.py의 로직에 맞는 객체 리스트를 반환하도록 mock
    mock_agent.invoke.return_value = {"messages": [DummyMsg("테스트 응답입니다.")]}
    response = client.post("/chat", json={"message": "안녕?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "테스트 응답입니다." 