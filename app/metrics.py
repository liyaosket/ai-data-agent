from collections import defaultdict


class MetricsCollector:

    def __init__(self, backend=None,):

        # Counter
        self.task_total = 0
        self.task_success = 0
        self.task_failed = 0

        self.llm_calls = 0
        self.cache_hits = 0

        # Token
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0

        # Cost
        self.total_cost = 0.0

        # Duration
        self.llm_duration = []
        self.task_duration = []

        # Tool
        self.tool_calls = defaultdict(int)
        self.backend = backend

    def record_event(
        self,
        event,
    ):

        event_type = event.event_type


        if event_type == "TASK_START":

            self.task_total += 1


        elif event_type == "TASK_END":

            if event.success:
                self.task_success += 1


        elif event_type == "TASK_ERROR":

            self.task_failed += 1


        elif event_type == "LLM_RESPONSE":

            self.llm_calls += 1

            self.input_tokens += (
                event.input_tokens or 0
            )

            self.output_tokens += (
                event.output_tokens or 0
            )

            self.total_tokens += (
                event.total_tokens or 0
            )

            self.total_cost += (
                event.cost or 0
            )

            self.llm_duration.append(
                event.duration
            )


        elif event_type == "LLM_CACHE_HIT":

            self.cache_hits += 1


        elif event_type == "TOOL_CALL":

            self.tool_calls[
                event.tool_name
            ] += 1

    def snapshot(self):
    
        data = self.report()
    
        if self.backend:
    
            self.backend.save(
                data
            )
    
        return data


    def report(self):

        cache_total = (
            self.llm_calls
            +
            self.cache_hits
        )

        cache_hit_rate = 0

        if cache_total:
            cache_hit_rate = (
                self.cache_hits
                /
                cache_total
            )


        avg_llm_latency = 0

        if self.llm_duration:

            avg_llm_latency = (
                sum(self.llm_duration)
                /
                len(self.llm_duration)
            )


        return {

            "tasks": {
                "total": self.task_total,
                "success": self.task_success,
                "failed": self.task_failed,
            },


            "llm": {

                "calls": self.llm_calls,

                "cache_hits": self.cache_hits,

                "cache_hit_rate":
                    round(
                        cache_hit_rate,
                        3,
                    ),

                "input_tokens":
                    self.input_tokens,

                "output_tokens":
                    self.output_tokens,

                "total_tokens":
                    self.total_tokens,

                "cost":
                    round(
                        self.total_cost,
                        6,
                    ),

                "avg_latency":
                    round(
                        avg_llm_latency,
                        3,
                    ),
            },


            "tools":
                dict(
                    self.tool_calls
                ),
        }
