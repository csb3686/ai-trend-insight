from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from typing import List, Optional
from app.models.trend import Trend
from app.models.technology import Technology
from app.schemas.trend import TrendHeatmapItem, TrendTopItem, TrendTimelineItem

class TrendService:
    def get_latest_period(self, db: Session):
        """데이터가 존재하는 가장 최신 연도와 월을 조회합니다."""
        result = db.query(Trend.year, Trend.month).order_by(desc(Trend.year), desc(Trend.month)).first()
        if result:
            return result.year, result.month
        return 2024, 4  # 기본값

    def get_heatmap_data(self, db: Session, year: Optional[int] = None, month: Optional[int] = None):
        """특정 시점의 모든 기술 트렌드 데이터를 조회합니다. (히트맵용)"""
        if not year or not month:
            year, month = self.get_latest_period(db)

        # Technology 테이블과 Join하여 이름과 카테고리 정보를 가져옵니다.
        results = db.query(
            Trend.tech_id,
            Technology.name,
            Technology.category,
            Trend.mention_count,
            Trend.rank_current,
            Trend.change_rate
        ).join(Technology, Trend.tech_id == Technology.id)\
         .filter(Trend.year == year, Trend.month == month)\
         .order_by(desc(Trend.mention_count))\
         .all()

        return year, month, [
            TrendHeatmapItem(
                tech_id=row.tech_id,
                name=row.name,
                category=row.category,
                mention_count=row.mention_count,
                rank=row.rank_current,
                change_rate=row.change_rate
            ) for row in results
        ]

    def get_top5_trends(self, db: Session, year: Optional[int] = None, month: Optional[int] = None):
        """변화율 기준 상승/하락 Top 5를 조회합니다."""
        if not year or not month:
            year, month = self.get_latest_period(db)

        # 급상승 (Rising)
        rising = db.query(
            Technology.name,
            Technology.category,
            Trend.change_rate,
            Trend.rank_current
        ).join(Technology, Trend.tech_id == Technology.id)\
         .filter(Trend.year == year, Trend.month == month)\
         .order_by(desc(Trend.change_rate))\
         .limit(5).all()

        # 급하락 (Falling)
        falling = db.query(
            Technology.name,
            Technology.category,
            Trend.change_rate,
            Trend.rank_current
        ).join(Technology, Trend.tech_id == Technology.id)\
         .filter(Trend.year == year, Trend.month == month)\
         .order_by(asc(Trend.change_rate))\
         .limit(5).all()

        return {
            "rising": [TrendTopItem(name=r.name, category=r.category, change_rate=r.change_rate, rank=r.rank_current) for r in rising],
            "falling": [TrendTopItem(name=f.name, category=f.category, change_rate=f.change_rate, rank=f.rank_current) for f in falling]
        }

    def get_tech_timeline(self, db: Session, tech_id: int):
        """특정 기술의 월별 트렌드 추이를 조회합니다."""
        results = db.query(
            Trend.year,
            Trend.month,
            Trend.mention_count,
            Trend.rank_current
        ).filter(Trend.tech_id == tech_id)\
         .order_by(Trend.year, Trend.month)\
         .all()

        return [
            TrendTimelineItem(
                year=row.year,
                month=row.month,
                mention_count=row.mention_count,
                rank=row.rank_current
            ) for row in results
        ]

    def get_all_keywords(self, db: Session):
        """모든 기술 키워드 목록을 조회합니다."""
        return db.query(Technology.id, Technology.name, Technology.category)\
                 .filter(Technology.is_active == True)\
                 .order_by(Technology.name)\
                 .all()

    def get_dashboard_summary(self, db: Session) -> dict:
        """대시보드 상단에 표시될 통계 요약 정보를 집계합니다."""
        from app.models.article import Article
        from datetime import datetime
        
        news_count = db.query(Article).filter(Article.type == 'news').count()
        github_count = db.query(Article).filter(Article.type == 'github_repo').count()
        tech_count = db.query(Technology).filter(Technology.is_active == True).count()
        
        return {
            "news_count": news_count,
            "github_count": github_count,
            "tech_count": tech_count,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "updated_minutes_ago": 1 # 임시값
        }

trend_service = TrendService()
