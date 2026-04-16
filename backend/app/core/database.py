from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

# SQLAlchemy 엔진 생성
# pool_pre_ping=True: 연결 유효성을 미리 체크하여 'MySQL server has gone away' 에러 방지
engine = create_engine(
    settings.mysql_url, 
    pool_pre_ping=True,
    echo=False,
    pool_size=10,        # 기본 연결 수 확대
    max_overflow=20,     # 최대 초과 허용 연결 수
    pool_timeout=10,     # 연결 대기 시간 10초 제한
    connect_args={"connect_timeout": 5}
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델의 베이스 클래스
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성 주입을 위한 제너레이터
    FastAPI의 Depends(get_db)로 사용하며, 요청 종료 시 자동으로 닫힙니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
