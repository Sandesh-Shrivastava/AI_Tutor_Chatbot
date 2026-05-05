import sys
import os
from pathlib import Path

# Add root directory to sys.path for internal imports
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Internal imports
from database.session_logger import (
    get_or_create_user,
    start_session,
    get_session_history,
    get_session_messages,
    log_message,
    update_topic,
    get_topic_performance,
)
from rag.chain import build_chain, ask

app = FastAPI(title="AI Tutor API", version="1.0.0")

# Enable CORS for React frontend (localhost:3000 or 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Models ────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    level: str = "beginner"

class SessionRequest(BaseModel):
    user_id: int
    subject: str
    level: str = "beginner"
    mode: str = "normal"

class ChatRequest(BaseModel):
    session_id: int
    user_id: int
    question: str
    subject: str
    level: str = "beginner"
    mode: str = "normal"

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
async def root_path():
    return {"status": "AI Tutor API is online", "version": "1.0.0"}

@app.post("/auth/login")
async def login(req: LoginRequest):
    try:
        user = get_or_create_user(req.username, level=req.level)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions/start")
async def start_new_session(req: SessionRequest):
    try:
        session_id = start_session(
            user_id=req.user_id,
            subject=req.subject,
            level=req.level,
            mode=req.mode
        )
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/history/{user_id}")
async def get_history(user_id: int):
    try:
        return get_session_history(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/{session_id}/messages")
async def get_messages(session_id: int):
    try:
        return get_session_messages(session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/ask")
async def chat_ask(req: ChatRequest, background_tasks: BackgroundTasks):
    try:
        # 1. Log User Message
        log_message(req.session_id, "user", req.question)
        
        # 2. Update Topic (async)
        topic_proxy = " ".join(req.question.split()[:5])
        background_tasks.add_task(update_topic, req.user_id, req.subject, topic_proxy)
        
        # 3. Build Chain & Ask
        # We build the chain on the fly to stay stateless. 
        # For better performance, consider a session-based cache.
        chain, _ = build_chain(
            subject=req.subject,
            level=req.level,
            mode=req.mode
        )
        
        answer, source_docs = ask(chain, req.question)
        
        # 4. Format Sources
        sources = list({
            doc.metadata.get("source", "") 
            for doc in source_docs if doc.metadata.get("source")
        })
        
        # 5. Log Assistant Message
        log_message(req.session_id, "assistant", answer)
        
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/topics/{user_id}")
async def analytics_topics(user_id: int):
    try:
        return get_topic_performance(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
