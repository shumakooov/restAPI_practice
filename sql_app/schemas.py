from pydantic import BaseModel


class ProductBase(BaseModel):
    category: str
    brand_name: str
    product_name: str
    price: str
    price_int: int


class ProductCreate(ProductBase):
    update_date: str


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True