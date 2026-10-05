from redis_cache_backend import RedisCacheBackend


cache = RedisCacheBackend()


key = "test:key"


print("写入")

cache.set(
    key,
    {
        "answer": "hello redis"
    },
    ttl_seconds=10,
)


print("读取")

result = cache.get(key)

print(result)


print("删除")

cache.delete(key)

print("再次读取")

result = cache.get(key)

print(result)
