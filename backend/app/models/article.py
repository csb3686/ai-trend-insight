from sqlalchemy import Column, BigInteger, Integer, String, Text, Enum, DateTime, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Article(Base):
    """수집된 뉴스 기사 및 GitHub 저장소 모델"""
    __tablename__ = "articles"

    id = Column(BigInteger, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum('news', 'github_repo'), default='news', nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    description = Column(Text)
    content = Column(Text)
    author = Column(String(200))
    published_at = Column(DateTime)
    
    # GitHub 전용 필드
    github_stars = Column(Integer)
    github_language = Column(String(100))
    github_forks = Column(Integer)
    
    # 상태 필드
    is_processed = Column(Boolean, default=False)
    is_embedded = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    source = relationship("Source")
    technologies = relationship("ArticleTechnology", back_populates="article")


class ArticleTechnology(Base):
    """기사(Articles)와 기술(Technologies)의 다대다 매핑 테이블"""
    __tablename__ = "article_technologies"

    id = Column(BigInteger, primary_key=True, index=True)
    article_id = Column(BigInteger, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    tech_id = Column(Integer, ForeignKey("technologies.id", ondelete="CASCADE"), nullable=False)
    mention_count = Column(Integer, default=1)
    in_title = Column(Boolean, default=False)
    in_content = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    article = relationship("Article", back_populates="technologies")
    technology = relationship("Technology")

    __table_args__ = (UniqueConstraint('article_id', 'tech_id', name='uq_article_tech'),)
