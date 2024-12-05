from litestar import Router, post
from app.models import Compra, DetalleCompra, Producto
from app.db import engine, SessionLocal
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from litestar.exceptions import HTTPException

# Esquemas para recibir los datos de la compra
class DetalleCompraSchema(BaseModel):
    producto_id: int
    cantidad: int

class CompraSchema(BaseModel):
    proveedor: str
    detalles: List[DetalleCompraSchema]

@post("/")
async def registrar_compra(data: CompraSchema) -> Dict[str, str]:
    """Registra una nueva compra y actualiza el stock"""
    try:
        # Usar la sesión configurada correctamente
        db: Session = SessionLocal()

        fecha_compra = datetime.utcnow()

        # Crear la compra
        compra = Compra(proveedor=data.proveedor, fecha=fecha_compra)
        db.add(compra)
        db.commit()
        db.refresh(compra)  # Obtener el ID de la compra recién insertada

        detalles_respuesta = []  # Para almacenar los detalles de la respuesta
        total_compra = 0

        # Procesar cada detalle de la compra
        for detalle in data.detalles:
            producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} no encontrado")

            # Calcular precio total (precio * cantidad)
            precio_total = producto.precio * detalle.cantidad
            total_compra += precio_total

            # Actualizar el stock del producto: aumentar el stock por la cantidad comprada
            producto.stock += detalle.cantidad
            db.commit()  # Guardar la actualización del stock

            # Registrar el detalle de la compra
            detalle_compra = DetalleCompra(
                compra_id=compra.id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio=producto.precio
            )
            db.add(detalle_compra)

            # Crear respuesta del detalle
            detalles_respuesta.append({
                "producto_id": detalle.producto_id,
                "producto_nombre": producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_total": precio_total,
                "proveedor": data.proveedor,
                "fecha": fecha_compra
            })

        # Actualizar el total de la compra en la tabla 'compras'
        compra.total = total_compra
        db.commit()

        # Responder con los detalles de la compra
        return {
            "message": "Compra registrada exitosamente",
            "compra_id": compra.id,
            "detalles": detalles_respuesta,
            "fecha_compra": fecha_compra,
            "total_compra": total_compra
        }

    except HTTPException as e:
        # Manejo de errores específicos
        return {"status_code": e.status_code, "detail": e.detail}
    
    except Exception as e:
        # Manejo de errores generales
        db.rollback()  # En caso de error, revertir la transacción
        return {"status_code": 500, "detail": f"Error inesperado: {str(e)}"}

    finally:
        db.close()  # Cerrar la sesión al final

# Router para la ruta /compras
router = Router(
    path="/compras",
    route_handlers=[registrar_compra],
)
