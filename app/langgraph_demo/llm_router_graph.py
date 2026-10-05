from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agent.llm_router import LLMRouter


class AgentState(TypedDict, total=False):
    question: str

    route: str
    intent: str
    tools: list[str]
    reason: str

    result: str


router = LLMRouter()


def router_node(state: AgentState):
    question = state["question"]

    print(f"\n[Router Node] question={question}")

    decision = router.route(question)

    print(f"[Router Node] route={decision.route}")
    print(f"[Router Node] intent={decision.intent}")
    print(f"[Router Node] tools={decision.tools}")

    return {
        "route": decision.route,
        "intent": decision.intent,
        "tools": decision.tools,
        "reason": decision.reason,
    }


def sql_node(state: AgentState):
    print("[SQL Node]")

    return {
        "result": f"SQL branch selected for: {state['question']}"
    }


def rag_node(state: AgentState):
    print("[RAG Node]")

    return {
        "result": f"RAG branch selected for: {state['question']}"
    }


def analysis_node(state: AgentState):
    print("[Analysis Node]")

    return {
        "result": f"Analysis branch selected for: {state['question']}"
    }


def system_node(state: AgentState):
    print("[System Node]")

    return {
        "result": f"System branch selected for: {state['question']}"
    }


def route_condition(state: AgentState):
    route = state["route"]

    if route == "data_query":
        return "sql"

    if route == "knowledge":
        return "rag"

    if route == "analysis":
        return "analysis"

    if route == "system":
        return "system"

    raise ValueError(f"Unknown route: {route}")


def summary_node(state: AgentState):
    print("[Summary Node]")

    return {
        "result": state["result"]
    }


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("sql", sql_node)
    graph.add_node("rag", rag_node)
    graph.add_node("analysis", analysis_node)
    graph.add_node("system", system_node)
    graph.add_node("summary", summary_node)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        route_condition,
        {
            "sql": "sql",
            "rag": "rag",
            "analysis": "analysis",
            "system": "system",
        },
    )

    graph.add_edge("sql", "summary")
    graph.add_edge("rag", "summary")
    graph.add_edge("analysis", "summary")
    graph.add_edge("system", "summary")

    graph.add_edge("summary", END)

    return graph.compile()


def main():
    graph = build_graph()

    questions = [
        "查询昨天支付订单总量",
        "公司的退款政策是什么？",
        "分析一下昨天支付订单为什么下降？",
        "系统现在有哪些任务正在运行？",
    ]

    for question in questions:
        print("\n" + "=" * 60)

        result = graph.invoke(
            {
                "question": question
            }
        )

        print("\n[Final State]")
        print(result)


if __name__ == "__main__":
    main()
