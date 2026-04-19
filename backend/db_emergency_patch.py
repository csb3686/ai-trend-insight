import os
import pymysql
from dotenv import load_dotenv

def run_patch():
    # .env 로드
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    load_dotenv(dotenv_path=env_path)

    print("--- [DB Patch] Starting Urgent Schema Correction ---")
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
            autocommit=True
        )
        with conn.cursor() as cursor:
            # 컬럼 존재 여부 확인 후 추가
            cursor.execute("SHOW COLUMNS FROM articles LIKE 'tech_category'")
            if not cursor.fetchone():
                print("[DB Patch] Adding 'tech_category' column to 'articles' table...")
                cursor.execute("ALTER TABLE articles ADD COLUMN tech_category VARCHAR(100) DEFAULT NULL AFTER author")
                print("[DB Patch] Column successfully added!")
            else:
                print("[DB Patch] Column 'tech_category' already exists. No action needed.")
        
        print("--- [DB Patch] Patching completed successfully! ---")
    except Exception as e:
        print(f"[DB Patch] Error occurred: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_patch()
