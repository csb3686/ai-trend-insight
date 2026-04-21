from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.core.config import get_settings
from app.core.database import get_db
from app.api.v1 import api_router
from pipeline.collectors.github_trending_collector import GithubTrendingCollector
from pipeline.collectors.hacker_news_collector import HackerNewsCollector
from pipeline.collectors.geek_news_collector import GeekNewsCollector
from pipeline.processors.stats_aggregator import TrendsAggregator
from pipeline.generate_hybrid_data import HybridDataGenerator # 하이브리드 생성기 추가
from pipeline.github_master_sync import GitHubMasterSync # GitHub 마스터 싱크 추가
from pipeline.sanitize_db import sanitize # DB 정화 함수 추가

app = FastAPI(
    title="TrendRadar API",
    description="AI 기술 트렌드 인사이트 플랫폼 API 서버",
    version="1.0.0"
)

# --- DB 스키마 자가 치유 로직 (progress 컬럼 자동 추가) ---
@app.on_event("startup")
async def init_db_schema():
    from app.core.database import SessionLocal
    print("--- [Initialization] DB 스킨 검사 및 자가 치유 시작 ---")
    db = SessionLocal()
    try:
        # progress 컬럼 존재 여부 확인
        check_sql = text("SHOW COLUMNS FROM collection_logs LIKE 'progress'")
        result = db.execute(check_sql).fetchone()
        
        if not result:
            print("[Initialization] progress 컬럼이 없습니다. 수동 생성 중...")
            add_sql = text("ALTER TABLE collection_logs ADD COLUMN progress INT NOT NULL DEFAULT 0 AFTER status")
            db.execute(add_sql)
            db.commit()
            print("[Initialization] progress 컬럼 생성 완료! [OK]")
        else:
            print("[Initialization] 스키마가 최신 상태입니다. [OK]")
    except Exception as e:
        print(f"[Initialization Warning] 스키마 확인 중 오류 (이미 존재할 수 있음): {e}")
    finally:
        db.close()

import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.trend import Trend
from sqlalchemy import delete

@app.post("/debug/hybrid-sync")
async def run_hybrid_pipeline_debug(db: Session = Depends(get_db)):
    """2~4월 데이터 생성 -> 트렌드 재집계 통합 실행 (하이브리드 버전)"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            # 1. 하이브리드 데이터 생성 (300개 기사)
            generator = HybridDataGenerator()
            await loop.run_in_executor(executor, generator.run)
            
            # 2. 트렌드 재집계 (생성된 기사 기반 통계 산출)
            aggregator = TrendsAggregator()
            await loop.run_in_executor(executor, aggregator.aggregate_all)
            
            return {"status": "success", "message": "2~4월 하이브리드 데이터 보강 완료"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

@app.post("/debug/final-polish")
async def run_final_polish_debug(db: Session = Depends(get_db)):
    """DB 정화 -> 고품질 데이터 재주입 -> 최종 통계 재집계 통합 수행"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            # 1. DB 정화 (깨진 링크 및 오표기 소스 삭제)
            await loop.run_in_executor(executor, sanitize)
            
            # 2. 뉴스 데이터 재주입 (구글 검색 링크 버전)
            generator = HybridDataGenerator()
            await loop.run_in_executor(executor, generator.run)
            
            # 3. 깃허브 데이터 재주입 (ID 고정 및 깃허브 검색 버전)
            sync = GitHubMasterSync()
            await loop.run_in_executor(executor, sync.run)
            
            # 4. 최종 트렌드 재집계
            aggregator = TrendsAggregator()
            await loop.run_in_executor(executor, aggregator.aggregate_all)
            
            return {"status": "success", "message": "데이터 정교화 및 링크 정상화 완료"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

@app.post("/debug/github-master-sync")
async def run_github_master_sync_debug(db: Session = Depends(get_db)):
    """오늘의 실시간 크롤링 + 2~4월 유명 레포 보강 + 트렌드 재집계 통합 실행"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            sync = GitHubMasterSync()
            await loop.run_in_executor(executor, sync.run)
            return {"status": "success", "message": "GitHub 실시간 수집 및 역사적 데이터 보강 완료"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

@app.post("/debug/super-sync")
async def run_full_pipeline_debug(db: Session = Depends(get_db)):
    """기존 4월 데이터 삭제 -> 실시간 수집 -> 트렌드 재집계 통합 실행 (완전 실데이터 버전)"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            # 1. 기존 4월 데이터 초기화 (더미 및 이전 수집 잔재 제거)
            db.execute(delete(Trend).where(Trend.year == 2026, Trend.month == 4))
            db.commit()
            
            # 2. 수집기 가동
            collectors = [GithubTrendingCollector(), HackerNewsCollector(), GeekNewsCollector()]
            for c in collectors:
                await loop.run_in_executor(executor, c.run)
            
            # 3. 트렌드 재집계 (오늘 수집된 실제 기사수 기반)
            aggregator = TrendsAggregator()
            await loop.run_in_executor(executor, aggregator.aggregate_all)
            
            return {"status": "success", "message": "4월 데이터 초기화 및 실시간 수집/집계 완료"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# CORS 설정 (라우터 등록 전에 배치해야 안전하게 적용됩니다)
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(api_router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["System"])
async def health_check():
    """시스템 상태 확인을 위한 헬스체크 API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/", tags=["Root"])
async def root():
    return {"message": "TrendRadar API Server is running."}
