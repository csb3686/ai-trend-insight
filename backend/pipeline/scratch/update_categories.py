import os
import pymysql
from dotenv import load_dotenv

def update_existing_categories():
    # .env 로드
    load_dotenv()
    
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
        autocommit=True
    )
    
    try:
        with conn.cursor() as cursor:
            # 1. GitHub 데이터 전환 (LANGUAGE -> Trend)
            sql_github = "UPDATE articles SET tech_category = 'Trend' WHERE type = 'github_repo' AND (tech_category = 'LANGUAGE' OR tech_category IS NULL)"
            cursor.execute(sql_github)
            github_count = cursor.rowcount
            
            # 2. 뉴스 데이터 전환 (LANGUAGE -> News)
            sql_news = "UPDATE articles SET tech_category = 'News' WHERE type = 'news' AND (tech_category = 'LANGUAGE' OR tech_category IS NULL)"
            cursor.execute(sql_news)
            news_count = cursor.rowcount
            
            print(f"✅ 카테고리 업데이트 완료!")
            print(f" - GitHub (Trend): {github_count}건")
            print(f" - News (News): {news_count}건")
            
    finally:
        conn.close()

if __name__ == "__main__":
    update_existing_categories()
