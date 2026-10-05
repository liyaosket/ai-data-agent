from executor import Executor


plan = {
    "goal": "测试 Agent Task 依赖",
    "tasks": [
        {
            "id": "daily_trend",
            "description": "获取最近30天每日支付金额",
            "dependencies": [],
        },
        {
            "id": "anomaly",
            "description": "检测每日支付金额是否存在统计异常",
            "dependencies": [
                "daily_trend"
            ],
        },
        {
            "id": "chart",
            "description": "生成每日支付金额趋势图",
            "dependencies": [
                "daily_trend"
            ],
        },
    ],
}


executor = Executor()

results = executor.run_plan(plan)


print("\n========== FINAL RESULTS ==========\n")

for task_id, result in results.items():
    print(f"\n[{task_id}]")
    print(result)
