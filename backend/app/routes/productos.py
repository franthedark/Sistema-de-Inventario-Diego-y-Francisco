from litestar import Router, post, get
from app.models import Producto
from app.schemas import ProductoSchema
from app.db import SessionLocal
from typing import List, Dict, Any

@post("/")
async def crear_producto(data: ProductoSchema) -> Dict[str, any]:
    """Crea un nuevo producto."""
    with SessionLocal() as session:
        # Crear un nuevo producto usando los datos recibidos
        producto = Producto(**data.dict())
        session.add(producto)
        session.commit()
        session.refresh(producto)
    return {"message": "Producto creado", "producto": data.dict()}

@get("/")
async def listar_productos() -> List[Dict[str, Any]]:
    """Devuelve una lista de productos."""
    with SessionLocal() as session:
        productos = session.query(Producto).all()
    # Convertir a JSON serializable
    return [
        {"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion, "precio": p.precio, "stock": p.stock}
        for p in productos
    ]

# Configurar el router
router = Router(
    path="/productos",
    route_handlers=[listar_productos, crear_producto],
)