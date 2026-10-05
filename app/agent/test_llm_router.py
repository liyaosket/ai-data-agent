from app.agent.llm_router import LLMRouter


def main():

    router = LLMRouter()

    queries = [
        "Kafka offset 为什么会重复消费？",
        "昨天支付订单有多少？",
        "分析一下昨天订单为什么下降？",
        "Kafka consumer lag 现在怎么样？",
        "Flink checkpoint 原理是什么？",
        "Iceberg 表为什么适合数据湖？",
    ]

    for query in queries:

        print("=" * 80)
        print("QUERY:", query)

        decision = router.route(query)

        print("ROUTE:", decision.route)
        print("INTENT:", decision.intent)
        print("TOOLS:", decision.tools)
        print("REASON:", decision.reason)


if __name__ == "__main__":
    main()
