from . import *


async def get_projects(
    get_employees_commons: PaginationDep_get,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[ProjectSchema]:
    e = aliased(Project)
    res = await session.scalars(
        select(e)
        .where(e.id >= get_employees_commons.skip)
        .limit(get_employees_commons.limit)
        .order_by(e.id)
    )
    projects = res.all()
    validated_projects = [ProjectSchema.model_validate(project) for project in projects]
    for project in validated_projects:
        print(project)
    return validated_projects


async def get_project(
    project_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> ProjectRelSchema:
    project = await session.get(
        Project, project_id, options=[selectinload(Project.project_tasks)]
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=f"There's no project with id {project_id}",
        )
    res = ProjectRelSchema.model_validate(project)
    print(res)
    return res


async def delete_projects(
    projects_id: List[int] | int, session: Annotated[AsyncSession, Depends(get_session)]
) -> List[ProjectSchema]:
    if isinstance(projects_id, int):
        projects_id = [projects_id]
    deleted_projects: List[ProjectSchema] = []
    for project_id in projects_id:
        project = await session.get(Project, project_id)
        if project is not None:
            deleted_project = ProjectSchema.model_validate(project)
            await session.delete(project)
            await session.commit()
            deleted_projects.append(deleted_project)
        else:
            raise HTTPException(
                status_code=404, detail=f"Project with id:{project_id} not found!"
            )
    return deleted_projects


async def create_projects(
    projects: List[ProjectBase], session: Annotated[AsyncSession, Depends(get_session)]
) -> List[ProjectSchema]:
    mapped_projects: List[Project] = [
        Project(
            project_name=project.project_name.strip(),
            start_date=project.start_date,
            end_date=project.end_date,
            is_completed=project.is_completed,
        )
        for project in projects
    ]
    session.add_all(mapped_projects)
    await session.commit()

    for project in mapped_projects:
        await session.refresh(project)

    projects_validated = [
        ProjectSchema.model_validate(project) for project in mapped_projects
    ]

    return projects_validated


async def update_project(
    update_id: int,
    update_data: UpdateProjectSchema,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProjectSchema:
    prev_project = await session.get(Project, update_id)
    if prev_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project with id:{update_id} not found",
        )
    if request.method == "PATCH":
        update_dict = update_data.model_dump(exclude_unset=True)
    else:
        update_dict = update_data.model_dump()

    for key, val in update_dict.items():
        setattr(prev_project, key, val)

    await session.commit()
    await session.refresh(prev_project)

    project_validated = ProjectSchema.model_validate(prev_project)
    print(project_validated)
    return project_validated


async def project_avg_salary(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[Dict[str, Any]]:
    t = aliased(Task)
    p = aliased(Project)
    subquery = (
        select(
            t.project_id.label("project_id"),
            func.avg(Employee.salary).cast(Integer).label("project_avg_salary"),
        )
        .join(t.task_employees)
        .group_by(t.project_id)
        .order_by(t.project_id)
        .subquery()
    )

    query = select(p.id, p.project_name, subquery.c.project_avg_salary).join(
        p, p.id == subquery.c.project_id
    )

    res = await session.execute(query)
    result = []
    for row in res:
        print(row._asdict())
        result.append(row._asdict())
    return result


# async def main():
#     # await create_tables()
#     # await insert_data()
#     await get_projects(8)
#     # await update_project(9, UpdateProjectSchema(is_completed=True), partial=True)


# asyncio.run(main())
