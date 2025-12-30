from typing import Annotated, Any, Dict, List

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import Integer, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from core.models import Employee, Project, Task
from relation.schemas.relations import ProjectRelSchema

from ..schemas.project import ProjectBase, ProjectSchema, UpdateProjectSchema
from . import PaginationDep_get, get_session


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
    validated_projects = [
        ProjectSchema.model_validate(project.__dict__) for project in projects
    ]
    return validated_projects


async def get_project(
    project_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> ProjectRelSchema:
    project = await session.get(
        Project, project_id, options=[selectinload(Project.project_tasks)]
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There's no project with id {project_id}",
        )
    res = ProjectRelSchema.model_validate(project.__dict__)
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
            deleted_project = ProjectSchema.model_validate(project.__dict__)
            await session.delete(project)
            await session.commit()
            deleted_projects.append(deleted_project)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id:{project_id} not found!",
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
        ProjectSchema.model_validate(project.__dict__) for project in mapped_projects
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
            status_code=status.HTTP_404_NOT_FOUND,
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

    project_validated = ProjectSchema.model_validate(prev_project.__dict__)
    return project_validated


async def project_avg_salary(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> List[Dict[str, Any]]:
    project_avg_salary_cte = (
        select(
            Task.project_id,
            func.avg(Employee.salary).cast(Integer).label("project_avg_salary"),
        )
        .group_by(Task.project_id)
        .cte("project_avg_salary")
    )
    query = select(
        Project.id,
        Project.project_name,
        project_avg_salary_cte.c.project_avg_salary,
    ).join(
        project_avg_salary_cte,
        Project.id == project_avg_salary_cte.c.project_id,
    )
    res = await session.execute(query)
    result = []
    for row in res:
        result.append(row._asdict())
    return result


# async def main():
#     # await create_tables()
#     # await insert_data()
#     await get_projects(8)
#     # await update_project(9, UpdateProjectSchema(is_completed=True), partial=True)


# asyncio.run(main())
