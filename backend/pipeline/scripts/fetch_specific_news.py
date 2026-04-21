import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 레포지토리 루트 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../../.."))

from backend.pipeline.collectors.base_collector import BaseCollector

class CustomSearchCollector(BaseCollector):
    def __init__(self):
        super().__init__(source_name="ManualSearch", auto_log=False)

    def fetch_hackernews(self, keyword):
        print(f"[HackerNews] Searching for: {keyword} (No GitHub)")
        # 넉넉하게 30개를 가져와서 github를 걸러낸 뒤 5개를 채웁니다.
        url = f"https://hn.algolia.com/api/v1/search?query={keyword}&tags=story&hitsPerPage=30"
        try:
            res = requests.get(url, timeout=10)
            data = res.json()
            saved = 0
            for hit in data.get('hits', []):
                if saved >= 5:
                    break
                title = hit.get('title', '')
                link = hit.get('url')
                if not link:
                    link = f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                
                # Github.com 링크 원천 필터링 (순수 블로그/뉴스만 남김)
                if 'github.com' in link:
                    continue
                
                content = hit.get('story_text', '') or f"{keyword}에 관련된 HackerNews 기사입니다."
                
                if self.save_article(title, link, content, datetime.now(), 'news', keyword):
                    saved += 1
            print(f" -> {saved} REAL NEWS articles saved from HN.")
        except Exception as e:
            print(f"HN Fetch Error for {keyword}: {e}")

    def fetch_geeknews(self, keyword):
        print(f"[GeekNews] Searching for: {keyword}")
        url = f"https://news.hada.io/search?q={keyword}"
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            rows = soup.select(".topic_row")
            saved = 0
            for row in rows[:5]:
                title_el = row.select_one(".topictitle a")
                if not title_el:
                    continue
                title = title_el.text.strip()
                link = title_el.get('href', '')
                if link.startswith('/'):
                    link = 'https://news.hada.io' + link
                
                desc_el = row.select_one(".topicdesc")
                desc = desc_el.text.strip() if desc_el else f"{keyword} 관련 긱뉴스 글입니다."
                
                if self.save_article(title, link, desc, datetime.now(), 'news', keyword):
                    saved += 1
            print(f" -> {saved} articles saved from GeekNews.")
        except Exception as e:
            print(f"GeekNews Fetch Error for {keyword}: {e}")

if __name__ == "__main__":
    techs = ["python", "TypeScript", "Go", "LLM", "Rust", "LangChain", "JavaScript", "Java", "AWS"]
    collector = CustomSearchCollector()
    
    for t in techs:
        collector.fetch_hackernews(t)
        collector.fetch_geeknews(t)
        time.sleep(1) # politely wait
    
    collector.close()
    print("All specific tech news fetched!")
