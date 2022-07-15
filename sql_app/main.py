from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_products = crud.get_product_by_name(db, product_name=product.product_name)
    db_brand = crud.get_products_by_brand(db, brand_name=product.brand_name)
    if db_products and db_brand:
        raise HTTPException(status_code=400, detail="Product already exist")
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_products = crud.get_products(db, skip=skip, limit=limit)
    return db_products


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, product_id)
    return {"status": "ok"}


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product = crud.update_product(db, product_id, product)
    return db_product


@app.get("/products/brands/{brand_name}", response_model=List[schemas.Product])
def read_brand(brand_name: str, db: Session = Depends(get_db)):
    db_brands = crud.get_products_by_brand(db, brand_name=brand_name)
    if not db_brands:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brands
