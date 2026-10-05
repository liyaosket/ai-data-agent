from parallel_executor import ParallelExecutor


executor = ParallelExecutor(
    max_workers=2,
)

task = {
    "id": "T1",
    "description": "查询最近7天每天的订单数量",
}

result = executor.execute_task(
    task=task,
)

print()
print("=" * 70)
print("TRACE")
print("=" * 70)

for event in executor.get_execution_trace().get_events():
    print(
        f"{event.timestamp} | "
        f"task={event.task_id} | "
        f"attempt={event.attempt} | "
        f"{event.event_type:<15} | "
        f"tool={event.tool_name} | "
        f"duration={event.duration} | "
        f"input={event.input_tokens} | "
        f"output={event.output_tokens} | "
        f"total={event.total_tokens} | "
        f"success={event.success}"
    )
