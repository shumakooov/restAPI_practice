from typing import List, Union

from pydantic import BaseModel


class PriceBase(BaseModel):
    category: str
    brand_name: str
    product_name: str
    price: str
    price_int: int


class PriceCreate(PriceBase):
    update_date: str


class Price(PriceBase):
    id: int

    class Config:
        orm_mode = True