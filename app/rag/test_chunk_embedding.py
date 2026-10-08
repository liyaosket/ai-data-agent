import sys

from app.rag.pdf_parser import parse_pdf
from app.rag.structure_chunker import build_chunks
from app.rag.chunk_embedder import embed_chunks


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python -m app.rag.test_chunk_embedding <pdf_path>"
        )
        return

    pdf_path = sys.argv[1]

    document = parse_pdf(pdf_path)

    chunks = build_chunks(document)

    print("document:", document.document_id)
    print("pages:", len(document.pages))
    print("chunks:", len(chunks))

    embedded_chunks = embed_chunks(chunks)

    print()
    print("embedded chunks:", len(embedded_chunks))

    for chunk, embedding in embedded_chunks[:3]:
        print()
        print("=" * 60)
        print("chunk_id:", chunk.chunk_id)
        print("content:", chunk.content[:200])
        print("dimension:", len(embedding))
        print("embedding preview:", embedding[:5])


if __name__ == "__main__":
    main()
