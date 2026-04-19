import os
import sys

# 현재 디렉토리 구조상 모듈 임포트를 위해 경로 추가 (로컬 단독 실행용)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.pipeline.collectors.base_collector import BaseCollector
from backend.pipeline.collectors.rss_parser import fetch_and_parse_rss

class GeekNewsCollector(BaseCollector):
    def __init__(self, auto_log=True):
        # DB에 저장될 source_name 설정
        super().__init__(source_name="GeekNews", auto_log=auto_log)
        self.feed_url = "https://news.hada.io/rss/news"

    def run(self):
        print(f"[{self.source_name}] RSS 데이터 수집 시작...")
        try:
            articles = fetch_and_parse_rss(self.feed_url)
            saved_count = 0
            
            for article in articles:
                is_saved = self.save_article(
                    title=article['title'],
                    url=article['link'],
                    content=article['description'],
                    published_at=article['published_at'],
                    target_type='news',
                    tech_category='News'
                )
                if is_saved:
                    saved_count += 1
            
            print(f"[{self.source_name}] 총 {len(articles)}개 파싱 완료, {saved_count}개 신규 저장됨.")
            self.log_collection(items_collected=saved_count, status="success")
            
        except Exception as e:
            error_msg = str(e)
            print(f"[{self.source_name}] 수집 중 에러 발생: {error_msg}")
            self.log_collection(items_collected=0, status="failed", error_message=error_msg)
        finally:
            self.close()

if __name__ == "__main__":
    collector = GeekNewsCollector()
    collector.run()
