import requests

from .exceptions import ApiClientError


class ApiClientBase:
    @staticmethod
    def _make_request(url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except (requests.HTTPError, requests.RequestException):
            raise ApiClientError("Can't retrieve data from the api")

        return response
