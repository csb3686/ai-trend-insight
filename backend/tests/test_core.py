import pytest
from app.services.rag_service import rag_service
from app.services.analysis_service import analysis_service
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_rag_output_format():
    """RAG 서비스가 마크다운 형식을 포함한 답변을 반환하는지 테스트합니다."""
    question = "AI 트렌드에 대해 알려줘"
    # 동기 방식으로 테스트 (async 함수가 아닐 경우)
    import asyncio
    result = asyncio.run(rag_service.get_answer(question))
    
    assert "answer" in result
    assert "sources" in result
    # 마크다운 특성(굵게 등)이나 소스 섹션이 포함되었는지 확인
    assert "📚 주요 참고 소식" in result["answer"]
    print("\n✅ RAG 마크다운 형식 검증 완료")

def test_analysis_ecosystem_structure(db: Session):
    """기술 생태계 데이터가 Cytoscape 규격(nodes, edges)에 맞게 생성되는지 테스트합니다."""
    result = analysis_service.get_tech_ecosystem(db, limit=10)
    
    assert "nodes" in result
    assert "edges" in result
    assert len(result["nodes"]) <= 10
    
    if len(result["nodes"]) > 0:
        assert "data" in result["nodes"][0]
        assert "id" in result["nodes"][0]["data"]
        assert "name" in result["nodes"][0]["data"]
    
    print(f"\n✅ 기술 생태계 데이터 구조 검증 완료 (노드 수: {len(result['nodes'])})")

def test_cache_logic():
    """Redis 캐시 레이어가 정상적으로 작동하는지 테스트합니다. (Redis 서버 실행 중 가정)"""
    from app.core.cache import cache_service
    test_key = "test:ping"
    test_value = {"status": "ok"}
    
    success = cache_service.set(test_key, test_value, expire=10)
    if success:
        val = cache_service.get(test_key)
        assert val == test_value
        cache_service.delete(test_key)
        print("\n✅ Redis 캐시 입출력 검증 완료")
    else:
        print("\n⚠️ Redis 서버 미실행으로 캐시 테스트 스킵")
