from litestar import Router, post, put, Request
from app.models import User
from app.db import SessionLocal
from typing import Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext  

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True

    class Config:
        orm_mode = True

class LoginSchema(BaseModel):
    username: str
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para encriptar contraseñas
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@post("/register")
async def register(data: UserSchema) -> Dict[str, Any]:
    """Registrar un nuevo usuario."""
    with SessionLocal() as session:
        # Encriptar la contraseña antes de guardar
        hashed_password = hash_password(data.password)
        user = User(username=data.username, email=data.email, hashed_password=hashed_password, is_active=data.is_active)
        session.add(user)
        session.commit()
        session.refresh(user)
    return {"message": "Usuario registrado", "user": data.dict()}

@post("/login")
async def login(data: LoginSchema) -> Dict[str, Any]:
    """Iniciar sesión del usuario."""
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == data.username).first()
        if user and verify_password(data.password, user.hashed_password):
            return {"message": "Inicio de sesión exitoso", "user": {"id": user.id, "username": user.username}}
        return {"message": "Credenciales incorrectas"}, 401

@post("/logout")
async def logout(request: Request) -> Dict[str, Any]:
    """Cerrar sesión del usuario."""
    return {"message": "Sesión cerrada correctamente"}

@put("/disable")
async def disable_user(user_id: int) -> Dict[str, Any]:
    """Deshabilitar (inactivar) un usuario."""
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = False
            session.commit()
            return {"message": f"Usuario {user_id} deshabilitado correctamente"}
        return {"message": "Usuario no encontrado"}, 404

@put("/change_password")
async def change_password(user_id: int, new_password: str) -> Dict[str, Any]:
    """Cambiar la contraseña de un usuario."""
    with SessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.hashed_password = hash_password(new_password)
            session.commit()
            return {"message": f"Contraseña de usuario {user_id} actualizada"}
        return {"message": "Usuario no encontrado"}, 404


router = Router(
    path="/users",
    route_handlers=[register, login, logout, disable_user, change_password],
)
