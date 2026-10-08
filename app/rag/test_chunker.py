import sys

from app.rag.pdf_parser import parse_pdf
from app.rag.structure_chunker import build_chunks


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python -m app.rag.test_chunker <pdf_path>"
        )
        return

    pdf_path = sys.argv[1]

    document = parse_pdf(pdf_path)

    chunks = build_chunks(document)

    print("=" * 70)
    print("Chunking Result")
    print("=" * 70)

    print("document:", document.document_id)
    print("pages:", len(document.pages))
    print("chunks:", len(chunks))

    for chunk in chunks[:20]:
        print()
        print("-" * 70)
        print("chunk_id:", chunk.chunk_id)
        print("metadata:", chunk.metadata)
        print("content:")
        print(chunk.content[:1000])


if __name__ == "__main__":
    main()
