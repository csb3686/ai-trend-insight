import os
import pymysql
from dotenv import load_dotenv

def reset_embedding_status(limit=200):
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
            # 모든 기사 리셋 (전수 조사 모드)
            sql = "UPDATE articles SET is_embedded = 0"
            cursor.execute(sql)
            count = cursor.rowcount
            
            print(f"✅ {count}개의 기사 임베딩 상태가 '전체' 리셋되었습니다.")
            print("💡 이제 'embedder.py'를 다시 실행하면 새로운 벡터 DB에 데이터가 쌓입니다.")
            
    finally:
        conn.close()

if __name__ == "__main__":
    reset_embedding_status()
