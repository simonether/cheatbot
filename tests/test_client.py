"""
Tests for the CheatBotClient.
"""
import json
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from cheatbot.client import CheatBotClient
from cheatbot.models import Service, BaseFormField

# Path to the test data file
TEST_DATA_PATH = Path(__file__).parent / "fixtures" / "services.json"


@pytest.fixture
def mock_services_data():
    """Load the mock services data from the JSON file."""
    with open(TEST_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def mock_response(mock_services_data):
    """Create a mock response object."""
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json = MagicMock(return_value=mock_services_data)
    return response


@pytest.mark.asyncio
@patch("cheatbot.client.httpx.AsyncClient")
@patch("cheatbot.client.logger")
async def test_initialize(mock_logger, MockAsyncClient, mock_response):
    """
    Tests the initialize method with proper mocking.
    """
    # Configure the mock client instance
    mock_client_instance = AsyncMock()
    mock_client_instance.request.return_value = mock_response
    MockAsyncClient.return_value = mock_client_instance

    # Initialize the client with a dummy API key
    async with CheatBotClient(api_key="test_api_key") as client:
        # The initialize method is called automatically when entering the context manager
        pass

    # --- Assertions ---
    assert client.services is not None
    services = client.services.get_all()
    assert isinstance(services, list)
    assert len(services) > 0
    assert isinstance(services[0], Service)
    assert services[0].service == 540
    assert isinstance(services[0].form, list)
    assert len(services[0].form) > 0
    assert all(isinstance(item, BaseFormField) for item in services[0].form)

    # Check that the logger was called correctly
    mock_logger.info.assert_any_call("Fetching services from the CheatBot API.")
    mock_logger.info.assert_any_call(
        "Successfully fetched and validated %d services.", len(mock_response.json())
    )
    mock_logger.info.assert_any_call(
        "ServiceManager initialized with %d services.", len(mock_response.json())
    )

    # Check that the request was made correctly
    mock_client_instance.request.assert_called_once_with("get", "/services")