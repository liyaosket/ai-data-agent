from parallel_executor import ParallelExecutor


class FakeTaskRunner:

    def __init__(self):
        self.calls = 0

    def run_task(self, task, context):
        self.calls += 1

        print(
            f"[FakeTaskRunner] "
            f"执行次数: {self.calls}"
        )

        if self.calls < 3:
            raise RuntimeError(
                "模拟临时故障"
            )

        return {
            "success": True,
            "answer": "第三次执行成功",
        }


def main():
    executor = ParallelExecutor(
        max_workers=1
    )

    fake_runner = FakeTaskRunner()

    executor.task_runner = fake_runner

    plan = {
        "tasks": [
            {
                "id": "T1",
                "description": "模拟一个会失败两次的任务",
                "dependencies": [],
            }
        ]
    }

    results = executor.run_plan(plan)

    print("\n========== RESULTS ==========")
    print(results)

    print(
        "\n========== TASK RECORDS =========="
    )

    records = executor.get_task_records()

    for task_id, record in records.items():
        print(task_id)
        print("status:", record.status)
        print("attempt:", record.attempt)
        print("history:", record.history)


if __name__ == "__main__":
    main()
