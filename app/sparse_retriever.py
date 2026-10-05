from app.rag_db import get_rag_connection


class SparseRetriever:

    def search(self, query, top_k=5):
        conn = get_rag_connection()

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        document_id,
                        content,
                        ts_rank_cd(
                            content_tsv,
                            websearch_to_tsquery(
                                'simple',
                                %s
                            )
                        ) AS score
                    FROM rag_chunks
                    WHERE content_tsv @@
                          websearch_to_tsquery(
                              'simple',
                              %s
                          )
                    ORDER BY score DESC
                    LIMIT %s
                    """,
                    (
                        query,
                        query,
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
