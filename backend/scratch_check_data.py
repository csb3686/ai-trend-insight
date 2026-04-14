import os
import pymysql
from dotenv import load_dotenv

# .env 로드
load_dotenv()

def check_data():
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            # 월별 기사 수 확인
            cursor.execute("""
                SELECT DATE_FORMAT(published_at, '%Y-%m') as month, COUNT(*) as count 
                FROM articles 
                GROUP BY month 
                ORDER BY month DESC
            """)
            print("--- Monthly Article Counts ---")
            for row in cursor.fetchall():
                print(f"{row['month']}: {row['count']} articles")
            
            # 기술별 2-3월 데이터 합산 확인 (비교용)
            cursor.execute("""
                SELECT t.name, SUM(at.mention_count) as total 
                FROM article_technologies at 
                JOIN articles a ON at.article_id = a.id 
                JOIN technologies t ON at.tech_id = t.id
                WHERE a.published_at BETWEEN '2026-02-01' AND '2026-03-31'
                GROUP BY t.id
            """)
            print("\n--- Feb~Mar Mentions per Tech ---")
            for row in cursor.fetchall():
                print(f"{row['name']}: {row['total']}")
                
    finally:
        conn.close()

if __name__ == "__main__":
    check_data()
