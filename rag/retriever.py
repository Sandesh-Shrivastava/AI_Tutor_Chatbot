"""
retriever.py — Qdrant retriever setup for LangChain.
Creates a subject-filtered Qdrant vector store retriever.
"""

from __future__ import annotations

import sys
from pathlib import Path

from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (
    EMBEDDING_MODEL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    QDRANT_URL,
)

_client: QdrantClient | None = None
_embeddings: HuggingFaceEmbeddings | None = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)
    return _client


def get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def build_retriever(subject: str | None = None, k: int = 4):
    """
    Build a LangChain retriever backed by Qdrant.

    Args:
        subject: If provided, filters results to this subject only.
        k:       Number of documents to retrieve per query.

    Returns:
        A LangChain VectorStoreRetriever.
    """
    client = get_qdrant_client()
    embeddings = get_embeddings()

    vector_store = Qdrant(
        client=client,
        collection_name=QDRANT_COLLECTION,
        embeddings=embeddings,
        content_payload_key="text",
        metadata_payload_key=None,  # all remaining fields become metadata
    )

    search_kwargs: dict = {"k": k}
    if subject:
        search_kwargs["filter"] = Filter(
            must=[FieldCondition(key="subject", match=MatchValue(value=subject))]
        )

    return vector_store.as_retriever(search_kwargs=search_kwargs)
