# 🎓 AI Tutor Chatbot — Production Grade RAG Portal

An ultra-modern, production-ready AI tutoring platform built with **React (Next.js)** and **FastAPI**. It uses Retrieval-Augmented Generation (RAG) to provide strictly isolated, subject-specific learning support powered by **LLaMA 3.3 (70B)** via Groq.

---

## 🎨 Design Aesthetic: "Industrial Architect"
The portal features a premium, high-performance UI designed for professional focus:
- **Palette**: Absolute Carbon Black, Vibrant Vermilion (Orange), and Concrete Grey.
- **Vibe**: High-precision brutalism with a technical terminal-style layout.
- **Glassmorphism**: Sharp, non-blurred glass panels with 1px industrial borders.

---

## 🚀 Key Features
- **Strict Subject Isolation**: The AI is hard-coded to stay within the bounds of the active subject (e.g., Physics, AI, Social Science).
- **Ultra-Concise Normal Mode**: Delivers direct, one-line answers for rapid learning.
- **Socratic Mentorship Mode**: Guides students via thought-provoking questions rather than direct answers.
- **Session Persistence**: Stays logged in and maintains state even after a browser refresh.
- **Hybrid Search**: Leverages Qdrant Cloud for high-speed semantic retrieval from uploaded textbooks.

---

## 🏗️ Tech Stack
- **Frontend**: Next.js 14+, Tailwind CSS, Framer Motion, Zustand.
- **Backend**: FastAPI (Python), LangChain, Groq LPU.
- **Vector Store**: Qdrant Cloud (Semantic Search).
- **Relational DB**: MySQL (Session logging & Analytics).
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`.

---

## 📂 Curriculum Subjects
1.  **Physics**
2.  **Chemistry**
3.  **Biology**
4.  **Mathematics**
5.  **Computer Science**
6.  **Social Science** (History, Geography, Political Science, Economics)
7.  **General Knowledge**

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL Server

### 2. Environment Configuration
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_key_here
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_key
MYSQL_URL=mysql+pymysql://user:pass@host/db
```

### 3. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API (with auto-reload)
python3 api/main.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The UI will be available at [**http://localhost:3000**](http://localhost:3000).

---

## 📁 Repository Structure
```
├── api/                # FastAPI Backend Server
├── frontend/           # Next.js React Application
├── ingestion/          # PDF Parsing & Vector Ingestion
├── rag/                # LangChain & Qdrant Logic
├── prompts/            # Subject-Isolated Prompt Templates
├── database/           # MySQL Session Logger
└── config.py           # Centralized Configuration
```

---

## 🛡️ License
Copyright © 2026 Sandesh Shrivastava. All rights reserved.
