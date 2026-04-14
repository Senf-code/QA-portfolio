import os

import pytest

from api.client import ApiClient


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    timeout = int(os.getenv("API_TIMEOUT", "10"))
    return ApiClient(base_url=base_url, timeout=timeout)
