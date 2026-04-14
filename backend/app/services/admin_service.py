import time
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.collection_log import CollectionLog
from app.schemas.admin import HealthCheckDetail, ComponentHealth, HealthStatus, CollectionLogResponse
from app.core.config import get_settings
import requests

settings = get_settings()

class AdminService:
    async def check_system_health(self, db: Session) -> HealthCheckDetail:
        """MySQL, ChromaDB, LLM 상태를 정밀 진단합니다."""
        components = {}
        overall_status = HealthStatus.OK

        # 1. MySQL 진단
        try:
            start_time = time.time()
            db.execute(text("SELECT 1"))
            latency = (time.time() - start_time) * 1000
            components["mysql"] = ComponentHealth(status=HealthStatus.OK, latency_ms=latency)
        except Exception as e:
            components["mysql"] = ComponentHealth(status=HealthStatus.ERROR, message=str(e))
            overall_status = HealthStatus.ERROR

        # 2. ChromaDB 진단
        try:
            start_time = time.time()
            # 헬스체크 엔드포인트 호출
            res = requests.get(f"{settings.chroma_url}/api/v1/heartbeat", timeout=2)
            latency = (time.time() - start_time) * 1000
            if res.status_code == 200:
                components["chromadb"] = ComponentHealth(status=HealthStatus.OK, latency_ms=latency)
            else:
                components["chromadb"] = ComponentHealth(status=HealthStatus.ERROR, message=f"HTTP {res.status_code}")
                overall_status = HealthStatus.ERROR
        except Exception as e:
            components["chromadb"] = ComponentHealth(status=HealthStatus.ERROR, message=str(e))
            overall_status = HealthStatus.ERROR

        # 3. Groq LLM 진단 (간단한 모델 리스트 조회로 키 유효성 확인)
        try:
            start_time = time.time()
            headers = {"Authorization": f"Bearer {settings.groq_api_key}"}
            res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
            latency = (time.time() - start_time) * 1000
            if res.status_code == 200:
                components["llm_groq"] = ComponentHealth(status=HealthStatus.OK, latency_ms=latency)
            else:
                components["llm_groq"] = ComponentHealth(status=HealthStatus.ERROR, message=f"Auth Failed: {res.status_code}")
                if overall_status != HealthStatus.ERROR:
                    overall_status = HealthStatus.WARNING
        except Exception as e:
            components["llm_groq"] = ComponentHealth(status=HealthStatus.ERROR, message=str(e))
            if overall_status != HealthStatus.ERROR:
                overall_status = HealthStatus.WARNING

        return HealthCheckDetail(
            status=overall_status,
            components=components
        )

    def get_collection_logs(self, db: Session, limit: int = 20) -> List[CollectionLog]:
        """최근 수집 및 처리 이력을 조회합니다."""
        return db.query(CollectionLog).order_by(CollectionLog.start_time.desc()).limit(limit).all()

    # --- 수동 트리거 로직 (실제 파이프라인 함수 연동) ---
    
    async def run_collection_task(self, db_session_factory, task_type: str, triggered_by: str = "manual"):
        """백그라운드에서 실제 수집/임베딩 작업을 수행하고 로그를 남깁니다."""
        # 지연 임포트로 순환 참조 방지 및 실행 시점에 로드
        from pipeline import scheduler

        db = db_session_factory()
        log = CollectionLog(task_type=task_type, triggered_by=triggered_by, status='IN_PROGRESS')
        db.add(log)
        db.commit()
        db.refresh(log)

        try:
            start_time = time.time()
            if task_type == 'COLLECT':
                # 수집 및 기본 전처리 수행
                scheduler.job_geek_news()
                scheduler.job_hacker_news()
                scheduler.job_github_trending()
                scheduler.job_process_data()
            elif task_type == 'EMBED':
                # AI 임베딩 수행
                scheduler.job_embed_data()
            elif task_type == 'STATS':
                # 트렌드 통계 재집계
                scheduler.job_aggregate_trends()
            
            log.status = 'SUCCESS'
            log.end_time = datetime.now()
            # 간단한 기록 (실제 수집량 계산은 생략하거나 나중에 보완)
            log.processed_count = 1 
            db.commit()
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            log.status = 'FAIL'
            log.end_time = datetime.now()
            log.error_message = f"{str(e)}\n{error_trace[:500]}"
            db.commit()
        finally:
            db.close()

admin_service = AdminService()
