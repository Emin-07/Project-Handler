from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from src.routers import employee, notes, projects, tasks
import uvicorn
from typing import List, Dict
from src.database.queries.data_handler import get_global_data, reset_data
from src.schemas import UnexpectedFileFormatExcpetion

app = FastAPI()

app.include_router(employee.router)
app.include_router(projects.router)
app.include_router(notes.router)
app.include_router(tasks.router)


@app.get("/", response_model=dict[str, str])
async def read_root() -> dict[str, str]:
    return {"message": "Hello world"}


@app.patch("/", response_model=Dict)
async def reset_data_to_default(
    data_resetter: Dict = Depends(reset_data),
) -> Dict:
    return data_resetter


@app.put("/", response_model=Dict[str, List])
async def upload_data_from_user(data=Depends(get_global_data)) -> Dict[str, List]:
    return data


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


# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)
