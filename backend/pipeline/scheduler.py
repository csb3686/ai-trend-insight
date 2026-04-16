import os
import sys
import time
import schedule
from datetime import datetime

# 현재 디렉토리 구조상 모듈 임포트를 위해 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.pipeline.collectors.geek_news_collector import GeekNewsCollector
from backend.pipeline.collectors.hacker_news_collector import HackerNewsCollector
from backend.pipeline.collectors.github_trending_collector import GithubTrendingCollector
from backend.pipeline.processors.processor import DataProcessorManager
from backend.pipeline.processors.stats_aggregator import TrendsAggregator
from backend.pipeline.embedder.embedder import ArticleEmbedder
from backend.app.core.database import SessionLocal

def job_geek_news():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GeekNews 수집 시작...")
    collector = GeekNewsCollector()
    collector.run()

def job_hacker_news():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] HackerNews 수집 시작...")
    collector = HackerNewsCollector()
    collector.run()

def job_github_trending():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GitHub Trending 수집 시작...")
    collector = GithubTrendingCollector()
    collector.run()

def job_process_data():
    """수집된 기사 데이터를 AI 분석 및 엔티티 추출"""
    db = SessionLocal()
    try:
        print("--- [Scheduler] 기사 데이터 전처리 시작 ---")
        processor = DataProcessorManager()
        processor.process_pending_articles(db)
        print("--- [Scheduler] 기사 데이터 전처리 완료 ---")
    finally:
        db.close()

def job_embed_data():
    """최신 기사들을 벡터 DB로 임베딩"""
    db = SessionLocal()
    try:
        print("--- [Scheduler] AI 임베딩 작업 시작 ---")
        embedder = ArticleEmbedder()
        embedder.run_embedding_pipeline()
        print("--- [Scheduler] AI 임베딩 작업 완료 ---")
    finally:
        db.close()

def job_aggregate_trends():
    """월별 트렌드 통계 집계 시작"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 월별 트렌드 통계 집계 시작...")
    aggregator = TrendsAggregator()
    aggregator.aggregate_all()

def main():
    print("==================================================")
    print("🚀 AI Trend Insight - Python 스케줄러(매니저) 출근 🚀")
    print("==================================================")
    
    # 스케줄 등록
    schedule.every(1).hours.do(job_geek_news)        # 1시간마다 수집
    schedule.every(3).hours.do(job_hacker_news)      # 3시간마다 수집
    schedule.every(6).hours.do(job_github_trending)  # 6시간마다 수집
    
    schedule.every(1).hours.do(job_process_data)     # 1시간마다 전처리 (수집 직후 위주)
    schedule.every(1).hours.do(job_embed_data)       # 1시간마다 AI 임베딩
    schedule.every(6).hours.do(job_aggregate_trends) # 6시간마다 통계 갱신
    
    print("[스케줄러 설정 완료] 백그라운드 무한 대기 모드 진입...")
    print("작업을 종료하시려면 터미널 창을 클릭하고 Ctrl + C 를 누르세요.\n")

    # 무한 루프
    while True:
        try:
            schedule.run_pending()
            time.sleep(60) # 1분에 한 번씩 스케줄 시계 확인 (CPU 부하 방지)
        except KeyboardInterrupt:
            print("\n[스케줄러 종료] 매니저가 퇴근합니다. 수고하셨습니다!")
            break
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 스케줄러 자체 오류 발생: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
