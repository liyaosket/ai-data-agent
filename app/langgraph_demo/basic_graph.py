from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    question: str
    result: str


def analyze_node(state: AgentState):
    question = state["question"]

    result = f"分析问题：{question}"

    return {
        "result": result
    }


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node(
        "analyze",
        analyze_node,
    )

    graph.add_edge(
        START,
        "analyze",
    )

    graph.add_edge(
        "analyze",
        END,
    )

    return graph.compile()


def main():
    graph = build_graph()

    result = graph.invoke({
        "question": "分析昨天支付订单为什么下降",
        "result": "",
    })

    print(result)


if __name__ == "__main__":
    main()
