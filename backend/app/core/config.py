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
    # Google Gemini API
    # ========================
    gemini_api_key: str

    # ========================
    # GitHub API
    # ========================
    github_token: str

    # ========================
    # MySQL 데이터베이스
    # ========================
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str
    mysql_database: str = "ai_trend"

    # ========================
    # Chroma 벡터 DB
    # ========================
    chroma_host: str = "localhost"
    chroma_port: int = 8001

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
        # 프로젝트 루트의 .env 파일을 자동으로 읽습니다
        env_file = "../../.env"
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
