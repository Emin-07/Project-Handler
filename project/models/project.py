import datetime
from typing import Annotated, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.setup import Base
from task.models.task import Task

intpk = Annotated[int, mapped_column(primary_key=True)]
DateStr = Annotated[
    str,
    mapped_column(
        server_default=datetime.datetime.strftime(
            datetime.datetime.utcnow(), "%Y-%m-%d"
        )
    ),
]


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
