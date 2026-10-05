import math

from app.qwen_embedding import QwenEmbeddingModel


def cosine_similarity(a, b):
    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    norm_a = math.sqrt(
        sum(x * x for x in a)
    )

    norm_b = math.sqrt(
        sum(x * x for x in b)
    )

    return dot / (norm_a * norm_b)


model = QwenEmbeddingModel()


texts = [
    "订单数据每天凌晨 2 点同步到数据仓库。",
    "每天凌晨两点，订单数据会同步到数仓。",
    "北京今天的天气很好。",
    "Kafka 用于实时传输订单事件。",
]


vectors = model.embed_batch(texts)


query = "订单什么时候同步到数据仓库？"

query_vector = model.embed(query)


print("=" * 60)
print("Semantic Similarity")
print("=" * 60)

print()
print("Query:")
print(query)


results = []

for text, vector in zip(texts, vectors):

    score = cosine_similarity(
        query_vector,
        vector,
    )

    results.append(
        {
            "text": text,
            "score": score,
        }
    )


results.sort(
    key=lambda x: x["score"],
    reverse=True,
)


print()

for rank, result in enumerate(
    results,
    start=1,
):
    print(
        f"{rank}. "
        f"{result['score']:.4f} "
        f"{result['text']}"
    )
