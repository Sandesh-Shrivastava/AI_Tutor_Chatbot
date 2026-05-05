"""
config.py — Centralized configuration for AI Tutor Chatbot
All secrets are loaded from a .env file via python-dotenv
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ─────────────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
LLM_MODEL: str = "llama-3.3-70b-versatile"

# ── Qdrant ───────────────────────────────────────────────────────────────────
QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "ai_tutor_docs")

# ── Embeddings ───────────────────────────────────────────────────────────────
EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

# ── Database ─────────────────────────────────────────────────────────────────
# Render provides DATABASE_URL. We support both MySQL and PostgreSQL.
raw_db_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL") or "mysql+pymysql://root@localhost/ai_tutor"

# SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://' (Render default)
if raw_db_url and raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)

DATABASE_URL: str = raw_db_url

# ── Document Ingestion ───────────────────────────────────────────────────────
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 50
DOCS_DIR: str = os.path.join(os.path.dirname(__file__), "ingestion", "docs")

# ── Streamlit ────────────────────────────────────────────────────────────────
APP_TITLE: str = "AI Tutor Chatbot"
SUPPORTED_SUBJECTS: list[str] = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Python Programming",
    "Data Science",
]
STUDENT_LEVELS: list[str] = ["beginner", "intermediate", "advanced"]
