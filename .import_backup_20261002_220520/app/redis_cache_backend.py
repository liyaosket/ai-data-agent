import json

import redis

from cache_backend import CacheBackend


class RedisCacheBackend(CacheBackend):

    def __init__(
        self,
        host="localhost",
        port=6379,
        db=0,
    ):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get(self, key: str):

        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set(
        self,
        key: str,
        value,
        ttl_seconds: float = None,
    ):

        serialized = json.dumps(
            value,
            ensure_ascii=False,
            default=str,
        )

        if ttl_seconds is not None:

            self.client.setex(
                key,
                int(ttl_seconds),
                serialized,
            )

        else:

            self.client.set(
                key,
                serialized,
            )

    def delete(self, key: str):

        self.client.delete(key)

    def clear(self):

        self.client.flushdb()
