from pydantic import BaseModel, Field
from typing import Optional


class EmployeeBase(BaseModel):
    first_name: str = Field(..., description="Employee's first name")
    last_name: str = Field(..., description="Employee's last name")

    salary: int = Field(..., description="Employee's salary")
    is_working: bool = Field(
        default=True, description="Status of Employee if he's working"
    )

    class Config:
        from_attributes = True


class EmployeeSchema(EmployeeBase):
    id: int = Field(..., description="Employee unique identifier")


class UpdateEmployeeSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    salary: Optional[int] = None
    is_working: Optional[bool] = None
