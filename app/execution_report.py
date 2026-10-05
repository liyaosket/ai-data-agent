class ExecutionReport:

    def print_report(self, summary: dict):

        print()
        print("=" * 60)
        print("EXECUTION SUMMARY")
        print("=" * 60)

        print(
            f"Total Tasks : {summary['total_tasks']}"
        )

        print(
            f"Success     : {summary['success']}"
        )

        print(
            f"Failed      : {summary['failed']}"
        )

        print(
            f"Timeout     : {summary['timeout']}"
        )

        print(
            f"Skipped     : {summary['skipped']}"
        )

        print(
            f"Cancelled   : {summary['cancelled']}"
        )

        print()
        print("-" * 60)

        for task in summary["tasks"]:

            duration = task["duration"]

            if duration is not None:
                duration_text = (
                    f"{duration:.2f}s"
                )
            else:
                duration_text = "-"

            print(
                f"{task['task_id']:>4} | "
                f"{task['status']:<9} | "
                f"attempts={task['attempt']:<2} | "
                f"duration={duration_text}"
            )

            if task["error"]:
                print(
                    f"       error: "
                    f"{task['error']}"
                )
