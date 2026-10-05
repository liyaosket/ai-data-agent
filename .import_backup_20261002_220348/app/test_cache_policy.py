import time

from llm_cache import LLMCache
from memory_cache_backend import InMemoryCacheBackend


backend = InMemoryCacheBackend(
    max_size=10,
    ttl_seconds=1,
)

cache = LLMCache(
    backend=backend,
)

input_items = [
    {
        "role": "user",
        "content": "hello",
    }
]


response = {
    "answer": "world"
}


print("写入 Cache")

cache.set(
    input_items,
    "test-model",
    response,
)


print("立即读取:")

result = cache.get(
    input_items,
    "test-model",
)

print(result)


print()
print("等待 1.5 秒...")

time.sleep(1.5)


print("再次读取:")

result = cache.get(
    input_items,
    "test-model",
)

print(result)


print()
print("=" * 60)
print("LRU TEST")
print("=" * 60)


backend = InMemoryCacheBackend(
    max_size=2,
    ttl_seconds=100,
)

cache = LLMCache(
    backend=backend,
)


def make_input(text):
    return [
        {
            "role": "user",
            "content": text,
        }
    ]


A = make_input("A")
B = make_input("B")
C = make_input("C")


cache.set(
    A,
    "test-model",
    "response-A",
)

cache.set(
    B,
    "test-model",
    "response-B",
)


# 访问 A
cache.get(
    A,
    "test-model",
)


# 加入 C
cache.set(
    C,
    "test-model",
    "response-C",
)


print("A:", cache.get(A, "test-model"))
print("B:", cache.get(B, "test-model"))
print("C:", cache.get(C, "test-model"))
