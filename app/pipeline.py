from planner import create_plan
from executor import Executor


def run_pipeline(question: str):
    print("\n========== USER QUESTION ==========\n")
    print(question)

    # 1. Planner
    print("\n========== PLANNER ==========\n")

    plan = create_plan(question)

    print("Goal:")
    print(plan["goal"])

    print("\nTasks:")

    for task in plan["tasks"]:
        print(
            f"- {task['id']}: "
            f"{task['description']} "
            f"(dependencies={task['dependencies']})"
        )

    # 2. Executor
    print("\n========== EXECUTOR ==========\n")

    executor = Executor()

    results = executor.run_plan(plan)

    # 3. Results
    print("\n========== EXECUTION RESULTS ==========\n")

    for task_id, result in results.items():
        print(f"[{task_id}]")
        print(result)
        print()

    return {
        "plan": plan,
        "results": results,
    }


def main():
    question = input("请输入你的问题：").strip()

    run_pipeline(question)


if __name__ == "__main__":
    main()
