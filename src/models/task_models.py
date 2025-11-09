from pydantic import BaseModel, Field
from typing import Optional
from . import DateString, Priority


class TaskBase(BaseModel):
    task_description: str = Field(..., description="Information about task")
    start_date: DateString = Field(
        default="2000-01-01", description="Date when task started"
    )
    end_date: DateString = Field(
        default="2000-01-01", description="Date when task ended or will end"
    )
    priority: Priority = Field(
        default=Priority.low_priority, description="Task priority"
    )
    project_id: int = Field(..., description="Project id that this task belongs to")

    class Config:
        from_attributes = True


class TaskSchema(TaskBase):
    id: int = Field(..., description="Task unique identifier")


class TaskEmployeeSchema(BaseModel):
    task_id: int = Field(..., gt=0, description="ID of the task that employee works on")
    employee_id: int = Field(
        ..., gt=0, description="ID of the employee that works on the task"
    )


class UpdateTaskSchema(BaseModel):
    task_description: Optional[str] = None
    start_date: Optional[DateString] = None
    end_date: Optional[DateString] = None
    priority: Optional[Priority] = None
    project_id: Optional[int] = None
