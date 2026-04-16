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
        """변화율 기준 상승/하락 Top 5를 조회하며, 시각화용 타임라인과 인사이트를 포함합니다."""
        if not year or not month:
            year, month = self.get_latest_period(db)

        # 급상승 (Rising)
        rising_rows = db.query(
            Trend.tech_id,
            Technology.name,
            Technology.category,
            Trend.change_rate,
            Trend.rank_current
        ).join(Technology, Trend.tech_id == Technology.id)\
         .filter(Trend.year == year, Trend.month == month)\
         .order_by(desc(Trend.change_rate))\
         .limit(5).all()

        # 급하락 (Falling)
        falling_rows = db.query(
            Trend.tech_id,
            Technology.name,
            Technology.category,
            Trend.change_rate,
            Trend.rank_current
        ).join(Technology, Trend.tech_id == Technology.id)\
         .filter(Trend.year == year, Trend.month == month)\
         .order_by(asc(Trend.change_rate))\
         .limit(5).all()

        def populate_extra_data(rows):
            results = []
            for r in rows:
                # 1. 시계열 데이터 (최근 4개월)
                timeline_data = db.query(
                    Trend.year,
                    Trend.month,
                    Trend.mention_count,
                    Trend.rank_current,
                    Trend.change_rate
                ).filter(Trend.tech_id == r.tech_id)\
                 .order_by(Trend.year, Trend.month)\
                 .all()

                timeline = [
                    TrendTimelineItem(
                        year=t.year, month=t.month, 
                        mention_count=t.mention_count, rank=t.rank_current
                    ) for t in timeline_data[-4:] # 최근 4개월만
                ]

                # 2. 급성장 헤드라인 (가장 높은 변화율 기준)
                peak_headline = f"{r.name}에 대한 관심도 변화 발생"
                if timeline_data:
                    # 변화율이 가장 높았던 달(골든 먼스) 찾기
                    peak_row = max(timeline_data, key=lambda x: x.change_rate if x.change_rate is not None else 0)
                    from app.models.article import Article
                    month_str = str(peak_row.month).zfill(2)
                    pattern = f"{peak_row.year}-{month_str}%"
                    
                    peak_article = db.query(Article.title).filter(
                        Article.title.contains(r.name),
                        Article.published_at.like(pattern)
                    ).order_by(desc(Article.created_at)).first()
                    
                    if peak_article:
                        peak_headline = peak_article.title

                results.append(TrendTopItem(
                    tech_id=r.tech_id,
                    name=r.name,
                    category=r.category,
                    change_rate=r.change_rate,
                    rank=r.rank_current,
                    peak_headline=peak_headline,
                    timeline=timeline
                ))
            return results

        return {
            "rising": populate_extra_data(rising_rows),
            "falling": populate_extra_data(falling_rows)
        }

    def get_tech_timeline(self, db: Session, tech_id: int):
        """특정 기술의 월별 트렌드 추이 및 인사이트(원인 분석)를 조회합니다."""
        from app.models.article import Article

        # 1. 기술 기본 정보 조회 (이름, 설명)
        tech = db.query(Technology.name, Technology.description).filter(Technology.id == tech_id).first()
        if not tech:
            return None
            
        tech_name = tech.name or "해당 기술"
        tech_description = tech.description

        # 2. 시계열 데이터 조회
        results = db.query(
            Trend.year,
            Trend.month,
            Trend.mention_count,
            Trend.rank_current,
            Trend.change_rate
        ).filter(Trend.tech_id == tech_id)\
         .order_by(Trend.year, Trend.month)\
         .all()

        if not results:
            return {
                "tech_id": tech_id,
                "name": tech_name,
                "description": tech_description,
                "timeline": []
            }

        timeline = [
            TrendTimelineItem(
                year=row.year,
                month=row.month,
                mention_count=row.mention_count,
                rank=row.rank_current
            ) for row in results
        ]

        # 3. 순위 변동 계산 (최근 2개월 비교)
        rank_current = results[-1].rank_current
        rank_change = 0
        if len(results) >= 2:
            rank_change = (results[-2].rank_current or 0) - (results[-1].rank_current or 0)

        # 4. 급상승 원인 분석 (0토큰 방식)
        # 전 시계열 중 가장 높은 변화율(상승폭)을 보인 '골든 먼스'를 찾습니다.
        peak_row = max(results, key=lambda x: x.change_rate if x.change_rate is not None else 0)
        
        peak_article = None
        if tech_name:
            # 더 안전한 LIKE 패턴 매칭 방식으로 변경 (YYYY-MM 형식)
            month_str = str(peak_row.month).zfill(2)
            pattern = f"{peak_row.year}-{month_str}%"
            
            peak_article = db.query(Article.title).filter(
                Article.title.contains(tech_name),
                Article.published_at.like(pattern)
            ).order_by(desc(Article.created_at)).first()

        return {
            "tech_id": tech_id,
            "name": tech_name,
            "description": tech_description,
            "rank_current": rank_current,
            "rank_change": rank_change,
            "peak_year": peak_row.year,
            "peak_month": peak_row.month,
            "peak_headline": peak_article.title if peak_article else f"{tech_name}에 대한 관련 분야 관심도 급증",
            "timeline": timeline
        }

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
        
        # 진짜 마지막 업데이트 시간 조회 (최신 기사 기준)
        last_article = db.query(Article).order_by(desc(Article.created_at)).first()
        last_updated_dt = last_article.created_at if last_article else datetime.now()
        
        # 몇 분 전인지 계산
        minutes_ago = int((datetime.now() - last_updated_dt).total_seconds() / 60)
        
        return {
            "news_count": news_count,
            "github_count": github_count,
            "tech_count": tech_count,
            "last_updated": last_updated_dt.strftime("%Y-%m-%d %H:%M"),
            "updated_minutes_ago": minutes_ago
        }

trend_service = TrendService()
