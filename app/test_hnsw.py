from dotenv import load_dotenv

from app.qwen_embedding import QwenEmbeddingModel
from app.rag_db import get_rag_connection


load_dotenv()


def run_explain(conn, query_vector):
    with conn.cursor() as cur:

        cur.execute("SET enable_seqscan = off")

        cur.execute(
            """
            EXPLAIN (ANALYZE, BUFFERS)
            SELECT
                id,
                document_id,
                content,
                1 - (embedding <=> %s::vector) AS score
            FROM rag_chunks
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT 5
            """,
            (
                query_vector,
                query_vector,
            ),
        )

        return [row[0] for row in cur.fetchall()]


def main():
    model = QwenEmbeddingModel()

    query = "Kafka 如何传输订单数据？"

    query_vector = model.embed(query)

    conn = get_rag_connection()

    try:
        plan = run_explain(conn, query_vector)

        print("=" * 70)
        print("HNSW Query Plan")
        print("=" * 70)

        for line in plan:
            print(line)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
