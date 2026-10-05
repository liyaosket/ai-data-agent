class CostAggregator:

    def __init__(self, trace):
        self.trace = trace

    def build(self):
        task_costs = {}

        total_cost = 0.0
        cache_hits = 0
        llm_calls = 0

        for event in self.trace.get_events():

            if event.event_type == "LLM_RESPONSE":
                llm_calls += 1

            if event.event_type == "LLM_CACHE_HIT":
                cache_hits += 1

            if event.cost is None:
                continue

            task_costs.setdefault(
                event.task_id,
                0.0,
            )

            task_costs[event.task_id] += event.cost
            total_cost += event.cost

        total_llm_events = (
            llm_calls + cache_hits
        )

        cache_hit_rate = (
            cache_hits / total_llm_events
            if total_llm_events > 0
            else 0.0
        )

        return {
            "total_cost": total_cost,
            "task_costs": task_costs,
            "llm_calls": llm_calls,
            "cache_hits": cache_hits,
            "cache_hit_rate": cache_hit_rate,
        }
