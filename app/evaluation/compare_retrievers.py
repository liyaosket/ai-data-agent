import json

from app.pgvector_retriever import PgVectorRetriever
from app.sparse_retriever import SparseRetriever
from app.hybrid_retriever import HybridRetriever
from app.reranker import Reranker

from app.evaluation.evaluator import RetrievalEvaluator


def evaluate_method(
    name,
    dataset,
    search_function,
    evaluator,
    top_k=5
):
    """
    评估单个 Retrieval 方法
    """

    recall_scores = []
    mrr_scores = []


    print()
    print("=" * 70)
    print(name)
    print("=" * 70)


    for item in dataset:

        query = item["query"]

        relevant_documents = item[
            "relevant_documents"
        ]


        results = search_function(
            query
        )


        recall = evaluator.recall_at_k(
            results,
            relevant_documents,
            k=top_k
        )


        mrr = evaluator.mrr(
            results,
            relevant_documents
        )


        recall_scores.append(
            recall
        )

        mrr_scores.append(
            mrr
        )


        print()
        print(
            "Query:",
            query
        )

        print(
            "Recall@{}:".format(top_k),
            recall
        )

        print(
            "MRR:",
            mrr
        )


    avg_recall = (
        sum(recall_scores)
        /
        len(recall_scores)
    )

    avg_mrr = (
        sum(mrr_scores)
        /
        len(mrr_scores)
    )


    return {
        "method": name,
        "recall": avg_recall,
        "mrr": avg_mrr,
    }



def main():

    # =========================
    # 加载测试数据
    # =========================

    with open(
        "app/evaluation/dataset.json",
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(f)



    evaluator = RetrievalEvaluator()


    # =========================
    # 初始化 Retriever
    # =========================

    dense_retriever = PgVectorRetriever()

    sparse_retriever = SparseRetriever()

    hybrid_retriever = HybridRetriever()

    reranker = Reranker()



    results = []



    # =========================
    # Dense Retrieval
    # =========================

    results.append(
        evaluate_method(
            "Dense Retrieval",
            dataset,
            lambda query:
                dense_retriever.search(
                    query,
                    top_k=5
                ),
            evaluator
        )
    )



    # =========================
    # Sparse Retrieval
    # =========================

    results.append(
        evaluate_method(
            "Sparse Retrieval",
            dataset,
            lambda query:
                sparse_retriever.search(
                    query,
                    top_k=5
                ),
            evaluator
        )
    )



    # =========================
    # Hybrid Retrieval
    # =========================

    results.append(
        evaluate_method(
            "Hybrid Retrieval",
            dataset,
            lambda query:
                hybrid_retriever.search(
                    query,
                    top_k=5,
                    candidate_k=20
                ),
            evaluator
        )
    )



    # =========================
    # Hybrid + Reranker
    # =========================

    def hybrid_rerank_search(query):

        candidates = hybrid_retriever.search(
            query,
            top_k=20,
            candidate_k=50
        )


        reranked = reranker.rerank(
            query,
            candidates,
            top_k=5
        )


        return reranked



    results.append(
        evaluate_method(
            "Hybrid + Reranker",
            dataset,
            hybrid_rerank_search,
            evaluator
        )
    )



    # =========================
    # 最终汇总
    # =========================

    print()
    print()
    print("=" * 70)
    print("Final Comparison")
    print("=" * 70)

    print()

    print(
        "{:<25} {:<15} {:<15}".format(
            "Method",
            "Recall@5",
            "MRR"
        )
    )


    print("-" * 70)


    for result in results:

        print(
            "{:<25} {:<15.4f} {:<15.4f}".format(
                result["method"],
                result["recall"],
                result["mrr"]
            )
        )



if __name__ == "__main__":
    main()
