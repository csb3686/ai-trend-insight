import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """시스템 헬스체크 API가 정상적으로 응답하는지 확인 (Smoke Test)"""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_get_trends_heatmap(client: AsyncClient):
    """트렌드 데이터(히트맵)가 정상적인 구조로 반환되는지 확인"""
    response = await client.get("/api/v1/trends/heatmap")
    assert response.status_code == 200
    data = response.json()
    
    # 실제 서버 반환 구조 검증 (year, month, data)
    assert "data" in data
    assert "year" in data
    assert "month" in data
    assert isinstance(data["data"], list)

@pytest.mark.asyncio
async def test_get_articles_pagination(client: AsyncClient):
    """기사 목록 API의 페이징 처리가 정상적으로 작동하는지 확인 (skip/limit 사용)"""
    # 307 Redirect 방지를 위해 경로 끝에 / 추가
    response = await client.get("/api/v1/articles/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    
    # ArticleListResponse 구조 검증 (items, total)
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) <= 5

@pytest.mark.asyncio
async def test_chat_rag_response(client: AsyncClient):
    """RAG 챗봇 API가 올바른 구조의 응답을 반환하는지 확인"""
    # 실제 서버는 'message' 필드를 기대함
    chat_payload = {"message": "AI 트렌드 요약해줘"}
    response = await client.post("/api/v1/chat", json=chat_payload)
    
    # 챗봇은 LLM 응답 대기 시간이 있을 수 있으므로 상태 코드 먼저 확인
    assert response.status_code == 200
    data = response.json()
    
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)

@pytest.mark.asyncio
async def test_invalid_article_id(client: AsyncClient):
    """존재하지 않는 기사 ID 요청 시 404 에러를 반환하는지 확인 (Negative Test)"""
    response = await client.get("/api/v1/articles/9999999")
    assert response.status_code == 404
