class PlannerEvaluator:
    """
    Evaluate the structural quality of a Planner-generated DAG.

    Current metrics:
    - task_count
    - dependency_count
    - max_parallelism
    - critical_path_length
    - dependency_valid
    """

    def evaluate(self, plan: dict) -> dict:
        tasks = plan.get("tasks", [])

        self._validate_task_ids(tasks)
        dependency_valid = self._validate_dependencies(tasks)

        task_count = len(tasks)

        dependency_count = sum(
            len(task.get("dependencies", []))
            for task in tasks
        )

        max_parallelism = self._calculate_max_parallelism(tasks)

        critical_path_length = self._calculate_critical_path(tasks)

        return {
            "task_count": task_count,
            "dependency_count": dependency_count,
            "max_parallelism": max_parallelism,
            "critical_path_length": critical_path_length,
            "dependency_valid": dependency_valid,
        }
    
    def evaluate_stability(self, results):
        if not results:
            raise ValueError("No planner evaluation results.")

        task_counts = [r["task_count"] for r in results]
        dependency_counts = [r["dependency_count"] for r in results]
        parallelisms = [r["max_parallelism"] for r in results]
        critical_paths = [r["critical_path_length"] for r in results]

        task_range = max(task_counts) - min(task_counts)
        dependency_range = max(dependency_counts) - min(dependency_counts)
        parallelism_range = max(parallelisms) - min(parallelisms)
        critical_path_range = max(critical_paths) - min(critical_paths)

        return {
            "task_count_range": task_range,
            "dependency_count_range": dependency_range,
            "parallelism_range": parallelism_range,
            "critical_path_range": critical_path_range,
        }

    def _validate_task_ids(self, tasks: list[dict]):
        task_ids = [task["id"] for task in tasks]

        if len(task_ids) != len(set(task_ids)):
            raise ValueError("Duplicate task id detected.")

    def _validate_dependencies(self, tasks: list[dict]) -> bool:
        task_ids = {
            task["id"]
            for task in tasks
        }

        for task in tasks:
            task_id = task["id"]

            for dependency in task.get("dependencies", []):

                if dependency == task_id:
                    raise ValueError(
                        f"Task {task_id} cannot depend on itself."
                    )

                if dependency not in task_ids:
                    raise ValueError(
                        f"Task {task_id} depends on "
                        f"unknown task {dependency}."
                    )

        return True

    def _calculate_max_parallelism(
        self,
        tasks: list[dict],
    ) -> int:

        if not tasks:
            return 0

        remaining = {
            task["id"]: set(
                task.get("dependencies", [])
            )
            for task in tasks
        }

        completed = set()
        max_parallelism = 0

        while remaining:

            ready = [
                task_id
                for task_id, dependencies
                in remaining.items()
                if dependencies.issubset(completed)
            ]

            if not ready:
                raise ValueError(
                    "Invalid DAG: circular dependency detected."
                )

            max_parallelism = max(
                max_parallelism,
                len(ready),
            )

            for task_id in ready:
                completed.add(task_id)
                del remaining[task_id]

        return max_parallelism

    def _calculate_critical_path(
        self,
        tasks: list[dict],
    ) -> int:

        if not tasks:
            return 0

        task_map = {
            task["id"]: task
            for task in tasks
        }

        memo = {}

        def depth(task_id: str) -> int:

            if task_id in memo:
                return memo[task_id]

            task = task_map[task_id]

            dependencies = task.get(
                "dependencies",
                [],
            )

            if not dependencies:
                memo[task_id] = 1
                return 1

            max_depth = 0

            for dependency in dependencies:

                if dependency not in task_map:
                    raise ValueError(
                        f"Unknown dependency: {dependency}"
                    )

                max_depth = max(
                    max_depth,
                    depth(dependency),
                )

            memo[task_id] = max_depth + 1

            return memo[task_id]

        return max(
            depth(task["id"])
            for task in tasks
        )