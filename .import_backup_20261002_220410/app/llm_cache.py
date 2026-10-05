import hashlib
import json

from memory_cache_backend import InMemoryCacheBackend


class LLMCache:

    def __init__(self, backend=None):

        self.backend = (
            backend
            if backend is not None
            else InMemoryCacheBackend()
        )

    def _make_key(
        self,
        input_items,
        model,
    ):

        payload = {
            "model": model,
            "input": input_items,
        }

        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        )

        return hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()

    def get(
        self,
        input_items,
        model,
    ):

        key = self._make_key(
            input_items,
            model,
        )

        return self.backend.get(key)

    def set(
        self,
        input_items,
        model,
        response,
        ttl_seconds=None,
    ):

        key = self._make_key(
            input_items,
            model,
        )

        self.backend.set(
            key,
            response,
            ttl_seconds,
        )

    def delete(
        self,
        input_items,
        model,
    ):

        key = self._make_key(
            input_items,
            model,
        )

        self.backend.delete(key)

    def clear(self):
        self.backend.clear()


llm_cache = LLMCache()
