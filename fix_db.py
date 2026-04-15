import pymysql
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()

def fix_logs_table():
    try:
        # DB 연결 정보 (환경 변수에서 로드)
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root'),
            database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
            autocommit=True
        )
        
        cursor = conn.cursor()
        
        print("🛠️ 낡은 로그 테이블 구조를 철거 중...")
        cursor.execute("DROP TABLE IF EXISTS collection_logs")
        
        print("🚀 최신 조종석 2.2용 로그 테이블 건축 중 (source_id 포함)...")
        create_sql = """
        CREATE TABLE collection_logs (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            task_type ENUM('COLLECT', 'EMBED', 'STATS', 'OTHER') NOT NULL DEFAULT 'COLLECT',
            source_id INT UNSIGNED COMMENT '수집 출처 FK',
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME,
            status ENUM('IN_PROGRESS', 'SUCCESS', 'FAIL') DEFAULT 'IN_PROGRESS' NOT NULL,
            collected_count INT DEFAULT 0,
            processed_count INT DEFAULT 0,
            error_message TEXT,
            triggered_by VARCHAR(50) DEFAULT 'manual'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        cursor.execute(create_sql)
        
        print("✅ DB 구조 수리 완료! 이제 에러 없이 조종석을 사용하실 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 수리 중 에러 발생: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_logs_table()
