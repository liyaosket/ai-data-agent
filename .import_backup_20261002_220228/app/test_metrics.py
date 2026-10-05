from metrics import MetricsCollector


class Event:

    def __init__(
        self,
        event_type,
        **kwargs
    ):

        self.event_type = event_type

        for k, v in kwargs.items():
            setattr(
                self,
                k,
                v,
            )


metrics = MetricsCollector()


events = [

    Event(
        "TASK_START"
    ),


    Event(
        "LLM_RESPONSE",
        input_tokens=1000,
        output_tokens=200,
        total_tokens=1200,
        cost=0.01,
        duration=2.5,
    ),


    Event(
        "TOOL_CALL",
        tool_name="run_sql",
    ),


    Event(
        "LLM_CACHE_HIT"
    ),


    Event(
        "TASK_END",
        success=True,
    ),
]


for e in events:

    metrics.record_event(e)


print(
    metrics.report()
)
