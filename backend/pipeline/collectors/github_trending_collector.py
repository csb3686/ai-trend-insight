import os
import sys
import time
from datetime import datetime

# 현재 디렉토리 구조상 모듈 임포트를 위해 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.pipeline.collectors.base_collector import BaseCollector
from playwright.sync_api import sync_playwright

class GithubTrendingCollector(BaseCollector):
    def __init__(self):
        super().__init__(source_name="GitHub Trending")
        # 핫한 언어 3개(Python, TypeScript, Rust)와 전체(All) 트렌딩 타겟
        self.target_urls = [
            "https://github.com/trending",
            "https://github.com/trending/python",
            "https://github.com/trending/typescript",
            "https://github.com/trending/rust"
        ]

    def run(self):
        print(f"[{self.source_name}] Playwright 기반 크롤링 시작...")
        saved_count = 0
        total_parsed = 0
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for url in self.target_urls:
                print(f"[{self.source_name}] 접속 중: {url}")
                try:
                    page.goto(url, timeout=60000)
                    time.sleep(2) # 동적 렌더링 대기
                    
                    # 트렌딩 레포지토리 리스트(BoxRow) 찾기
                    repos = page.locator("article.Box-row").all()
                    
                    for repo in repos:
                        # 1. 제목 및 URL (예: "facebook/react")
                        h2 = repo.locator("h2.h3 a")
                        if h2.count() == 0:
                            continue
                        repo_path = h2.inner_text().replace('\n', '').replace(' ', '')
                        repo_url = f"https://github.com/{repo_path}"
                        
                        # 2. 설명
                        desc_locator = repo.locator("p.col-9")
                        description = desc_locator.inner_text().strip() if desc_locator.count() > 0 else ""
                        
                        # 3. 추가 메타데이터 (Language, Stars) - 포트폴리오용 단순화
                        content = f"GitHub Repository: {repo_path}\nDescription: {description}"
                        
                        total_parsed += 1
                        
                        # Database 저장
                        is_saved = self.save_article(
                            title=f"GitHub Trending: {repo_path}",
                            url=repo_url,
                            content=content,
                            published_at=datetime.now(),
                            target_type='github_repo'
                        )
                        
                        if is_saved:
                            saved_count += 1

                except Exception as e:
                    print(f"[{self.source_name}] {url} 처리 중 에러: {str(e)}")

            browser.close()

        print(f"[{self.source_name}] 총 {total_parsed}개 레포 파싱 완료, {saved_count}개 신규 저장됨.")
        
        if saved_count > 0 or total_parsed > 0:
            self.log_collection(items_collected=saved_count, status="success")
        else:
            self.log_collection(items_collected=0, status="failed", error_message="No repos parsed")

if __name__ == "__main__":
    collector = GithubTrendingCollector()
    collector.run()
