from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from task_state import TaskStatus


@dataclass
class TaskRecord:
    task_id: str

    status: TaskStatus = TaskStatus.PENDING

    attempt: int = 0

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    error: Optional[str] = None
    result: Optional[dict] = None

    timeout_seconds: Optional[float] = None

    history: list = field(default_factory=list)

    def start(self):
        self.status = TaskStatus.RUNNING
        self.attempt += 1
        self.start_time = datetime.now()
        self.end_time = None
        self.error = None

    def success(self, result: dict):
        self.status = TaskStatus.SUCCESS
        self.end_time = datetime.now()
        self.result = result

    def fail(self, error: str):
        self.status = TaskStatus.FAILED
        self.end_time = datetime.now()
        self.error = error

    def retrying(self, error: str):
        self.status = TaskStatus.RETRYING
        self.error = error

        self.history.append({
            "attempt": self.attempt,
            "error": error,
        })

    def timeout(self):
        self.status = TaskStatus.TIMEOUT
        self.end_time = datetime.now()

        self.history.append({
            "attempt": self.attempt,
            "error": "Task timeout",
        })

    def duration(self):
        if not self.start_time:
            return None

        end = self.end_time or datetime.now()

        return (
            end - self.start_time
        ).total_seconds()

    def skip(self, reason: str):
        self.status = TaskStatus.SKIPPED
        self.end_time = datetime.now()
        self.error = reason
    
        self.history.append({
            "status": "SKIPPED",
            "reason": reason,
        })
