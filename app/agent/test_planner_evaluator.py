from app.agent.planner_evaluator import PlannerEvaluator


def main():
    plan = {
        "goal": "分析昨天支付订单为什么下降",
        "tasks": [
            {
                "id": "T1",
                "description": "获取核心指标",
                "dependencies": [],
            },
            {
                "id": "T2",
                "description": "获取维度数据",
                "dependencies": [],
            },
            {
                "id": "T3",
                "description": "检索业务背景",
                "dependencies": [],
            },
            {
                "id": "T4",
                "description": "分析异常原因",
                "dependencies": ["T2", "T3"],
            },
            {
                "id": "T5",
                "description": "生成最终归因",
                "dependencies": ["T1", "T4"],
            },
            {
                "id": "T6",
                "description": "生成图表",
                "dependencies": ["T1", "T2"],
            },
        ],
    }

    evaluator = PlannerEvaluator()
    metrics = evaluator.evaluate(plan)

    print("\n========== PLANNER EVALUATION ==========\n")

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
