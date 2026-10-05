from enum import Enum


class TaskStatus(str, Enum):

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    RETRYING = "RETRYING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    TIMEOUT = "TIMEOUT"

    SKIPPED = "SKIPPED"

    CANCELLED = "CANCELLED"

    @property
    def is_terminal(self):
        return self in {
            TaskStatus.SUCCESS,
            TaskStatus.FAILED,
            TaskStatus.TIMEOUT,
            TaskStatus.SKIPPED,
            TaskStatus.CANCELLED,
        }

    @property
    def is_failure(self):
        return self in {
            TaskStatus.FAILED,
            TaskStatus.TIMEOUT,
            TaskStatus.CANCELLED,
            TaskStatus.SKIPPED,
        }
