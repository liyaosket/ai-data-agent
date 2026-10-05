import time
from dataclasses import dataclass

from app.chunker import TextChunker
from app.qwen_embedding import QwenEmbeddingModel
from app.rag_db import get_rag_connection
from app.rag_seed_data import build_documents


EMBEDDING_BATCH_SIZE = 20


@dataclass
class ChunkRecord:
    document_id: int
    chunk_index: int
    content: str


def insert_documents(documents):
    conn = get_rag_connection()
    chunker = TextChunker(chunk_size=300, overlap=50)

    try:
        records = []

        with conn.cursor() as cur:
            for doc in documents:
                cur.execute(
                    """
                    INSERT INTO rag_documents
                    (source_type, title, content)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (
                        doc.source_type,
                        doc.title,
                        doc.content,
                    ),
                )

                document_id = cur.fetchone()[0]

                chunks = chunker.split(doc.content)

                for chunk_index, content in enumerate(chunks):
                    records.append(
                        ChunkRecord(
                            document_id=document_id,
                            chunk_index=chunk_index,
                            content=content,
                        )
                    )

        conn.commit()
        return records

    finally:
        conn.close()


def embed_chunks(
    model: QwenEmbeddingModel,
    chunks: list[ChunkRecord],
):
    embeddings = []

    total = len(chunks)

    for start in range(0, total, EMBEDDING_BATCH_SIZE):
        batch = chunks[start:start + EMBEDDING_BATCH_SIZE]

        texts = [
            chunk.content
            for chunk in batch
        ]

        batch_embeddings = model.embed_batch(texts)

        embeddings.extend(batch_embeddings)

        print(
            f"Embedded {min(start + len(batch), total)}/{total}"
        )

    return embeddings


def insert_chunks(
    chunks: list[ChunkRecord],
    embeddings,
):
    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk count {len(chunks)} "
            f"!= embedding count {len(embeddings)}"
        )

    conn = get_rag_connection()

    try:
        with conn.cursor() as cur:

            for chunk, embedding in zip(
                chunks,
                embeddings,
            ):
                cur.execute(
                    """
                    INSERT INTO rag_chunks
                    (
                        document_id,
                        chunk_index,
                        content,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        chunk.document_id,
                        chunk.chunk_index,
                        chunk.content,
                        embedding,
                    ),
                )

        conn.commit()

    finally:
        conn.close()


def main():
    start_time = time.perf_counter()

    print("=" * 70)
    print("RAG Ingestion")
    print("=" * 70)

    documents = build_documents()

    print(f"Documents: {len(documents)}")

    print()
    print("Step 1: insert documents")

    chunks = insert_documents(documents)

    print(f"Chunks: {len(chunks)}")

    print()
    print("Step 2: embedding")

    model = QwenEmbeddingModel()

    embeddings = embed_chunks(
        model,
        chunks,
    )

    print()
    print("Step 3: insert chunks")

    insert_chunks(
        chunks,
        embeddings,
    )

    elapsed = time.perf_counter() - start_time

    print()
    print("=" * 70)
    print("Ingestion Completed")
    print("=" * 70)

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
