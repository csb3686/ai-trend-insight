from fastapi import APIRouter
from app.api.v1.endpoints import chat, trends, articles, admin

api_router = APIRouter()
# prefix를 ""로 설정하여 chat.py 내부의 /chat 경로를 그대로 사용합니다.
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(trends.router, prefix="/trends", tags=["Trends"])
api_router.include_router(articles.router, prefix="/articles", tags=["Articles"])
api_router.include_router(admin.router, tags=["Admin & Health"])
