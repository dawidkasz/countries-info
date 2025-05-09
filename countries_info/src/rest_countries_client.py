import pydantic
import requests

from .api_client_base import ApiClientBase
from .exceptions import ApiClientError, RestCountriesClientError
from .schemas import CountryInfoSchema


class RestCountriesClient(ApiClientBase):
    URL_BASE = "https://restcountries.com/v3.1"
    URL_COUNTRY_INFO = URL_BASE + "/name/{name}"

    def fetch_country_info(self, country_name: str) -> CountryInfoSchema:
        response = self._make_request(self.URL_COUNTRY_INFO.format(name=country_name))

        try:
            country_info_json = response.json()[0]
        except (requests.JSONDecodeError, KeyError, IndexError):
            raise RestCountriesClientError(f"No data found for country {country_name}")

        try:
            return CountryInfoSchema(
                name=country_info_json["name"]["common"],
                capital=country_info_json.get("capital", []),
                languages=list(country_info_json.get("languages", {}).values()),
                population=country_info_json.get("population", 0),
                biggest_city=country_info_json.get("biggest_city"),
            )
        except (KeyError, pydantic.ValidationError):
            raise RestCountriesClientError("Unexpected response format")

    def _make_request(self, endpoint: str):
        try:
            return super()._make_request(endpoint)
        except ApiClientError as exc:
            raise RestCountriesClientError from exc
