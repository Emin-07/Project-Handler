import json
import aiofiles
<<<<<<< HEAD:src/database/queries/data_handler.py
from src.models import UnexpectedFileFormatExcpetion
from sqlalchemy.orm import Session
=======
from models import UnexpectedFileFormatExcpetion
>>>>>>> parent of 492047d (Docker с Docker-composeбыли добавлены + небольшие изменения):database/queries/data_handler.py
from . import *

default_data_path = "test_data.json"
user_data_path = "user_data.json"

active_data = None
active_path = None


async def recreate_tables() -> None:
    # Dropping and then creating tables

    # async_engine.echo = False
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # async_engine.echo = True


async def add_data_into_db(data: Dict[str, List], session: AsyncSession) -> None:
    # async_engine.echo = False
    session.add_all(
        [
            Project(**ProjectBase(**project).model_dump())
            for project in data.get("projects", [])
        ]
    )
    session.add_all(
        [Task(**TaskBase(**task).model_dump()) for task in data.get("tasks", [])]
    )
    session.add_all(
        [
            Employee(**EmployeeBase(**employee).model_dump())
            for employee in data.get("employees", [])
        ]
    )
    await session.flush()
    session.add_all(
        [Note(**NoteBase(**note).model_dump()) for note in data.get("notes", [])]
    )
    session.add_all(
        [
            TaskEmployees(**TaskEmployeeSchema(**tasks_employee).model_dump())
            for tasks_employee in data.get("tasks_employees", [])
        ]
    )
    await session.commit()
    # async_engine.echo = True


async def get_global_data(
    session: Annotated[AsyncSession, Depends(get_session)],
    file: UploadFile | str | None = "",
) -> Dict[str, List]:
    global active_data
    global active_path

    if file is not None and not isinstance(file, str):
        user_file_extension: str = file.filename[file.filename.index(".") :]  # type: ignore
        if user_file_extension == ".json":
            content = await file.read()
            active_path = user_data_path
            async with aiofiles.open(active_path, "w") as f:
                active_data = json.loads(content)
                await f.write(json.dumps(active_data))
                await recreate_tables()
                await add_data_into_db(active_data, session)
            return active_data
        else:
            raise UnexpectedFileFormatExcpetion(user_file_extension)
    else:
        try:
            active_path = default_data_path
            async with aiofiles.open(active_path) as f:
                content = await f.read()
                active_data = json.loads(content)
                return active_data
        except FileNotFoundError:
            print("File not found: ", active_path)
            return {}


async def get_data():
    global active_data
    global active_path

    if active_data is None:
        try:
            active_path = default_data_path
            async with aiofiles.open(active_path) as f:
                data = await f.read()
                active_data = json.loads(data)
        except FileNotFoundError:
            print("File was not found", active_path)
    return active_data


async def reset_data(session: Annotated[AsyncSession, Depends(get_session)]) -> Dict:
    global active_data
    global active_path

    await recreate_tables()
    # Inserting Data in Json file
    active_path = default_data_path
    async with aiofiles.open(default_data_path) as f:
        content = await f.read()
        active_data = json.loads(content)
        await add_data_into_db(active_data, session)

    return active_data

    # return {"message": "Data resetted to default successfully", "data": active_data}
