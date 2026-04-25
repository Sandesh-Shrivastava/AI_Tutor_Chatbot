"""
chunker.py — Text chunking utilities for the document ingestion pipeline.
Uses LangChain's RecursiveCharacterTextSplitter to break PDF text into
overlapping chunks with subject/chapter metadata attached.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


@dataclass
class DocumentChunk:
    """A single text chunk with its associated metadata."""
    text: str
    subject: str
    chapter: str
    source: str
    page: Optional[int] = None
    chunk_index: int = 0
    metadata: dict = field(default_factory=dict)

    def to_qdrant_payload(self) -> dict:
        """Return a flat dict suitable as a Qdrant point payload."""
        return {
            "text": self.text,
            "subject": self.subject,
            "chapter": self.chapter,
            "source": self.source,
            "page": self.page,
            "chunk_index": self.chunk_index,
            **self.metadata,
        }


def extract_text_from_pdf(pdf_path: str | Path) -> list[tuple[int, str]]:
    """
    Extract text from each page of a PDF.

    Returns:
        List of (page_number, page_text) tuples. Page numbers are 1-indexed.
    """
    pages: list[tuple[int, str]] = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append((i + 1, text))
    print(f"  [PDF] Extracted {len(pages)} pages from {Path(pdf_path).name}")
    return pages


def extract_text_from_txt(txt_path: str | Path) -> list[tuple[int, str]]:
    """Extract text from a plain-text file as a single 'page'."""
    text = Path(txt_path).read_text(encoding="utf-8", errors="ignore")
    return [(1, text)] if text.strip() else []


def chunk_pages(
    pages: list[tuple[int, str]],
    subject: str,
    chapter: str,
    source: str,
) -> list[DocumentChunk]:
    """
    Chunk extracted page text into overlapping segments.

    Args:
        pages:   List of (page_number, text) from a document.
        subject: High-level subject label (e.g. "Physics").
        chapter: Chapter or topic label (e.g. "Kinematics").
        source:  Original filename (for citation purposes).

    Returns:
        List of DocumentChunk objects ready for embedding.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[DocumentChunk] = []
    global_index = 0

    for page_num, page_text in pages:
        splits = splitter.split_text(page_text)
        for split in splits:
            if split.strip():
                chunks.append(
                    DocumentChunk(
                        text=split.strip(),
                        subject=subject,
                        chapter=chapter,
                        source=source,
                        page=page_num,
                        chunk_index=global_index,
                    )
                )
                global_index += 1

    print(f"  [Chunker] Created {len(chunks)} chunks for '{subject} → {chapter}'")
    return chunks
