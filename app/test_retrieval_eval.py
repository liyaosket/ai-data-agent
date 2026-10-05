from app.pgvector_retriever import PgVectorRetriever
from app.rag_eval_dataset import EVAL_QUERIES


def is_relevant(content, expected_keywords):
    content_lower = content.lower()

    return all(
        keyword.lower() in content_lower
        for keyword in expected_keywords
    )


def main():
    retriever = PgVectorRetriever()

    for k in [1, 3, 5]:
        hits = 0

        print()
        print("=" * 70)
        print(f"Recall@{k}")
        print("=" * 70)

        for item in EVAL_QUERIES:
            results = retriever.search(
                item["query"],
                top_k=k,
            )

            found = any(
                is_relevant(
                    result["content"],
                    item["expected_keywords"],
                )
                for result in results
            )

            if found:
                hits += 1

            print(
                f"{'✓' if found else '✗'} "
                f"{item['query']}"
            )

        recall = hits / len(EVAL_QUERIES)

        print()
        print(f"Recall@{k}: {recall:.2%}")


if __name__ == "__main__":
    main()
