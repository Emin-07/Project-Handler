from pydantic import BaseModel, Field
from typing import Optional


class NoteBase(BaseModel):
    note_info: str = Field(..., description="Note text")
    employee_id: int = Field(
        ..., description="The ID of the employee who wrote this note"
    )
    task_id: int = Field(..., description="The ID of the task this note belongs to.")

    class Config:
        from_attributes = True


class NoteSchema(NoteBase):
    id: int = Field(..., description="Note unique identifier")


class UpdateNoteSchema(BaseModel):
    note_info: Optional[str] = None
    employee_id: Optional[int] = None
    task_id: Optional[int] = None
