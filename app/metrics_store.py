import json
import os
from datetime import datetime


class MetricsStore:


    def __init__(
        self,
        path="metrics_history.json",
    ):

        self.path = path


    def save(
        self,
        metrics_snapshot,
    ):

        record = {

            "timestamp":
                datetime.utcnow()
                .isoformat(),

            "metrics":
                metrics_snapshot,
        }


        history = []


        if os.path.exists(
            self.path
        ):

            with open(
                self.path,
                "r",
                encoding="utf-8",
            ) as f:

                history = json.load(f)


        history.append(
            record
        )


        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                history,
                f,
                ensure_ascii=False,
                indent=2,
            )


    def load(self):

        if not os.path.exists(
            self.path
        ):

            return []


        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)
