from typing import List

from src.schemas.employee import EmployeeSchema
from src.schemas.project import ProjectSchema
from src.schemas.note import NoteSchema
from src.schemas.task import TaskSchema


class EmployeeRelSchema(EmployeeSchema):
    employee_tasks: List["TaskSchema"] = []
    employee_notes: List["NoteSchema"] = []


class ProjectRelSchema(ProjectSchema):
    project_tasks: List["TaskSchema"] = []


class NoteRelSchema(NoteSchema):
    note_task: "TaskSchema"
    written_by: "EmployeeSchema"


class TaskRelSchema(TaskSchema):
    task_employees: List["EmployeeSchema"] = []
    task_project: "ProjectSchema"
    task_notes: List["NoteSchema"] = []
