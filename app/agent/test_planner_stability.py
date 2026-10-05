from app.agent.llm_router import LLMRouter
from app.agent.planner_evaluator import PlannerEvaluator
from app.planner import create_plan


QUERY = "分析一下昨天支付订单为什么下降？"


def main():
    router = LLMRouter()
    evaluator = PlannerEvaluator()

    print("\n========== PLANNER STABILITY TEST ==========\n")
    print("Query:", QUERY)

    decision = router.route(QUERY)

    print("\n========== ROUTER ==========\n")
    print("route:", decision.route)
    print("intent:", decision.intent)
    print("tools:", decision.tools)

    results = []

    for i in range(5):
        print(f"\n========== RUN {i + 1} ==========\n")

        plan = create_plan(
            QUERY,
            route_decision=decision,
        )

        metrics = evaluator.evaluate(plan)

        results.append(metrics)

        print("task_count:", metrics["task_count"])
        print("dependency_count:", metrics["dependency_count"])
        print("max_parallelism:", metrics["max_parallelism"])
        print(
            "critical_path_length:",
            metrics["critical_path_length"],
        )
        print(
            "dependency_valid:",
            metrics["dependency_valid"],
        )

    print("\n========== SUMMARY ==========\n")

    for i, metrics in enumerate(results, start=1):
        print(
            f"Run {i}: "
            f"tasks={metrics['task_count']}, "
            f"dependencies={metrics['dependency_count']}, "
            f"parallelism={metrics['max_parallelism']}, "
            f"critical_path={metrics['critical_path_length']}, "
            f"dependency_valid={metrics['dependency_valid']}"
        )

    stability = evaluator.evaluate_stability(results)

    print("\n========== STABILITY RANGE ==========\n")

    print(
        "task_count_range:",
        stability["task_count_range"]
    )

    print(
        "dependency_count_range:",
        stability["dependency_count_range"]
    )

    print(
        "parallelism_range:",
        stability["parallelism_range"]
    )

    print(
        "critical_path_range:",
        stability["critical_path_range"]
    )

if __name__ == "__main__":
    main()