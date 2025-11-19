from typing import Annotated, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime
from .db_setup import Base
import enum

intpk = Annotated[int, mapped_column(primary_key=True)]
DateStr = Annotated[
    str,
    mapped_column(
        server_default=datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
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


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[intpk]

    first_name: Mapped[str]
    last_name: Mapped[str]
    salary: Mapped[int]
    is_working: Mapped[bool] = mapped_column(default=True)
    employee_tasks: Mapped[List["Task"]] = relationship(
        back_populates="task_employees", secondary="tasks_employees"
    )

    employee_notes: Mapped[List["Note"]] = relationship(
        back_populates="written_by", cascade="all, delete-orphan", passive_deletes=True
    )


class TaskEmployees(Base):
    __tablename__ = "tasks_employees"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True
    )


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[intpk]

    project_name: Mapped[str]
    start_date: Mapped[DateStr]
    end_date: Mapped[DateStr]
    is_completed: Mapped[bool] = mapped_column(default=False)

    project_tasks: Mapped[List["Task"]] = relationship(
        back_populates="task_project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[intpk]
    note_info: Mapped[str]

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE")
    )
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))

    written_by: Mapped["Employee"] = relationship(back_populates="employee_notes")
    note_task: Mapped["Task"] = relationship(back_populates="task_notes")
