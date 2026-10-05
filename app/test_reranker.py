from app.hybrid_retriever import HybridRetriever
from app.reranker import Reranker


def print_results(title, results, score_field):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    for rank, result in enumerate(results, start=1):
        print()
        print(f"Rank: {rank}")
        print(
            f"Score: {result[score_field]:.6f}"
        )

        print(
            f"Chunk ID: {result['id']}"
        )

        print(
            f"Document ID: {result['document_id']}"
        )

        print(
            f"Dense Rank: {result.get('dense_rank')}"
        )

        print(
            f"Sparse Rank: {result.get('sparse_rank')}"
        )

        print(
            f"Retrieval Source: "
            f"{result.get('retrieval_source')}"
        )

        print(
            f"Content:\n{result['content']}"
        )

def compare_results(
    before,
    after
):

    print("\n")
    print("=" * 70)
    print("Ranking Change")
    print("=" * 70)


    print("\nBefore:")
    for rank, item in enumerate(
        before,
        start=1
    ):
        print(
            rank,
            item["document_id"]
        )


    print("\nAfter:")
    for rank, item in enumerate(
        after,
        start=1
    ):
        print(
            rank,
            item["document_id"]
        )


def main():
    query = "Kafka consumer 如何保存和提交 offset？"

    # 1. Hybrid Retrieval
    hybrid_retriever = HybridRetriever()

    candidates = hybrid_retriever.search(
        query=query,
        top_k=10,
        candidate_k=10,
    )

    # 2. 打印 Reranker 之前的结果
    print_results(
        "Before Rerank - Hybrid Retrieval",
        candidates,
        "rrf_score",
    )

    # 3. Reranker
    reranker = Reranker()

    reranked_results = reranker.rerank(
        query=query,
        documents=candidates,
        top_k=5,
    )

    # 4. 打印 Reranker 之后的结果
    print_results(
        "After Rerank",
        reranked_results,
        "rerank_score",
    )

    compare_results(
        candidates,
        reranked_results
    )


if __name__ == "__main__":
    main()
