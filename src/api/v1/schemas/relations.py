from typing import List

from .employee import EmployeeSchema
from .project import ProjectSchema
from .note import NoteSchema
from .task import TaskSchema


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
