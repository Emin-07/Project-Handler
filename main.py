from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
import uvicorn
from typing import Dict
from src.database.queries.data_helper import get_global_data, reset_data
from src.api.v1.schemas import UnexpectedFileFormatExcpetion
from src.api.v1_group import router

app = FastAPI()

app.include_router(router)


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
