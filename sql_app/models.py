from sqlalchemy import Column, Integer, String, DateTime, Numeric

from database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    brand_name = Column(String(64))
    product_name = Column(String(64))
    price = Column(String(16))
    price_int = Column(Numeric(10, 2))
    update_date = Column(DateTime)
