"""
session_logger.py — Helper functions to log all chat activity to MySQL.

Public API:
    get_or_create_user(username, level)   -> User
    start_session(user_id, subject, ...)  -> int (session_id)
    end_session(session_id)
    log_message(session_id, role, content)
    update_topic(user_id, subject, topic)
    get_session_history(user_id, limit)   -> list[dict]
    get_topic_performance(user_id)        -> list[dict]
    get_session_messages(session_id)      -> list[dict]
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from sqlalchemy.orm import Session as DBSession

from database.models import (
    LevelEnum,
    Message,
    ModeEnum,
    RoleEnum,
    Session,
    SessionLocal,
    TopicPerformance,
    User,
    init_db,
)


@contextmanager
def get_db() -> Generator[DBSession, None, None]:
    """Provide a transactional database session."""
    db: DBSession = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ── User ──────────────────────────────────────────────────────────────────────

def get_or_create_user(
    username: str,
    level: str = "beginner",
) -> dict:
    """
    Return existing user or create a new one.
    Returns a dict with user id, username, and level.
    """
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username, level=LevelEnum(level))
            db.add(user)
            db.flush()  # get the id before commit
        return {"id": user.id, "username": user.username, "level": user.level.value}


def update_user_level(user_id: int, level: str) -> None:
    with get_db() as db:
        db.query(User).filter(User.id == user_id).update({"level": LevelEnum(level)})


# ── Session ───────────────────────────────────────────────────────────────────

def start_session(
    user_id: int,
    subject: str,
    level: str = "beginner",
    mode: str = "normal",
) -> int:
    """Create a new session and return its id."""
    with get_db() as db:
        session = Session(
            user_id=user_id,
            subject=subject,
            level=LevelEnum(level),
            mode=ModeEnum(mode),
        )
        db.add(session)
        db.flush()
        return session.id


def end_session(session_id: int) -> None:
    """Mark a session as ended with the current timestamp."""
    with get_db() as db:
        db.query(Session).filter(Session.id == session_id).update(
            {"ended_at": datetime.utcnow()}
        )


def get_session_history(user_id: int, limit: int = 10) -> list[dict]:
    """Return the most recent sessions for a user (newest first)."""
    with get_db() as db:
        rows = (
            db.query(Session)
            .filter(Session.user_id == user_id)
            .order_by(Session.started_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "session_id": r.id,
                "subject": r.subject,
                "level": r.level.value if r.level else None,
                "mode": r.mode.value if r.mode else None,
                "started_at": r.started_at,
                "ended_at": r.ended_at,
            }
            for r in rows
        ]


# ── Messages ──────────────────────────────────────────────────────────────────

def log_message(session_id: int, role: str, content: str) -> None:
    """Log a single message (user or assistant) to the messages table."""
    with get_db() as db:
        msg = Message(
            session_id=session_id,
            role=RoleEnum(role),
            content=content,
        )
        db.add(msg)


def get_session_messages(session_id: int) -> list[dict]:
    """Return all messages for a given session in chronological order."""
    with get_db() as db:
        rows = (
            db.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.timestamp.asc())
            .all()
        )
        return [
            {"role": r.role.value, "content": r.content, "timestamp": r.timestamp}
            for r in rows
        ]


# ── Topic Performance ─────────────────────────────────────────────────────────

def update_topic(user_id: int, subject: str, topic: str) -> None:
    """
    Increment query_count for a topic. Inserts a new row if it doesn't exist.
    Uses MySQL's ON DUPLICATE KEY UPDATE via a raw-ish ORM approach.
    """
    with get_db() as db:
        existing = (
            db.query(TopicPerformance)
            .filter(
                TopicPerformance.user_id == user_id,
                TopicPerformance.topic == topic,
            )
            .first()
        )
        if existing:
            existing.query_count += 1
            existing.last_queried = datetime.utcnow()
        else:
            db.add(
                TopicPerformance(
                    user_id=user_id,
                    subject=subject,
                    topic=topic,
                    query_count=1,
                )
            )


def get_topic_performance(user_id: int, limit: int = 10) -> list[dict]:
    """Return a user's most-queried topics (weakest topics first)."""
    with get_db() as db:
        rows = (
            db.query(TopicPerformance)
            .filter(TopicPerformance.user_id == user_id)
            .order_by(TopicPerformance.query_count.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "topic": r.topic,
                "subject": r.subject,
                "query_count": r.query_count,
                "last_queried": r.last_queried,
            }
            for r in rows
        ]


# ── Init ──────────────────────────────────────────────────────────────────────

def setup_database() -> None:
    """Call once on app startup to ensure all tables exist."""
    init_db()
