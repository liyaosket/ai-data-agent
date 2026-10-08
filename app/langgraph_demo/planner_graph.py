from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.agent.llm_router import LLMRouter
from app.agent.router import RouteDecision
from app.langgraph_demo.dag_scheduler import get_ready_tasks
from app.metrics_registry import get_metrics
from app.planner import create_plan
from app.result_store import ResultStore
from app.task_runner import TaskRunner

from .dag_scheduler import get_ready_tasks
from .parallel_executor import execute_tasks_parallel


class AgentState(TypedDict, total=False):
    # 用户输入
    question: str

    # Router
    route: str
    intent: str
    tools: list[str]
    reason: str

    # Runtime
    task_results: dict[str, Any]
    
    completed_tasks: list[str]

    # Planner
    plan: Any

    # 最终结果
    result: str


router = LLMRouter()
metrics = get_metrics()
result_store = ResultStore()
task_runner = TaskRunner(metrics=metrics)


def router_node(state: AgentState):
    question = state["question"]

    print("\n========== Router ==========")
    print(f"Question: {question}")

    decision = router.route(question)

    print(f"Route: {decision.route}")
    print(f"Intent: {decision.intent}")
    print(f"Tools: {decision.tools}")

    return {
        "route": decision.route,
        "intent": decision.intent,
        "tools": decision.tools,
        "reason": decision.reason,
    }


def planner_node(state: AgentState):
    print("\n========== Planner ==========")

    question = state["question"]

    route_decision = RouteDecision(
        route=state["route"],
        intent=state["intent"],
        tools=state["tools"],
        reason=state["reason"],
    )

    plan = create_plan(
        question,
        route_decision=route_decision,
    )

    print(f"Plan generated: {plan}")

    return {
        "plan": plan,
    }



def execution_condition(state: AgentState):
    plan = state["plan"]

    tasks = plan["tasks"]

    completed_tasks = set(
        state.get("completed_tasks", [])
    )

    if len(completed_tasks) == len(tasks):
        return "done"

    return "continue"


def execute_node(state):
    tasks = state["plan"]["tasks"]

    completed_tasks = set(state.get("completed_tasks", []))

    ready_tasks = get_ready_tasks(
        tasks,
        completed_tasks,
    )

    if not ready_tasks:
        return {
            "task_results": state.get("task_results", {}),
            "completed_tasks": list(completed_tasks),
        }

    def execute_task(task):
        context = {
            "question": state["question"],
            "plan": state["plan"],
            "task_results": state.get("task_results", {}),
        }

        return task_runner.run_task(
            task=task,
            context=context,
            attempt=1,
        )

    results = execute_tasks_parallel(
        ready_tasks,
        execute_task,
        max_workers=4,
    )

    task_results = dict(state.get("task_results", {}))
    task_results.update(results)

    completed_tasks.update(results.keys())

    return {
        "task_results": task_results,
        "completed_tasks": list(completed_tasks),
    }
    

def execution_node(state: AgentState):
    print("\n========== Execution ==========")

    plan = state["plan"]
    tasks = plan["tasks"]

    completed_tasks = set(
        state.get("completed_tasks", [])
    )

    task_results = dict(
        state.get("task_results", {})
    )

    ready_tasks = get_ready_tasks(
        tasks,
        completed_tasks,
    )

    if not ready_tasks:
        if len(completed_tasks) == len(tasks):
            print("All tasks completed")

            return {
                "result": "All tasks completed"
            }

        raise RuntimeError(
            "No ready task found. "
            "The DAG may contain invalid dependencies."
        )

    # 本阶段先只执行一个 Ready Task
    task = ready_tasks[0]

    task_id = task["id"]

    print(f"Ready task: {task_id}")
    print(f"Description: {task['description']}")

    context = {
        "question": state["question"],
        "route": state["route"],
        "intent": state["intent"],
        "tools": state["tools"],
        "plan": plan,
        "results": task_results,
    }

    task_result = task_runner.run_task(
        task=task,
        context=context,
        attempt=1,
    )

    task_results[task_id] = task_result

    completed_tasks.add(task_id)

    print(f"Task {task_id} completed")

    return {
        "task_results": task_results,
        "completed_tasks": list(completed_tasks),
        "result": f"Task {task_id} completed",
    }


def summary_node(state: AgentState):
    print("\n========== Summary ==========")

    return {"result": state["result"]}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("planner", planner_node)
    graph.add_node("execution", execution_node)
    graph.add_node("summary", summary_node)

    graph.add_edge(START, "router")

    graph.add_edge("router", "planner")

    graph.add_edge("planner", "execution")

    graph.add_conditional_edges(
        "execution",
        execution_condition,
        {
            "continue": "execution",
            "done": "summary",
        },
    )

    graph.add_edge("summary", END)

    graph.add_edge("summary", END)
    

    return graph.compile()


def main():
    graph = build_graph()

    question = "查询昨天支付订单总量"

    result = graph.invoke({"question": question})

    print("\n========== Final State ==========")
    print(result)


if __name__ == "__main__":
    main()
