from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import SessionLocal
from pydantic import BaseModel, EmailStr
from typing import List

router = APIRouter()

# Esquema de entrada para usuarios
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # En un caso real, aplica hash a las contraseñas

# Esquema de salida para usuarios
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# Dependency para la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar usuarios
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Endpoint para crear un nuevo usuario
@router.post("/", response_model=UserOut)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya está registrado
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Crear y guardar el nuevo usuario
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password  # Aplica hashing en un caso real
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Endpoint para obtener un usuario por ID
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
