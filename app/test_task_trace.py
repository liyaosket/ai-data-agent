from app.task_runner import TaskRunner


runner = TaskRunner()

task = {
    "id": "T1",
    "description": "查询最近7天每天的订单数量",
}

context = {}

result = runner.run_task(
    task=task,
    context=context,
    attempt=1,
)

print()
print("=" * 70)
print("EXECUTION TRACE")
print("=" * 70)

for event in runner.trace.get_task_events("T1"):

    print(
        f"{event.timestamp} | "
        f"attempt={event.attempt} | "
        f"{event.event_type:<15} | "
        f"tool={event.tool_name} | "
        f"duration={event.duration} | "
        f"success={event.success}"
    )
