from task_state import TaskStatus


class ExecutionSummary:

    def __init__(self, task_records: dict):
        self.task_records = task_records

    def build(self):
        summary = {
            "total_tasks": len(self.task_records),
            "success": 0,
            "failed": 0,
            "timeout": 0,
            "skipped": 0,
            "cancelled": 0,
            "pending": 0,
            "running": 0,
            "retrying": 0,
            "tasks": [],
        }

        for task_id, record in self.task_records.items():

            status = record.status

            if status == TaskStatus.SUCCESS:
                summary["success"] += 1

            elif status == TaskStatus.FAILED:
                summary["failed"] += 1

            elif status == TaskStatus.TIMEOUT:
                summary["timeout"] += 1

            elif status == TaskStatus.SKIPPED:
                summary["skipped"] += 1

            elif status == TaskStatus.CANCELLED:
                summary["cancelled"] += 1

            elif status == TaskStatus.PENDING:
                summary["pending"] += 1

            elif status == TaskStatus.RUNNING:
                summary["running"] += 1

            elif status == TaskStatus.RETRYING:
                summary["retrying"] += 1

            summary["tasks"].append({
                "task_id": task_id,
                "status": status.value,
                "attempt": record.attempt,
                "duration": record.duration(),
                "error": record.error,
            })

        return summary
