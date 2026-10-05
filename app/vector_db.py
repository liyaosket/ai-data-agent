from pgvector.psycopg2 import register_vector

from app.db import get_connection


def init_vector_db():
    conn = get_connection()

    try:
        register_vector(conn)

        with conn.cursor() as cur:
            cur.execute(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )

        conn.commit()

    finally:
        conn.close()
