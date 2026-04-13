from sqlalchemy import Column, BigInteger, Integer, SmallInteger, DateTime, Numeric, UniqueConstraint, func, ForeignKey
from app.core.database import Base

class Trend(Base):
    """월별 기술 트렌드 집계 모델"""
    __tablename__ = "trends"

    id = Column(BigInteger, primary_key=True, index=True)
    tech_id = Column(Integer, ForeignKey("technologies.id", ondelete="CASCADE"), nullable=False)
    year = Column(SmallInteger, nullable=False)
    month = Column(SmallInteger, nullable=False)
    
    mention_count = Column(Integer, default=0)
    article_count = Column(Integer, default=0)
    
    prev_month_count = Column(Integer, default=0)
    change_rate = Column(Numeric(8, 2))
    
    rank_current = Column(Integer)
    rank_prev = Column(Integer)
    
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('tech_id', 'year', 'month', name='uq_trend_tech_month'),)
