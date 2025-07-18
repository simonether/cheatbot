"""
All models related to form fields are collected here.
"""
from typing import Any, Literal, Annotated, Union

from pydantic import Field

from .common import CamelCaseModel


class BaseFormField(CamelCaseModel):
    """Base model for all form fields."""

    name: str = Field(description="The name of the field, derived from the form dictionary key.")
    position: int | None = Field(None, description="The field's position in the form.")
    label: str | None = Field(None, description="The display label for the field.")
    hint: str | None = Field(None, description="A hint for the field.")
    placeholder: str | None = Field(None, description="Placeholder text for the field.")


class StringFormField(BaseFormField):
    """String input field."""

    type: Literal["string"]
    editable: bool | None = None
    default_value: str | None = Field(None, alias="defaultValue")
    max_length: int | None = Field(None, alias="maxLength")


class NumberFormField(BaseFormField):
    """Numeric input field."""

    type: Literal["number"]
    min: str | int | None = None
    max: str | int | None = None
    calculator: bool | None = None
    default_value: str | int | None = Field(None, alias="defaultValue")
    right_label: str | None = Field(None, alias="rightLabel")
    label_on_edit: str | None = Field(None, alias="labelOnEdit")
    current_min_on_edit: bool | None = Field(None, alias="currentMinOnEdit")
    disabled: bool | str | None = None


class TextareaFormField(BaseFormField):
    """Text area input field."""

    type: Literal["textarea"]
    disabled: bool | None = None
    default_value: str | None = Field(None, alias="defaultValue")


class WarningFieldParams(CamelCaseModel):
    """Parameters for the warning field."""

    text: str
    type: str


class WarningFormField(BaseFormField):
    """Warning message field."""

    type: Literal["warning"]
    params: WarningFieldParams


class TagsFieldParams(CamelCaseModel):
    """Parameters for the tags field."""

    values: list[str]


class TagsFormField(BaseFormField):
    """Tags input field."""

    type: Literal["tags"]
    params: TagsFieldParams


class SelectOption(CamelCaseModel):
    """Option for a select field."""

    label: Any
    value: Any


class SelectFormField(BaseFormField):
    """Select input field."""

    type: Literal["select"]
    options: list[SelectOption]
    calculator: bool | None = None
    default_value: Any | None = Field(None, alias="defaultValue")


class CheckboxFormField(BaseFormField):
    """Checkbox input field."""

    type: Literal["checkbox"]
    calculator: bool | None = None
    default_value: bool | None = Field(None, alias="defaultValue")


class RadioTabsOption(CamelCaseModel):
    """Option for a radio tabs field."""

    text: str | int
    value: str | int


class RadioTabsFormField(BaseFormField):
    """Radio tabs input field."""

    type: Literal["radioTabs"]
    options: list[RadioTabsOption]
    default_value: str | int | None = Field(None, alias="defaultValue")


class ChannelFormField(BaseFormField):
    """Channel input field."""

    type: Literal["channel"]
    editable: bool | None = None


class ListFormField(BaseFormField):
    """List input field."""

    type: Literal["list"]
    min: str
    max: str
    calculator: bool


class MultipleFloatingSpeedParams(CamelCaseModel):
    """Parameters for the multipleFloatingSpeed field."""

    limit: dict[str, int | str]
    intervalMin: dict[str, int | str]


class MultipleFloatingSpeedFormField(BaseFormField):
    """Model for multipleFloatingSpeed field."""

    type: Literal["multipleFloatingSpeed"]
    params: MultipleFloatingSpeedParams


class FloatingSpeedFormField(BaseFormField):
    """Stub for floatingSpeed field."""

    type: Literal["floatingSpeed"]


class SpreadFormField(BaseFormField):
    """Stub for spread field."""

    type: Literal["spread"]
    editable: bool | None = None
    required: bool | None = None
    calculator: bool | None = None


class PostFormField(BaseFormField):
    """Stub for post field."""

    type: Literal["post"]


class DelayedStartFormField(BaseFormField):
    """Stub for delayedStart field."""

    type: Literal["delayedStart"]


class HiddenSliderFormField(BaseFormField):
    """Stub for hiddenSlider field."""

    type: Literal["hiddenSlider"]


class RangeBonusFormField(BaseFormField):
    """Stub for rangeBonus field."""

    type: Literal["rangeBonus"]


class RelationsFormField(BaseFormField):
    """Stub for relations field."""

    type: Literal["relations"]


class ReactionsTemplateFormField(BaseFormField):
    """Stub for reactionsTemplate field."""

    type: Literal["reactionsTemplate"]


class ReactionsFormField(BaseFormField):
    """Stub for reactions field."""

    type: Literal["reactions"]


class VoteTypeFieldFormField(BaseFormField):
    """Stub for voteTypeField field."""

    type: Literal["voteTypeField"]


class RegionsFormField(BaseFormField):
    """Stub for regions field."""

    type: Literal["regions"]


class LimitsFormField(BaseFormField):
    """Stub for limits field."""

    type: Literal["limits"]


class VerifyChannelWarningFormField(BaseFormField):
    """Stub for verifyChannelWarning field."""

    type: Literal["verifyChannelWarning"]


class DurationParams(CamelCaseModel):
    """Parameters for the duration field."""

    types: list[dict[str, str]]
    max: int
    min: int


class DurationFormField(BaseFormField):
    """Model for duration field."""

    type: Literal["duration"]
    params: DurationParams | None = None


class DurationModel(CamelCaseModel):
    """Model for duration."""

    type: str
    value: int


FormField = Annotated[
    Union[
        StringFormField,
        NumberFormField,
        TextareaFormField,
        WarningFormField,
        TagsFormField,
        SelectFormField,
        CheckboxFormField,
        RadioTabsFormField,
        ChannelFormField,
        ListFormField,
        MultipleFloatingSpeedFormField,
        FloatingSpeedFormField,
        SpreadFormField,
        PostFormField,
        DelayedStartFormField,
        HiddenSliderFormField,
        RangeBonusFormField,
        RelationsFormField,
        ReactionsTemplateFormField,
        ReactionsFormField,
        VoteTypeFieldFormField,
        RegionsFormField,
        LimitsFormField,
        VerifyChannelWarningFormField,
        DurationFormField,
    ],
    Field(discriminator="type"),
]