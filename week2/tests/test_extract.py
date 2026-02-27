# Exercise 2: Unit tests for extract_action_items and extract_action_items_llm (AI-generated)
import json
from unittest.mock import MagicMock, patch

import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


# --- Heuristic extractor tests (existing) ---

def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# --- LLM extractor tests (AI-generated) ---

def _mock_ollama_response(items: list[str]) -> MagicMock:
    """Build a fake ollama chat() response returning the given items."""
    msg = MagicMock()
    msg.content = json.dumps({"items": items})
    resp = MagicMock()
    resp.message = msg
    return resp


@patch("week2.app.services.extract.chat")
def test_llm_extract_bullet_list(mock_chat):
    """LLM correctly extracts items from bullet-style notes."""
    mock_chat.return_value = _mock_ollama_response(
        ["Set up database", "Write unit tests"]
    )
    result = extract_action_items_llm("- Set up database\n- Write unit tests")
    assert result == ["Set up database", "Write unit tests"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_llm_extract_keyword_prefixed(mock_chat):
    """LLM handles keyword-prefixed lines like 'TODO:' or 'ACTION:'."""
    mock_chat.return_value = _mock_ollama_response(
        ["Fix login bug", "Deploy to staging"]
    )
    result = extract_action_items_llm("TODO: Fix login bug\nACTION: Deploy to staging")
    assert "Fix login bug" in result
    assert "Deploy to staging" in result


@patch("week2.app.services.extract.chat")
def test_llm_extract_empty_input(mock_chat):
    """Empty or whitespace-only input returns an empty list without calling the LLM."""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    mock_chat.assert_not_called()


@patch("week2.app.services.extract.chat")
def test_llm_extract_no_action_items(mock_chat):
    """When the LLM finds no action items it returns an empty list."""
    mock_chat.return_value = _mock_ollama_response([])
    result = extract_action_items_llm("Just a casual note with no tasks.")
    assert result == []


@patch("week2.app.services.extract.chat")
def test_llm_extract_prose_paragraph(mock_chat):
    """LLM can pull tasks out of a prose paragraph."""
    mock_chat.return_value = _mock_ollama_response(
        ["Schedule design review", "Update Jira board"]
    )
    result = extract_action_items_llm(
        "We discussed the roadmap. We need to schedule a design review "
        "and update the Jira board before Friday."
    )
    assert len(result) == 2
