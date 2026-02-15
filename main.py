from typing import Dict

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from auth.routes.jwt_auth import router as jwt_auth_router
from employee.routes.employee import router as employee_router
from note.routes.note import router as note_router
from project.routes.project import router as project_router
from relation.schemas import UnexpectedFileFormatExcpetion
from relation.services.data_helper import get_global_data, reset_data
from task.routes.task import router as task_router

app = FastAPI()

app.include_router(note_router)
app.include_router(employee_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(jwt_auth_router)


def data_is_valid(data: dict) -> bool:
    if (
        isinstance(data, dict)
        and isinstance(next(iter(data)), str)
        and isinstance(data.get(next(iter(data))), list)
    ):
        return True
    return False


@app.get("/", response_model=dict[str, str])
async def read_root() -> dict[str, str]:
    return {"message": "Hello world"}


@app.patch("/", response_model=Dict[str, str])
async def reset_data_to_default(
    data: Dict = Depends(reset_data),
) -> Dict[str, str]:
    if data_is_valid(data):
        return {"message": "Data resetted successfully"}
    return {"message": "Something went wrong!"}


@app.put("/", response_model=Dict[str, str])
async def upload_data_from_user(data=Depends(get_global_data)) -> Dict[str, str]:
    if data_is_valid(data):
        return {"message": "Data from user uploaded successfully"}
    return {"message": "Something went wrong!"}


@app.exception_handler(UnexpectedFileFormatExcpetion)
async def fileformat_exception_handler(
    req: Request, exc: UnexpectedFileFormatExcpetion
):
    user_host = req.client.host  # type: ignore
    return JSONResponse(
        status_code=415,
        content={
            "message": f"Unexpected file format ({exc.filetype}) passed at {user_host}, file should be with extension .json"
        },
    )


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
