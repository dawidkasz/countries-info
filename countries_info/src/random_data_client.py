import pydantic
import requests

from .api_client_base import ApiClientBase
from .exceptions import ApiClientError, RandomDataClientError
from .schemas import RandomAddressSchema


class RandomDataClient(ApiClientBase):
    URL_BASE = "https://random-data-api.com/api/v2"
    URL_ADDRESSES = URL_BASE + "/addresses"

    def fetch_random_address(self) -> RandomAddressSchema:
        response = self._make_request(self.URL_ADDRESSES)

        try:
            return RandomAddressSchema(**response.json())
        except (requests.JSONDecodeError, pydantic.ValidationError):
            raise RandomDataClientError("Unexpected response format")

    def _make_request(self, endpoint: str):
        try:
            return super()._make_request(endpoint)
        except ApiClientError as exc:
            raise RandomDataClientError from exc
