from litestar import Router, post
from app.models import Venta, DetalleVenta, Producto
from app.db import SessionLocal
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from sqlalchemy import select
from litestar.exceptions import HTTPException
from sqlalchemy.orm import Session

# Esquema para recibir detalles de la venta
class DetalleVentaSchema(BaseModel):
    producto_id: int
    cantidad: int

class VentaSchema(BaseModel):
    detalles: List[DetalleVentaSchema]

def calcular_total_venta(detalles: List[DetalleVentaSchema], connection) -> float:
    total = 0
    for detalle in detalles:
        producto = connection.execute(select(Producto).where(Producto.id == detalle.producto_id)).fetchone()
        if producto:
            total += producto.precio * detalle.cantidad
    return total

@post("/")
async def registrar_venta(data: VentaSchema) -> Dict[str, str]:
    """Registra una nueva venta y actualiza el stock"""
    try:
        db: Session = SessionLocal()

        fecha_venta = datetime.utcnow()

        # Crear la venta
        venta = Venta(fecha=fecha_venta)
        db.add(venta)
        db.commit()
        db.refresh(venta)

        detalles_respuesta = []
        total_venta = 0
        total_productos_vendidos = 0
        ganancias = 0

        for detalle in data.detalles:
            producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} no encontrado")
            
            if not producto.estado:
                raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} deshabilitado")

            precio_total = producto.precio * detalle.cantidad
            total_venta += precio_total

            ganancia = producto.precio * detalle.cantidad
            ganancias += ganancia

            if producto.stock < detalle.cantidad:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para el producto {producto.nombre}")
            producto.stock -= detalle.cantidad
            db.commit()  

            detalle_venta = DetalleVenta(
                venta_id=venta.id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio=producto.precio
            )
            db.add(detalle_venta)

            detalles_respuesta.append({
                "producto_id": detalle.producto_id,
                "producto_nombre": producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_total": precio_total,
                "fecha": fecha_venta
            })

            total_productos_vendidos += detalle.cantidad

        # Actualizar el total de la venta en la tabla 'ventas'
        venta.total = total_venta
        venta.total_productos_vendidos = total_productos_vendidos
        venta.ganancias = ganancias
        db.commit()

        # Sincronizar los cambios
        db.refresh(venta)

        # Responder con los detalles de la venta
        return {
            "message": "Venta registrada exitosamente",
            "venta_id": venta.id,
            "detalles": detalles_respuesta,
            "fecha_venta": fecha_venta,
            "total_venta": total_venta,
            "total_productos_vendidos": total_productos_vendidos,
            "ganancias": ganancias
        }

    except HTTPException as e:
        return {"status_code": e.status_code, "detail": e.detail}
    
    except Exception as e:
        db.rollback()  
        return {"status_code": 500, "detail": f"Error inesperado: {str(e)}"}

    finally:
        db.close() 



router = Router(
    path="/ventas",
    route_handlers=[registrar_venta],
)

