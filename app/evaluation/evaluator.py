class RetrievalEvaluator:

    def recall_at_k(
        self,
        results,
        relevant_docs,
        k
    ):

        retrieved = [
            r["document_id"]
            for r in results[:k]
        ]

        hits = 0

        for doc in relevant_docs:
            if doc in retrieved:
                hits += 1

        return hits / len(relevant_docs)


    def mrr(
        self,
        results,
        relevant_docs
    ):

        for rank, item in enumerate(
            results,
            start=1
        ):
            if item["document_id"] in relevant_docs:
                return 1 / rank

        return 0
