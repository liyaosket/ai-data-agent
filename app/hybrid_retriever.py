from app.pgvector_retriever import PgVectorRetriever
from app.sparse_retriever import SparseRetriever


class HybridRetriever:

    def __init__(
        self,
        dense_retriever=None,
        sparse_retriever=None,
    ):
        self.dense_retriever = dense_retriever or PgVectorRetriever()
        self.sparse_retriever = sparse_retriever or SparseRetriever()

    def search(
        self,
        query,
        top_k=5,
        candidate_k=10,
        rrf_k=60,
    ):
        dense_results = self.dense_retriever.search(
            query,
            top_k=candidate_k,
        )

        sparse_results = self.sparse_retriever.search(
            query,
            top_k=candidate_k,
        )

        scores = {}
        documents = {}
        dense_ranks = {}
        sparse_ranks = {}

        # Dense ranking
        for rank, result in enumerate(dense_results, start=1):
            chunk_id = result["id"]

            dense_ranks[chunk_id] = rank

            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1.0 / (rrf_k + rank)
            )

            documents[chunk_id] = result

        # Sparse ranking
        for rank, result in enumerate(sparse_results, start=1):
            chunk_id = result["id"]

            sparse_ranks[chunk_id] = rank

            scores[chunk_id] = (
                scores.get(chunk_id, 0.0)
                + 1.0 / (rrf_k + rank)
            )

            documents[chunk_id] = result

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []

        for chunk_id, rrf_score in ranked[:top_k]:
            result = documents[chunk_id].copy()

            result["rrf_score"] = rrf_score
            result["dense_rank"] = dense_ranks.get(chunk_id)
            result["sparse_rank"] = sparse_ranks.get(chunk_id)

            results.append(result)

        return results
