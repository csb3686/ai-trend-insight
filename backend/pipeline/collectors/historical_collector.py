import os
import sys
import time
import requests
from datetime import datetime

# 현재 디렉토리 구조상 모듈 임포트를 위해 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.pipeline.collectors.base_collector import BaseCollector
from backend.app.core.database import SessionLocal
from backend.app.models.trend import Trend
from backend.app.models.technology import Technology

class HistoricalCollector(BaseCollector):
    def __init__(self):
        super().__init__(source_name="Historical API Collector")
        self.github_search_url = "https://api.github.com/search/repositories"
        # API 토큰이 있다면 headers에 추가 (Rate limiting 방지용)
        # self.headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
        self.headers = {}

    def fetch_github_mentions(self, keyword, start_date, end_date):
        """특정 기간 동안의 GitHub 레포지토리 수를 수집합니다."""
        query = f"{keyword} created:{start_date}..{end_date}"
        params = {"q": query, "per_page": 1}
        
        try:
            response = requests.get(self.github_search_url, params=params, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('total_count', 0)
            elif response.status_code == 403:
                print(f"[{self.source_name}] Rate limit exceeded. Waiting...")
                time.sleep(60) # 1분 대기
                return self.fetch_github_mentions(keyword, start_date, end_date)
            else:
                print(f"[{self.source_name}] Error for {keyword}: {response.status_code}")
                return 0
        except Exception as e:
            print(f"[{self.source_name}] Exception: {str(e)}")
            return 0

    def update_trends(self, tech_list, year, month):
        """DB의 trends 테이블을 실 수령 데이터로 업데이트합니다."""
        db = SessionLocal()
        start_date = f"{year}-{month:02d}-01"
        # 간단한 말일 처리
        last_day = 28 if month == 2 else 31
        end_date = f"{year}-{month:02d}-{last_day}"
        
        print(f"[{self.source_name}] {year}년 {month}월 데이터 업데이트 시작...")
        
        for tech_name in tech_list:
            # 기술 ID 조회
            tech = db.query(Technology).filter(Technology.name == tech_name).first()
            if not tech: continue
            
            # 실 데이터 수집
            mention_count = self.fetch_github_mentions(tech_name, start_date, end_date)
            print(f" -> {tech_name}: {mention_count} mentions")
            
            # Trend 테이블 업데이트 (없으면 생성)
            trend = db.query(Trend).filter(
                Trend.tech_id == tech.id, 
                Trend.year == year, 
                Trend.month == month
            ).first()
            
            if trend:
                trend.mention_count = mention_count
            else:
                trend = Trend(
                    tech_id=tech.id,
                    year=year,
                    month=month,
                    mention_count=mention_count,
                    article_count=mention_count // 10, # 가중치 기반 기사수 추정
                    change_rate=0.0,
                    rank_current=0
                )
                db.add(trend)
            
            time.sleep(2) # GitHub API 가이드 준수 (search는 느리게)
        
        db.commit()
        db.close()
        print(f"[{self.source_name}] {month}월 업데이트 완료.")

    def run_for_top_techs(self):
        # 사용자님과 확정한 Top 20 기술 리스트
        top_20 = [
            "GitHub Actions", "MySQL", "Docker", "RAG", "PostgreSQL", 
            "LangChain", "Gemini", "GCP", "LLM", "AWS", 
            "Terraform", "Spring", "MongoDB", "Java", "Django", 
            "Kubernetes", "Go", "Redis", "C++", "React"
        ]
        
        # 2월과 3월 순차 업데이트
        self.update_trends(top_20, 2026, 2)
        self.update_trends(top_20, 2026, 3)

if __name__ == "__main__":
    collector = HistoricalCollector()
    collector.run_for_top_techs()
