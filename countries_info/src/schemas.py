from pydantic import BaseModel


class RandomAddressSchema(BaseModel):
    country: str
