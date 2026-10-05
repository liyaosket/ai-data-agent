from app.context_manager import ContextManager
from app.task_runner import TaskRunner


class Executor:
    def __init__(self):
        self.context_manager = ContextManager()
        self.task_runner = TaskRunner()

    def execute_task(self, task: dict):
        task_id = task["id"]

        dependencies = task.get(
            "dependencies",
            [],
        )

        context = self.context_manager.build_context(
            dependencies
        )

        print(
            f"\n[Executor] 开始任务: {task_id}"
        )

        print(
            f"[Executor] 描述: "
            f"{task['description']}"
        )

        print(
            f"[Executor] Dependencies: "
            f"{dependencies}"
        )

        result = self.task_runner.run_task(
            task,
            context,
        )

        self.context_manager.save_task_result(
            task_id,
            result,
        )

        return result

    def run_plan(self, plan: dict):
        tasks = {
            task["id"]: task
            for task in plan["tasks"]
        }

        completed = set()

        while len(completed) < len(tasks):
            progress = False

            for task_id, task in tasks.items():
                if task_id in completed:
                    continue

                dependencies = task.get(
                    "dependencies",
                    [],
                )

                if not all(
                    dependency in completed
                    for dependency in dependencies
                ):
                    continue

                self.execute_task(task)

                completed.add(task_id)

                progress = True

            if not progress:
                remaining = [
                    task_id
                    for task_id in tasks
                    if task_id not in completed
                ]

                raise RuntimeError(
                    "任务依赖无法解析，"
                    f"可能存在循环依赖。"
                    f"剩余任务: {remaining}"
                )

        return self.context_manager.get_all_results()
