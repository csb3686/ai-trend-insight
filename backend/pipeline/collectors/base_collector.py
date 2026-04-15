import os
import hashlib
from datetime import datetime
import pymysql
from dotenv import load_dotenv

class BaseCollector:
    def __init__(self, source_name):
        self.source_name = source_name
        # 루트 디렉토리의 .env 로드
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', '.env')
        load_dotenv(dotenv_path=env_path)

        # 데이터베이스 연결
        self.conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root'), # 기본값
            database=os.getenv('MYSQL_DATABASE', 'ai_trend'),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.source_id = self._get_source_id()

    def _get_source_id(self):
        """현재 source_name에 해당하는 source_id를 가져오거나 생성합니다."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM sources WHERE name = %s", (self.source_name,))
            result = cursor.fetchone()
            if result:
                return result['id']
            else:
                cursor.execute("INSERT INTO sources (name, url) VALUES (%s, %s)", (self.source_name, ""))
                return cursor.lastrowid

    def is_url_exists(self, url):
        """DB에 이미 존재하는 URL인지 확인"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id FROM articles WHERE url = %s", (url,))
            return cursor.fetchone() is not None

    def save_article(self, title, url, content, published_at, target_type='news'):
        """단일 기사를 articles 테이블에 저장"""
        if self.is_url_exists(url):
            return False  # 이미 존재함

        with self.conn.cursor() as cursor:
            sql = """
            INSERT INTO articles (source_id, title, content, url, published_at, type)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (self.source_id, title, content, url, published_at, target_type))
            return True # 저장 성공

    def log_collection(self, items_collected, status="success", error_message=None):
        """수집 이력 남기기 (Cockpit 2.0 규격 대응)"""
        # status 값을 SUCCESS/FAIL로 변환
        final_status = "SUCCESS" if status.lower() == "success" else "FAIL"
        
        with self.conn.cursor() as cursor:
            sql = """
            INSERT INTO collection_logs (task_type, source_id, collected_count, status, error_message, end_time, triggered_by)
            VALUES ('COLLECT', %s, %s, %s, %s, NOW(), 'scheduler')
            """
            cursor.execute(sql, (self.source_id, items_collected, final_status, error_message))

    def close(self):
        if self.conn:
            self.conn.close()
