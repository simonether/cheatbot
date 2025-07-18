"""
This module contains common Pydantic models.
"""
from pydantic import BaseModel, ConfigDict


class CamelCaseModel(BaseModel):
    """A Pydantic model that uses camelCase for its field names."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")
