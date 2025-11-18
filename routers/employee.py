from fastapi import APIRouter, Depends
from typing import List


from models.employee_models import (
    EmployeeSchema,
)

from models.relation_models import EmployeeRelSchema

from database.queries.employee_queries import (
    get_employees,
    get_employee,
    create_employees,
    delete_employees,
    update_employee,
)


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeSchema])
async def get_employees_handle(
    employees: List[EmployeeSchema] = Depends(get_employees),
) -> List[EmployeeSchema]:
    return employees


@router.get("/{employee_id}", response_model=EmployeeRelSchema)
async def get_employee_handle(
    employee: EmployeeRelSchema = Depends(get_employee),
) -> EmployeeRelSchema:
    return employee


@router.post("/", response_model=List[EmployeeSchema])
async def create_employees_handle(
    new_employees: List[EmployeeSchema] = Depends(create_employees),
) -> List[EmployeeSchema]:
    return new_employees


@router.delete("/", response_model=List[EmployeeSchema])
async def delete_employees_handle(
    deleted_employees: List[EmployeeSchema] = Depends(delete_employees),
) -> List[EmployeeSchema]:
    return deleted_employees


@router.put("/{employee_id}", response_model=EmployeeSchema)
async def replace_employee_handle(
    updated_employee: EmployeeSchema = Depends(update_employee),
) -> EmployeeSchema:
    return updated_employee


@router.patch("/{employee_id}", response_model=EmployeeSchema)
async def update_employee_handle(
    updated_employee: EmployeeSchema = Depends(update_employee),
) -> EmployeeSchema:
    return updated_employee
