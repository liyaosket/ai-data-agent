from app.qwen_embedding import QwenEmbeddingModel


def embed_chunks(chunks):
    texts = [chunk.content for chunk in chunks]

    model = QwenEmbeddingModel()
    embeddings = model.embed_batch(texts)

    if len(embeddings) != len(chunks):
        raise ValueError(
            f"Embedding count mismatch: "
            f"chunks={len(chunks)}, embeddings={len(embeddings)}"
        )

    return [
        (chunk, embedding)
        for chunk, embedding in zip(chunks, embeddings)
    ]
