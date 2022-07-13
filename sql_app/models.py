from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    brand_name = Column(String(64))
    product_name = Column(String(64))
    price = Column(String(16))
    price_int = Column(Numeric(10, 2))
    update_date = Column(DateTime)
