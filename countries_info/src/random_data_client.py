import pydantic
import requests

from countries_info.src.exceptions import RandomDataClientError
from countries_info.src.schemas import RandomAddressSchema


class RandomDataClient:
    URL_BASE = "https://random-data-api.com/api/v2"
    URL_ADDRESSES = "/addresses"

    def fetch_random_address(self) -> RandomAddressSchema:
        response = self._make_request(self.URL_ADDRESSES)

        try:
            return RandomAddressSchema(**response.json())
        except (requests.JSONDecodeError, pydantic.ValidationError):
            raise RandomDataClientError("Unexpected response format")

    def _make_request(self, endpoint_suffix: str):
        try:
            response = requests.get(self.URL_BASE + endpoint_suffix)
            response.raise_for_status()
        except (requests.HTTPError, requests.RequestException):
            raise RandomDataClientError("Can't retrieve data from the api")

        return response
