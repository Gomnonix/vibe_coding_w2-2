import streamlit as st
import requests
import re

st.set_page_config(page_title="Vibe 챗봇", page_icon="💬")
st.title("💬 Vibe 챗봇")
st.markdown("상품 검색 및 챗봇 대화가 가능합니다.")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 채팅 메시지 표시
for msg in st.session_state['messages']:
    with st.chat_message(msg["role"]):
        # assistant 답변에서 구매 사이트 링크를 하이퍼링크로 변환
        if msg["role"] == "assistant":
            lines = msg["content"].split('\n')
            for line in lines:
                if line.startswith("2. 구매 사이트 링크:"):
                    # URL 추출
                    url_match = re.search(r'(https?://\S+)', line)
                    if url_match:
                        url = url_match.group(1)
                        st.markdown(f"[구매 사이트로 이동]({url})", unsafe_allow_html=True)
                    else:
                        st.markdown(line)
                else:
                    st.markdown(line)
        else:
            st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("메시지를 입력하세요")
if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    try:
        # FastAPI 백엔드 /chat 엔드포인트 호출
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": user_input},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            bot_msg = data.get("response", "챗봇 응답이 없습니다.")
        else:
            bot_msg = f"[에러] 서버 응답 오류: {response.status_code}"
    except Exception as e:
        bot_msg = f"[에러] 서버 연결 실패: {e}"
    st.session_state['messages'].append({"role": "assistant", "content": bot_msg})
    st.rerun()
