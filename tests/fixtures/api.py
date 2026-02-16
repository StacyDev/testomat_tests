from typing import Any, Generator

import pytest

from src.api.testomat_api_client import TestomatApiClient


@pytest.fixture
def api_client(configs) -> Generator[TestomatApiClient, None, None]:
    client = TestomatApiClient(configs.base_url_app, configs.token)
    yield client
