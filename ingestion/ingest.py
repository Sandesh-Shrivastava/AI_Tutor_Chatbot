"""
ingest.py — Main document ingestion pipeline.

Usage:
    python ingestion/ingest.py --subject Physics --chapter Kinematics --file ingestion/docs/ncert_11.pdf
    python ingestion/ingest.py --subject Physics --chapter Kinematics --file ingestion/docs/notes.txt
    python ingestion/ingest.py --bulk-dir ingestion/docs/Physics
        (expects folder structure: docs/<Subject>/<Chapter>/<file>.pdf)

The script will:
    1. Parse the file (PDF or TXT)
    2. Chunk the text
    3. Generate embeddings via HuggingFace sentence-transformers
    4. Upsert into Qdrant with subject/chapter metadata
"""

from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    EMBEDDING_MODEL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    QDRANT_URL,
)
from ingestion.chunker import (
    DocumentChunk,
    chunk_pages,
    extract_text_from_pdf,
    extract_text_from_txt,
)

# ── Globals ───────────────────────────────────────────────────────────────────
_embedding_model: SentenceTransformer | None = None
_qdrant_client: QdrantClient | None = None


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        print(f"[Embed] Loading model: {EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY or None,
        )
    return _qdrant_client


# ── Qdrant helpers ────────────────────────────────────────────────────────────

def ensure_collection(client: QdrantClient, vector_size: int) -> None:
    """Create the Qdrant collection if it doesn't already exist."""
    existing = {c.name for c in client.get_collections().collections}
    if QDRANT_COLLECTION not in existing:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        print(f"[Qdrant] Created collection '{QDRANT_COLLECTION}'")
    else:
        print(f"[Qdrant] Collection '{QDRANT_COLLECTION}' already exists")


def upsert_chunks(chunks: list[DocumentChunk]) -> None:
    """Embed and upsert a list of DocumentChunks into Qdrant."""
    if not chunks:
        print("[Ingest] No chunks to upsert.")
        return

    model = get_embedding_model()
    client = get_qdrant_client()

    texts = [c.text for c in chunks]
    print(f"[Embed] Encoding {len(texts)} chunks…")
    vectors = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    ensure_collection(client, vector_size=len(vectors[0]))

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload=chunk.to_qdrant_payload(),
        )
        for vec, chunk in zip(vectors, chunks)
    ]

    client.upsert(collection_name=QDRANT_COLLECTION, points=points)
    print(f"[Qdrant] Upserted {len(points)} points into '{QDRANT_COLLECTION}'")


# ── File loading ──────────────────────────────────────────────────────────────

def load_file(file_path: Path, subject: str, chapter: str) -> list[DocumentChunk]:
    """Load a single PDF or TXT file and return its chunks."""
    suffix = file_path.suffix.lower()
    source = file_path.name

    if suffix == ".pdf":
        pages = extract_text_from_pdf(file_path)
    elif suffix == ".txt":
        pages = extract_text_from_txt(file_path)
    else:
        print(f"[Ingest] Unsupported file type: {suffix}. Skipping.")
        return []

    return chunk_pages(pages, subject=subject, chapter=chapter, source=source)


def bulk_ingest(docs_dir: Path) -> None:
    """
    Ingest all files in a directory tree.

    Expected structure:
        <docs_dir>/<Subject>/<Chapter>/<file>.pdf
        <docs_dir>/<Subject>/<Chapter>/<file>.txt

    If files are directly under <docs_dir>/<Subject>/, the chapter is
    derived from the filename stem.
    """
    all_chunks: list[DocumentChunk] = []

    for subject_dir in sorted(docs_dir.iterdir()):
        if not subject_dir.is_dir():
            continue
        subject = subject_dir.name

        for item in sorted(subject_dir.rglob("*")):
            if item.is_file() and item.suffix.lower() in {".pdf", ".txt"}:
                # Derive chapter from parent folder name (or filename if flat)
                chapter = item.parent.name if item.parent != subject_dir else item.stem
                print(f"\n[Bulk] {subject} → {chapter}: {item.name}")
                chunks = load_file(item, subject=subject, chapter=chapter)
                all_chunks.extend(chunks)

    print(f"\n[Bulk] Total chunks across all subjects: {len(all_chunks)}")
    upsert_chunks(all_chunks)


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest documents into the AI Tutor Qdrant vector store."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=Path, help="Path to a single PDF or TXT file.")
    group.add_argument(
        "--bulk-dir",
        type=Path,
        help="Root docs directory for bulk ingestion (see folder structure docs).",
    )
    parser.add_argument(
        "--subject",
        type=str,
        help="Subject label (required when using --file).",
    )
    parser.add_argument(
        "--chapter",
        type=str,
        default="General",
        help="Chapter/topic label (optional, default: 'General').",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.file:
        if not args.subject:
            parser.error("--subject is required when using --file")
        if not args.file.exists():
            parser.error(f"File not found: {args.file}")
        print(f"\n[Ingest] Single file mode: {args.file}")
        chunks = load_file(args.file, subject=args.subject, chapter=args.chapter)
        upsert_chunks(chunks)

    elif args.bulk_dir:
        if not args.bulk_dir.exists():
            parser.error(f"Directory not found: {args.bulk_dir}")
        print(f"\n[Ingest] Bulk mode: {args.bulk_dir}")
        bulk_ingest(args.bulk_dir)

    print("\n✅  Ingestion complete!")


if __name__ == "__main__":
    main()
