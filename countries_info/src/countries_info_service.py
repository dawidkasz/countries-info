import concurrent.futures

from countries_info.src.exceptions import RestCountriesClientError
from countries_info.src.random_data_client import RandomDataClient
from countries_info.src.rest_countries_client import RestCountriesClient
from countries_info.src.schemas import CountryInfoSchema


def get_random_countries_info(
    num_countries: int,
    random_data_client: RandomDataClient,
    rest_countries_client: RestCountriesClient,
) -> list[tuple[str, CountryInfoSchema | None]]:
    country_names = _get_random_country_names(random_data_client, num_countries)
    countries_info = _get_countries_info(rest_countries_client, country_names)

    return sorted(
        countries_info, key=lambda x: x[1].population if x[1] else 0, reverse=True
    )


def _get_random_country_names(
    random_data_client: RandomDataClient, num_countries: int
) -> set[str]:
    with concurrent.futures.ThreadPoolExecutor() as exc:
        futures = [
            exc.submit(random_data_client.fetch_random_address)
            for _ in range(num_countries)
        ]

        return set(
            future.result().country
            for future in concurrent.futures.as_completed(futures)
        )


def _get_countries_info(
    rest_countries_client: RestCountriesClient, country_names: set[str]
) -> list[tuple[str, CountryInfoSchema | None]]:
    def _request_handler(country_name: str) -> tuple[str, CountryInfoSchema | None]:
        try:
            return country_name, rest_countries_client.fetch_country_info(country_name)
        except RestCountriesClientError:
            return country_name, None

    with concurrent.futures.ThreadPoolExecutor() as exc:
        futures = [exc.submit(_request_handler, name) for name in country_names]
        return [future.result() for future in futures]
