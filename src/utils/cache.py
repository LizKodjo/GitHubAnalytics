import logging
import time
from typing import Any, Optional


logger = logging.getLogger(__name__)


class MemoryCache:
    """Simple in-memory cache for development"""

    def __init__(self):
        self._storage = {}

    async def get(self, key: str) -> Optional[Any]:
        data = self._storage.get(key)
        if data and data['expires'] > time.time():
            return data['value']
        elif data:
            # Remove expired entry
            del self._storage[key]
        return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        try:
            self._storage[key] = {
                'value': value,
                'expires': time.time() + ttl
            }
            return True
        except Exception as e:
            logger.warning(f"Cache set failed: {e}")
            return False

    async def delete(self, key: str) -> bool:
        if key in self._storage:
            del self._storage[key]
        return True
