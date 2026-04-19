try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

import json
from typing import Any, Optional
from app.core.config import get_settings

settings = get_settings()

class CacheService:
    def __init__(self):
        if not REDIS_AVAILABLE:
            print("--- [Cache] redis 패키지가 설치되지 않았습니다. 캐싱 기능이 비활성화됩니다. (pip install redis 필요) 🛡️ ---")
            self.client = None
            return

        try:
            # 타임아웃을 매우 짧게 설정(0.1초)하여 Redis 서버가 없어도 서비스가 지연되지 않게 함
            self.client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=0.1,
                socket_timeout=0.1
            )
            # 연결 확인
            self.client.ping()
            print("--- [Cache] Redis 연결 성공! 고속 캐싱 모드 활성화 🚀 ---")
        except Exception:
            print("--- [Cache] Redis 서버를 찾을 수 없습니다. 표준 DB 모드로 동작합니다. 🛡️ ---")
            self.client = None

    def get(self, key: str) -> Optional[Any]:
        """캐시에서 데이터를 조회하고 JSON을 파싱합니다."""
        if not self.client: return None
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None

    def set(self, key: str, value: Any, expire: int = None) -> bool:
        """데이터를 JSON으로 직렬화하여 캐시에 저장합니다."""
        if not self.client: return False
        try:
            expire = expire or settings.cache_expire
            return self.client.set(key, json.dumps(value), ex=expire)
        except Exception:
            return False

    def delete(self, key: str):
        """특정 캐시 키를 삭제합니다."""
        if self.client:
            self.client.delete(key)

cache_service = CacheService()
