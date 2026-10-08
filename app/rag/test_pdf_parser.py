import sys

from app.rag.pdf_parser import parse_pdf


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python -m app.rag.test_pdf_parser <pdf_path>")
        return

    pdf_path = sys.argv[1]

    document = parse_pdf(pdf_path)

    print("=" * 60)
    print("Document")
    print("=" * 60)

    print("document_id:", document.document_id)
    print("source:", document.source)
    print("title:", document.title)
    print("document_type:", document.document_type)

    print()
    print("metadata:")
    print(document.metadata)

    print()
    print("pages:", len(document.pages))

    for page in document.pages:
        print()
        print(f"--- Page {page.page_number} ---")
        print("blocks:", len(page.blocks))

        for index, block in enumerate(page.blocks[:3]):
            print(f"[Block {index}]")
            print("type:", block.block_type)
            print("content:", block.content[:200])
            print("metadata:", block.metadata)


if __name__ == "__main__":
    main()
