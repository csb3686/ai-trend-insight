from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, JSON, func
from app.core.database import Base

class Technology(Base):
    """기술 키워드 마스터 모델 (Python, React, LangChain 등)"""
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(Enum(
        'language', 'framework', 'database', 'devops', 
        'ai_ml', 'cloud', 'tool', 'other'
    ), default='other', nullable=False)
    aliases = Column(JSON)  # 별칭 목록 (JSON)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
