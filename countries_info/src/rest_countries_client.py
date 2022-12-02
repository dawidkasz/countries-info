import pydantic
import requests

from countries_info.src.exceptions import RestCountriesClientError
from countries_info.src.schemas import CountryInfoSchema


class RestCountriesClient:
    URL_BASE = "https://restcountries.com/v3.1"
    URL_COUNTRY_INFO = "/name/{name}"

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
            )
        except (KeyError, pydantic.ValidationError):
            raise RestCountriesClientError("Unexpected response format")

    def _make_request(self, endpoint_suffix: str):
        try:
            response = requests.get(self.URL_BASE + endpoint_suffix)
            response.raise_for_status()
        except (requests.HTTPError, requests.RequestException):
            raise RestCountriesClientError("Can't retrieve data from the api")

        return response
