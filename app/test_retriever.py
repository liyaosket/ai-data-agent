from app.vector_store import VectorStore
from app.retriever import Retriever


vector_store = VectorStore()

vector_store.add(
    vector=[0.95, 0.90, 0.10, 0.05, 0.80],
    text="订单数据每天凌晨 2 点同步到数据仓库。",
    metadata={
        "source": "data_platform.md",
        "category": "order",
    },
)

vector_store.add(
    vector=[0.92, 0.88, 0.08, 0.04, 0.78],
    text="用户信息每天凌晨 3 点同步到数据仓库。",
    metadata={
        "source": "data_platform.md",
        "category": "user",
    },
)

vector_store.add(
    vector=[0.70, 0.65, 0.75, 0.10, 0.20],
    text="Kafka 用于实时传输订单事件。",
    metadata={
        "source": "kafka.md",
        "category": "kafka",
    },
)

vector_store.add(
    vector=[0.30, 0.25, 0.85, 0.60, 0.10],
    text="Flink 用于实时计算订单指标。",
    metadata={
        "source": "flink.md",
        "category": "flink",
    },
)

vector_store.add(
    vector=[0.05, 0.10, 0.05, 0.95, 0.02],
    text="今天北京天气晴朗。",
    metadata={
        "source": "weather.md",
        "category": "weather",
    },
)


retriever = Retriever(vector_store)


query_vector = [
    0.93,
    0.88,
    0.10,
    0.05,
    0.78,
]


results = retriever.retrieve(
    query_vector,
    top_k=3,
    score_threshold=0.8,
)


for i, result in enumerate(results, start=1):
    print(f"Rank {i}")
    print(f"Score: {result['score']:.4f}")
    print(f"Text: {result['text']}")
    print(f"Metadata: {result['metadata']}")
    print()



print("=== Kafka documents only ===")

results = retriever.retrieve(
    query_vector,
    top_k=3,
    metadata_filter={
        "category": "kafka"
    },
)

for result in results:
    print(
        result["score"],
        result["text"],
        result["metadata"],
    )
