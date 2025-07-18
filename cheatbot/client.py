"""
CheatBot API client.
"""
import httpx
import logging
from typing import Optional

from .models import (
    Service,
    Profile,
    CreateTaskParams,
    TaskCreateResponse,
    TaskStatus,
    TelegramViewSubscriptionCreate,
    TelegramReactionSubscriptionCreate,
    TelegramSubscription,
)
from .services import ServiceManager

logger = logging.getLogger(__name__)


class CheatBotClient:
    """
    Asynchronous client for interacting with the CheatBot API.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.cheatbot.ru"):
        """
        Initializes the CheatBotClient.

        Args:
            api_key: Your CheatBot API key.
            base_url: The base URL of the CheatBot API.
        """
        self._api_key = api_key
        self._base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None
        self.services: Optional[ServiceManager] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Initializes and returns the httpx client, creating one if it doesn't exist."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                params={"access-token": self._api_key},
                event_hooks={'response': [self._log_response]}
            )
        return self._client

    async def _log_response(self, response):
        """Logs the request and response."""
        request = response.request
        logger.debug(f"Request: {request.method} {request.url}")
        try:
            response.raise_for_status()
            logger.debug(f"Response: {response.status_code}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {request.url}: {e.response.status_code} - {e.response.text}")
            raise

    async def initialize(self):
        """
        Initializes the service manager by fetching the services from the API.
        This method should be called before any other method that requires services.
        """
        if self.services is None:
            services = await self._fetch_services()
            self.services = ServiceManager(services)
            logger.info("ServiceManager initialized with %d services.", len(services))

    async def aclose(self):
        """Closes the underlying httpx client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Makes a request to the API."""
        client = await self._get_client()
        return await client.request(method, url, **kwargs)

    async def _fetch_services(self) -> list[Service]:
        """
        Fetches and validates the list of services from the CheatBot API.
        """
        logger.info("Fetching services from the CheatBot API.")
        response = await self._request("get", "/services")
        services_data = response.json()
        validated_data = [Service(**v) for v in services_data.values()]
        logger.info("Successfully fetched and validated %d services.", len(validated_data))
        return validated_data

    async def get_profile_info(self) -> Profile:
        """
        Fetches the user's profile information.
        """
        logger.info("Fetching profile information.")
        response = await self._request("get", "/pb/profile/info")
        return Profile(**response.json())

    async def create_task(self, task: CreateTaskParams) -> TaskCreateResponse:
        """
        Creates a new task.
        """
        logger.info(f"Creating a new task for service {task.service}.")
        response = await self._request(
            "post", "/pb/task/create", json=task.model_dump(by_alias=True, exclude_none=True)
        )
        return TaskCreateResponse(**response.json())

    async def get_task_status(self, task_id: int) -> TaskStatus:
        """
        Fetches the status of a single task.
        """
        logger.info(f"Fetching status for task {task_id}.")
        response = await self._request("get", f"/pb/task/{task_id}")
        # The API returns a list with a single item
        return TaskStatus(**response.json()[0])

    async def get_tasks_status(self, task_ids: list[int]) -> dict[int, TaskStatus]:
        """
        Fetches the status of a list of tasks.
        """
        logger.info(f"Fetching status for tasks: {task_ids}")
        orders = ",".join(map(str, task_ids))
        response = await self._request("get", f"/pb/task/status?orders={orders}")
        return {int(k): TaskStatus(**v) for k, v in response.json().items()}

    async def create_telegram_view_subscription(
        self, subscription: TelegramViewSubscriptionCreate
    ) -> TaskCreateResponse:
        """
        Creates a new Telegram view subscription.
        """
        logger.info(f"Creating a new Telegram view subscription for {subscription.link}.")
        response = await self._request(
            "post",
            "/pb/telegram-subscription/create-view",
            json=subscription.model_dump(by_alias=True),
        )
        return TaskCreateResponse(**response.json())

    async def create_telegram_reaction_subscription(
        self, subscription: TelegramReactionSubscriptionCreate
    ) -> TaskCreateResponse:
        """
        Creates a new Telegram reaction subscription.
        """
        logger.info(f"Creating a new Telegram reaction subscription for {subscription.link}.")
        response = await self._request(
            "post",
            "/pb/telegram-subscription/create-reaction",
            json=subscription.model_dump(by_alias=True),
        )
        return TaskCreateResponse(**response.json())

    async def get_telegram_subscription_status(self, subscription_id: int) -> TelegramSubscription:
        """
        Fetches the status of a Telegram subscription.
        """
        logger.info(f"Fetching status for Telegram subscription {subscription_id}.")
        response = await self._request("get", f"/pb/telegram-subscription/{subscription_id}")
        # The API returns a list with a single item
        return TelegramSubscription(**response.json()[0])