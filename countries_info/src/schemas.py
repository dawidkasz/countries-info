from pydantic import BaseModel


class RandomAddressSchema(BaseModel):
    country: str


class CountryInfoSchema(BaseModel):
    name: str
    capital: list[str]
    languages: list[str]
    population: int
    biggest_city: str | None