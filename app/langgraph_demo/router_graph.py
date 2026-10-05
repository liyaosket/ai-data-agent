from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    question: str
    route: Literal["sql", "rag"]
    result: str


def router_node(state: AgentState):
    question = state["question"]

    if "订单" in question or "销售" in question:
        route = "sql"
    else:
        route = "rag"

    print(f"[Router] route={route}")

    return {
        "route": route
    }


def sql_node(state: AgentState):
    question = state["question"]

    print(f"[SQL] processing: {question}")

    return {
        "result": f"SQL result for: {question}"
    }


def rag_node(state: AgentState):
    question = state["question"]

    print(f"[RAG] processing: {question}")

    return {
        "result": f"RAG result for: {question}"
    }


def summary_node(state: AgentState):
    result = state["result"]

    print("[Summary] generating final answer")

    return {
        "result": f"Final answer: {result}"
    }


def route_condition(state: AgentState):
    return state["route"]


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("sql", sql_node)
    graph.add_node("rag", rag_node)
    graph.add_node("summary", summary_node)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        route_condition,
        {
            "sql": "sql",
            "rag": "rag",
        },
    )

    graph.add_edge("sql", "summary")
    graph.add_edge("rag", "summary")

    graph.add_edge("summary", END)

    return graph.compile()


def main():
    graph = build_graph()

    questions = [
        "查询昨天支付订单总量",
        "公司的退款政策是什么？",
    ]

    for question in questions:
        print("\n==============================")
        print("Question:", question)
        print("==============================")

        result = graph.invoke({
            "question": question,
            "route": "",
            "result": "",
        })

        print("\nFinal State:")
        print(result)


if __name__ == "__main__":
    main()
