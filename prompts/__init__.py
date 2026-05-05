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
from prompts.normal import NORMAL_TEMPLATE


_LEVEL_TEMPLATES: dict[str, PromptTemplate] = {
    "beginner": BEGINNER_TEMPLATE,
    "intermediate": INTERMEDIATE_TEMPLATE,
    "advanced": ADVANCED_TEMPLATE,
}


def get_prompt_template(level: str = "beginner", mode: str = "normal", subject: str = "General") -> PromptTemplate:
    """
    Return the appropriate PromptTemplate based on student level and mode.
    """
    if mode == "socratic":
        template = SOCRATIC_TEMPLATE
    elif mode == "normal":
        template = NORMAL_TEMPLATE
    else:
        template = _LEVEL_TEMPLATES.get(level, BEGINNER_TEMPLATE)
    
    # Inject the specific subject so the AI can enforce subject isolation
    return template.partial(subject=subject.replace("_", " "))
