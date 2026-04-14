from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_rag(request: ChatRequest):
    """
    RAG 기반 인공지능 전문 챗봇과 대화합니다.
    """
    try:
        result = await rag_service.get_answer(request.message)
        return ChatResponse(
            answer=result["answer"],
            context=result["context"]  # 개발 및 디버깅용으로 컨텍스트 포함
        )
    except Exception as e:
        # 자세한 에러 메시지를 포함하여 반환 (개발 단계)
        raise HTTPException(status_code=500, detail=str(e))
