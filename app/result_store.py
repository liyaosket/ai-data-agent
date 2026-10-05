import threading
import uuid


class ResultStore:

    def __init__(self):
        self._results = {}
        self._lock = threading.Lock()

    def save(self, columns, rows):
        result_id = str(uuid.uuid4())

        with self._lock:
            self._results[result_id] = {
                "columns": columns,
                "rows": rows,
            }

        return result_id

    def get(self, result_id):
        with self._lock:
            if result_id not in self._results:
                raise KeyError(
                    f"Result 不存在: {result_id}"
                )

            return self._results[result_id]

    def delete(self, result_id):
        with self._lock:
            self._results.pop(
                result_id,
                None,
            )


result_store = ResultStore()
