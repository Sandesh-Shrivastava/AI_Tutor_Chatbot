"""
main.py — Streamlit Chat UI for the AI Tutor Chatbot.

Run with:
    streamlit run app/main.py

Features:
- Subject selector + level toggle + Socratic mode toggle
- Multi-turn chat with LLaMA 3.3 via RAG (LangChain + Qdrant)
- All conversations logged to MySQL
- Sidebar: recent sessions, quick-switch
- Progress tab: weak topics + session stats dashboard
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import APP_TITLE, STUDENT_LEVELS, SUPPORTED_SUBJECTS
from database.session_logger import (
    end_session,
    get_or_create_user,
    get_session_history,
    get_session_messages,
    log_message,
    setup_database,
    start_session,
    update_topic,
)
from rag.chain import ask, build_chain
from app.dashboard import render_dashboard

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Main background with a vibrant mesh gradient */
    .stApp {
        background: radial-gradient(at 0% 0%, rgba(20, 184, 166, 0.15) 0, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.15) 0, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(14, 165, 233, 0.1) 0, transparent 50%),
                    radial-gradient(at 0% 100%, rgba(16, 185, 129, 0.1) 0, transparent 50%),
                    #020617;
        min-height: 100vh;
    }

    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* Title Styling */
    .app-title {
        font-size: 6.5rem;
        font-weight: 900;
        line-height: 1.1;
        background: linear-gradient(135deg, #2dd4bf, #06b6d4, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        letter-spacing: -0.05em;
    }

    .app-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }

    /* Chat bubbles with vibrant gradients and animations */
    .chat-bubble-user {
        background: linear-gradient(135deg, #0d9488, #0891b2);
        color: white;
        padding: 1rem 1.4rem;
        border-radius: 20px 20px 4px 20px;
        margin: 0.8rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 10px 25px -5px rgba(20, 184, 166, 0.3);
        font-size: 1rem;
        line-height: 1.6;
        animation: fadeInUp 0.3s ease-out;
    }

    .chat-bubble-assistant {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        color: #f1f5f9;
        padding: 1rem 1.4rem;
        border-radius: 20px 20px 20px 4px;
        margin: 0.8rem 0;
        max-width: 85%;
        border: 1px solid rgba(20, 184, 166, 0.2);
        font-size: 1rem;
        line-height: 1.7;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        animation: fadeInUp 0.4s ease-out;
    }

    /* Hero Image Wrapper */
    .hero-container {
        animation: float 4s ease-in-out infinite;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Modern Card UI */
    .modern-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    .modern-card:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: translateY(-2px);
        border-color: rgba(20, 184, 166, 0.4);
    }

    /* Input box refinement */
    .stChatInput > div {
        border-radius: 16px !important;
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        transition: all 0.3s;
    }

    /* Sidebar buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05);
        color: #f1f5f9;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        transition: all 0.2s;
        text-align: left !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(79, 70, 229, 0.2));
        border-color: #7c3aed;
        color: #a78bfa;
    }

    /* Source citation */
    .source-tag {
        display: inline-block;
        background: rgba(96, 165, 250, 0.12);
        color: #60a5fa;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 20px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        margin-right: 4px;
        margin-top: 6px;
    }

    /* Login form transparency and glow */
    [data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.1) !important;
        backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(20, 184, 166, 0.2) !important;
        border-radius: 24px !important;
        padding: 3rem !important;
        box-shadow: 0 0 40px rgba(20, 184, 166, 0.2), 
                    0 0 80px rgba(20, 184, 166, 0.1) !important;
        transition: transform 0.3s ease;
    }
    [data-testid="stForm"]:hover {
        transform: scale(1.01);
        border-color: rgba(20, 184, 166, 0.6) !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(124, 58, 237, 0.3); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(124, 58, 237, 0.5); }
</style>
""",
    unsafe_allow_html=True,
)

# ── DB init (once) ────────────────────────────────────────────────────────────
@st.cache_resource
def init_database():
    setup_database()

init_database()

# ── Session state defaults ────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "username": None,
        "user_id": None,
        "user_level": "beginner",
        "session_id": None,
        "chain": None,
        "memory": None,
        "messages": [],           # list of {"role": str, "content": str}
        "subject": SUPPORTED_SUBJECTS[0],
        "mode": "normal",
        "active_tab": "chat",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ── Helper for Image ──────────────────────────────────────────────────────────
def _get_image_base64():
    import base64
    img_path = "/Users/sandeshshrivastava/.gemini/antigravity/brain/6a3c91cb-db6d-4f6c-a246-7c6654cfe374/ai_tutor_hero_vibrant_1777111816067.png"
    try:
        with open(img_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return ""

# ── Login screen ──────────────────────────────────────────────────────────────
def show_login():
    _, col, _ = st.columns([0.8, 2, 0.8])
    
    with col:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<p class="app-title" style="text-align:center;">🎓 AI Tutor Chatbot</p>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
            
            st.markdown('<p style="font-size:0.9rem; color:#94a3b8; margin-bottom:0.5rem;">Select your level:</p>', unsafe_allow_html=True)
            level = st.pills(
                "Level",
                options=STUDENT_LEVELS,
                selection_mode="single",
                default="beginner",
                format_func=lambda x: x.capitalize(),
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Start Learning →", use_container_width=True)

        if submitted and username.strip():
            user = get_or_create_user(username.strip(), level=level)
            st.session_state.username = user["username"]
            st.session_state.user_id = user["id"]
            st.session_state.user_level = user["level"]
            st.rerun()
        elif submitted:
            st.warning("Please enter a username.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.caption(f"Level: **{st.session_state.user_level.capitalize()}**")
        st.divider()

        # Controls
        subject = st.selectbox(
            "📚 Subject",
            SUPPORTED_SUBJECTS,
            index=SUPPORTED_SUBJECTS.index(st.session_state.subject),
            key="sidebar_subject",
        )
        level = st.selectbox(
            "🎯 Student Level",
            STUDENT_LEVELS,
            index=STUDENT_LEVELS.index(st.session_state.user_level),
            format_func=lambda x: x.capitalize(),
            key="sidebar_level",
        )
        socratic = st.toggle("🔮 Socratic Mode", value=(st.session_state.mode == "socratic"))

        # Apply control changes
        new_mode = "socratic" if socratic else "normal"
        changed = (
            subject != st.session_state.subject
            or level != st.session_state.user_level
            or new_mode != st.session_state.mode
        )
        if changed:
            st.session_state.subject = subject
            st.session_state.user_level = level
            st.session_state.mode = new_mode
            # Rebuild chain with new settings
            _rebuild_chain()

        st.divider()

        if st.button("➕ New Session", use_container_width=True):
            _new_session()

        st.divider()

        # Recent sessions
        st.markdown("#### 🕒 Recent Sessions")
        sessions = get_session_history(st.session_state.user_id, limit=6)
        for s in sessions:
            label = f"{s['subject'] or 'General'} · {s['level'] or '?'}"
            if st.button(label, key=f"sess_{s['session_id']}", use_container_width=True):
                msgs = get_session_messages(s["session_id"])
                st.session_state.messages = [
                    {"role": m["role"], "content": m["content"]} for m in msgs
                ]
                st.session_state.session_id = s["session_id"]
                st.session_state.chain = None  # read-only replay
                st.rerun()

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            _close_session()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ── Chain helpers ─────────────────────────────────────────────────────────────
def _rebuild_chain():
    chain, memory = build_chain(
        subject=st.session_state.subject,
        level=st.session_state.user_level,
        mode=st.session_state.mode,
    )
    st.session_state.chain = chain
    st.session_state.memory = memory

def _new_session():
    _close_session()
    # Clear messages and build fresh chain
    st.session_state.messages = []
    _rebuild_chain()
    session_id = start_session(
        user_id=st.session_state.user_id,
        subject=st.session_state.subject,
        level=st.session_state.user_level,
        mode=st.session_state.mode,
    )
    st.session_state.session_id = session_id

def _close_session():
    if st.session_state.session_id:
        try:
            end_session(st.session_state.session_id)
        except Exception:
            pass
        st.session_state.session_id = None

# ── Chat UI ───────────────────────────────────────────────────────────────────
def render_chat():
    st.markdown('<p class="app-title">🎓 AI Tutor Chatbot</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="app-subtitle">Subject: <b>{st.session_state.subject}</b> · '
        f'Level: <b>{st.session_state.user_level.capitalize()}</b> · '
        f'Mode: <b>{"🔮 Socratic" if st.session_state.mode == "socratic" else "💬 Normal"}</b></p>',
        unsafe_allow_html=True,
    )

    # Init session on first open
    if st.session_state.chain is None:
        _new_session()

    # Chat history
    chat_area = st.container()
    with chat_area:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-bubble-user">{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                content = msg["content"]
                sources_html = ""
                if "sources" in msg:
                    for src in msg["sources"]:
                        sources_html += f'<span class="source-tag">📄 {src}</span>'
                st.markdown(
                    f'<div class="chat-bubble-assistant">{content}'
                    f'{("<br>" + sources_html) if sources_html else ""}</div>',
                    unsafe_allow_html=True,
                )

    # Input
    user_input = st.chat_input(
        placeholder="Ask me anything about " + st.session_state.subject + "…",
        key="chat_input",
    )

    if user_input and user_input.strip():
        question = user_input.strip()

        # Add user message to UI
        st.session_state.messages.append({"role": "user", "content": question})
        log_message(st.session_state.session_id, "user", question)

        # Update topic performance (use first 5 words of question as proxy topic)
        topic_label = " ".join(question.split()[:5])
        update_topic(st.session_state.user_id, st.session_state.subject, topic_label)

        # Get answer
        with st.spinner("Thinking…"):
            answer, source_docs = ask(st.session_state.chain, question)

        # Format source citations
        sources = list(
            {doc.metadata.get("source", "") for doc in source_docs if doc.metadata.get("source")}
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )
        log_message(st.session_state.session_id, "assistant", answer)

        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.username:
        show_login()
        return

    render_sidebar()

    tab_chat, tab_dashboard = st.tabs(["💬 Chat", "📊 Progress Dashboard"])

    with tab_chat:
        render_chat()

    with tab_dashboard:
        render_dashboard(
            user_id=st.session_state.user_id,
            username=st.session_state.username,
        )

if __name__ == "__main__":
    main()
