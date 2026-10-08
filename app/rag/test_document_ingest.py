import sys

from app.rag.document_ingester import ingest_pdf


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python -m app.rag.test_document_ingest <pdf_path>"
        )
        return

    pdf_path = sys.argv[1]

    document_id = ingest_pdf(pdf_path)

    print()
    print("=" * 60)
    print("INGEST SUCCESS")
    print("rag_documents.id:", document_id)
    print("=" * 60)


if __name__ == "__main__":
    main()
