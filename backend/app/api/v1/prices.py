from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.price import Price
from app.core.database import SessionLocal
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Esquema de entrada para precios
class PriceCreate(BaseModel):
    product_id: int
    price: float
    store: str
    user_id: int  # Opcional: para rastrear quién añadió el precio

# Esquema de salida para precios
class PriceOut(BaseModel):
    id: int
    product_id: int
    price: float
    store: str

    class Config:
        orm_mode = True

# Dependency para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar precios de un producto
@router.get("/", response_model=List[PriceOut])
def get_prices(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no Encontrado")

    prices = db.query(Price).filter(Price.product_id == product_id).all()
    return prices

# Endpoint para agregar un nuevo precio
@router.post("/", response_model=PriceOut)
def add_price(price_data: PriceCreate, db: Session = Depends(get_db)):
    # Verificar que el producto existe
    product = db.query(Product).filter(Product.id == price_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no Encontrado")

    # Crear y guardar el nuevo precio
    new_price = Price(
        product_id=price_data.product_id,
        price=price_data.price,
        store=price_data.store
    )
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price
