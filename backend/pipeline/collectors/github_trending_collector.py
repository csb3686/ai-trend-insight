import os
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 현재 디렉토리 구조상 모듈 임포트를 위해 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.pipeline.collectors.base_collector import BaseCollector

class GithubTrendingCollector(BaseCollector):
    def __init__(self):
        super().__init__(source_name="GitHub Trending")
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.github_token}" if self.github_token else ""
        }

    def run(self):
        print(f"[{self.source_name}] API 기반 전 세계 Top 100 공정 수집 시작...")
        
        # 1. 최근 7일 내 생성되었거나 업데이트된 프로젝트 중 별이 많은 순서대로 100개 조회
        # (이것이 진정한 '전 세계 트렌드'를 가장 공정하게 반영하는 지표입니다.)
        target_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        url = f"https://api.github.com/search/repositories?q=created:>{target_date}&sort=stars&order=desc&per_page=100"
        
        saved_count = 0
        total_parsed = 0
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            repos = data.get('items', [])
            total_parsed = len(repos)
            
            for repo in repos:
                repo_full_name = repo['full_name']
                repo_url = repo['html_url']
                description = repo['description'] or "설명 없음"
                language = repo['language'] or "Unknown"
                stars = repo['stargazers_count']
                topics = ", ".join(repo.get('topics', []))
                
                # AI 분석 및 집계를 위한 최적의 컨텐츠 구성
                content = (
                    f"Repository: {repo_full_name}\n"
                    f"Main Language: {language}\n"
                    f"Stars: {stars}\n"
                    f"Topics: {topics}\n"
                    f"Description: {description}"
                )
                
                # Database 저장
                is_saved = self.save_article(
                    title=f"GitHub Trending: {repo_full_name}",
                    url=repo_url,
                    content=content,
                    published_at=datetime.now(),
                    target_type='github_repo'
                )
                
                if is_saved:
                    saved_count += 1
                    
            print(f"[{self.source_name}] 총 {total_parsed}개 레포 파싱 완료, {saved_count}개 신규 저장됨.")
            self.log_collection(items_collected=saved_count, status="success")
            
        except Exception as e:
            print(f"[{self.source_name}] 수집 중 오류 발생: {str(e)}")
            self.log_collection(items_collected=0, status="failed", error_message=str(e))

if __name__ == "__main__":
    collector = GithubTrendingCollector()
    collector.run()

if __name__ == "__main__":
    collector = GithubTrendingCollector()
    collector.run()
