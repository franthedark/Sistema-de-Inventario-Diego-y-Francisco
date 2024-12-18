from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, User

DATABASE_URL = "sqlite:///./database.sqlite"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar las credenciales del usuario
def verify_user(db: Session, username: str, password: str) -> bool:
    user = db.query(User).filter(User.username == username, User.password == password).first()
    return user is not None