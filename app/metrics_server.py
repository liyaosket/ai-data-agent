from fastapi import FastAPI


app = FastAPI()

from app.metrics_backend import MetricsBackend


backend = MetricsBackend()


@app.get("/metrics")
def get_metrics_api():

    data = backend.latest()

    if data is None:

        return {
            "message": "no metrics available"
        }


    return data
