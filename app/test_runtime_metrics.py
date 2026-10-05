from app.task_runner import TaskRunner
from app.metrics_registry import get_metrics


metrics = get_metrics()


runner = TaskRunner(
    metrics=metrics
)


task = {

    "id": "METRIC_TEST",

    "description":
        "请回答：什么是ETL？",

    "dependencies": [],
}


result = runner.run_task(
    task,
    context={},
)


print()
print("================")
print("RESULT")
print("================")

print(
    result["answer"]
)


print()
print("================")
print("METRICS")
print("================")


print(
    metrics.report()
)


print()
print("saving metrics snapshot...")

metrics.snapshot()

print("metrics snapshot saved")
