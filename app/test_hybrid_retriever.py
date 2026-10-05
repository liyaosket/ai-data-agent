from app.hybrid_retriever import HybridRetriever


def main():
    retriever = HybridRetriever()

    query = "Kafka offset commit"

    results = retriever.search(
        query,
        top_k=5,
        candidate_k=10,
        rrf_k=60,
    )

    print("=" * 70)
    print("Hybrid Retrieval + RRF")
    print("=" * 70)
    print(f"Query: {query}")

    for rank, result in enumerate(results, start=1):
        print()
        print(f"Rank: {rank}")
        print(f"RRF Score: {result['rrf_score']:.6f}")
        print(f"Dense/Sparse ID: {result['id']}")
        print(f"Document ID: {result['document_id']}")
        print(f"Content: {result['content']}")
        print(f"Dense Rank: {result['dense_rank']}")
        print(f"Sparse Rank: {result['sparse_rank']}")


if __name__ == "__main__":
    main()
