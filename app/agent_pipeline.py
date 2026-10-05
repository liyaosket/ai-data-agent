from planner import create_plan
from parallel_executor import ParallelExecutor

def run_agent_pipeline(
    question: str,
):
    print("\n========== QUESTION ==========\n")
    print(question)

    # 1. Planner
    print("\n========== PLANNING ==========\n")

    plan = create_plan(question)

    print("Goal:")
    print(plan["goal"])

    print("\nTasks:")

    for task in plan["tasks"]:
        print(
            f"- {task['id']}: "
            f"{task['description']} "
            f"dependencies={task['dependencies']}"
        )

    # 2. Executor
    print("\n========== EXECUTION ==========\n")

    executor = ParallelExecutor(
        max_workers=3
    )

    results = executor.run_plan(plan)

    # 3. Results
    print("\n========== RESULTS ==========\n")

    for task_id, result in results.items():
        print(f"\n[{task_id}]")
        print(result)

    return {
        "plan": plan,
        "results": results,
    }


def main():
    question = input(
        "请输入你的问题："
    ).strip()

    run_agent_pipeline(question)


if __name__ == "__main__":
    main()
