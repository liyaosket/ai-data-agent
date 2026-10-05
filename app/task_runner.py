import json
import time

from app.execution_trace import ExecutionTrace
from app.task_agent import MODEL
from app.tools.router import execute_tool
from app.llm_cost import calculate_cost
from app.cached_llm import cached_call_llm
from app.metrics import MetricsCollector

class TaskRunner:

    def __init__(
        self,
        trace=None,
        metrics=None,
    ):

        if trace:

            self.trace = trace

        else:

            self.trace = ExecutionTrace(
                metrics=metrics
            )


    def run_task(self, task: dict, context: dict, attempt: int = 1,):

        task_id = task["id"]

        input_items = [{
            "role": "user",
            "content": json.dumps(
                {
                    "task": task,
                    "context": context,
                },
                ensure_ascii=False,
            ),
        }]

        tool_results = []

        self.trace.add_event(
            task_id=task_id,
            event_type="TASK_START",
            attempt=attempt,
        )

        while True:

            # -------------------------
            # LLM Call
            # -------------------------

            llm_start = time.perf_counter()

            try:
                response, cache_hit, duration = cached_call_llm(
                    input_items
                )

            except Exception as e:

                duration = time.perf_counter() - llm_start

                self.trace.add_event(
                    task_id=task_id,
                    event_type="LLM_RESPONSE",
                    attempt=attempt,
                    duration=duration,
                    success=False,
                    error=str(e),
                )

                self.trace.add_event(
                    task_id=task_id,
                    event_type="TASK_ERROR",
                    attempt=attempt,
                    error=str(e),
                )

                raise

            duration = time.perf_counter() - llm_start

            if not cache_hit:
            
                usage = response.usage
            
                cost = calculate_cost(
                    model=MODEL,
                    input_tokens=usage.input_tokens,
                    output_tokens=usage.output_tokens,
                )
            
                self.trace.add_event(
                    task_id=task_id,
                    event_type="LLM_RESPONSE",
                    attempt=attempt,
                    input_tokens=usage.input_tokens,
                    output_tokens=usage.output_tokens,
                    total_tokens=usage.total_tokens,
                    cost=cost,
                    duration=duration,
                    success=True,
                )
            else:
            
                self.trace.add_event(
                    task_id=task_id,
                    event_type="LLM_CACHE_HIT",
                    attempt=attempt,
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                    cost=0.0,
                    duration=0.0,
                    success=True,
                )

            # -------------------------
            # Find Tool Calls
            # -------------------------

            tool_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            # -------------------------
            # No Tool Call
            # -------------------------

            if not tool_calls:

                self.trace.add_event(
                    task_id=task_id,
                    event_type="TASK_END",
                    attempt=attempt,
                    success=True,
                )

                return {
                    "success": True,
                    "task_id": task_id,
                    "answer": response.output_text,
                    "tool_results": tool_results,
                }

            # -------------------------
            # Add LLM output
            # -------------------------

            input_items += response.output

            # -------------------------
            # Execute Tools
            # -------------------------

            for tool_call in tool_calls:

                arguments = json.loads(tool_call.arguments)

                print(
                    f"\n[TaskRunner] Tool: {tool_call.name}"
                )

                print(
                    f"[TaskRunner] Arguments: {arguments}"
                )

                # -------------------------
                # Tool Call Trace
                # -------------------------

                self.trace.add_event(
                    task_id=task_id,
                    event_type="TOOL_CALL",
                    attempt=attempt,
                    tool_name=tool_call.name,
                    metadata={
                        "arguments": arguments,
                    },
                )

                tool_start = time.perf_counter()

                try:
                    result = execute_tool(
                        tool_call.name,
                        arguments,
                    )

                except Exception as e:

                    duration = time.perf_counter() - tool_start

                    self.trace.add_event(
                        task_id=task_id,
                        event_type="TOOL_RESULT",
                        attempt=attempt,
                        tool_name=tool_call.name,
                        duration=duration,
                        success=False,
                        error=str(e),
                    )

                    raise

                duration = time.perf_counter() - tool_start

                # -------------------------
                # Tool Result Trace
                # -------------------------

                self.trace.add_event(
                    task_id=task_id,
                    event_type="TOOL_RESULT",
                    attempt=attempt,
                    tool_name=tool_call.name,
                    duration=duration,
                    success=result.get("success", True),
                    metadata={
                        "result": result,
                    },
                )

                tool_results.append({
                    "tool": tool_call.name,
                    "arguments": arguments,
                    "result": result,
                })

                print(
                    f"[TaskRunner] Tool Result: {result}"
                )

                input_items.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(
                        result,
                        ensure_ascii=False,
                        default=str,
                    ),
                })
