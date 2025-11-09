from . import *


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
        EmployeeSchema.model_validate(employee) for employee in employees
    ]
    for employee in validated_employees:
        print(employee)
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
            status_code=418,
            detail=f"Sry you're a teapot, there's no user with id {employee_id}",
        )
    res = EmployeeRelSchema.model_validate(employee)
    print(res)
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
            deleted_employee = EmployeeSchema.model_validate(employee)
            await session.delete(employee)
            await session.commit()
            deleted_employees.append(deleted_employee)
        else:
            raise HTTPException(
                status_code=404, detail=f"Employee with id:{employee_id} not found!"
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
        EmployeeSchema.model_validate(employee) for employee in mapped_employees
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
            status_code=404,
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

    employee_validated = EmployeeSchema.model_validate(prev_employee)
    print(employee_validated)
    return employee_validated


# async def main():
#     # await create_tables()
#     # await insert_data()
#     # await create_employee("Patrick", "Bateman", 1_000_000, 1)
#     # await update_employee(84, salary=999_999)
#     await project_avg_salary()


# asyncio.run(main())
