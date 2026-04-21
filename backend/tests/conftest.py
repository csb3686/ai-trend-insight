import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import SessionLocal, Base

@pytest.fixture(scope="session")
def event_loop():
    """비동기 테스트를 위한 이벤트 루프 설정"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db():
    """각 테스트마다 독립적인 DB 세션을 제공"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
async def client():
    """FastAPI 비동기 테스트를 위한 httpx 클라이언트"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_news_item():
    """테스트용 가공 뉴스 데이터 픽스처"""
    return {
        "title": "pytest를 활용한 QA 자동화 기술",
        "url": "https://test.com/qa-automation",
        "content": "이것은 단위 테스트를 위한 모의 기사 내용입니다. QA 엔지니어가 작성함.",
        "published_at": "2026-04-19 12:00:00"
    }
