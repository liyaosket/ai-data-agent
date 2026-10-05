from app.vector_store import VectorStore
from app.retriever import Retriever
from app.context_assembler import ContextAssembler
from app.mock_llm import MockLLM
from app.rag_pipeline import RAGPipeline


# --------------------------------
# 1. Create VectorStore
# --------------------------------

vector_store = VectorStore()


vector_store.add(
    vector=[0.95, 0.90, 0.10, 0.05, 0.80],
    text="Kafka 用于实时传输订单事件。",
    metadata={
        "source": "kafka.md",
        "category": "kafka",
    },
)


vector_store.add(
    vector=[0.70, 0.65, 0.75, 0.10, 0.20],
    text="Flink 消费 Kafka 中的订单事件，并进行实时计算。",
    metadata={
        "source": "flink.md",
        "category": "flink",
    },
)


vector_store.add(
    vector=[0.92, 0.88, 0.08, 0.04, 0.78],
    text="订单数据每天凌晨 2 点同步到数据仓库。",
    metadata={
        "source": "data_platform.md",
        "category": "order",
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


# --------------------------------
# 2. Create components
# --------------------------------

retriever = Retriever(vector_store)

context_assembler = ContextAssembler(
    max_chars=3000
)

llm = MockLLM()


# --------------------------------
# 3. Create RAG Pipeline
# --------------------------------

rag = RAGPipeline(
    retriever=retriever,
    context_assembler=context_assembler,
    llm=llm,
)


# --------------------------------
# 4. Query
# --------------------------------

question = "Kafka 的订单数据是怎么进入数据仓库的？"

query_vector = [
    0.90,
    0.85,
    0.20,
    0.05,
    0.70,
]


# --------------------------------
# 5. Run
# --------------------------------

result = rag.run(
    question=question,
    query_vector=query_vector,
    top_k=3,
    score_threshold=0.5,
)


# --------------------------------
# 6. Print
# --------------------------------

print("=" * 60)
print("QUESTION")
print("=" * 60)

print(result["question"])


print("\n" + "=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

for document in result["retrieved_documents"]:
    print(
        f"score={document['score']:.4f}"
    )

    print(
        document["text"]
    )

    print(
        document["metadata"]
    )

    print()


print("=" * 60)
print("CONTEXT")
print("=" * 60)

print(result["context"])


print("\n" + "=" * 60)
print("ANSWER")
print("=" * 60)

print(result["answer"])
