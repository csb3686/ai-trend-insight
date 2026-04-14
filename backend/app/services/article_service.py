from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
from app.models.article import Article, ArticleTechnology
from app.models.source import Source
from app.models.technology import Technology
from app.schemas.article import ArticleListItem, ArticleDetail, SourceInfo

class ArticleService:
    def get_articles(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 10, 
        type: Optional[str] = None,
        source_id: Optional[int] = None
    ):
        """기사 목록을 페이지네이션 및 필터링하여 조회합니다."""
        # 타입 필터가 없을 경우, 뉴스와 깃허브를 골고루 섞기 위해 별도 처리
        if not type and not source_id:
            # 뉴스와 깃허브를 각각 가져옴 (충분한 양)
            news_items = db.query(Article).filter(Article.type == 'news')\
                           .order_by(desc(Article.published_at)).limit(limit).all()
            github_items = db.query(Article).filter(Article.type == 'github_repo')\
                             .order_by(desc(Article.published_at)).limit(limit).all()
            
            # 교차로 섞기 (Interleaving)
            articles = []
            for i in range(limit):
                if i < len(news_items): articles.append(news_items[i])
                if len(articles) >= limit: break
                if i < len(github_items): articles.append(github_items[i])
                if len(articles) >= limit: break
            
            total = db.query(Article).count()
        else:
            query = db.query(Article).options(joinedload(Article.source))
            if type:
                query = query.filter(Article.type == type)
            if source_id:
                query = query.filter(Article.source_id == source_id)
                
            total = query.count()
            articles = query.order_by(desc(Article.published_at), desc(Article.id))\
                           .offset(skip)\
                           .limit(limit)\
                           .all()
                       
        return total, [
            ArticleListItem(
                id=art.id,
                title=art.title,
                url=art.url,
                source_name=art.source.name if art.source else "Unknown",
                type=art.type,
                tech_category=art.technologies[0].technology.category if art.technologies and art.technologies[0].technology else "Others",
                published_at=art.published_at,
                created_at=art.created_at
            ) for art in articles
        ]

    def get_article_by_id(self, db: Session, article_id: int):
        """기사 상세 정보를 조회합니다."""
        article = db.query(Article).options(
            joinedload(Article.source),
            joinedload(Article.technologies).joinedload(ArticleTechnology.technology)
        ).filter(Article.id == article_id).first()
        
        if not article:
            return None
            
        # 연관 기술 이름 리스트 추출
        tech_names = [at.technology.name for at in article.technologies if at.technology]
        
        return ArticleDetail(
            id=article.id,
            title=article.title,
            url=article.url,
            content=article.content,
            description=article.description,
            author=article.author,
            type=article.type,
            source=SourceInfo(
                id=article.source.id,
                name=article.source.name,
                url=article.source.url
            ),
            published_at=article.published_at,
            github_stars=article.github_stars,
            github_language=article.github_language,
            technologies=tech_names
        )

    def get_articles_by_tech(self, db: Session, tech_id: int, limit: int = 3):
        """특정 기술이 언급된 최신 기사 3건을 조회합니다. (히트맵 상세 패널용)"""
        results = db.query(Article).join(ArticleTechnology)\
                    .filter(ArticleTechnology.tech_id == tech_id)\
                    .order_by(desc(Article.published_at))\
                    .limit(limit)\
                    .all()
        
        return [
            ArticleListItem(
                id=art.id,
                title=art.title,
                url=art.url,
                source_name=art.source.name if art.source else "Unknown",
                type=art.type,
                published_at=art.published_at,
                created_at=art.created_at
            ) for art in results
        ]

article_service = ArticleService()
