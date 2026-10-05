from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TraceEvent:
    task_id: str
    event_type: str
    timestamp: datetime = field(default_factory=datetime.now)

    attempt: Optional[int] = None

    tool_name: Optional[str] = None
    duration: Optional[float] = None

    success: Optional[bool] = None
    error: Optional[str] = None

    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost: Optional[float] = None

    metadata: dict = field(default_factory=dict)

class ExecutionTrace:
    def __init__(
        self,
        metrics=None,
    ):
        self.events = []
        self.metrics = metrics

    def add_event(
        self,
        task_id: str,
        event_type: str,
        attempt: int = None,
        tool_name: str = None,
        duration: float = None,
        success: bool = None,
        error: str = None,
        input_tokens: int = None,
        output_tokens: int = None,
        total_tokens: int = None,
        cost: float = None,
        metadata: dict = None,
    ):
        event = TraceEvent(
            task_id=task_id,
            event_type=event_type,
            attempt=attempt,
            tool_name=tool_name,
            duration=duration,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=cost,
            success=success,
            error=error,
            metadata=metadata or {},
        )

        self.events.append(event)
        if self.metrics:
            self.metrics.record_event(
                event
            )
        return event

    def get_events(self):
        return self.events

    def get_task_events(self, task_id: str):
        return [
            event
            for event in self.events
            if event.task_id == task_id
        ]
