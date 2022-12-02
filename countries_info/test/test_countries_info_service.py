import responses

from countries_info.src.countries_info_service import get_random_countries_info
from countries_info.src.random_data_client import RandomDataClient
from countries_info.src.rest_countries_client import RestCountriesClient
from countries_info.src.schemas import CountryInfoSchema


@responses.activate
def test_get_random_countries_info(
    random_data_client: RandomDataClient, rest_countries_client: RestCountriesClient
):
    responses.add(
        responses.GET,
        random_data_client.URL_BASE + random_data_client.URL_ADDRESSES,
        json={"country": "Poland"},
        status=200,
    )
    responses.add(
        responses.GET,
        random_data_client.URL_BASE + random_data_client.URL_ADDRESSES,
        json={"country": "Malaysia"},
        status=200,
    )
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Poland"),
        json=[
            {
                "name": {"common": "Poland"},
                "capital": ["Warsaw"],
                "languages": {"pol": "Polish"},
                "population": 37950802,
            }
        ],
        status=200,
    )
    responses.add(
        responses.GET,
        rest_countries_client.URL_BASE
        + rest_countries_client.URL_COUNTRY_INFO.format(name="Malaysia"),
        status=400,
    )

    assert get_random_countries_info(2, random_data_client, rest_countries_client) == {
        "Poland": CountryInfoSchema(
            name="Poland", capital=["Warsaw"], languages=["Polish"], population=37950802
        ),
        "Malaysia": None,
    }
