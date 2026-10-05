from context_manager import ContextManager


manager = ContextManager()


daily_result = {
    "success": True,
    "task_id": "daily_trend",
    "tool_results": [
        {
            "tool": "run_sql",
            "result": {
                "success": True,
                "result_id": "abc-123",
                "columns": [
                    "day",
                    "daily_paid_amount",
                ],
                "row_count": 30,
            },
        }
    ],
}


manager.save_task_result(
    "daily_trend",
    daily_result,
)


context = manager.build_context(
    ["daily_trend"]
)


print("\n========== CONTEXT ==========\n")
print(context)
