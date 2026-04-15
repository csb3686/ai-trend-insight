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
from backend.pipeline.processors.ai_analyst import AIAnalyst

class DataProcessorManager:
    def __init__(self):
        self.db_host = os.getenv('MYSQL_HOST', 'localhost')
        self.db_port = int(os.getenv('MYSQL_PORT', 3306))
        self.db_user = os.getenv('MYSQL_USER', 'root')
        self.db_password = os.getenv('MYSQL_PASSWORD', 'root')
        self.db_name = os.getenv('MYSQL_DATABASE', 'ai_trend')
        self.batch_size = 100
        self.extractor = None 
        self.ai_analyst = AIAnalyst() # AI 분석기 로드

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
                # 1. 처리 대기 중(is_processed=0)인 데이터 가져오기 (type 필드 포함)
                sql_select = """
                    SELECT id, title, content, type 
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
                    article_type = row['type']
                    raw_title = row['title'] or ""
                    raw_content = row['content'] or ""
                    
                    cleaned_title = DataCleaner.clean_text(raw_title)
                    cleaned_content = DataCleaner.clean_text(raw_content)
                    
                    # 3. 기술 키워드 추출
                    title_keywords = self.extractor.extract_keywords(cleaned_title)
                    content_keywords = self.extractor.extract_keywords(cleaned_content)
                    all_tech_ids = set(title_keywords.keys()) | set(content_keywords.keys())
                    
                    # [지능형 필터 및 신기술 감지 로직]
                    # 등록된 기술이 없고, GitHub 프로젝트인 경우 AI 분석 수행
                    if not all_tech_ids and article_type == 'github_repo':
                        # 1단계: 0원 노이즈 필터
                        if self.ai_analyst.is_obvious_noise(cleaned_title, cleaned_content):
                            print(f"[Processor] Noise Detected (Heuristic): {cleaned_title}")
                        else:
                            # 2-3단계: AI 정밀 분석 (잠재적 신기술 탐색)
                            print(f"[Processor] AI Analyzing for Potential Tech: {cleaned_title}")
                            ai_res = self.ai_analyst.analyze_potential_tech(cleaned_title, "", cleaned_content)
                            
                            if ai_res and ai_res.get('is_tech'):
                                tech_name = ai_res.get('tech_name')
                                # 신규 기술 후보 등록 (승인 대기열)
                                sql_pending = """
                                    INSERT INTO pending_technologies (name, category, description, article_id)
                                    VALUES (%s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE updated_at = NOW()
                                """
                                cursor.execute(sql_pending, (
                                    tech_name, 
                                    ai_res.get('category', 'other').lower(),
                                    f"AI 감지 사유: {ai_res.get('reason')}",
                                    article_id
                                ))
                                print(f"[Processor] New Tech Candidate Found: {tech_name}")

                    # 4. 기존 기술 매핑 저장 (있을 경우)
                    for tech_id in all_tech_ids:
                        mention_count = title_keywords.get(tech_id, {}).get('mention_count', 0) + \
                                        content_keywords.get(tech_id, {}).get('mention_count', 0)
                        in_title = 1 if tech_id in title_keywords else 0
                        in_content = 1 if tech_id in content_keywords else 0
                        
                        sql_tech_insert = """
                            INSERT INTO article_technologies (article_id, tech_id, mention_count, in_title, in_content)
                            VALUES (%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE mention_count = VALUES(mention_count)
                        """
                        cursor.execute(sql_tech_insert, (article_id, tech_id, mention_count, in_title, in_content))

                    # 5. 언어 판별 및 기사 업데이트
                    sql_update = """
                        UPDATE articles 
                        SET content = %s, is_processed = 1 
                        WHERE id = %s
                    """
                    
                    if len(cleaned_content) >= 20:
                        cursor.execute(sql_update, (cleaned_content, article_id))
                        processed_count += 1
                    else:
                        cursor.execute(sql_update, ("", article_id))
                        processed_count += 1

                conn.commit()
                print(f"[Processor Manager] 총 {processed_count}개 기사 처리 완료 (AI 분석 포함).")
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
