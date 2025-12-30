from typing import Annotated, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.setup import Base
from note.models.note import Note
from relation.models.relation import UserPassword
from task.models.task import Task

intpk = Annotated[int, mapped_column(primary_key=True)]


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

    user_password: Mapped["UserPassword"] = relationship(
        back_populates="employee", cascade="all, delete-orphan", uselist=False
    )


class TaskEmployees(Base):
    __tablename__ = "tasks_employees"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True
    )
