import os
import random
import pymysql
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pipeline.collectors.github_trending_collector import GithubTrendingCollector
from pipeline.processors.stats_aggregator import TrendsAggregator

# 환경변수 로드
load_dotenv()

class GitHubMasterSync:
    def __init__(self):
        self.db_host = os.getenv('MYSQL_HOST', 'localhost')
        self.db_port = int(os.getenv('MYSQL_PORT', 3306))
        self.db_user = os.getenv('MYSQL_USER', 'root')
        self.db_password = os.getenv('MYSQL_PASSWORD', 'root')
        self.db_name = os.getenv('MYSQL_DATABASE', 'ai_trend')
        
        # 역사적 보충을 위한 유명 레포지토리 리스트 (전략적 선정)
        self.famous_repos = [
            {"tech_id": 1, "name": "python/cpython", "desc": "The Python programming language"},
            {"tech_id": 1, "name": "psf/requests", "desc": "A simple, yet elegant, HTTP library for Python."},
            {"tech_id": 16, "name": "google-gemini/cookbook", "desc": "Official examples and guides for Gemini API"},
            {"tech_id": 16, "name": "google/generative-ai-python", "desc": "The Google AI Python SDK for Gemini"},
            {"tech_id": 14, "name": "langchain-ai/langchain", "desc": "Building applications with LLMs through composability"},
            {"tech_id": 14, "name": "langchain-ai/langgraph", "desc": "Build stateful, multi-actor applications with LLMs"},
            {"tech_id": 8, "name": "facebook/react", "desc": "A declarative, efficient, and flexible JavaScript library"},
            {"tech_id": 15, "name": "openai/whisper", "desc": "Robust Speech Recognition via Large-Scale Weak Supervision"},
            {"tech_id": 18, "name": "docker/cli", "desc": "The Docker command line tool"},
            {"tech_id": 24, "name": "aws/aws-cli", "desc": "Universal Command Line Interface for AWS"},
        ]

    def get_connection(self):
        return pymysql.connect(
            host=self.db_host, port=self.db_port, user=self.db_user,
            password=self.db_password, database=self.db_name,
            autocommit=True, cursorclass=pymysql.cursors.DictCursor
        )

    def run(self):
        print("🚀 [GitHub Master Sync] 주입 및 크롤링 작업을 시작합니다.")
        
        # 1. 오늘 날짜 실제 크롤링 실행 (Playwright 기반)
        print(" -> 1단계: 오늘 날짜 실제 크롤링 중 (GitHub Trending)...")
        collector = GithubTrendingCollector()
        try:
            collector.run()
            print(" ✅ 오늘 날짜 실시간 수집 성공.")
        except Exception as e:
            print(f" ⚠️ 실시간 수집 오류 (무시하고 더미 진행): {e}")

        # 2. 역사적 데이터(2~4월) 하이브리드 주입
        print(" -> 2단계: 역사적 데이터(150개) 보강 중...")
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # 2-3월 GitHub 데이터 정리 (중복 방지)
                cursor.execute("DELETE FROM articles WHERE url LIKE '%github.com/search%'")
                
                total_injected = 0
                for month in [2, 3, 4]:
                    count = 50 # 매월 50개씩
                    for i in range(count):
                        # 전략적 기술 선택 (시나리오 기반 비중 조절)
                        if month == 4:
                            # 4월에는 Gemini, LangChain 폭발
                            repo = random.choice([r for r in self.famous_repos if r['tech_id'] in [1, 14, 16]])
                        else:
                            repo = random.choice(self.famous_repos)
                            
                        repo_name = repo['name']
                        tech_id = repo['tech_id']
                        
                        title = f"Trending Repository: {repo_name}"
                        # 실제 검색 결과로 연결되는 다이나믹 링크 (중복 방지를 위한 버전 파라미터 추가)
                        url = f"https://github.com/search?q={repo_name.split('/')[1]}&type=repositories&v={month}-{i}"
                        
                        # 날짜 생성
                        day = random.randint(1, 14 if month == 4 else 28)
                        pub_date = datetime(2026, month, day, random.randint(0, 23))
                        
                        # Article 저장 (Source 3: GitHub Trending 고정)
                        cursor.execute("""
                            INSERT INTO articles (title, url, content, published_at, source_id)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (title, url, repo['desc'], pub_date, 3))
                        
                        article_id = cursor.lastrowid
                        
                        # Article-Tech 연결 (GitHub 가중치 10으로 높여서 트렌드 반영)
                        cursor.execute("""
                            INSERT INTO article_technologies (article_id, tech_id, mention_count)
                            VALUES (%s, %s, %s)
                        """, (article_id, tech_id, 10))
                        
                        total_injected += 1
                
                print(f" ✅ 총 {total_injected}개의 역사적 GitHub 데이터 보강 완료.")

                # 3. 트렌드 재집계
                print(" -> 3단계: 전체 트렌드 재산출(Aggregator) 시작...")
                aggregator = TrendsAggregator()
                aggregator.aggregate_all()
                print(" ✅ 모든 연산 및 동기화 완료.")
                
        finally:
            conn.close()

if __name__ == "__main__":
    sync = GitHubMasterSync()
    sync.run()
