class CountriesInfoError(Exception):
    """Base exception for all errors"""


class ApiClientError(CountriesInfoError):
    pass


class RandomDataClientError(ApiClientError):
    pass


class RestCountriesClientError(ApiClientError):
    pass
