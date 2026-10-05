import threading
import time
from collections import OrderedDict

from cache_backend import CacheBackend


class InMemoryCacheBackend(CacheBackend):

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: float = 3600,
    ):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

        self._cache = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: str):

        with self._lock:

            item = self._cache.get(key)

            if item is None:
                return None

            value, created_at, ttl = item

            if (
                time.time() - created_at
                > ttl
            ):
                del self._cache[key]
                return None

            self._cache.move_to_end(key)

            return value

    def set(
        self,
        key: str,
        value,
        ttl_seconds: float = None,
    ):

        ttl = (
            ttl_seconds
            if ttl_seconds is not None
            else self.ttl_seconds
        )

        with self._lock:

            self._cache[key] = (
                value,
                time.time(),
                ttl,
            )

            self._cache.move_to_end(key)

            while len(self._cache) > self.max_size:
                self._cache.popitem(
                    last=False
                )

    def delete(self, key: str):

        with self._lock:
            self._cache.pop(key, None)

    def clear(self):

        with self._lock:
            self._cache.clear()
