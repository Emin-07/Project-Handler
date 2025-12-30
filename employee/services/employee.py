from typing import Annotated, List

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from auth.utils.utils import hash_password
from core.models import Employee, UserPassword
from relation.schemas.relations import (
    EmployeeRelSchema,
)

from ..schemas.employee import (
    EmployeeBase,
    EmployeeSchema,
    UpdateEmployeeSchema,
)
from . import PaginationDep_get, get_session


async def get_all_users(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[EmployeeSchema]:
    e = aliased(Employee)

    res = await session.scalars(select(e).order_by(e.id))
    employees = res.all()
    validated_employees = [
        EmployeeSchema.model_validate(employee.__dict__) for employee in employees
    ]
    return validated_employees


async def sign_in_by_id(
    user_id: int,
    password: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    employee = await session.get(Employee, user_id)
    res = await session.scalars(select(UserPassword.user_id))
    logged_ids = res.all()
    if employee is None or user_id in logged_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {user_id} not found, {logged_ids}, {employee}",
        )
    hashed_pwd = hash_password(password)
    hexed_and_hashed_pwd = hashed_pwd.hex()
    session.add(UserPassword(user_id=user_id, hashed_password=hexed_and_hashed_pwd))
    await session.commit()
    return dict({"user": employee, "password": password})


async def get_user_pwd(
    employee_id: int, session: Annotated[AsyncSession, Depends(get_session)]
):
    pwd = await session.scalars(
        select(UserPassword.hashed_password).where(UserPassword.user_id == employee_id)
    )
    res = ""
    for letter in pwd:
        res += letter
    return res


async def get_employees(
    get_employees_commons: PaginationDep_get,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[EmployeeSchema]:
    e = aliased(Employee)

    res = await session.scalars(
        select(e)
        .where(e.id >= get_employees_commons.skip)
        .limit(get_employees_commons.limit)
        .order_by(e.id)
    )
    employees = res.all()
    validated_employees = [
        EmployeeSchema.model_validate(employee.__dict__) for employee in employees
    ]
    return validated_employees


async def get_employee(
    employee_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> EmployeeRelSchema:
    employee = await session.get(
        Employee,
        employee_id,
        options=(
            selectinload(Employee.employee_tasks),
            selectinload(Employee.employee_notes),
        ),
    )
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {employee_id} not found",
        )
    res = EmployeeRelSchema.model_validate(employee.__dict__)
    return res


async def delete_employees(
    employees_id: List[int] | int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[EmployeeSchema]:
    if isinstance(employees_id, int):
        employees_id = [employees_id]
    deleted_employees: List[EmployeeSchema] = []
    for employee_id in employees_id:
        employee = await session.get(Employee, employee_id)
        if employee is not None:
            deleted_employee = EmployeeSchema.model_validate(employee.__dict__)
            await session.delete(employee)
            await session.commit()
            deleted_employees.append(deleted_employee)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id:{employee_id} not found!",
            )
    return deleted_employees


async def create_employees(
    employees: List[EmployeeBase],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[EmployeeSchema]:
    mapped_employees: List[Employee] = [
        Employee(
            first_name=employee.first_name.title().strip(),
            last_name=employee.last_name.title().strip(),
            salary=employee.salary,
            is_working=employee.is_working,
        )
        for employee in employees
    ]

    session.add_all(mapped_employees)

    await session.commit()

    for employee in mapped_employees:
        await session.refresh(employee)

    employees_validated = [
        EmployeeSchema.model_validate(employee.__dict__)
        for employee in mapped_employees
    ]

    return employees_validated


async def update_employee(
    update_id: int,
    update_data: UpdateEmployeeSchema,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EmployeeSchema:
    prev_employee = await session.get(Employee, update_id)
    if prev_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id:{update_id} not found",
        )

    if request.method == "PATCH":
        update_dict = update_data.model_dump(exclude_unset=True)
    else:
        update_dict = update_data.model_dump()

    for key, val in update_dict.items():
        setattr(prev_employee, key, val)

    await session.commit()
    await session.refresh(prev_employee)

    employee_validated = EmployeeSchema.model_validate(prev_employee.__dict__)
    return employee_validated


# async def main():
#     # await create_tables()
#     # await insert_data()
#     # await create_employee("Patrick", "Bateman", 1_000_000, 1)
#     # await update_employee(84, salary=999_999)
#     await project_avg_salary()


# asyncio.run(main())
