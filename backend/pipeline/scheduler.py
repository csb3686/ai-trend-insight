import os
import sys
import time
import schedule
import traceback
from datetime import datetime
from backend.app.core.logger import get_logger

# 현재 디렉토리 구조상 모듈 임포트를 위해 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.pipeline.collectors.geek_news_collector import GeekNewsCollector
from backend.pipeline.collectors.hacker_news_collector import HackerNewsCollector
from backend.pipeline.collectors.github_trending_collector import GithubTrendingCollector
from backend.pipeline.processors.processor import DataProcessorManager
from backend.pipeline.processors.stats_aggregator import TrendsAggregator
from backend.pipeline.embedder.embedder import ArticleEmbedder
from backend.app.core.database import SessionLocal

logger = get_logger()

def job_geek_news(auto_log=True):
    logger.info("GeekNews 수집 작업 시작...")
    try:
        collector = GeekNewsCollector(auto_log=auto_log)
        collector.run()
        logger.info("GeekNews 수집 작업 정상 종료")
        return True
    except Exception as e:
        logger.error(f"GeekNews 수집 중 중명적 에러: {e}")
        logger.error(traceback.format_exc())
        return False

def job_hacker_news(auto_log=True):
    logger.info("HackerNews 수집 작업 시작...")
    try:
        collector = HackerNewsCollector(auto_log=auto_log)
        collector.run()
        logger.info("HackerNews 수집 작업 정상 종료")
        return True
    except Exception as e:
        logger.error(f"HackerNews 수집 중 치명적 에러: {e}")
        logger.error(traceback.format_exc())
        return False

def job_github_trending(auto_log=True):
    logger.info("GitHub Trending 수집 작업 시작...")
    try:
        collector = GithubTrendingCollector(auto_log=auto_log)
        collector.run()
        logger.info("GitHub Trending 수집 작업 정상 종료")
        return True
    except Exception as e:
        logger.error(f"GitHub Trending 수집 중 치명적 에러: {e}")
        logger.error(traceback.format_exc())
        return False

def job_process_data():
    """수집된 기사 데이터를 AI 분석 및 엔티티 추출"""
    logger.info("기사 데이터 전처리 작업 시작...")
    try:
        processor = DataProcessorManager()
        processor.process_batch()
        logger.info("기사 데이터 전처리 작업 완료")
    except Exception as e:
        logger.error(f"기사 전처리 중 에러 발생: {e}")
        logger.error(traceback.format_exc())

def job_embed_data():
    """최신 기사들을 벡터 DB로 임베딩"""
    logger.info("AI 임베딩 작업 시작...")
    try:
        embedder = ArticleEmbedder()
        embedder.run_embedding_pipeline()
        logger.info("AI 임베딩 작업 완료")
    except Exception as e:
        logger.error(f"임베딩 작업 중 에러 발생: {e}")
        logger.error(traceback.format_exc())

def job_aggregate_trends():
    """월별 트렌드 통계 집계 시작"""
    logger.info("월별 트렌드 통계 집계 시작...")
    try:
        aggregator = TrendsAggregator()
        aggregator.aggregate_all()
        logger.info("월별 트렌드 통계 집계 완료")
    except Exception as e:
        logger.error(f"통계 집계 중 에러 발생: {e}")
        logger.error(traceback.format_exc())

def main():
    logger.info("==================================================")
    logger.info("🚀 AI Trend Insight - Python 스케줄러 출근 완료 🚀")
    logger.info("==================================================")
    
    # 스케줄 등록
    schedule.every(1).hours.do(job_geek_news)        # 1시간마다 수집
    schedule.every(3).hours.do(job_hacker_news)      # 3시간마다 수집
    schedule.every(6).hours.do(job_github_trending)  # 6시간마다 수집
    
    schedule.every(1).hours.do(job_process_data)     # 1시간마다 전처리
    schedule.every(1).hours.do(job_embed_data)       # 1시간마다 임베딩
    schedule.every(6).hours.do(job_aggregate_trends) # 6시간마다 통계 갱신
    
    logger.info("[스케줄러] 백그라운드 무한 대기 모드 진입...")

    # 무한 루프
    while True:
        try:
            schedule.run_pending()
            time.sleep(60) 
        except KeyboardInterrupt:
            logger.info("[스케줄러] 사용자에 의해 종료되었습니다.")
            break
        except Exception as e:
            logger.error(f"스케줄러 루프 내 예상치 못한 오류: {e}")
            logger.error(traceback.format_exc())
            time.sleep(60)

if __name__ == "__main__":
    main()
