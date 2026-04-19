import os
import sys
import pymysql
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

# 경로 설정 (모듈 임포트를 위해)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.app.core.config import get_settings
from backend.app.core.embedding_utils import GoogleDirectEmbeddings, LocalEmbeddings
from backend.pipeline.embedder.text_splitter import ArticleTextSplitter

settings = get_settings()

class ArticleEmbedder:
    def __init__(self):
        # 1. DB 설정
        self.db_host = settings.mysql_host
        self.db_port = settings.mysql_port
        self.db_user = settings.mysql_user
        self.db_password = settings.mysql_password
        self.db_name = settings.mysql_database
        
        # 2. 임베딩 모델 설정 (로컬/구글 스위칭)
        if settings.embedding_provider == "local":
            self.embeddings = LocalEmbeddings(model_name="jhgan/ko-sroberta-multitask")
            print("[Embedder] Using Local Embedding Mode (ko-sroberta)")
        else:
            self.embeddings = GoogleDirectEmbeddings(
                model="gemini-embedding-001",
                api_key=settings.gemini_api_key
            )
            print("[Embedder] Using Google Gemini Embedding Mode")
        
        # 3. ChromaDB 설정 (RAGService와 완벽 동기화)
        # 프로젝트 루트 디렉토리 찾기
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.persist_directory = os.path.normpath(os.path.join(curr_dir, "../../../", settings.chroma_storage_path))
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

    def run_embedding_pipeline(self, batch_size=1000):
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

                # 3. ChromaDB에 추가 (이미 존재하면 로드 후 추가)
                vector_db = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                
                # 배치 단위로 데이터 추가
                vector_db.add_texts(
                    texts=all_chunks,
                    metadatas=all_metadatas
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
            raise e # 에러를 다시 던져서 Admin Log에 기록되게 합니다.
        finally:
            conn.close()

if __name__ == "__main__":
    embedder = ArticleEmbedder()
    embedder.run_embedding_pipeline()
