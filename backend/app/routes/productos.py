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

@post("/actualizar-stock")
async def actualizar_stock(producto_id: int, cantidad: int) -> Dict[str, str]:
    """Actualiza el stock de un producto después de una compra o venta."""
    with SessionLocal() as session:
        producto = session.query(Producto).get(producto_id)
        if not producto:
            return {"error": f"Producto con ID {producto_id} no encontrado"}

        # Actualizar el stock
        producto.stock += cantidad  
        session.commit()  # Guardar los cambios en la base de datos
        session.refresh(producto)  # Refrescar la instancia con los nuevos datos

    return {
        "message": f"Stock del producto {producto.nombre} actualizado exitosamente",
        "nuevo_stock": producto.stock
    }

# Configurar el router para manejar las rutas de productos
router = Router(
    path="/productos",
    route_handlers=[listar_productos, crear_producto, actualizar_stock],  # Añadimos la nueva ruta
)
