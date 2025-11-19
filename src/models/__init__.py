import enum
from pydantic import BeforeValidator
from datetime import datetime
from typing import Annotated

import re

DateString = Annotated[str, BeforeValidator(lambda x: validate_date_format(x))]


def validate_date_format(date_str: str) -> str:
    if not isinstance(date_str, str):
        raise ValueError("Date must be string")
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern=pattern, string=date_str):
        raise ValueError("String must be formatted like YYYY-MM-DD")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date")

    return date_str


class Priority(enum.IntEnum):
    high_priority = 3
    mid_priority = 2
    low_priority = 1


class UnexpectedFileFormatExcpetion(Exception):
    def __init__(self, filetype: str) -> None:
        self.filetype = filetype
