from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable


def execute_tasks_parallel(
    tasks: list[dict[str, Any]],
    execute_task: Callable[[dict[str, Any]], Any],
    max_workers: int = 4,
) -> dict[str, Any]:
    """
    并行执行一批已经满足依赖条件的 Task。

    注意：
    传入的 tasks 必须已经是 ready tasks。
    """

    if not tasks:
        return {}

    results = {}

    worker_count = min(
        max_workers,
        len(tasks),
    )

    with ThreadPoolExecutor(
        max_workers=worker_count
    ) as executor:

        future_to_task = {
            executor.submit(
                execute_task,
                task,
            ): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            task_id = task["id"]

            results[task_id] = future.result()

    return results
