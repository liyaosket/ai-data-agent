import time

from dotenv import load_dotenv

from app.qwen_embedding import QwenEmbeddingModel


load_dotenv()


model = QwenEmbeddingModel()

texts = [
    "Kafka 用于实时传输订单事件。",
    "Flink 消费 Kafka 中的订单事件，并进行实时计算。",
    "订单数据每天凌晨 2 点同步到数据仓库。",
]

start = time.perf_counter()

vectors = model.embed_batch(texts)

elapsed = time.perf_counter() - start

print("=" * 60)
print("Embedding Test")
print("=" * 60)

print(f"Model: {model.model}")
print(f"Dimensions: {model.dimensions}")
print(f"Documents: {len(texts)}")
print(f"Latency: {elapsed:.3f}s")

for i, vector in enumerate(vectors):
    print()
    print(f"Document {i + 1}")
    print(f"Vector length: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")
