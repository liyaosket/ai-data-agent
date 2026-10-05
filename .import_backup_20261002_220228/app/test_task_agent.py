from task_agent import create_task_agent_response


task = {
    "id": "daily_trend",
    "description": "分析最近30天每日支付金额趋势",
    "dependencies": [],
}

context = {}

response = create_task_agent_response(
    task,
    context,
)

print("\n========== RESPONSE ==========\n")

for item in response.output:
    print(item)
