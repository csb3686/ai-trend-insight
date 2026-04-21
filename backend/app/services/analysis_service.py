from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any
from app.models.technology import Technology
from app.models.article import ArticleTechnology
from app.models.trend import Trend

class AnalysisService:
    def get_tech_ecosystem(self, db: Session, limit: int = 30) -> Dict[str, Any]:
        """
        기술 간의 상관관계(동시 언급)를 분석하여 네트워크 그래프 데이터를 생성합니다.
        가장 많이 언급된 기술 상위 limit(기본 40)개를 대상으로 합니다.
        """
        # 1. 상위 기술 ID 추출 (최신 트렌드 기준, 중복 제거)
        top_techs = db.query(
            Technology.id, 
            Technology.name, 
            Technology.category,
            func.coalesce(func.max(Trend.mention_count), 0).label("max_mentions")
        ).outerjoin(Trend, Technology.id == Trend.tech_id)\
         .filter(Technology.is_active == True)\
         .group_by(Technology.id, Technology.name, Technology.category)\
         .order_by(desc("max_mentions"))\
         .limit(limit).all()
        
        tech_ids = [t.id for t in top_techs]
        tech_info = {t.id: {"name": t.name, "category": t.category} for t in top_techs}

        # 2. 동시 언급(Co-occurrence) 점수 계산
        # 같은 article_id를 가진 기술 쌍을 찾습니다.
        at1 = ArticleTechnology.__table__.alias("at1")
        at2 = ArticleTechnology.__table__.alias("at2")

        # 셀프 조인을 통해 같은 기사 내 서로 다른 기술 조합을 찾음
        co_occurrence = db.query(
            at1.c.tech_id.label("tech1"),
            at2.c.tech_id.label("tech2"),
            func.count(at1.c.article_id).label("weight")
        ).filter(
            at1.c.article_id == at2.c.article_id,
            at1.c.tech_id < at2.c.tech_id, # 중복 쌍 방지 (A-B만 잡고 B-A는 스킵)
            at1.c.tech_id.in_(tech_ids),
            at2.c.tech_id.in_(tech_ids)
        ).group_by(at1.c.tech_id, at2.c.tech_id)\
         .having(func.count(at1.c.article_id) > 0)\
         .order_by(desc("weight"))\
         .all()

        # 3. Cytoscape 형식으로 변환
        nodes = []
        for t in top_techs:
            nodes.append({
                "data": {
                    "id": str(t.id),
                    "name": t.name,
                    "category": t.category
                }
            })

        edges = []
        for rel in co_occurrence:
            edges.append({
                "data": {
                    "source": str(rel.tech1),
                    "target": str(rel.tech2),
                    "weight": rel.weight
                }
            })

        return {
            "nodes": nodes,
            "edges": edges
        }

analysis_service = AnalysisService()
