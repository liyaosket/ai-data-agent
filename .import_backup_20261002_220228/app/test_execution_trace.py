from execution_trace import ExecutionTrace


trace = ExecutionTrace()

trace.add_event(
    task_id="T1",
    event_type="TASK_START",
    attempt=1,
)

trace.add_event(
    task_id="T1",
    event_type="LLM_CALL",
    attempt=1,
)

trace.add_event(
    task_id="T1",
    event_type="TOOL_CALL",
    attempt=1,
    tool_name="run_sql",
)

trace.add_event(
    task_id="T1",
    event_type="TOOL_RESULT",
    attempt=1,
    tool_name="run_sql",
    duration=0.35,
    success=True,
)

trace.add_event(
    task_id="T1",
    event_type="LLM_RESPONSE",
    attempt=1,
)

trace.add_event(
    task_id="T1",
    event_type="TASK_END",
    attempt=1,
)

for event in trace.get_task_events("T1"):
    print(
        event.event_type,
        event.tool_name,
        event.duration,
        event.success,
    )
