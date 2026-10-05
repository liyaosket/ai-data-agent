from app.metrics import MetricsCollector
from app.metrics_backend import MetricsBackend


backend = MetricsBackend()


metrics = MetricsCollector(
    backend=backend
)


def get_metrics():

    return metrics
