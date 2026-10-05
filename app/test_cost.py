from app.execution_trace import ExecutionTrace
from cost_aggregator import CostAggregator


trace = ExecutionTrace()

trace.add_event(
    task_id="T1",
    event_type="LLM_RESPONSE",
    input_tokens=1000,
    output_tokens=500,
    total_tokens=1500,
    cost=0.0035,
)

trace.add_event(
    task_id="T1",
    event_type="TOOL_RESULT",
)

trace.add_event(
    task_id="T2",
    event_type="LLM_RESPONSE",
    input_tokens=2000,
    output_tokens=1000,
    total_tokens=3000,
    cost=0.007,
)

aggregator = CostAggregator(trace)

result = aggregator.build()

print(result)
