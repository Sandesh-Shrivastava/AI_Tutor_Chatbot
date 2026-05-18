# 🎓 AI Tutor Chatbot — Industrial Grade RAG Portal

An ultra-modern, production-ready AI tutoring platform built with **React (Vite + JavaScript)** and **FastAPI**. This system uses Retrieval-Augmented Generation (RAG) to provide strictly isolated, subject-specific learning support powered by **LLaMA 3.3**.

---

## 🎨 Design Aesthetic: "Industrial Architect"
The portal features a premium, high-performance UI designed for professional focus:
- **Palette**: Absolute Carbon Black, Vibrant Vermilion (Orange), and Concrete Grey.
- **Vibe**: High-precision brutalism with a technical terminal-style layout.
- **Micro-Animations**: Real-time terminal scanlines and sharp state transitions.

---

## 🚀 Key Features
- **Strict Subject Isolation**: The AI is hard-coded to stay within the bounds of the active subject. It will refuse to answer off-topic questions with a specific warning message.
- **Flexible Social Science**: Includes History, Geography, Civics, Politics, and Global Affairs.
- **Ultra-Concise Normal Mode**: Delivers direct, one-line answers for rapid learning.
- **Socratic Mentorship Mode**: Guides students via thought-provoking questions to encourage critical thinking.
- **Session Persistence**: Robust state management that maintains user login even after browser refreshes.

---

## 📂 Curriculum Subjects
1.  **Physics**
2.  **Chemistry**
3.  **Biology**
4.  **Mathematics**
5.  **Computer Science**
6.  **Social Science** (History, Geography, Politics, Civics, Global Affairs)
7.  **General Knowledge (GK)**

---

## 🏗️ Tech Stack
- **Frontend**: React.js (Vite), Tailwind CSS v4, Framer Motion, Zustand, React Router v6.
- **Backend**: FastAPI (Python), LangChain, LangChain-Groq.
- **Database**: Dual-Support (MySQL & PostgreSQL) for flexible cloud logging and telemetry.
- **Vector Store**: Qdrant Cloud (Semantic Search).
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` / Sentence Transformers.

---

## 🛠️ Installation & Setup

### 1. Environment Configuration
Create a `.env` file in the root directory for the backend:
```bash
GROQ_API_KEY=your_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=postgres://user:pass@host:port/db  # Or MySQL URL
```

Create a `.env` file in the `frontend/` directory:
```bash
VITE_API_URL=http://localhost:8000
```

### 2. Backend Setup
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

---

## 📁 Repository Structure
- `api/` & `app/`: FastAPI Backend Server & Application Logic.
- `frontend/`: React (Vite) Single Page Application.
- `prompts/`: Logic for Subject Isolation & Mode Control.
- `rag/`: Vector search and chain orchestration.
- `database/`: Schema and session logging logic.

---

## 🛡️ License
Copyright © 2026 Sandesh Shrivastava. All rights reserved.
