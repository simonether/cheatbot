"""
This module contains Pydantic models for Telegram subscriptions.
"""
from pydantic import Field

from .common import CamelCaseModel


class TelegramViewSubscriptionCreate(CamelCaseModel):
    """Pydantic model for creating a new Telegram view subscription."""

    link: str
    limit: int
    duration_type: str = Field(..., alias="durationType")
    duration_value: int = Field(..., alias="durationValue")
    day: int
    daily_message_limit: int = Field(..., alias="dailyMessageLimit")


class TelegramReactionSubscriptionCreate(CamelCaseModel):
    """Pydantic model for creating a new Telegram reaction subscription."""

    link: str
    limit: int
    limit_post: int = Field(..., alias="limitPost")
    duration_type: str = Field(..., alias="durationType")
    duration_value: int = Field(..., alias="durationValue")
    reactions: list[int]


class TelegramSubscription(CamelCaseModel):
    """Pydantic model for a Telegram subscription."""

    id: int
    service: str
    type: str
    link: str
    cost: int
    progress: str
    created: int
    amount: int