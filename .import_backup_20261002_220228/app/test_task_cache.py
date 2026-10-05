from task_runner import TaskRunner


task = {
    "id": "CACHE_TEST",
    "description": "请简单回答：什么是数据仓库？",
    "dependencies": [],
}


runner = TaskRunner()


print("=" * 60)
print("第一次执行")
print("=" * 60)

result1 = runner.run_task(
    task,
    context={},
    attempt=1,
)

print()
print("第一次结果：")
print(result1["answer"])


print()
print("=" * 60)
print("第二次执行")
print("=" * 60)

result2 = runner.run_task(
    task,
    context={},
    attempt=1,
)

print()
print("第二次结果：")
print(result2["answer"])


print()
print("=" * 60)
print("TRACE")
print("=" * 60)

for event in runner.trace.get_events():
    print(
        event.event_type,
        "| cost =", event.cost,
        "| input =", event.input_tokens,
        "| output =", event.output_tokens,
        "| duration =", event.duration,
    )
