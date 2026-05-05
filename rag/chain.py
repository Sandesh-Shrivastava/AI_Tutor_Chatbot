"""
chain.py — LangChain ConversationalRetrievalChain wiring.

Build a chain given:
    - subject (for Qdrant filtering)
    - level   (beginner / intermediate / advanced)
    - mode    (normal / socratic)

Returns a callable chain that accepts {"question": str} and returns {"answer": str}.
"""

from __future__ import annotations
import sys
import os

# Robust path injection for Streamlit Cloud
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, LLM_MODEL
from prompts import get_prompt_template
from rag.memory import build_memory
from rag.retriever import build_retriever

# Graceful fallback response when no relevant context is found
_NO_CONTEXT_MSG = (
    "I couldn't find relevant material for your question in the current subject. "
    "Could you try rephrasing, or select a different subject?"
)


def build_chain(
    subject: str | None = None,
    level: str = "beginner",
    mode: str = "normal",
    memory=None,
):
    """
    Build and return a ConversationalRetrievalChain.

    Args:
        subject:  Subject to filter Qdrant results by (e.g. "Physics").
        level:    Student level → controls which prompt template is used.
        mode:     "normal" | "socratic"
        memory:   Existing ConversationBufferMemory (pass None to create fresh).

    Returns:
        (chain, memory) tuple. Memory is returned so the Streamlit app can
        persist it across reruns.
    """
    if not GROQ_API_KEY:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to your .env file."
        )

    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.3,
    )

    retriever = build_retriever(subject=subject, k=4)
    mem = memory or build_memory()
    prompt = get_prompt_template(level=level, mode=mode)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=mem,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        verbose=False,
    )

    return chain, mem


def ask(chain, question: str) -> tuple[str, list]:
    """
    Run a question through the chain.

    Returns:
        (answer_text, source_documents)
    """
    try:
        result = chain.invoke({"question": question})
        answer = result.get("answer", "").strip()
        sources = result.get("source_documents", [])

        # Graceful fallback
        if not answer or answer.lower() in {"", "i don't know", "i do not know"}:
            return _NO_CONTEXT_MSG, []

        return answer, sources
    except Exception as e:
        err_msg = str(e).lower()
        if "connection refused" in err_msg or "connectionerror" in err_msg:
            return (
                "❌ **Database Connection Error**: I couldn't connect to the Qdrant vector database. "
                "Please ensure your `QDRANT_URL` and `QDRANT_API_KEY` are correctly set in the `.env` file "
                "and that the service is running.",
                [],
            )
        return f"⚠️ **An error occurred**: {str(e)}", []
