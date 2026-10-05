from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

from app.rag_db import get_rag_connection
from app.qwen_embedding import QwenEmbeddingModel


load_dotenv()


def search(query: str, top_k: int = 5):
    embedding_model = QwenEmbeddingModel()

    query_vector = embedding_model.embed(query)

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
                    query_vector,
                    query_vector,
                    top_k,
                ),
            )

            rows = cur.fetchall()

            for row in rows:
                print()
                print("Chunk ID:", row[0])
                print("Document ID:", row[1])
                print("Score:", row[3])
                print("Content:", row[2])

    finally:
        conn.close()


if __name__ == "__main__":
    search("Kafka 如何传输订单数据？")
