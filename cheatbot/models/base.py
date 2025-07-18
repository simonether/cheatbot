"""
Pydantic models for CheatBot API.
"""
from typing import Any

from pydantic import Field, model_validator

from .common import CamelCaseModel
from .fields import FormField


class Category(CamelCaseModel):
    """Pydantic model for a service category."""

    name: str
    slug: str


class ServiceType(CamelCaseModel):
    """Pydantic model for a service type."""

    url: str
    name: str
    type_position: int = Field(..., alias="typePosition")


class TaskExchange(CamelCaseModel):
    """Pydantic model for task exchange information."""

    name: str | None = None
    check_time: int = Field(..., alias="checkTime")
    time_for_work: int = Field(..., alias="timeForWork")
    is_need_screen: str = Field(..., alias="isNeedScreen")
    need_for_report: str | None = Field(None, alias="needForReport")
    is_task_anonymous: bool = Field(..., alias="isTaskAnonymous")


class Urls(CamelCaseModel):
    """Pydantic model for API URLs."""

    submit: str
    calculator: str


class Service(CamelCaseModel):
    """Pydantic model for a service."""

    service: int
    rate: float
    is_show_pause: bool = Field(..., alias="isShowPause")
    is_show_repeat: bool = Field(..., alias="isShowRepeat")
    is_show_edit: bool = Field(..., alias="isShowEdit")
    average_execution_time: str | None = Field(None, alias="averageExecutionTime")
    form: list[FormField]
    free: bool
    name: str
    type: ServiceType
    urls: Urls
    group: str | None = None
    refill: bool
    refund: bool
    country: str
    enabled: bool
    category: Category
    subscription: bool
    task_exchange: TaskExchange = Field(..., alias="taskExchange")
    multiple_limit: Any | None = Field(None, alias="multipleLimit")
    service_position: int = Field(..., alias="servicePosition")
    hide_public_service: bool = Field(..., alias="hidePublicService")
    hide_private_service: bool = Field(..., alias="hidePrivateService")

    @model_validator(mode="before")
    @classmethod
    def process_form_dict(cls, data: Any) -> Any:
        """Transforms the form dictionary into a sorted list of typed field objects."""
        if isinstance(data, dict) and "form" in data:
            form_data = data.get("form")
            if isinstance(form_data, dict):
                form_list = []
                for name, field_data in form_data.items():
                    if isinstance(field_data, dict):
                        field_data["name"] = name
                        if "type" not in field_data:
                            field_data["type"] = name
                        form_list.append(field_data)
                data["form"] = sorted(form_list, key=lambda x: x.get("position", 999))
        return data

    def get_field(self, name: str) -> FormField | None:
        """Returns a form field by its name."""
        for field in self.form:
            if field.name == name:
                return field
        return None

    def get_tags(self) -> list[str] | None:
        """Returns the list of tags if they exist in the service."""
        tags_field = self.get_field("descriptionTags")
        if tags_field and hasattr(tags_field, "params") and tags_field.params and hasattr(tags_field.params, "values"):
            return tags_field.params.values
        return None

    @property
    def comment_field(self) -> FormField | None:
        """Returns the comment field if it exists in the service."""
        return self.get_field("comments")


class Services(CamelCaseModel):
    """Pydantic model for a dictionary of services."""

    services: dict[str, Service]