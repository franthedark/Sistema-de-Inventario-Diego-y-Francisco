from litestar import Router, post, get
from app.models import Producto
from app.db import SessionLocal
from typing import List, Dict, Any
from pydantic import BaseModel
from typing import List, Dict

class ProductoSchema(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int

    class Config:
        orm_mode = True

@post("/")
async def crear_producto(data: ProductoSchema) -> Dict[str, any]:
    """Crea un nuevo producto."""
    with SessionLocal() as session:
        # Crear un nuevo producto usando los datos recibidos
        producto = Producto(**data.dict())
        session.add(producto)
        session.commit()  # Confirmar los cambios en la base de datos
        session.refresh(producto)  # Refrescar la instancia del producto
    return {"message": "Producto creado", "producto": data.dict()}

@get("/")
async def listar_productos() -> List[Dict[str, Any]]:
    """Devuelve una lista de productos."""
    with SessionLocal() as session:
        productos = session.query(Producto).all()  # Obtener todos los productos
    # Convertir los productos a un formato serializable
    return [
        {"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion, "precio": p.precio, "stock": p.stock}
        for p in productos
    ]


# Configurar el router para manejar las rutas de productos
router = Router(
    path="/productos",
    route_handlers=[listar_productos, crear_producto],  # Añadimos la nueva ruta
)
