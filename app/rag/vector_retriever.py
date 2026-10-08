from app.rag_db import get_rag_connection
from app.qwen_embedding import QwenEmbeddingModel


class VectorRetriever:

    def __init__(self):
        self.embedding_model = QwenEmbeddingModel()

    def search(
        self,
        query,
        top_k=5,
        document_id=None,
    ):
        query_embedding = self.embedding_model.embed(query)

        conn = get_rag_connection()

        try:
            with conn.cursor() as cur:

                if document_id is None:
                    cur.execute(
                        """
                        SELECT
                            id,
                            document_id,
                            chunk_index,
                            content,
                            metadata,
                            1 - (embedding <=> %s::vector) AS score
                        FROM rag_chunks
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                        """,
                        (
                            query_embedding,
                            query_embedding,
                            top_k,
                        ),
                    )
                else:
                    cur.execute(
                        """
                        SELECT
                            id,
                            document_id,
                            chunk_index,
                            content,
                            metadata,
                            1 - (embedding <=> %s::vector) AS score
                        FROM rag_chunks
                        WHERE document_id = %s
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                        """,
                        (
                            query_embedding,
                            document_id,
                            query_embedding,
                            top_k,
                        ),
                    )

                rows = cur.fetchall()

                return [
                    {
                        "id": row[0],
                        "document_id": row[1],
                        "chunk_index": row[2],
                        "content": row[3],
                        "metadata": row[4],
                        "score": float(row[5]),
                    }
                    for row in rows
                ]

        finally:
            conn.close()
