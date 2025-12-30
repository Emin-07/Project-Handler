import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.setup import Base
from employee.models.employee import Employee

intpk = Annotated[int, mapped_column(primary_key=True)]
DateStr = Annotated[
    str,
    mapped_column(
        server_default=datetime.datetime.strftime(
            datetime.datetime.utcnow(), "%Y-%m-%d"
        )
    ),
]


class UserPassword(Base):
    __tablename__ = "user_password"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True
    )
    hashed_password: Mapped[str]

    employee: Mapped["Employee"] = relationship(back_populates="user_password")
