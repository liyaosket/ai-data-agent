from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name=
        "BAAI/bge-reranker-base"
    ):

        self.model = CrossEncoder(
            model_name
        )


    def rerank(
        self,
        query,
        documents,
        top_k=5
    ):

        pairs = []

        for doc in documents:
            pairs.append(
                [
                    query,
                    doc["content"]
                ]
            )


        scores = self.model.predict(
            pairs
        )


        results = []

        for doc, score in zip(
            documents,
            scores
        ):

            item = doc.copy()

            item["rerank_score"] = float(score)

            results.append(item)


        results.sort(
            key=lambda x:
            x["rerank_score"],
            reverse=True
        )


        return results[:top_k]
