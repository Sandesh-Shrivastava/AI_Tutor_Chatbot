# 🎓 AI Tutor Chatbot — Industrial Grade RAG Portal

An ultra-modern, production-ready AI tutoring platform built with **React (Next.js)** and **FastAPI**. This system uses Retrieval-Augmented Generation (RAG) to provide strictly isolated, subject-specific learning support powered by **LLaMA 3.3 (70B)**.

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
- **Frontend**: Next.js 14, Tailwind CSS, Framer Motion, Zustand.
- **Backend**: FastAPI (Python), LangChain.
- **Database**: Dual-Support (MySQL & PostgreSQL) for flexible cloud deployment.
- **Vector Store**: Qdrant Cloud (Semantic Search).
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`.

---

## 🛠️ Installation & Setup

### 1. Environment Configuration
Create a `.env` file:
```bash
GROQ_API_KEY=your_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=postgres://user:pass@host:port/db  # Or MYSQL_URL
```

### 2. Backend Setup
```bash
pip install -r requirements.txt
python3 api/main.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Repository Structure
- `api/`: FastAPI Backend Server.
- `frontend/`: Next.js React Application.
- `prompts/`: Logic for Subject Isolation & Mode Control.
- `rag/`: Vector search and chain orchestration.
- `database/`: Schema and session logging logic.

---

## 🔮 Future Enhancements
The AI Tutor is an evolving platform. Upcoming features include:

### 🚀 1. Production Deployment
- **Cloud Infrastructure**: Migration to a fully containerized architecture (Docker/Kubernetes).
- **Edge Deployment**: Deploying the frontend to Vercel Edge for sub-100ms global response times.
- **Horizontal Scaling**: Implementing a load balancer to handle thousands of concurrent students.

### 🧠 2. Intelligent Features
- **Adaptive Learning Analytics**: A personalized dashboard that tracks student "Mastery Levels" per topic using Bayesian Knowledge Tracing.
- **Multimodal Tutoring**: Voice-to-Voice interaction and AI-generated video explanations.
- **Visual Synthesis**: Real-time generation of diagrams, flowcharts, and 3D models to explain complex Physics and Chemistry concepts.
- **Automated Quiz Engine**: AI-generated mock exams based on the specific textbook data stored in the Qdrant vector store.
- **Collaborative Terminals**: Shared "Study Rooms" where multiple students can interact with the same tutor in real-time.

---

## 🛡️ License
Copyright © 2026 Sandesh Shrivastava. All rights reserved.
