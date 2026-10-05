from app.langgraph_demo.dag_scheduler import get_ready_tasks


def test_ready_tasks():
    tasks = [
        {
            "id": "T1",
            "description": "获取基础数据",
            "dependencies": [],
        },
        {
            "id": "T2",
            "description": "分析基础数据",
            "dependencies": ["T1"],
        },
        {
            "id": "T3",
            "description": "查询其他数据",
            "dependencies": [],
        },
        {
            "id": "T4",
            "description": "综合分析",
            "dependencies": ["T2", "T3"],
        },
    ]

    ready = get_ready_tasks(tasks, set())

    assert {task["id"] for task in ready} == {"T1", "T3"}

    ready = get_ready_tasks(
        tasks,
        {"T1", "T3"},
    )

    assert {task["id"] for task in ready} == {"T2"}

    ready = get_ready_tasks(
        tasks,
        {"T1", "T2", "T3"},
    )

    assert {task["id"] for task in ready} == {"T4"}


if __name__ == "__main__":
    test_ready_tasks()
    print("DAG scheduler test passed")
