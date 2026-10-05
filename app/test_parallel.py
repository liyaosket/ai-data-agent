from parallel_executor import ParallelExecutor


def main():

    plan = {
        "goal": "测试 DAG 并行执行",

        "tasks": [
            {
                "id": "T1",
                "description": (
                    "查询最近30天每天的订单数量"
                ),
                "dependencies": [],
            },

            {
                "id": "T2",
                "description": (
                    "查询最近30天每天的成交金额"
                ),
                "dependencies": [],
            },

            {
                "id": "T3",
                "description": (
                    "基于 T1 的结果进行数据概览"
                ),
                "dependencies": ["T1"],
            },

            {
                "id": "T4",
                "description": (
                    "基于 T2 的结果进行异常检测"
                ),
                "dependencies": ["T2"],
            },

            {
                "id": "T5",
                "description": (
                    "综合 T3 和 T4 的结果进行总结"
                ),
                "dependencies": ["T3", "T4"],
            },
        ],
    }

    executor = ParallelExecutor(
        max_workers=3
    )

    results = executor.run_plan(plan)

    print("\n========== FINAL ==========\n")

    for task_id, result in results.items():
        print(task_id)
        print(result)


if __name__ == "__main__":
    main()
