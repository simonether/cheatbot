"""Models related to task status and creation responses."""
from typing import Optional

from .common import CamelCaseModel


class TaskData(CamelCaseModel):
    """Data of a created task."""

    id: int
    cost: float


class TaskCreateResponse(CamelCaseModel):
    """Response received after successfully creating a task."""

    task: TaskData
    complete: bool


class TaskStatus(CamelCaseModel):
    """Represents the status of a specific task."""

    status: str
    remains: Optional[int] = None
    start_count: Optional[int] = None
