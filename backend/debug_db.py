import pymysql
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()

def check_db():
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root'),
            database=os.getenv('MYSQL_DATABASE', 'ai_trend')
        )
        with conn.cursor() as cursor:
            cursor.execute("DESC collection_logs")
            columns = cursor.fetchall()
            print("--- Collection Logs Columns ---")
            for col in columns:
                print(f"Col: {col[0]}, Type: {col[1]}")
            
            progress_exists = any(col[0] == 'progress' for col in columns)
            print(f"\nProgress Column Exists: {progress_exists}")
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

if __name__ == "__main__":
    check_db()
