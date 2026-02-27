# Exercise 3: Refactored with Pydantic schemas and proper error handling (AI-generated)
# Exercise 4: Added /extract-llm endpoint for LLM-powered extraction (AI-generated)
from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemDetail,
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    """Extract action items from text using heuristic rules."""
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text.strip())

    items = extract_action_items(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


# Exercise 4: LLM-powered extraction endpoint (AI-generated)
@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    """Extract action items from text using an LLM via Ollama."""
    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text.strip())

    try:
        items = extract_action_items_llm(payload.text)
    except Exception as e:
        logger.error("LLM extraction failed: %s", e)
        raise HTTPException(status_code=502, detail=f"LLM extraction failed: {e}")

    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemDetail])
def list_all(note_id: Optional[int] = None) -> list[ActionItemDetail]:
    """List all action items, optionally filtered by note_id."""
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemDetail(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    """Mark an action item as done or not done."""
    db.mark_action_item_done(action_item_id, payload.done)
    return MarkDoneResponse(id=action_item_id, done=payload.done)
