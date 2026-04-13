from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, func
from app.core.database import Base

class Source(Base):
    """데이터 수집 출처 모델 (GeekNews, HackerNews, GitHub 등)"""
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(Enum('rss', 'api', 'crawl'), nullable=False)
    url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
