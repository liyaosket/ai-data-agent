from app.rag.vector_retriever import VectorRetriever


def main():
    retriever = VectorRetriever()

    query = "这个人的大数据开发经验有几年？"

    results = retriever.search(
        query=query,
        top_k=5,
        document_id=1002,
    )

    print()
    print("=" * 80)
    print("QUERY")
    print(query)
    print("=" * 80)

    for i, result in enumerate(results, start=1):
        print()
        print("-" * 80)
        print(f"Rank: {i}")
        print(f"Chunk ID: {result['id']}")
        print(f"Chunk Index: {result['chunk_index']}")
        print(f"Score: {result['score']:.4f}")
        print(f"Metadata: {result['metadata']}")
        print()
        print(result["content"])


if __name__ == "__main__":
    main()
