from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    # 실제 로직 대신 입력 메시지를 그대로 반환
    return ChatResponse(reply=f"Echo: {request.message}") 