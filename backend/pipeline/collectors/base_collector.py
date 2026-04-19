import os
import hashlib
from datetime import datetime
import pymysql
import traceback
from dotenv import load_dotenv
from backend.app.core.logger import get_logger

class BaseCollector:
    def __init__(self, source_name, auto_log=True):
        self.source_name = source_name
        self.auto_log = auto_log
        self.logger = get_logger()
        
        # 루트 디렉토리의 .env 로드
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', '.env')
        load_dotenv(dotenv_path=env_path)

        try:
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
            self.logger.info(f"[{self.source_name}] Collector 초기화 완료 (Source ID: {self.source_id})")
        except Exception as e:
            self.logger.error(f"[{self.source_name}] DB 연결 실패: {e}")
            self.logger.error(traceback.format_exc())
            raise e

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

    def save_article(self, title, url, content, published_at, target_type='news', tech_category=None):
        """단일 기사를 articles 테이블에 저장 (카테고리 지정 가능)"""
        if self.is_url_exists(url):
            return False  # 이미 존재함

        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO articles (source_id, title, content, url, published_at, type, tech_category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (self.source_id, title, content, url, published_at, target_type, tech_category))
                self.logger.info(f"[{self.source_name}] 신규 기사 저장: {title[:30]}...")
                return True # 저장 성공
        except Exception as e:
            self.logger.error(f"[{self.source_name}] 기사 저장 중 에러: {e}")
            return False

    def log_collection(self, items_collected, status="success", error_message=None):
        """수집 이력 남기기 (auto_log가 True일 때만 실제 DB 기록)"""
        if not self.auto_log:
            return

        # status 값을 SUCCESS/FAIL로 변환
        final_status = "SUCCESS" if status.lower() == "success" else "FAIL"
        
        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO collection_logs (task_type, source_id, collected_count, status, error_message, end_time, triggered_by)
                VALUES ('COLLECT', %s, %s, %s, %s, NOW(), 'scheduler')
                """
                cursor.execute(sql, (self.source_id, items_collected, final_status, error_message))
            
            log_msg = f"[{self.source_name}] 수집 작업 완료 - 상태: {final_status}, 개수: {items_collected}"
            if error_message:
                log_msg += f", 에러: {error_message}"
                self.logger.error(log_msg)
            else:
                self.logger.info(log_msg)
        except Exception as e:
            self.logger.error(f"[{self.source_name}] 수집 로그 기록 실패: {e}")

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                self.logger.info(f"[{self.source_name}] DB 연결 종료")
            except:
                pass
