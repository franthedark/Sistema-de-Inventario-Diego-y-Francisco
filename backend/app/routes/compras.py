from litestar import Router, post
from app.models import Compra, DetalleCompra, Producto
from app.db import SessionLocal
from pydantic import BaseModel
from typing import Dict

class DetalleCompraSchema(BaseModel):
    producto_id: int
    cantidad: int
    precio: float

class CompraSchema(BaseModel):
    proveedor: str
    detalles: list[DetalleCompraSchema]

@post("/")
async def registrar_compra(data: CompraSchema) -> Dict[str, str]:
    """Registra una nueva compra y actualiza el stock"""
    with SessionLocal() as session:
        compra = Compra(proveedor=data.proveedor)
        session.add(compra)
        session.commit()

        for detalle in data.detalles:
            producto = session.query(Producto).get(detalle.producto_id)
            if not producto:
                return {"error": f"Producto con ID {detalle.producto_id} no encontrado"}

            # Actualizar stock
            producto.stock += detalle.cantidad

            # Registrar el detalle de la compra
            detalle_compra = DetalleCompra(
                compra_id=compra.id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio=detalle.precio
            )
            session.add(detalle_compra)

        session.commit()

    return {"message": "Compra registrada exitosamente"}

router = Router(
    path="/compras",
    route_handlers=[
        registrar_compra  # Ejemplo de función para manejar una venta
    ],
)