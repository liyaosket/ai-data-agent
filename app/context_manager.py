class ContextManager:
    def __init__(self):
        self.tasks = {}

    def save_task_result(
        self,
        task_id: str,
        result: dict,
    ):
        self.tasks[task_id] = result

    def get_task_result(
        self,
        task_id: str,
    ):
        if task_id not in self.tasks:
            raise KeyError(
                f"Task result 不存在: {task_id}"
            )

        return self.tasks[task_id]

    def build_context(
        self,
        dependencies: list[str],
    ) -> dict:
        context = {}

        for task_id in dependencies:
            context[task_id] = self.get_task_result(
                task_id
            )

        return context

    def get_all_results(self):
        return self.tasks
