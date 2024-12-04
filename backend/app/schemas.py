from pydantic import BaseModel

class ProductoSchema(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int
