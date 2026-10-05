import time

from app.langgraph_demo.parallel_executor import (
    execute_tasks_parallel,
)


def execute_task(task):
    task_id = task["id"]

    print(f"START {task_id}")

    time.sleep(1)

    print(f"END {task_id}")

    return {
        "task_id": task_id,
        "success": True,
    }


def main():
    tasks = [
        {
            "id": "T1",
            "description": "task 1",
        },
        {
            "id": "T2",
            "description": "task 2",
        },
        {
            "id": "T3",
            "description": "task 3",
        },
    ]

    start = time.perf_counter()

    results = execute_tasks_parallel(
        tasks,
        execute_task,
        max_workers=3,
    )

    duration = time.perf_counter() - start

    print("\nResults:")
    print(results)

    print(f"\nDuration: {duration:.2f}s")

    assert set(results.keys()) == {
        "T1",
        "T2",
        "T3",
    }

    assert duration < 2.5

    print("\nParallel executor test passed")


if __name__ == "__main__":
    main()
