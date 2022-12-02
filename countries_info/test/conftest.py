import pytest

from countries_info.src.random_data_client import RandomDataClient
from countries_info.src.rest_countries_client import RestCountriesClient


@pytest.fixture
def random_data_client() -> RandomDataClient:
    return RandomDataClient()


@pytest.fixture
def rest_countries_client() -> RestCountriesClient:
    return RestCountriesClient()
