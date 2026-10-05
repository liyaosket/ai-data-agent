from llm_cache import LLMCache


cache = LLMCache()

input_items = [
    {
        "role": "user",
        "content": "什么是数据仓库？",
    }
]

response = {
    "answer": "数据仓库是面向分析的数据存储系统。"
}


print("第一次查询：")

result = cache.get(
    input_items,
    "test-model",
)

print("cache:", result)


cache.set(
    input_items,
    "test-model",
    response,
)


print()
print("第二次查询：")

result = cache.get(
    input_items,
    "test-model",
)

print("cache:", result)
