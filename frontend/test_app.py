import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
from unittest.mock import patch


def test_app_renders_title():
    at = AppTest.from_file("app.py")
    at.run()
    assert at.title[0].value == "💬 Vibe 챗봇"


def test_app_renders_input():
    at = AppTest.from_file("app.py")
    at.run()
    assert at.chat_input[0].placeholder == "메시지를 입력하세요"


def test_user_message_adds_to_session():
    at = AppTest.from_file("app.py")
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "테스트 응답"}
        if at.chat_input:
            at.chat_input[0].set_value("테스트 메시지").run()
            assert any(m["content"] == "테스트 메시지" for m in st.session_state["messages"])
            assert any(m["content"] == "테스트 응답" for m in st.session_state["messages"])
        else:
            pytest.skip("chat_input 위젯이 탐지되지 않음 (Streamlit Testing API 버전 확인 필요)") 