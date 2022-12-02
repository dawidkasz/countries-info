import pytest
import responses

from countries_info.src.exceptions import RandomDataClientError
from countries_info.src.random_data_client import RandomDataClient


@responses.activate
def test_fetch_random_country_valid(random_data_client: RandomDataClient):
    responses.add(
        responses.GET,
        random_data_client.URL_BASE + random_data_client.URL_ADDRESSES,
        json={"country": "Mali", "country_code": "AQ", "zip": "89732"},
        status=200,
    )

    assert random_data_client.fetch_random_address().dict() == {"country": "Mali"}


@responses.activate
def test_fetch_random_country_bad_request(random_data_client: RandomDataClient):
    responses.add(
        responses.GET,
        random_data_client.URL_BASE + random_data_client.URL_ADDRESSES,
        status=400,
    )

    with pytest.raises(RandomDataClientError):
        random_data_client.fetch_random_address()


@responses.activate
def test_fetch_random_country_unexpected_response(random_data_client: RandomDataClient):
    responses.add(
        responses.GET,
        random_data_client.URL_BASE + random_data_client.URL_ADDRESSES,
        json={"country_code": "AQ"},
        status=200,
    )

    with pytest.raises(RandomDataClientError):
        random_data_client.fetch_random_address()
