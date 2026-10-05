from app.task_agent import create_task_agent_response


response = create_task_agent_response([
    {
        "role": "user",
        "content": "请简单回答：什么是数据仓库？",
    }
])

print("response type:", type(response))

print()
print("usage:")
print(response.usage)

print()
print("input_tokens:", response.usage.input_tokens)
print("output_tokens:", response.usage.output_tokens)
print("total_tokens:", response.usage.total_tokens)
