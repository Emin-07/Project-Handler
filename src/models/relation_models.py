from typing import List

from .employee_models import EmployeeSchema
from .project_models import ProjectSchema
from .note_models import NoteSchema
from .task_models import TaskSchema


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
