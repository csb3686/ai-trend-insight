"""
환경변수 설정 모듈

.env 파일을 읽어 Pydantic Settings 클래스로 관리합니다.
새로운 환경변수 추가 시 이 파일에 필드를 추가하세요.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    프로젝트 전역 설정 클래스
    .env 파일 또는 시스템 환경변수에서 값을 자동으로 로드합니다.
    """

    # ========================
    # Google Gemini API (Embedding용)
    # ========================
    gemini_api_key: str

    # ========================
    # Groq API (LLM용)
    # ========================
    groq_api_key: str

    # ========================
    # GitHub API
    # ========================
    github_token: str

    # ========================
    # LLM & Embedding Settings
    # ========================
    use_llm_provider: str = "groq"
    embedding_provider: str = "local"

    # ========================
    # MySQL 데이터베이스
    # ========================
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str
    mysql_database: str = "ai_trend"

    # ========================
    # Redis 캐시
    # ========================
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_expire: int = 3600  # 기본 만료 시간 (1시간)

    # ========================
    # Chroma 벡터 DB
    # ========================
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_storage_path: str = "chroma_storage"  # 로컬 저장소 폴더명

    # ========================
    # n8n 워크플로 서비스
    # ========================
    n8n_host: str = "localhost"
    n8n_port: int = 5678

    # ========================
    # Langflow 서비스
    # ========================
    langflow_host: str = "localhost"
    langflow_port: int = 7860

    # ========================
    # FastAPI 서버
    # ========================
    fastapi_host: str = "localhost"
    fastapi_port: int = 8000

    # ========================
    # 관리자 보안 (시크릿 URL용)
    # ========================
    admin_token: str

    # ========================
    # 편의 속성 (직접 설정 불필요)
    # ========================
    @property
    def mysql_url(self) -> str:
        """SQLAlchemy 접속 URL 반환"""
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            "?charset=utf8mb4"
        )

    @property
    def chroma_url(self) -> str:
        """Chroma 서버 URL 반환"""
        return f"http://{self.chroma_host}:{self.chroma_port}"

    @property
    def langflow_url(self) -> str:
        """Langflow 서버 URL 반환"""
        return f"http://{self.langflow_host}:{self.langflow_port}"

    class Config:
        # 현재 파일(config.py) 위치를 기준으로 프로젝트 루트의 .env 파일을 동적으로 찾습니다.
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        env_file = os.path.join(base_dir, ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False  # 대소문자 구분 없이 환경변수 매핑


@lru_cache()
def get_settings() -> Settings:
    """
    Settings 인스턴스를 반환합니다.
    @lru_cache로 한 번만 생성하고 재사용합니다.

    사용 예시:
        from app.core.config import get_settings
        settings = get_settings()
        print(settings.mysql_url)
    """
    return Settings()
