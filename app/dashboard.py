"""
dashboard.py — Progress dashboard tab for the AI Tutor Streamlit app.
Displays weak topics, session history, and usage stats pulled from MySQL.
"""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st

from database.session_logger import get_topic_performance, get_session_history


def render_dashboard(user_id: int, username: str) -> None:
    """Render the full progress dashboard for the given user."""

    st.markdown("## 📊 Your Learning Progress")
    st.markdown(f"Tracking insights for **{username}**")
    st.divider()

    # ── Session Stats ─────────────────────────────────────────────────────────
    sessions = get_session_history(user_id, limit=50)
    topics = get_topic_performance(user_id, limit=10)

    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    total_sessions = len(sessions)
    total_queries = sum(t["query_count"] for t in topics)
    avg_per_session = round(total_queries / max(total_sessions, 1), 1)

    col1.metric("📅 Total Sessions", total_sessions)
    col2.metric("💬 Total Queries", total_queries)
    col3.metric("⚡ Avg Queries / Session", avg_per_session)
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ── Weak Topics Chart ─────────────────────────────────────────────────────
    st.markdown("### 🔴 Weak Topics (Most Repeated Queries)")
    if topics:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        df_topics = pd.DataFrame(topics)
        fig, ax = plt.subplots(figsize=(8, 4), facecolor="none")
        ax.set_facecolor("none")

        bars = ax.barh(
            df_topics["topic"],
            df_topics["query_count"],
            color="#7c3aed",
            edgecolor="#a78bfa",
            linewidth=0.5,
        )
        ax.set_xlabel("Query Count", color="#e2e8f0", fontsize=11)
        ax.tick_params(colors="#e2e8f0")
        ax.invert_yaxis()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.spines[:].set_color("#374151")

        for bar in bars:
            ax.text(
                bar.get_width() + 0.05,
                bar.get_y() + bar.get_height() / 2,
                str(int(bar.get_width())),
                va="center",
                color="#a78bfa",
                fontsize=10,
            )

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.dataframe(
            df_topics[["topic", "subject", "query_count", "last_queried"]].rename(
                columns={
                    "topic": "Topic",
                    "subject": "Subject",
                    "query_count": "Times Asked",
                    "last_queried": "Last Asked",
                }
            ),
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No topic data yet. Start asking questions to see your weak topics here!")

    st.divider()

    # ── Session Timeline ──────────────────────────────────────────────────────
    st.markdown("### 📅 Session History")
    if sessions:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        df_sessions = pd.DataFrame(sessions)
        df_sessions["started_at"] = pd.to_datetime(df_sessions["started_at"])
        df_sessions["Date"] = df_sessions["started_at"].dt.date

        # Sessions per day chart
        sessions_per_day = df_sessions.groupby("Date").size().reset_index(name="Sessions")

        fig2, ax2 = plt.subplots(figsize=(8, 3), facecolor="none")
        ax2.set_facecolor("none")
        ax2.plot(
            sessions_per_day["Date"],
            sessions_per_day["Sessions"],
            color="#6366f1",
            linewidth=3,
            marker="o",
            markersize=8,
            markerfacecolor="#a78bfa",
        )
        ax2.fill_between(
            sessions_per_day["Date"],
            sessions_per_day["Sessions"],
            alpha=0.1,
            color="#6366f1",
        )
        ax2.set_xlabel("Date", color="#94a3b8")
        ax2.set_ylabel("Sessions", color="#94a3b8")
        ax2.tick_params(colors="#94a3b8")
        ax2.spines[:].set_color("#374151")
        ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.dataframe(
            df_sessions[["session_id", "subject", "level", "mode", "started_at", "ended_at"]].rename(
                columns={
                    "session_id": "Session",
                    "subject": "Subject",
                    "level": "Level",
                    "mode": "Mode",
                    "started_at": "Started",
                    "ended_at": "Ended",
                }
            ),
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No sessions yet. Complete your first chat session to see history here!")
