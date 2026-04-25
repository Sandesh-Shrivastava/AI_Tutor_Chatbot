"""
memory.py — Shared conversation memory for multi-turn context.
Each session gets its own ConversationBufferMemory instance.
"""

from langchain.memory import ConversationBufferMemory


def build_memory() -> ConversationBufferMemory:
    """
    Create a fresh ConversationBufferMemory.
    - memory_key must match what the chain expects ("chat_history")
    - return_messages=True → passes HumanMessage/AIMessage objects to the prompt
    - output_key → tells memory which chain output key to save
    """
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )
