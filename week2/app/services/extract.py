from __future__ import annotations

import json
import os
import re
from typing import Any, List

from dotenv import load_dotenv
from ollama import chat
from pydantic import BaseModel

load_dotenv()

# --- LLM model configuration ---
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# --- Exercise 1: LLM-powered extraction via Ollama (AI-generated) ---

class ActionItems(BaseModel):
    """Pydantic model for structured LLM output."""
    items: List[str]


def extract_action_items_llm(text: str) -> List[str]:
    """Extract action items from free-form text using an LLM via Ollama.

    Sends the text to a local Ollama model and asks it to return a JSON list
    of concise, actionable items.  Falls back to an empty list on error.
    """
    if not text or not text.strip():
        return []

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that extracts action items from notes. "
                    "Return ONLY the action items as a JSON object with an 'items' key "
                    "containing an array of short, actionable strings. "
                    "If there are no action items, return {\"items\": []}."
                ),
            },
            {"role": "user", "content": text},
        ],
        format=ActionItems.model_json_schema(),
    )

    parsed = ActionItems.model_validate_json(response.message.content)
    return parsed.items
