from metrics_store import MetricsStore


store = MetricsStore(
    "test_metrics.json"
)


snapshot = {

    "tasks": {

        "total": 10,

        "success": 9,

        "failed": 1,
    },


    "llm": {

        "calls": 20,

        "cost": 0.5,
    }
}


store.save(
    snapshot
)


data = store.load()


print(data)
