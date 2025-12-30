import datetime
import enum
from typing import Annotated, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.setup import Base
from employee.models.employee import Employee
from note.models.note import Note
from project.models.project import Project

intpk = Annotated[int, mapped_column(primary_key=True)]
DateStr = Annotated[
    str,
    mapped_column(
        server_default=datetime.datetime.strftime(
            datetime.datetime.utcnow(), "%Y-%m-%d"
        )
    ),
]


class Priority(enum.IntEnum):
    high_priority = 3
    mid_priority = 2
    low_priority = 1


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[intpk]
    task_description: Mapped[str]
    start_date: Mapped[DateStr]
    end_date: Mapped[DateStr]
    priority: Mapped[Priority] = mapped_column(default=Priority.low_priority)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )

    task_employees: Mapped[List["Employee"]] = relationship(
        back_populates="employee_tasks",
        secondary="tasks_employees",
        cascade="all, delete",
        passive_deletes=True,
    )

    task_project: Mapped["Project"] = relationship(back_populates="project_tasks")

    task_notes: Mapped[List["Note"]] = relationship(
        back_populates="note_task", cascade="all, delete-orphan", passive_deletes=True
    )
