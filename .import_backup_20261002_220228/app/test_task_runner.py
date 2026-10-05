from task_runner import TaskRunner


task = {
    "id": "daily_trend",
    "description": "分析最近30天每日支付金额趋势",
    "dependencies": [],
}

context = {}


runner = TaskRunner()

result = runner.run_task(
    task,
    context,
)

print("\n========== FINAL RESULT ==========\n")
print(result)
