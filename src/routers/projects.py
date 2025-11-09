from fastapi import APIRouter, Depends
from typing import List, Dict, Any, Annotated

from models.project_models import (
    ProjectSchema,
)

from models.relation_models import ProjectRelSchema


from database.queries.project_queries import (
    get_projects,
    get_project,
    create_projects,
    delete_projects,
    update_project,
    project_avg_salary,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectSchema])
async def get_projects_handle(
    projects: List[ProjectSchema] = Depends(get_projects),
) -> List[ProjectSchema]:
    return projects


@router.get("/avg_salary", response_model=List[Dict[str, Any]])
async def get_projects_avg_salary(
    data: Annotated[List, Depends(project_avg_salary)],
) -> List[Dict[str, Any]]:
    return data


@router.get("/{project_id}", response_model=ProjectRelSchema)
async def get_project_handle(
    project: Annotated[ProjectRelSchema, Depends(get_project)],
) -> ProjectRelSchema:
    return project


@router.post("/", response_model=List[ProjectSchema])
async def create_projects_handle(
    new_projects: Annotated[List[ProjectSchema], Depends(create_projects)],
) -> List[ProjectSchema]:
    return new_projects


@router.delete("/", response_model=List[ProjectSchema])
async def delete_projects_handle(
    deleted_projects: Annotated[List[ProjectSchema], Depends(delete_projects)],
) -> List[ProjectSchema]:
    return deleted_projects


@router.put("/{project_id}", response_model=ProjectSchema)
async def replace_project_handle(
    updated_project: Annotated[ProjectSchema, Depends(update_project)],
) -> ProjectSchema:
    return updated_project


@router.patch("/{project_id}", response_model=ProjectSchema)
async def update_project_handle(
    updated_project: Annotated[ProjectSchema, Depends(update_project)],
) -> ProjectSchema:
    return updated_project
