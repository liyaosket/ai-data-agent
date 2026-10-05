from app.pgvector_retriever import PgVectorRetriever


def main():
    retriever = PgVectorRetriever()

    query = "Kafka consumer 如何保存和提交 offset？"

    results = retriever.search(
        query,
        top_k=5,
    )

    print("=" * 70)
    print("Query:")
    print(query)
    print("=" * 70)

    for i, result in enumerate(results, start=1):
        print()
        print(f"Rank: {i}")
        print(f"Score: {result['score']:.4f}")
        print(f"Document ID: {result['document_id']}")
        print(f"Chunk ID: {result['id']}")
        print(f"Content: {result['content']}")


if __name__ == "__main__":
    main()
