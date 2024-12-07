from litestar import Router, post
from app.models import Compra, DetalleCompra, Producto
from app.db import SessionLocal
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from litestar.exceptions import HTTPException

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
        db: Session = SessionLocal()

        fecha_compra = datetime.utcnow()
        compra = Compra(proveedor=data.proveedor, fecha=fecha_compra)
        db.add(compra)
        db.commit()
        db.refresh(compra)

        total_compra = 0
        total_productos_vendidos = 0
        total_costo_productos = 0

        for detalle in data.detalles:
            producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} no encontrado")
            
            if not producto.estado:
                raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} deshabilitado")

            precio_total = producto.precio * detalle.cantidad
            total_compra += precio_total
            total_productos_vendidos += detalle.cantidad
            total_costo_productos += producto.precio * detalle.cantidad

            producto.stock += detalle.cantidad
            db.commit()

            detalle_compra = DetalleCompra(
                compra_id=compra.id,
                producto_id=detalle.producto_id,
                cantidad=detalle.cantidad,
                precio=producto.precio
            )
            db.add(detalle_compra)

        compra.total = total_compra
        compra.total_productos_vendidos = total_productos_vendidos
        compra.total_costo_productos = total_costo_productos
        db.commit()

        return {
            "message": "Compra registrada exitosamente",
            "compra_id": compra.id,
            "total": total_compra,
            "total_productos_vendidos": total_productos_vendidos,
            "total_costo_productos": total_costo_productos,
        }

    except HTTPException as e:
        return {"status_code": e.status_code, "detail": e.detail}

    except Exception as e:
        db.rollback()
        return {"status_code": 500, "detail": f"Error inesperado: {str(e)}"}

    finally:
        db.close()


router = Router(
    path="/compras",
    route_handlers=[registrar_compra],
)
