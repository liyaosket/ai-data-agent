from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentBlock:
    block_type: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentPage:
    page_number: int
    blocks: list[DocumentBlock] = field(default_factory=list)


@dataclass
class Document:
    document_id: str
    source: str
    title: str | None
    document_type: str
    pages: list[DocumentPage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
