import json
import logging
from typing import Any, Optional
import redis.asyncio as redis


logger = logging.getLogger(__name__)

class RedisCache:
    """Async Redis cache implementation"""
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._client: Optional[redis.Redis] = None
        
    async def _get_client(self) -> redis.Redis:
        """Get Redis client with connection pooling"""
        if self._client is None:
            self._client = redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return self._client
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            client = await self._get_client()
            value = await client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.warning(f"Cache get failed for key {key}: {e}")
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL"""
        try:
            client = await self._get_client()
            await client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.warning(f"Cache set failed for key {key}: {e}")
            return False
        
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            client = await self._get_client()
            await client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete failed for key {key}: {e}")
            return False
    
class MemoryCache:
    """Fallback in-memory cache for development"""
    
    def __init__(self):
        self._storage = {}
        
    async def get(self, key: str) -> Optional[Any]:
        return self._storage.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        self._storage[key] = value
        return True
    
    async def delete(self, key: str) -> bool:
        if key in self._storage:
            del self._storage[key]
        return True