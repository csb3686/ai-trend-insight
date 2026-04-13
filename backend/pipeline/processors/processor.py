import os
import sys
from dotenv import load_dotenv
import pymysql

# 경로 설정
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

# 루트 디렉토리의 .env 로드
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', '.env')
load_dotenv(dotenv_path=env_path)

from backend.pipeline.processors.cleaner import DataCleaner
from backend.pipeline.processors.language_detector import LanguageDetector
from backend.pipeline.processors.keyword_extractor import KeywordExtractor

class DataProcessorManager:
    def __init__(self):
        self.db_host = os.getenv('MYSQL_HOST', 'localhost')
        self.db_port = int(os.getenv('MYSQL_PORT', 3306))
        self.db_user = os.getenv('MYSQL_USER', 'root')
        self.db_password = os.getenv('MYSQL_PASSWORD', 'root')
        self.db_name = os.getenv('MYSQL_DATABASE', 'ai_trend')
        self.batch_size = 100
        self.extractor = None # 지연 로딩

    def get_connection(self):
        return pymysql.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def process_batch(self):
        """100개의 데이터를 가져와 일괄 정제 및 키워드 추출 후 DB에 업데이트"""
        conn = self.get_connection()
        if not self.extractor:
            self.extractor = KeywordExtractor(db_conn=conn)

        try:
            with conn.cursor() as cursor:
                # 1. 처리 대기 중(is_processed=0)인 최신 데이터 가져오기
                sql_select = """
                    SELECT id, title, content 
                    FROM articles 
                    WHERE is_processed = 0 
                    ORDER BY id DESC 
                    LIMIT %s
                """
                cursor.execute(sql_select, (self.batch_size,))
                rows = cursor.fetchall()

                if not rows:
                    print("[Processor Manager] 처리할 대기열 데이터가 없습니다.")
                    return 0

                processed_count = 0
                
                # 2. 각 로우별 데이터 다듬기
                for row in rows:
                    article_id = row['id']
                    raw_title = row['title'] or ""
                    raw_content = row['content'] or ""
                    
                    # HTML 제거 및 공백 정규화
                    cleaned_title = DataCleaner.clean_text(raw_title)
                    cleaned_content = DataCleaner.clean_text(raw_content)
                    
                    # 3. 기술 키워드 추출
                    # 제목과 본문을 각각 검사하여 in_title, in_content 판별
                    title_keywords = self.extractor.extract_keywords(cleaned_title)
                    content_keywords = self.extractor.extract_keywords(cleaned_content)
                    
                    # 합집합 기술 목록 생성
                    all_tech_ids = set(title_keywords.keys()) | set(content_keywords.keys())
                    
                    for tech_id in all_tech_ids:
                        mention_count = title_keywords.get(tech_id, {}).get('mention_count', 0) + \
                                        content_keywords.get(tech_id, {}).get('mention_count', 0)
                        in_title = 1 if tech_id in title_keywords else 0
                        in_content = 1 if tech_id in content_keywords else 0
                        
                        # 다대다 관계 저장
                        sql_tech_insert = """
                            INSERT INTO article_technologies (article_id, tech_id, mention_count, in_title, in_content)
                            VALUES (%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE 
                                mention_count = VALUES(mention_count),
                                in_title = VALUES(in_title),
                                in_content = VALUES(in_content)
                        """
                        cursor.execute(sql_tech_insert, (article_id, tech_id, mention_count, in_title, in_content))

                    # 4. 언어 판별 및 기사 업데이트
                    # 언어 판별은 본문 위주로 수행
                    lang = LanguageDetector.detect_language(cleaned_content)
                    
                    sql_update = """
                        UPDATE articles 
                        SET content = %s, is_processed = 1 
                        WHERE id = %s
                    """
                    
                    # 텍스트 길이 필터(20자 이상) 점검하고 저장
                    if len(cleaned_content) >= 20:
                        cursor.execute(sql_update, (cleaned_content, article_id))
                        processed_count += 1
                    else:
                        cursor.execute(sql_update, ("", article_id))
                        processed_count += 1

                # 커밋으로 확정 반영
                conn.commit()
                print(f"[Processor Manager] 총 {processed_count}개 기사의 정제 및 키워드 매핑이 완료되었습니다.")
                return processed_count
                
        except Exception as e:
            print(f"[Cleaner Manager] DB 처리 중 에러 발생: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

if __name__ == "__main__":
    manager = DataProcessorManager()
    manager.process_batch()
