from typing import List

from src.models.employee_models import EmployeeSchema
from src.models.project_models import ProjectSchema
from src.models.note_models import NoteSchema
from src.models.task_models import TaskSchema


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
