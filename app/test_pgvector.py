from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

from app.rag_db import get_rag_connection
from app.qwen_embedding import QwenEmbeddingModel


load_dotenv()


def main():
    embedding_model = QwenEmbeddingModel()

    text = "Kafka 用于实时传输订单事件。"

    vector = embedding_model.embed(text)

    print("Embedding dimension:", len(vector))

    conn = get_rag_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO rag_documents
                (source_type, title, content)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    "manual",
                    "Kafka 基础知识",
                    text,
                ),
            )

            document_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO rag_chunks
                (document_id, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    document_id,
                    0,
                    text,
                    vector,
                ),
            )

            chunk_id = cur.fetchone()[0]

        conn.commit()

        print("Document ID:", document_id)
        print("Chunk ID:", chunk_id)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
