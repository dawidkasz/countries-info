import pytest
import responses

from countries_info.src.exceptions import RestCountriesClientError
from countries_info.src.rest_countries_client import RestCountriesClient


@responses.activate
def test_fetch_country_info_valid(rest_countries_client: RestCountriesClient):
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Poland"),
        json=[
            {
                "name": {"common": "Poland", "official": "Republic of Poland"},
                "capital": ["Warsaw"],
                "region": "Europe",
                "languages": {"pol": "Polish"},
                "population": 37950802,
            }
        ],
        status=200,
    )

    assert rest_countries_client.fetch_country_info("Poland").dict() == {
        "name": "Poland",
        "capital": ["Warsaw"],
        "languages": ["Polish"],
        "population": 37950802,
    }


@responses.activate
def test_fetch_country_info_missing_data(rest_countries_client: RestCountriesClient):
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Poland"),
        json=[
            {
                "name": {"common": "Poland", "official": "Republic of Poland"},
                "capital": [],
                "region": "Europe",
            }
        ],
        status=200,
    )

    assert rest_countries_client.fetch_country_info("Poland").dict() == {
        "name": "Poland",
        "capital": [],
        "languages": [],
        "population": 0,
    }


@responses.activate
def test_fetch_country_bad_request(rest_countries_client: RestCountriesClient):
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Poland"),
        status=400,
    )

    with pytest.raises(RestCountriesClientError):
        rest_countries_client.fetch_country_info("Poland")


@responses.activate
def test_fetch_country_no_data_found(rest_countries_client: RestCountriesClient):
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Poland"),
        json=[],
        status=200,
    )

    with pytest.raises(RestCountriesClientError):
        rest_countries_client.fetch_country_info("Poland")


@responses.activate
def test_fetch_country_unexpected_response(rest_countries_client: RestCountriesClient):
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Poland"),
        json=[{}, {}],
        status=200,
    )

    with pytest.raises(RestCountriesClientError):
        rest_countries_client.fetch_country_info("Poland")
