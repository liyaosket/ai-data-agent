import json

from app.hybrid_retriever import HybridRetriever
from app.evaluation.evaluator import RetrievalEvaluator



def main():

    retriever = HybridRetriever()

    evaluator = RetrievalEvaluator()


    with open(
        "app/evaluation/dataset.json",
        "r",
        encoding="utf-8"
    ) as f:

        dataset = json.load(f)


    recall_scores = []
    mrr_scores = []


    for item in dataset:

        query = item["query"]

        relevant_docs = item[
            "relevant_documents"
        ]


        print()
        print("=" * 60)
        print(query)


        results = retriever.search(
            query=query,
            top_k=5,
            candidate_k=20
        )


        recall = evaluator.recall_at_k(
            results,
            relevant_docs,
            k=5
        )


        mrr = evaluator.mrr(
            results,
            relevant_docs
        )


        recall_scores.append(recall)
        mrr_scores.append(mrr)


        print(
            "Recall@5:",
            recall
        )

        print(
            "MRR:",
            mrr
        )


    print()
    print("=" * 60)

    print(
        "Average Recall@5:",
        sum(recall_scores)
        /
        len(recall_scores)
    )


    print(
        "Average MRR:",
        sum(mrr_scores)
        /
        len(mrr_scores)
    )



if __name__ == "__main__":
    main()
