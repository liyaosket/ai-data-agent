from app.sparse_retriever import SparseRetriever


def main():
    retriever = SparseRetriever()

    query = "Kafka offset commit"

    results = retriever.search(
        query,
        top_k=5,
    )

    print("=" * 70)
    print("Sparse Retrieval")
    print("=" * 70)
    print(f"Query: {query}")

    for rank, result in enumerate(results, start=1):
        print()
        print(f"Rank: {rank}")
        print(f"Score: {result['score']:.6f}")
        print(f"Document ID: {result['document_id']}")
        print(f"Chunk ID: {result['id']}")
        print(f"Content: {result['content']}")


if __name__ == "__main__":
    main()
