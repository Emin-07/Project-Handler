from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

from core.setup import async_session_factory


async def get_session():
    async with async_session_factory() as session:
        yield session


class PaginationParamsGetMany(BaseModel):
    skip: int = Field(default=0, ge=0, description="Amount of rows you wanna skip")
    limit: int = Field(
        default=3, ge=0, le=100, description="Amount of rows you wanna get"
    )


PaginationDep_get = Annotated[PaginationParamsGetMany, Depends()]
