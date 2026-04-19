import os
import pymysql
from dotenv import load_dotenv

def check_keyword(keyword="Docker"):
    load_dotenv()
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
            sql = "SELECT COUNT(*) as cnt FROM articles WHERE title LIKE %s OR content LIKE %s"
            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%"))
            result = cursor.fetchone()
            print(f"🔎 Keyword '{keyword}' count in articles: {result['cnt']}")
            
            if result['cnt'] > 0:
                print("--- Top 3 Articles ---")
                cursor.execute("SELECT title, type FROM articles WHERE title LIKE %s OR content LIKE %s LIMIT 3", (f"%{keyword}%", f"%{keyword}%"))
                for row in cursor.fetchall():
                    print(f"- [{row['type']}] {row['title']}")
                    
    finally:
        conn.close()

if __name__ == "__main__":
    check_keyword("Docker")
