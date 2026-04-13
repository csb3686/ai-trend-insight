import os
import sys
import pymysql
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# 경로 설정 (모듈 임포트를 위해)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.pipeline.embedder.text_splitter import ArticleTextSplitter

# .env 로드
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', '.env')
load_dotenv(dotenv_path=env_path)

class ArticleEmbedder:
    def __init__(self):
        # 1. DB 설정
        self.db_host = os.getenv('MYSQL_HOST', 'localhost')
        self.db_port = int(os.getenv('MYSQL_PORT', 3306))
        self.db_user = os.getenv('MYSQL_USER', 'root')
        self.db_password = os.getenv('MYSQL_PASSWORD', 'root')
        self.db_name = os.getenv('MYSQL_DATABASE', 'ai_trend')
        
        # 2. 임베딩 모델 설정
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")
            
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.api_key
        )
        
        # 3. ChromaDB 설정 (완전히 새로운 경로와 이름을 사용합니다)
        self.persist_directory = os.path.join(os.path.dirname(__file__), '../../chroma_storage')
        self.collection_name = "trend_insight_final"
        
        # 4. 텍스트 분할기 설정
        self.text_splitter = ArticleTextSplitter(chunk_size=500, chunk_overlap=50)

    def get_db_connection(self):
        return pymysql.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def run_embedding_pipeline(self, batch_size=20):
        """임베딩되지 않은 기사를 가져와 처리하는 전체 파이프라인"""
        conn = self.get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 1. 대상 기사 가져오기
                sql = "SELECT id, title, content, url, published_at FROM articles WHERE is_embedded = 0 LIMIT %s"
                cursor.execute(sql, (batch_size,))
                articles = cursor.fetchall()
                
                if not articles:
                    print("[Embedder] 임베딩할 새로운 기사가 없습니다.")
                    return 0

                print(f"[Embedder] 총 {len(articles)}개의 기사를 임베딩 처리합니다.")
                
                # 2. 텍스트 분할 및 문서 준비
                all_chunks = []
                all_metadatas = []
                article_ids = []
                
                for art in articles:
                    article_id = art['id']
                    content = art['content'] or art['title'] # 본문 없으면 제목이라도
                    
                    # 텍스트 쪼개기
                    chunks = self.text_splitter.split_text(content)
                    
                    for chunk in chunks:
                        all_chunks.append(chunk)
                        all_metadatas.append({
                            "article_id": article_id,
                            "title": art['title'],
                            "url": art['url'],
                            "published_at": str(art['published_at']) if art['published_at'] else ""
                        })
                    
                    article_ids.append(article_id)

                # 3. ChromaDB에 추가 (임베딩 모델이 내부적으로 호출됨)
                vector_db = Chroma.from_texts(
                    texts=all_chunks,
                    embedding=self.embeddings,
                    metadatas=all_metadatas,
                    persist_directory=self.persist_directory,
                    collection_name=self.collection_name
                )
                # 4. MySQL 상태 업데이트
                if article_ids:
                    format_strings = ','.join(['%s'] * len(article_ids))
                    update_sql = f"UPDATE articles SET is_embedded = 1 WHERE id IN ({format_strings})"
                    cursor.execute(update_sql, tuple(article_ids))

                print(f"[Embedder] {len(article_ids)}개 기사의 임베딩 저장 완료.")
                return len(article_ids)

        except Exception as e:
            print(f"[Embedder Error] {e}")
            return 0
        finally:
            conn.close()

if __name__ == "__main__":
    embedder = ArticleEmbedder()
    embedder.run_embedding_pipeline()
