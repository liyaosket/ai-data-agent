from cached_llm import cached_call_llm


input_items = [
    {
        "role": "user",
        "content": "请简单解释什么是数据仓库。",
    }
]


print("===== 第一次 =====")

response, cache_hit = cached_call_llm(
    input_items
)

print("cache_hit:", cache_hit)
print("answer:", response.output_text)


print()
print("===== 第二次 =====")

response, cache_hit = cached_call_llm(
    input_items
)

print("cache_hit:", cache_hit)
print("answer:", response.output_text)
