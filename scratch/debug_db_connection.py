import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def test_db_connection():
    print("🔍 데이터베이스 연결 테스트 시작...")
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'adminuser'),
            database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
            connect_timeout=5
        )
        print("✅ 성공: 데이터베이스에 성공적으로 연결되었습니다!")
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM articles")
            count = cursor.fetchone()[0]
            print(f"📊 현재 수집된 기사 수: {count}건")
            
        conn.close()
    except Exception as e:
        print(f"❌ 실패: 데이터베이스 연결 중 오류 발생!")
        print(f"👉 에러 내용: {e}")
        print("\n💡 해결책: MySQL 서비스가 켜져 있는지, 그리고 .env의 비밀번호(adminuser)가 맞는지 확인해 주세요.")

if __name__ == "__main__":
    test_db_connection()
