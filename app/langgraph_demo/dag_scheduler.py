from typing import Any


def get_ready_tasks(
    tasks: list[dict[str, Any]],
    completed_tasks: set[str],
) -> list[dict[str, Any]]:
    """
    返回当前所有依赖已经完成、可以执行的 Task。
    """

    ready = []

    for task in tasks:
        task_id = task["id"]

        # 已经执行过
        if task_id in completed_tasks:
            continue

        dependencies = set(task.get("dependencies", []))

        # 所有依赖都完成
        if dependencies.issubset(completed_tasks):
            ready.append(task)

    return ready
