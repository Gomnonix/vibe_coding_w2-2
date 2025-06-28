from fastapi import FastAPI, Request
from pydantic import BaseModel, SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import os

# 환경 변수에서 Gemini API Key 로드 (필요시 .env 사용)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM 및 Tool 초기화
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", api_key=SecretStr(GOOGLE_API_KEY) if GOOGLE_API_KEY else None)
ddg_tool = DuckDuckGoSearchRun()

# React Agent 생성 (단일 턴, 메모리 없음)
agent = create_react_agent(
    model=llm,
    tools=[ddg_tool],
    prompt=(
        "너는 사용자가 요청한 상품에 대해 실제로 구매 가능한 사이트와 최저가 정보를 DuckDuckGo 웹 검색을 통해 찾아주는 한국어 쇼핑 도우미야. "
        "검색어는 반드시 '최저가', '구매', '사이트' 등의 키워드를 포함해 보정해서 검색해. "
        "검색 결과에서 1. 상품명과 가격 정보, 2. 구매 가능한 쇼핑몰 또는 사이트 링크 이 두 가지만 한국어로 유용하고 정확하게 요약해서 제공해. "
        "불필요한 설명 없이 아래와 같은 포맷으로만 답변해: \n"
        "1. 상품명 및 가격: ...\n2. 구매 사이트 링크: ..."
    )
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_message = {"role": "user", "content": req.message}
    try:
        result = agent.invoke({"messages": [user_message]})
        messages = result["messages"] if isinstance(result, dict) and "messages" in result else result
        if isinstance(messages, list) and messages:
            answer = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
        else:
            answer = str(result)
    except Exception as e:
        answer = f"[에러] 챗봇 처리 중 오류: {e}"
    return {"response": answer}

@app.get("/health")
def health():
    return {"status": "ok"}
