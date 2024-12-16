from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.core.database import SessionLocal
from pydantic import BaseModel

router = APIRouter()

# Esquema de entrada
class ProductCreate(BaseModel):
    name: str
    category: str

# Dependency para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Verificar si el producto ya existe
    existing_product = db.query(Product).filter(Product.name == product.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    # Crear el nuevo producto
    new_product = Product(name=product.name, category=product.category)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created", "product": new_product}
