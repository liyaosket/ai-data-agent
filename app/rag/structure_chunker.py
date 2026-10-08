from app.rag.chunk_model import DocumentChunk
from app.rag.document_model import Document


MAX_CHARS = 2000


def build_chunks(document: Document) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    current_section: str | None = None
    current_blocks: list[str] = []
    current_block_types: list[str] = []

    chunk_index = 0

    def flush():
        nonlocal chunk_index

        if not current_blocks:
            return

        content = "\n\n".join(current_blocks)

        metadata = {
            "document_id": document.document_id,
            "source": document.source,
            "title": document.title,
            "document_type": document.document_type,
            "section": current_section,
            "page": current_page,
            "block_types": current_block_types.copy(),
        }

        chunks.append(
            DocumentChunk(
                chunk_id=(
                    f"{document.document_id}"
                    f"_chunk_{chunk_index:05d}"
                ),
                document_id=document.document_id,
                content=content,
                metadata=metadata,
            )
        )

        chunk_index += 1
        current_blocks.clear()
        current_block_types.clear()

    current_page = 1

    for page in document.pages:
        current_page = page.page_number

        for block in page.blocks:

            if block.block_type == "heading":
                flush()
                current_section = block.content
                continue

            if block.block_type not in {"paragraph", "code"}:
                continue

            text = block.content.strip()

            if not text:
                continue

            current_length = sum(
                len(item) for item in current_blocks
            )

            if (
                current_blocks
                and current_length + len(text) > MAX_CHARS
            ):
                flush()

            current_blocks.append(text)
            current_block_types.append(block.block_type)

    flush()

    return chunks
