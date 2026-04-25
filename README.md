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

## 🚀 Deployment Status: Cloud-Native
This project is fully configured for a **Production Environment**.

- **Vector Database**: Hosted on **Qdrant Cloud** (AWS London).
- **Relational Database**: Hosted on **Aiven for MySQL**.
- **LLM Inferences**: Powered by **LLaMA 3.3** via Groq.
- **Frontend**: Ready for **Streamlit Cloud**.

### 🛠️ Production Setup
1.  **Environment Secrets**: Ensure `.env` (or Streamlit Secrets) contains:
    *   `GROQ_API_KEY`
    *   `QDRANT_URL` (Cloud Endpoint)
    *   `QDRANT_API_KEY`
    *   `MYSQL_URL` (Aiven Connection String)
2.  **Database Migration**: Run `database/schema.sql` on the cloud DB.
3.  **Data Ingestion**: Run `python ingestion/ingest.py --bulk-dir ingestion/docs/` to sync the vector store.

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
