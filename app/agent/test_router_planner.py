from app.agent.llm_router import LLMRouter
from app.planner import create_plan
from app.agent.planner_evaluator import PlannerEvaluator

def main():

    query = "分析一下昨天支付订单为什么下降？"

    print("\n========== USER QUERY ==========\n")
    print(query)

    # 1. Router
    print("\n========== ROUTER ==========\n")

    router = LLMRouter()

    decision = router.route(query)

    print("route:", decision.route)
    print("intent:", decision.intent)
    print("tools:", decision.tools)
    print("reason:", decision.reason)

    # 2. Planner
    print("\n========== PLANNER ==========\n")

    plan = create_plan(
        query,
        route_decision=decision,
    )

    print("Goal:")
    print(plan["goal"])

    print("\nTasks:")

    for task in plan["tasks"]:
        print(
            f"- {task['id']}: "
            f"{task['description']} "
            f"dependencies={task['dependencies']}"
        )
        
    print("\n========== PLANNER EVALUATION ==========\n")

    evaluator = PlannerEvaluator()
    metrics = evaluator.evaluate(plan)

    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
