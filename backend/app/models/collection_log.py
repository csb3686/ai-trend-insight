from sqlalchemy import Column, BigInteger, Integer, String, Text, Enum, DateTime, func
from app.core.database import Base

class CollectionLog(Base):
    """데이터 수집 및 처리 이력 로그 모델"""
    __tablename__ = "collection_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    task_type = Column(Enum('COLLECT', 'EMBED', 'STATS', 'OTHER'), nullable=False, default='COLLECT')
    start_time = Column(DateTime, server_default=func.now())
    end_time = Column(DateTime)
    status = Column(Enum('IN_PROGRESS', 'SUCCESS', 'FAIL'), default='IN_PROGRESS', nullable=False)
    collected_count = Column(Integer, default=0)
    processed_count = Column(Integer, default=0)
    error_message = Column(Text)
    
    # 작업자 정보 (예: 'manual', 'scheduler')
    triggered_by = Column(String(50), default='manual')

    def __repr__(self):
        return f"<CollectionLog(id={self.id}, task={self.task_type}, status={self.status})>"
