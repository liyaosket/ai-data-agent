import math


class VectorStore:

    def __init__(self):
        self.documents = []

    def add(
        self,
        vector,
        text,
        metadata=None,
    ):
        self.documents.append(
            {
                "vector": vector,
                "text": text,
                "metadata": metadata or {},
            }
        )

    def _cosine_similarity(self, a, b):
        dot_product = sum(
            x * y
            for x, y in zip(a, b)
        )

        norm_a = math.sqrt(
            sum(x * x for x in a)
        )

        norm_b = math.sqrt(
            sum(x * x for x in b)
        )

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (
            norm_a * norm_b
        )

    def search(
        self,
        query_vector,
        top_k=3,
    ):
        results = []

        for document in self.documents:

            score = self._cosine_similarity(
                query_vector,
                document["vector"],
            )

            results.append(
                {
                    "text": document["text"],
                    "metadata": document["metadata"],
                    "score": score,
                }
            )

        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return results[:top_k]
