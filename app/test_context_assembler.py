from app.context_assembler import ContextAssembler


results = [
    {
        "score": 0.9912,
        "text": "Kafka 用于实时传输订单事件。",
        "metadata": {
            "source": "kafka.md",
            "category": "kafka",
        },
    },
    {
        "score": 0.9531,
        "text": "Flink 消费 Kafka 中的订单事件，并进行实时计算。",
        "metadata": {
            "source": "flink.md",
            "category": "flink",
        },
    },
    {
        "score": 0.9211,
        "text": "订单数据每天凌晨 2 点同步到数据仓库。",
        "metadata": {
            "source": "data_platform.md",
            "category": "order",
        },
    },
]


assembler = ContextAssembler()

context = assembler.assemble(results)

print(context)
