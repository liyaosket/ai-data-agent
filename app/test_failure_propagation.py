from parallel_executor import ParallelExecutor
from execution_report import ExecutionReport

class FailureTaskRunner:

    def run_task(self, task, context):

        task_id = task["id"]

        print(
            f"[FakeRunner] 执行 {task_id}"
        )

        if task_id == "T1":
            raise RuntimeError(
                "模拟 T1 永久失败"
            )

        return {
            "success": True,
            "answer": f"{task_id} success",
        }


def main():

    executor = ParallelExecutor(
        max_workers=2
    )

    executor.task_runner = (
        FailureTaskRunner()
    )

    # 为了这个测试不进行 retry
    executor.retry_policy.max_retries = 0

    plan = {
        "tasks": [

            {
                "id": "T1",
                "description": "模拟失败任务",
                "dependencies": [],
            },

            {
                "id": "T2",
                "description": "正常任务",
                "dependencies": [],
            },

            {
                "id": "T3",
                "description": "依赖 T1",
                "dependencies": ["T1"],
            },

            {
                "id": "T4",
                "description": "依赖 T3",
                "dependencies": ["T3"],
            },

            {
                "id": "T5",
                "description": "依赖 T2",
                "dependencies": ["T2"],
            },
        ]
    }

    try:
        results = executor.run_plan(plan)

        print("\n========== RESULTS ==========")

        for task_id, result in results.items():
            print(
                task_id,
                result,
            )

    except Exception as e:

        print(
            "\n========== EXECUTOR ERROR =========="
        )

        print(type(e).__name__)
        print(e)

    print(
        "\n========== TASK RECORDS =========="
    )

    records = executor.get_task_records()
    
    print(
        "\n========== EXECUTION SUMMARY =========="
    )
    summary = executor.get_execution_summary() 
    report = ExecutionReport()

    report.print_report(summary)

    for task_id, record in records.items():

        print(
            task_id,
            "=>",
            record.status,
        )


if __name__ == "__main__":
    main()
