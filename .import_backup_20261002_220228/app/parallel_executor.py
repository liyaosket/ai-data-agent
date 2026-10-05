from concurrent.futures import ThreadPoolExecutor, as_completed

from context_manager import ContextManager
from task_runner import TaskRunner
from task_record import TaskRecord
from retry_policy import RetryPolicy
import concurrent.futures
from task_state import TaskStatus
from execution_summary import ExecutionSummary
from execution_trace import ExecutionTrace

class ParallelExecutor:

    def __init__(
        self,
        max_workers: int = 3,
        retry_policy: RetryPolicy | None = None,
        task_timeout: float = 30.0,
    ):
        self.context_manager = ContextManager()
        self.trace = ExecutionTrace()

        self.task_runner = TaskRunner(trace=self.trace)
    
        self.max_workers = max_workers
    
        self.retry_policy = retry_policy or RetryPolicy(
            max_retries=2
        )
    
        self.task_timeout = task_timeout
    
        self.task_records = {}

    def get_task_records(self):
        return self.task_records

    def can_run_task(self, task, completed):
        dependencies = task.get("dependencies", [])
    
        return all(
            dependency in completed
            for dependency in dependencies
        )

    def get_execution_summary(self):
        return ExecutionSummary(
            self.task_records
        ).build()

    def has_failed_dependency(self, task):
        dependencies = task.get(
            "dependencies",
            []
        )

        for dependency in dependencies:

            record = self.task_records.get(
                dependency
            )

            if record and record.status.is_failure:
                return True

        return False

    def get_execution_trace(self):
        return self.trace

    def execute_task(self, task: dict):
        task_id = task["id"]
        dependencies = task.get("dependencies", [])

        context = self.context_manager.build_context(
            dependencies
        )

        record = TaskRecord(task_id=task_id)
        self.task_records[task_id] = record

        while True:
            record.start()

            print(
                f"\n[Executor] 开始任务: {task_id} "
                f"(attempt={record.attempt})"
            )


            try:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=1
                ) as task_executor:

                    future = task_executor.submit(
                        self.task_runner.run_task,
                        task,
                        context,
                    )

                    try:
                        result = future.result(
                            timeout=self.task_timeout
                        )

                        record.success(result)

                        print(
                            f"[Executor] 任务成功: {task_id} "
                            f"(attempt={record.attempt})"
                        )

                        return task_id, result

                    except concurrent.futures.TimeoutError:
                        record.timeout()

                        print(
                            f"[Executor] 任务超时: {task_id} "
                            f"(attempt={record.attempt})"
                        )

                        raise TimeoutError(
                            f"Task {task_id} "
                            f"执行超过 {self.task_timeout} 秒"
                        )

            except Exception as e:
                error_message = str(e)

                print(
                    f"[Executor] 任务失败: {task_id} "
                    f"(attempt={record.attempt})"
                )
                print(
                    f"[Executor] error: {error_message}"
                )

                if self.retry_policy.should_retry(
                    record.attempt,
                    e,
                ):
                    record.retrying(error_message)

                    print(
                        f"[Executor] 准备重试: {task_id}"
                    )

                    continue

                record.fail(error_message)

                print(
                    f"[Executor] 最终失败: {task_id} "
                    f"(attempt={record.attempt})"
                )

                raise

    def run_plan(self, plan: dict):
        tasks = {
            task["id"]: task
            for task in plan["tasks"]
        }
    
        completed = set()
    
        while len(completed) < len(tasks):
    
            progress = False
            ready_tasks = []
    
            for task_id, task in tasks.items():
    
                if task_id in completed:
                    continue
    
                dependencies = task.get(
                    "dependencies",
                    []
                )
    
                # 依赖还没有全部结束
                if not all(
                    dependency in completed
                    for dependency in dependencies
                ):
                    continue
    
                # 所有依赖已经结束
                # 但是其中存在失败
                if self.has_failed_dependency(task):
    
                    record = TaskRecord(
                        task_id=task_id
                    )
    
                    record.skip(
                        "依赖任务失败，跳过当前任务"
                    )
    
                    self.task_records[task_id] = record
    
                    completed.add(task_id)
    
                    print(
                        f"\n[Executor] "
                        f"任务跳过: {task_id}"
                    )
    
                    progress = True
    
                    continue
    
                # 没有失败依赖，可以执行
                ready_tasks.append(task)
    
            # 执行当前这一层所有 ready tasks
            if ready_tasks:
    
                print(
                    "\n========== READY TASKS =========="
                )
    
                for task in ready_tasks:
                    print(
                        f"- {task['id']}: "
                        f"{task['description']}"
                    )
    
                with ThreadPoolExecutor(
                    max_workers=self.max_workers
                ) as executor:
    
                    future_map = {
                        executor.submit(
                            self.execute_task,
                            task,
                        ): task
                        for task in ready_tasks
                    }
    
                    for future in as_completed(
                        future_map
                    ):
    
                        task = future_map[future]
                        task_id = task["id"]
    
                        try:
                            finished_task_id, result = (
                                future.result()
                            )
    
                            self.context_manager.save_task_result(
                                finished_task_id,
                                result,
                            )
    
                            completed.add(
                                finished_task_id
                            )
    
                            print(
                                f"\n[Executor] "
                                f"任务完成: "
                                f"{finished_task_id}"
                            )
    
                            progress = True
    
                        except Exception as e:
    
                            print(
                                f"\n[Executor] "
                                f"任务最终失败: {task_id}"
                            )
    
                            # 注意：
                            # execute_task 已经把 TaskRecord
                            # 设置成 FAILED / TIMEOUT
                            #
                            # 即使这里抛异常，我们也把它视为
                            # 一个已经结束的 Task。
                            completed.add(task_id)
    
                            progress = True
    
            # 本轮既没有执行 Task，
            # 也没有 SKIP Task
            if not progress:
    
                remaining = [
                    task_id
                    for task_id in tasks
                    if task_id not in completed
                ]
    
                raise RuntimeError(
                    "DAG 无法继续执行，"
                    f"可能存在循环依赖: {remaining}"
                )
    
        return self.context_manager.get_all_results()
