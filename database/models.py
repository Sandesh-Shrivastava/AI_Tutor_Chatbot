"""
models.py — SQLAlchemy ORM models for the AI Tutor database.
Mirrors database/schema.sql exactly.
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import DATABASE_URL


# ── Enums ──────────────────────────────────────────────────────────────────────

class LevelEnum(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class RoleEnum(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class ModeEnum(str, enum.Enum):
    normal = "normal"
    socratic = "socratic"


# ── Base ───────────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── Models ─────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    level = Column(Enum(LevelEnum), default=LevelEnum.beginner)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sessions = relationship("Session", back_populates="user", cascade="all, delete")
    topic_performances = relationship(
        "TopicPerformance", back_populates="user", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} level={self.level}>"


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(100))
    level = Column(Enum(LevelEnum))
    mode = Column(Enum(ModeEnum), default=ModeEnum.normal)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete")

    def __repr__(self) -> str:
        return f"<Session id={self.id} user_id={self.user_id} subject={self.subject!r}>"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(
        Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(Enum(RoleEnum), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message id={self.id} role={self.role} session_id={self.session_id}>"


class TopicPerformance(Base):
    __tablename__ = "topic_performance"
    __table_args__ = (
        UniqueConstraint("user_id", "topic", name="unique_user_topic"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(100))
    topic = Column(String(200))
    query_count = Column(Integer, default=1)
    last_queried = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="topic_performances")

    def __repr__(self) -> str:
        return (
            f"<TopicPerformance user_id={self.user_id} "
            f"topic={self.topic!r} count={self.query_count}>"
        )


# ── Engine & Session factory ───────────────────────────────────────────────────

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    """Create all tables (idempotent — safe to call on startup)."""
    Base.metadata.create_all(bind=engine)
    print("[DB] Tables ensured ✓")
