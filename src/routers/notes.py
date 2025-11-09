from fastapi import APIRouter, Depends
from typing import List

from models.note_models import NoteSchema

from models.relation_models import NoteRelSchema


from database.queries.note_queries import (
    get_notes,
    get_note,
    create_notes,
    delete_notes,
    update_note,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=List[NoteSchema])
async def get_notes_handle(
    notes: List[NoteSchema] = Depends(get_notes),
) -> List[NoteSchema]:
    return notes


@router.get("/{note_id}", response_model=NoteRelSchema)
async def get_note_handle(
    note: NoteRelSchema = Depends(get_note),
) -> NoteRelSchema:
    return note


@router.post("/", response_model=List[NoteSchema])
async def create_notes_handle(
    new_notes: List[NoteSchema] = Depends(create_notes),
) -> List[NoteSchema]:
    return new_notes


@router.delete("/", response_model=List[NoteSchema])
async def delete_notes_handle(
    deleted_notes: List[NoteSchema] = Depends(delete_notes),
) -> List[NoteSchema]:
    return deleted_notes


@router.put("/{note_id}", response_model=NoteSchema)
async def replace_notes_handle(
    updated_note: NoteSchema = Depends(update_note),
) -> NoteSchema:
    return updated_note


@router.patch("/{note_id}", response_model=NoteSchema)
async def update_note_handle(
    updated_note: NoteSchema = Depends(update_note),
) -> NoteSchema:
    return updated_note
