import json

from app.rag_db import get_rag_connection
from app.rag.pdf_parser import parse_pdf
from app.rag.structure_chunker import build_chunks
from app.rag.chunk_embedder import embed_chunks


def ingest_pdf(pdf_path):
    # 1. Parse PDF
    document = parse_pdf(pdf_path)

    # 2. Build chunks
    chunks = build_chunks(document)

    if not chunks:
        raise ValueError("No chunks generated from PDF")

    # 3. Generate embeddings
    embedded_chunks = embed_chunks(chunks)

    conn = get_rag_connection()

    try:
        with conn:
            with conn.cursor() as cur:

                # 4. Insert document
                cur.execute(
                    """
                    INSERT INTO rag_documents (
                        source_type,
                        source_uri,
                        title,
                        content,
                        metadata,
                        source_key
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        document.document_type,
                        document.source,
                        document.title,
                        "\n\n".join(
                            chunk.content
                            for chunk in chunks
                        ),
                        json.dumps({
                            "document_id": document.document_id,
                            "page_count": len(document.pages),
                        }),
                        document.document_id,
                    ),
                )

                document_db_id = cur.fetchone()[0]

                print(
                    f"Inserted document: id={document_db_id}"
                )

                # 5. Insert chunks
                for chunk_index, (chunk, embedding) in enumerate(
                    embedded_chunks
                ):
                    cur.execute(
                        """
                        INSERT INTO rag_chunks (
                            document_id,
                            chunk_index,
                            content,
                            metadata,
                            embedding
                        )
                        VALUES (%s, %s, %s, %s, %s::vector)
                        """,
                        (
                            document_db_id,
                            chunk_index,
                            chunk.content,
                            json.dumps(chunk.metadata),
                            embedding,
                        ),
                    )

                print(
                    f"Inserted chunks: {len(embedded_chunks)}"
                )

        return document_db_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
