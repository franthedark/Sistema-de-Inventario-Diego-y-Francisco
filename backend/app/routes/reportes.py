from litestar import Router, get
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db import SessionLocal
from app.models import Venta, DetalleVenta, Producto
from app.utils import parse_date
from app.routes.ventas import calcular_total_venta  # Importamos lógica desde ventas.py
from typing import Dict, Any

@get("/ventas")
async def reporte_ventas(fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
    """Genera un reporte de ventas en un rango de fechas"""
    fecha_inicio = parse_date(fecha_inicio)
    fecha_fin = parse_date(fecha_fin)

    if fecha_inicio > fecha_fin:
        return {"error": "La fecha de inicio no puede ser mayor que la fecha de fin"}

    with SessionLocal() as session:
        # Consulta para obtener datos agregados directamente desde la base de datos
        ventas = (
            session.query(Venta)
            .filter(Venta.fecha.between(fecha_inicio, fecha_fin))
            .all()
        )

        total_ventas = 0
        total_productos_vendidos = 0
        total_costo_productos = 0

        for venta in ventas:
            # Usamos la función desde ventas.py para calcular el total de cada venta
            total_ventas += calcular_total_venta(venta)
            for detalle in venta.detalles:
                total_productos_vendidos += detalle.cantidad
                total_costo_productos += detalle.cantidad * detalle.producto.precio

        ganancias = total_ventas - total_costo_productos

        reporte = {
            "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
            "total_ventas": total_ventas,
            "total_productos_vendidos": total_productos_vendidos,
            "ganancias": ganancias,
        }

    return reporte

router = Router(
    path="/reportes",
    route_handlers=[
        reporte_ventas  # Ejemplo de función para manejar una venta
    ],
)