from app.task_record import TaskRecord
from app.retry_policy import RetryPolicy


def main():

    record = TaskRecord(
        task_id="TEST_RETRY"
    )

    policy = RetryPolicy(
        max_retries=2
    )

    while True:

        record.start()

        print(
            f"attempt={record.attempt}"
        )

        try:

            raise RuntimeError(
                "模拟临时错误"
            )

        except Exception as e:

            if policy.should_retry(
                record.attempt,
                e,
            ):

                record.retrying(
                    str(e)
                )

                print(
                    "准备重试..."
                )

                continue

            record.fail(
                str(e)
            )

            break

    print("\n========== RESULT ==========")

    print(
        "status:",
        record.status
    )

    print(
        "attempt:",
        record.attempt
    )

    print(
        "history:",
        record.history
    )

    print()
    print("=" * 70)
    print("EXECUTION TRACE")
    print("=" * 70)

    trace = executor.get_execution_trace()

    for event in trace.get_events():
        print(
            f"{event.timestamp} | "
            f"task={event.task_id} | "
            f"attempt={event.attempt} | "
            f"{event.event_type:<15} | "
            f"tool={event.tool_name} | "
            f"duration={event.duration} | "
            f"success={event.success} | "
            f"error={event.error}"
        )

if __name__ == "__main__":
    main()
