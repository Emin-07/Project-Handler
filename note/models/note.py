from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.setup import Base
from employee.models.employee import Employee
from task.models.task import Task

intpk = Annotated[int, mapped_column(primary_key=True)]


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
