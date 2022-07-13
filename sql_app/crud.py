from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas


def get_price(db: Session, price_id: int):
    return db.query(models.Price).filter(models.Price.id == price_id).first()


def get_price_by_name(db: Session, product_name: str):
    return db.query(models.Price).filter(models.Price.product_name == product_name).order_by(models.Price.update_date).first()


def get_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Price).offset(skip).limit(limit).all()


def create_price(db: Session, price: schemas.PriceCreate):
    dt = datetime.now()
    db_price = models.Price(
        category=price.category,
        brand_name=price.brand_name,
        product_name=price.product_name,
        price=price.price,
        price_int=price.price_int,
        update_date=dt
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def delete_price(db: Session, price_id: int):
    db.query(models.Price).filter(models.Price.id == price_id).delete()
    db.commit()
    return


def update_price(db: Session, price_id: int, price: schemas.PriceCreate):
    item = db.query(models.Price).filter(models.Price.id == price_id).first()
    item.category = price.category
    item.brand_name = price.brand_name
    item.product_name = price.product_name
    item.price = price.price
    item.price_int = price.price_int
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

