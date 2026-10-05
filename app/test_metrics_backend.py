from app.metrics_backend import MetricsBackend


backend = MetricsBackend(
    "test_metrics.db"
)


data = {

    "tasks": {

        "total": 1,

        "success": 1,

        "failed": 0
    },


    "llm": {

        "calls": 1,

        "cost": 0.004
    }

}


backend.save(
    data
)


result = backend.latest()


print(result)
