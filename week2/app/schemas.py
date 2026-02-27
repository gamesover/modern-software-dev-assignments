# Exercise 3: Pydantic request/response schemas for well-defined API contracts (AI-generated)
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# --- Request schemas ---

class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, description="The note text")


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = False


class MarkDoneRequest(BaseModel):
    done: bool = True


# --- Response schemas ---

class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemResponse(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int] = None
    items: list[ActionItemResponse]


class ActionItemDetail(BaseModel):
    id: int
    note_id: Optional[int] = None
    text: str
    done: bool
    created_at: str


class MarkDoneResponse(BaseModel):
    id: int
    done: bool
