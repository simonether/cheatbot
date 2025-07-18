"""Models for creating a new task."""
from typing import List, Optional

from pydantic import Field

from .common import CamelCaseModel


class Interval(CamelCaseModel):
    """Represents a time interval with a speed coefficient."""

    from_time: str = Field(..., alias="from")
    to_time: str = Field(..., alias="to")
    speed_coefficient: int = Field(..., alias="speedCoefficient")


class CreateTaskParams(CamelCaseModel):
    """Represents the parameters for creating a new task."""

    service: int
    link: str
    quantity: int
    post: int
    gender: Optional[str] = None
    duration_type: Optional[str] = Field(None, alias="durationType")
    duration_value: Optional[int] = Field(None, alias="durationValue")
    intervals: Optional[List[Interval]] = None