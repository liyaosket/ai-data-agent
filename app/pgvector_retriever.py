from app.qwen_embedding import QwenEmbeddingModel
from app.rag_db import get_rag_connection


class PgVectorRetriever:

    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or QwenEmbeddingModel()

    def search(self, query, top_k=5):
        query_embedding = self.embedding_model.embed(query)

        conn = get_rag_connection()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        document_id,
                        content,
                        1 - (embedding <=> %s::vector) AS score
                    FROM rag_chunks
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        query_embedding,
                        query_embedding,
                        top_k,
                    ),
                )

                rows = cur.fetchall()

                return [
                    {
                        "id": row[0],
                        "document_id": row[1],
                        "content": row[2],
                        "score": float(row[3]),
                    }
                    for row in rows
                ]

        finally:
            conn.close()
