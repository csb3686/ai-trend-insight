import feedparser
from datetime import datetime
import time

def fetch_and_parse_rss(feed_url):
    """
    지정된 RSS 피드 URL을 파싱하여 리스트 형태로 반환합니다.
    - title: 문자열
    - link: 문자열 (url)
    - description: 요약 또는 본문
    - published_at: 파이썬 datetime 객체 (실패 시 현재 시간)
    """
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        title = entry.get('title', '')
        link = entry.get('link', '')
        description = entry.get('description', '')
        
        # 시간 파싱 로직
        published_at = datetime.now()
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_at = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            published_at = datetime.fromtimestamp(time.mktime(entry.updated_parsed))

        articles.append({
            'title': title,
            'link': link,
            'description': description,
            'published_at': published_at
        })

    return articles
