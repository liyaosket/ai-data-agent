import time

from parallel_executor import ParallelExecutor


class SlowTaskRunner:

    def run_task(self, task, context):
        print("[SlowTaskRunner] 开始执行")

        time.sleep(5)

        return {
            "success": True,
            "answer": "任务完成",
        }


def main():
    executor = ParallelExecutor(
        max_workers=1,
        task_timeout=2,
    )

    executor.task_runner = SlowTaskRunner()

    plan = {
        "tasks": [
            {
                "id": "T1",
                "description": "模拟一个慢任务",
                "dependencies": [],
            }
        ]
    }

    try:
        executor.run_plan(plan)

    except Exception as e:
        print(
            "\n========== FINAL ERROR =========="
        )
        print(type(e).__name__)
        print(e)

    print(
        "\n========== TASK RECORDS =========="
    )

    records = executor.get_task_records()

    for task_id, record in records.items():
        print("task_id:", task_id)
        print("status:", record.status)
        print("attempt:", record.attempt)
        print("duration:", record.duration())
        print("history:", record.history)


if __name__ == "__main__":
    main()
