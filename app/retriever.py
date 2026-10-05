class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(
        self,
        query_vector,
        top_k=3,
        score_threshold=0.0,
        metadata_filter=None,
    ):
        results = self.vector_store.search(
            query_vector,
            top_k=len(self.vector_store.documents),
        )

        filtered_results = []

        for result in results:
            if result["score"] < score_threshold:
                continue

            if metadata_filter:
                matched = True

                for key, value in metadata_filter.items():
                    if result["metadata"].get(key) != value:
                        matched = False
                        break

                if not matched:
                    continue

            filtered_results.append(result)

        filtered_results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return filtered_results[:top_k]
