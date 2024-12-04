from litestar import Router, post
from app.models import Venta, DetalleVenta, Producto
from app.db import SessionLocal
from pydantic import BaseModel
from typing import Dict

class DetalleVentaSchema(BaseModel):
    producto_id: int
    cantidad: int
    precio: float

class VentaSchema(BaseModel):
    detalles: list[DetalleVentaSchema]

@post("/")
async def registrar_venta(data: VentaSchema) -> Dict[str, str]:
    """Registra una nueva venta y actualiza el stock"""
    with SessionLocal() as session:
        venta = Venta()
        session.add(venta)
        session.commit()

        for detalle in data.detalles:
            producto = session.query(Producto).get(detalle.producto_id)
            if not producto:
                return {"error": f"Producto con ID {detalle.producto_id} no encontrado"}

            if producto.stock < detalle.cantidad:
                return {"error": f"Stock insuficiente para el producto con ID {detalle.producto_id}"}

            # Actualizar stock
            producto.stock -= detalle.cantidad

            # Registrar el detalle de la venta
            detalle_venta = DetalleVenta(
                venta_id=venta.id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio=detalle.precio
            )
            session.add(detalle_venta)

        session.commit()

    return {"message": "Venta registrada exitosamente"}

async def calcular_total_venta(venta: Venta) -> float:
    """Calcula el total de una venta sumando los detalles."""
    return sum(detalle.cantidad * detalle.precio for detalle in venta.detalles)

router = Router(
    path="/ventas",
    route_handlers=[
        registrar_venta  # Ejemplo de función para manejar una venta
    ],
)