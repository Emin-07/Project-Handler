from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from . import DateString


class ProjectBase(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    start_date: DateString = Field(
        default="2000-01-01", description="date when project started"
    )
    end_date: DateString = Field(
        default="2000-01-01", description="date when project ended"
    )
    is_completed: bool = Field(default=False, description="status of completion")

    model_config = ConfigDict(from_attributes=True)


class ProjectSchema(ProjectBase):
    id: int = Field(..., description="Project unique identifier")


class UpdateProjectSchema(BaseModel):
    project_name: Optional[str] = None
    start_date: Optional[DateString] = None
    end_date: Optional[DateString] = None
    is_completed: Optional[bool] = None
