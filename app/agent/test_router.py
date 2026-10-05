from app.agent.router import AgentRouter


def main():

    router = AgentRouter()

    queries = [
        "Kafka offset 为什么会重复消费？",
        "昨天支付订单有多少？",
        "分析一下昨天订单为什么下降？",
        "Kafka consumer lag 现在怎么样？",
        "Flink checkpoint 原理是什么？",
        "Iceberg 表为什么适合数据湖？",
    ]

    for query in queries:

        decision = router.route(query)

        print("=" * 70)

        print("Query:")
        print(query)

        print()

        print("Route:")
        print(decision.route)

        print()

        print("Reason:")
        print(decision.reason)

        print()


if __name__ == "__main__":
    main()
