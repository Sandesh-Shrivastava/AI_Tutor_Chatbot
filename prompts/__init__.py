"""
prompts/__init__.py — Prompt template registry.
Centralizes selection of the correct template based on level + mode.
"""

from __future__ import annotations

from langchain.prompts import PromptTemplate

from prompts.beginner import BEGINNER_TEMPLATE
from prompts.intermediate import INTERMEDIATE_TEMPLATE
from prompts.advanced import ADVANCED_TEMPLATE
from prompts.socratic import SOCRATIC_TEMPLATE


_LEVEL_TEMPLATES: dict[str, PromptTemplate] = {
    "beginner": BEGINNER_TEMPLATE,
    "intermediate": INTERMEDIATE_TEMPLATE,
    "advanced": ADVANCED_TEMPLATE,
}


def get_prompt_template(level: str = "beginner", mode: str = "normal") -> PromptTemplate:
    """
    Return the appropriate PromptTemplate based on student level and mode.

    Args:
        level: "beginner" | "intermediate" | "advanced"
        mode:  "normal" | "socratic"

    Returns:
        A LangChain PromptTemplate instance.
    """
    if mode == "socratic":
        return SOCRATIC_TEMPLATE

    template = _LEVEL_TEMPLATES.get(level)
    if template is None:
        raise ValueError(
            f"Unknown level '{level}'. Choose from: {list(_LEVEL_TEMPLATES.keys())}"
        )
    return template
