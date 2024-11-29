import jwt
import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Función para crear un token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiración de 1 hora
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar el token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

# Función para autenticar al usuario
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:  # Aquí deberías hacer un hash de la contraseña
        return user
    return None
