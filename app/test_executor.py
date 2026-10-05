from executor import Executor


plan = {
    "goal": "测试执行计划",
    "tasks": [
        {
            "id": "daily_trend",
            "description": "获取每日支付金额",
            "dependencies": [],
        },
        {
            "id": "anomaly",
            "description": "检测异常",
            "dependencies": [
                "daily_trend"
            ],
        },
        {
            "id": "chart",
            "description": "生成趋势图",
            "dependencies": [
                "daily_trend"
            ],
        },
    ],
}


executor = Executor()

results = executor.run_plan(plan)

print("\n========== RESULTS ==========\n")

for key, value in results.items():
    print(key)
    print(value)
    print()
