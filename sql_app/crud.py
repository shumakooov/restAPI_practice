from datetime import datetime

from sqlalchemy.orm import Session

import models
import schemas


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(models.Product).filter(models.Product.product_name == product_name)\
                                    .order_by(models.Product.update_date)\
                                    .first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    dt = datetime.now()
    db_product = models.Product(
        category=product.category,
        brand_name=product.brand_name,
        product_name=product.product_name,
        price=product.price,
        price_int=product.price_int,
        update_date=dt
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db.query(models.Product).filter(models.Product.id == product_id).delete()
    db.commit()
    return


def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    item = db.query(models.Product).filter(models.Product.id == product_id).first()
    item.category = product.category
    item.brand_name = product.brand_name
    item.product_name = product.product_name
    item.price = product.price
    item.price_int = product.price_int
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

