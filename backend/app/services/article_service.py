from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
from app.models.article import Article, ArticleTechnology
from app.models.technology import Technology
from app.schemas.article import ArticleListItem, ArticleDetail, SourceInfo

class ArticleService:
    def get_articles(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 10, 
        type: Optional[str] = None,
        source_id: Optional[int] = None,
        q: Optional[str] = None,
        category: Optional[str] = None
    ):
        """기사 목록을 페이지네이션 및 필터링하여 조회합니다."""
        query = db.query(Article).options(joinedload(Article.source))
        
        if type:
            query = query.filter(Article.type == type)
        if source_id:
            query = query.filter(Article.source_id == source_id)
        if q:
            query = query.filter(Article.title.ilike(f"%{q}%"))
        if category:
            query = query.join(ArticleTechnology).join(Technology)\
                         .filter(Technology.category == category)

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
                tech_category='Trend' if art.type == 'github_repo' else 'News',
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
        """특정 기술이 언급된 최신 기사를 조회합니다."""
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
                tech_category='Trend' if art.type == 'github_repo' else 'News',
                published_at=art.published_at,
                created_at=art.created_at
            ) for art in results
        ]

article_service = ArticleService()
