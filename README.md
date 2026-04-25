# 🎓 AI Tutor Chatbot

> Subject-aware RAG chatbot for personalized tutoring — Python · LangChain · LLaMA 3.3 · Qdrant · MySQL · Streamlit

---

## ✨ Features

- **Multi-level explanations** — Beginner / Intermediate / Advanced prompt modes
- **Socratic mode** — Bot asks guiding questions instead of giving direct answers
- **RAG pipeline** — Retrieves relevant textbook content from Qdrant before answering
- **Multi-turn memory** — Conversations maintain context across turns
- **Session & progress tracking** — Every query logged to MySQL; weak topics surfaced in dashboard
- **Subject selector** — Supports Physics, Maths, Chemistry, Python Programming, and more

---

## 🗂️ Project Structure

```
ai-tutor-chatbot/
├── ingestion/          # Phase 1: PDF → Qdrant pipeline
├── database/           # Phase 2: MySQL schema + ORM + loggers
├── rag/                # Phase 3: LangChain RAG chain
├── prompts/            # Phase 4: Prompt templates (4 modes)
├── app/                # Phase 5: Streamlit UI + dashboard
├── config.py           # Centralized config
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup

### 1. Clone & install dependencies
```bash
git clone <repo-url>
cd ai-tutor-chatbot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in GROQ_API_KEY, QDRANT_URL, MYSQL_URL
```

Get a **free** Groq API key at: https://console.groq.com

### 3. Start Qdrant (Docker)
```bash
docker run -d -p 6333:6333 qdrant/qdrant
# Or use the free cloud tier: https://cloud.qdrant.io
```

### 4. Set up MySQL
```bash
mysql -u root -p < database/schema.sql
```

### 5. Ingest documents
```bash
# Single file
python ingestion/ingest.py --subject Physics --chapter Kinematics --file ingestion/docs/ncert_11.pdf

# Bulk (folder structure: docs/<Subject>/<Chapter>/<file>.pdf)
python ingestion/ingest.py --bulk-dir ingestion/docs/
```

### 6. Run the app
```bash
streamlit run app/main.py
```

---

## 🏗️ Tech Stack

| Component | Technology |
|---|---|
| LLM | LLaMA 3.3 (70B) via Groq API |
| Orchestration | LangChain |
| Vector Store | Qdrant |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Database | MySQL + SQLAlchemy |
| Frontend | Streamlit |
| PDF Parsing | PyPDF2 |
| Analytics | Pandas + Matplotlib |

---

## 📁 Document Folder Structure (for bulk ingestion)

```
ingestion/docs/
├── Physics/
│   ├── Kinematics/
│   │   └── ncert_11_ch3.pdf
│   └── Laws_of_Motion/
│       └── ncert_11_ch5.pdf
├── Mathematics/
│   └── Calculus/
│       └── notes.pdf
└── Python_Programming/
    └── OOP/
        └── oop_notes.txt
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLaMA 3.3 inference |
| `QDRANT_URL` | Qdrant server URL (default: `http://localhost:6333`) |
| `QDRANT_API_KEY` | Qdrant API key (leave blank for local) |
| `QDRANT_COLLECTION` | Collection name (default: `ai_tutor_docs`) |
| `MYSQL_URL` | SQLAlchemy MySQL connection string |
