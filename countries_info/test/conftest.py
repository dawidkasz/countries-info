import pytest

from countries_info.src.random_data_client import RandomDataClient


@pytest.fixture
def random_data_client() -> RandomDataClient:
    return RandomDataClient()
