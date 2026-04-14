import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def sanitize():
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
        autocommit=True
    )
    try:
        with conn.cursor() as cursor:
            print("[Sanitize] 1. 소스(Sources) 테이블 정비 중...")
            # 기존 소스 모두 삭제 후 고정 ID로 재설정
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE sources")
            cursor.execute("""
                INSERT INTO sources (id, name, url) VALUES 
                (1, 'HackerNews', 'https://news.ycombinator.com'),
                (2, 'GeekNews', 'https://news.hada.io'),
                (3, 'GitHub Trending', 'https://github.com/trending')
            """)
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            print("[Sanitize] 2. 불량 데이터(Not Found URL 등) 삭제 중...")
            # 깨진 URL을 가진 기사들 삭제
            cursor.execute("DELETE FROM articles WHERE url LIKE '%hybrid-media.com%'")
            cursor.execute("DELETE FROM articles WHERE url LIKE '%github.com/search%'") # 기존 깃허브 데이터도 재주입을 위해 삭제
            
            print("[Sanitize] 3. 소스 불명 기사 정리 중...")
            # 정의되지 않은 source_id를 가진 기사들 삭제
            cursor.execute("DELETE FROM articles WHERE source_id NOT IN (1, 2, 3)")
            
            print(" ✅ 데이터베이스 정화 완료.")
    finally:
        conn.close()

if __name__ == "__main__":
    sanitize()
