from pathlib import Path
from typing import Any

import fitz
from app.rag.structure_classifier import classify_block

from app.rag.document_model import (
    Document,
    DocumentBlock,
    DocumentPage,
)


def parse_pdf(pdf_path: str) -> Document:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document_id = path.stem

    pdf = fitz.open(pdf_path)

    pages: list[DocumentPage] = []

    for page_index, page in enumerate(pdf):
        page_number = page_index + 1

        blocks: list[DocumentBlock] = []

        raw_blocks = page.get_text("blocks")

        for block in raw_blocks:
            text = block[4].strip()

            if not text:
                continue

            x0, y0, x1, y1 = block[:4]

            metadata: dict[str, Any] = {
                "page": page_number,
                "bbox": [x0, y0, x1, y1],
            }

            block_type = classify_block(text)

            blocks.append(
                DocumentBlock(
                    block_type=block_type,
                    content=text,
                    metadata=metadata,
                )
            )

        pages.append(
            DocumentPage(
                page_number=page_number,
                blocks=blocks,
            )
        )

    pdf.close()

    return Document(
        document_id=document_id,
        source=str(path),
        title=path.stem,
        document_type="pdf",
        pages=pages,
        metadata={
            "filename": path.name,
            "page_count": len(pages),
        },
    )
