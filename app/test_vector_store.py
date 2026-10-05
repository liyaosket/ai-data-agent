from app.vector_store import VectorStore


store = VectorStore()


store.add(
    vector=[0.95, 0.90, 0.10, 0.05, 0.80],
    text="订单数据每天凌晨 2 点同步到数据仓库。",
    metadata={
        "source": "data_warehouse.md",
        "type": "document",
    },
)


store.add(
    vector=[0.90, 0.85, 0.05, 0.05, 0.75],
    text="用户信息每天凌晨 3 点同步到数据仓库。",
    metadata={
        "source": "data_warehouse.md",
        "type": "document",
    },
)


store.add(
    vector=[0.80, 0.20, 0.90, 0.10, 0.70],
    text="Kafka 用于实时传输订单事件。",
    metadata={
        "source": "kafka.md",
        "type": "document",
    },
)


store.add(
    vector=[0.20, 0.10, 0.80, 0.90, 0.10],
    text="Flink 用于实时计算订单指标。",
    metadata={
        "source": "flink.md",
        "type": "document",
    },
)


store.add(
    vector=[0.05, 0.05, 0.05, 0.10, 0.05],
    text="北京今天的天气很好。",
    metadata={
        "source": "weather.md",
        "type": "document",
    },
)


query_vector = [
    0.93,
    0.88,
    0.10,
    0.05,
    0.78,
]


results = store.search(
    query_vector,
    top_k=3,
)


print("=" * 70)
print("VECTOR SEARCH")
print("=" * 70)


for index, result in enumerate(results, 1):

    print()
    print(f"Rank: {index}")
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print(f"Metadata: {result['metadata']}")
