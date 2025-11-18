from fastapi import APIRouter, Depends
from typing import List

from models.task_models import TaskSchema
from models.relation_models import TaskRelSchema

from database.queries.task_queries import (
    get_tasks,
    get_task,
    create_tasks,
    delete_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskSchema])
async def get_tasks_handle(
    tasks: List[TaskSchema] = Depends(get_tasks),
) -> List[TaskSchema]:
    return tasks


@router.get("/{task_id}", response_model=TaskRelSchema)
async def get_task_handle(task: TaskRelSchema = Depends(get_task)) -> TaskRelSchema:
    return task


@router.post("/", response_model=List[TaskSchema])
async def create_tasks_handle(
    new_task: List[TaskSchema] = Depends(create_tasks),
) -> List[TaskSchema]:
    return new_task


@router.delete("/", response_model=List[TaskSchema])
async def delete_tasks_handle(
    deleted_task: List[TaskSchema] = Depends(delete_tasks),
) -> List[TaskSchema]:
    return deleted_task


@router.put("/{task_id}", response_model=TaskSchema)
async def replace_task_handle(
    updated_task: TaskSchema = Depends(update_task),
) -> TaskSchema:
    return updated_task


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task_handle(
    updated_task: TaskSchema = Depends(update_task),
) -> TaskSchema:
    return updated_task
