from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from .database import get_db
from . import models, schemas

app = FastAPI(
    title="Customer & Order Management API",
    description="A CRUD REST API built with FastAPI, PostgreSQL, SQLAlchemy and Pydantic.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}

def commit_or_409(db: Session, detail: str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=detail)

@app.post("/customers", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    customer = models.Customer(**payload.model_dump())
    db.add(customer)
    commit_or_409(db, "A customer with this email already exists.")
    db.refresh(customer)
    return customer

@app.get("/customers", response_model=list[schemas.CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="skip must be >= 0 and limit must be between 1 and 100.")
    return db.scalars(select(models.Customer).offset(skip).limit(limit)).all()

@app.get("/customers/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer

@app.patch("/customers/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, payload: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(customer, key, value)
    commit_or_409(db, "A customer with this email already exists.")
    db.refresh(customer)
    return customer

@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    db.delete(customer)
    db.commit()

@app.post("/products", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(**payload.model_dump())
    db.add(product)
    commit_or_409(db, "A product with this SKU already exists.")
    db.refresh(product)
    return product

@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="skip must be >= 0 and limit must be between 1 and 100.")
    return db.scalars(select(models.Product).offset(skip).limit(limit)).all()

@app.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

@app.patch("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, payload: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    commit_or_409(db, "Invalid product update.")
    db.refresh(product)
    return product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(product)
    db.commit()

@app.post("/orders", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    customer = db.get(models.Customer, payload.customer_id)
    product = db.get(models.Product, payload.product_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    if product.stock < payload.quantity:
        raise HTTPException(status_code=409, detail="Insufficient product stock.")
    product.stock -= payload.quantity
    order = models.Order(**payload.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.get("/orders", response_model=list[schemas.OrderOut])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if skip < 0 or not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="skip must be >= 0 and limit must be between 1 and 100.")
    return db.scalars(select(models.Order).offset(skip).limit(limit)).all()

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order
