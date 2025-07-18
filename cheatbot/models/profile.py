"""
This module contains the Pydantic model for the user profile.
"""
from .common import CamelCaseModel


class Profile(CamelCaseModel):
    """Pydantic model for the user profile."""

    balance: float
    email: str
    active_task: int