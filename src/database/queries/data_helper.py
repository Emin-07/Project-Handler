# ruff: noqa
import json
import aiofiles
from sqlalchemy.orm import Session

from src.api.v1.schemas import UnexpectedFileFormatExcpetion
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
    if "projects" in data:
        session.add_all([Project(**project) for project in data.get("projects", [])])
        await session.flush()
    if "employees" in data:
        session.add_all(
            [Employee(**employee) for employee in data.get("employees", [])]
        )
        await session.flush()
    if "tasks" in data:
        session.add_all([Task(**task) for task in data.get("tasks", [])])
        await session.flush()
    if "tasks_employees" in data:
        session.add_all(
            [
                TaskEmployees(**tasks_employee)
                for tasks_employee in data.get("tasks_employees", [])
            ]
        )
        await session.flush()
    if "notes" in data:
        session.add_all([Note(**note) for note in data.get("notes", [])])

    if "user_password" in data:
        session.add_all(
            [UserPassword(**user_pwd) for user_pwd in data.get("user_password", [])]
        )

    await session.commit()


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


"""






SYNC versions







"""


def get_data_sync():
    global active_data
    global active_path

    if active_data is None:
        try:
            active_path = default_data_path
            with open(active_path) as f:
                data = f.read()
                active_data = json.loads(data)
        except FileNotFoundError:
            print("File was not found", active_path)
    return active_data


def add_data_into_db_sync(data: Dict[str, List], session: Session) -> None:
    try:
        project_id_mapping = {}
        employee_id_mapping = {}
        task_id_mapping = {}

        # 1. Проекты
        if "projects" in data:
            session.bulk_insert_mappings(Project, data["projects"])  # type: ignore
            session.flush()

            # Получаем созданные ID проектов
            projects = session.query(Project).all()
            project_id_mapping = {i + 1: p.id for i, p in enumerate(projects)}
            # print(f"DEBUG: Project IDs: {[p.id for p in projects]}")

        # 2. Сотрудники
        if "employees" in data:
            session.bulk_insert_mappings(Employee, data["employees"])  # type: ignore
            session.flush()

            # Получаем созданные ID сотрудников
            employees = session.query(Employee).all()
            employee_id_mapping = {i + 1: e.id for i, e in enumerate(employees)}
            # print(f"DEBUG: Employee IDs: {[e.id for e in employees]}")

        # 3. Задачи - исправляем project_id
        if "tasks" in data:
            fixed_tasks = []
            for task in data["tasks"]:
                expected_project_id = task["project_id"]
                actual_project_id = project_id_mapping.get(expected_project_id)

                if actual_project_id is None:
                    print(f"WARNING: No project found for ID {expected_project_id}")
                    continue

                task["project_id"] = actual_project_id
                fixed_tasks.append(task)

            session.bulk_insert_mappings(Task, fixed_tasks)  # type: ignore
            session.flush()

            # Получаем созданные ID задач
            tasks = session.query(Task).all()
            task_id_mapping = {i + 1: t.id for i, t in enumerate(tasks)}
            # print(f"DEBUG: Task IDs: {[t.id for t in tasks]}")

        # 4. Связи многие-ко-многим - исправляем task_id и employee_id
        if "tasks_employees" in data:
            fixed_relations = []
            for relation in data["tasks_employees"]:
                expected_task_id = relation["task_id"]
                expected_employee_id = relation["employee_id"]

                actual_task_id = task_id_mapping.get(expected_task_id)
                actual_employee_id = employee_id_mapping.get(expected_employee_id)

                if actual_task_id is None:
                    print(f"WARNING: No task found for ID {expected_task_id}")
                    continue
                if actual_employee_id is None:
                    print(f"WARNING: No employee found for ID {expected_employee_id}")
                    continue

                relation["task_id"] = actual_task_id
                relation["employee_id"] = actual_employee_id
                fixed_relations.append(relation)

            session.bulk_insert_mappings(TaskEmployees, fixed_relations)  # type: ignore

        # 5. Заметки - исправляем task_id и employee_id
        if "notes" in data:
            fixed_notes = []
            for note in data["notes"]:
                expected_task_id = note["task_id"]
                expected_employee_id = note["employee_id"]

                actual_task_id = task_id_mapping.get(expected_task_id)
                actual_employee_id = employee_id_mapping.get(expected_employee_id)

                if actual_task_id is None:
                    print(f"WARNING: No task found for ID {expected_task_id}")
                    continue
                if actual_employee_id is None:
                    print(f"WARNING: No employee found for ID {expected_employee_id}")
                    continue

                note["task_id"] = actual_task_id
                note["employee_id"] = actual_employee_id
                fixed_notes.append(note)

            session.bulk_insert_mappings(Note, fixed_notes)  # type: ignore

        if "user_password" in data:
            fixed_relations = []
            for relation in data["user_password"]:
                expected_employee_id = relation["user_id"]
                actual_employee_id = employee_id_mapping.get(expected_employee_id)

                if actual_employee_id is None:
                    print(f"WARNING: No employee found for ID {expected_employee_id}")
                    continue

                relation["employee_id"] = actual_employee_id
                fixed_relations.append(relation)
            session.bulk_insert_mappings(UserPassword, fixed_relations)  # type: ignore

        session.commit()
        # print("DEBUG: Data insertion completed successfully")

    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        raise
