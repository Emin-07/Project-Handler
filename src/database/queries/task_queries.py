from . import *


async def get_tasks(
    get_employees_commons: PaginationDep_get,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[TaskSchema]:
    e = aliased(Task)
    res = await session.scalars(
        select(e)
        .where(e.id >= get_employees_commons.skip)
        .limit(get_employees_commons.limit)
        .order_by(e.id)
    )
    tasks = res.all()
    tasks_validated = [TaskSchema.model_validate(task) for task in tasks]
    for task_validated in tasks_validated:
        print(task_validated)
    return tasks_validated


async def get_task(
    task_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> TaskRelSchema:
    task = await session.get(
        Task,
        task_id,
        options=[
            selectinload(Task.task_employees),
            selectinload(Task.task_notes),
            joinedload(Task.task_project),
        ],
    )
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"There's no task with id {task_id}",
        )
    res = TaskRelSchema.model_validate(task)
    print(res)
    return res


async def delete_tasks(
    tasks_id: List[int] | int, session: Annotated[AsyncSession, Depends(get_session)]
) -> List[TaskSchema]:
    if isinstance(tasks_id, int):
        tasks_id = [tasks_id]
    deleted_tasks: List[TaskSchema] = []
    for task_id in tasks_id:
        task = await session.get(Task, task_id)
        if task is not None:
            deleted_task = TaskSchema.model_validate(task)
            await session.delete(task)
            await session.commit()
            deleted_tasks.append(deleted_task)
        else:
            raise HTTPException(
                status_code=404, detail=f"Task with id:{task_id} not found!"
            )
    return deleted_tasks


async def create_tasks(
    new_tasks: List[TaskBase], session: Annotated[AsyncSession, Depends(get_session)]
) -> List[TaskSchema]:
    mapped_tasks: List[Task] = [
        Task(
            task_description=task.task_description,
            start_date=task.start_date,
            end_date=task.end_date,
            priority=task.priority.name,
            project_id=task.project_id,
        )
        for task in new_tasks
    ]
    session.add_all(mapped_tasks)
    await session.commit()

    for task in mapped_tasks:
        await session.refresh(task)

    tasks_validated = [TaskSchema.model_validate(task) for task in mapped_tasks]
    return tasks_validated


async def update_task(
    update_id: int,
    update_data: UpdateEmployeeSchema,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskSchema:
    prev_task = await session.get(Task, update_id)
    if prev_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id:{update_id} not found",
        )

    if request.method == "PATCH":
        update_dict = update_data.model_dump(exclude_unset=True)
    else:
        update_dict = update_data.model_dump()

    for key, val in update_dict.items():
        if key != "priority":
            setattr(prev_task, key, val)
        else:
            prev_task.priority = update_data.priority.name
    await session.commit()
    await session.refresh(prev_task)

    task_validated = TaskSchema.model_validate(prev_task)
    print(task_validated)
    return task_validated


# async def main():
#     # await create_tables()
#     # await insert_data()
#     # await create_task(
#     #     TaskBase(
#     #         task_description="do something important",
#     #         start_date="2000-01-01",
#     #         end_date="3000-01-01",
#     #         priority=Priority.high_priority,
#     #         project_id=8,
#     #     )
#     # )
#     # await get_tasks(31)
#     await update_task(31, UpdateTaskSchema(priority=3, project_id=4), partial=True)


# asyncio.run(main())
