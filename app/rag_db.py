import os

import psycopg2
from pgvector.psycopg2 import register_vector


def get_rag_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ecommerce"),
        user=os.getenv("RAG_DB_USER", "rag_writer"),
        password=os.getenv("RAG_DB_PASSWORD", "rag_writer_dev123456"),
    )

    register_vector(conn)

    return conn
