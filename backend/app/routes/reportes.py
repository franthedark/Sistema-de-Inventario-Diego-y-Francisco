from app.models import Venta, Producto
from app.db import SessionLocal
from datetime import datetime
from typing import Dict
from litestar import Router, get

# Obtener el reporte de ventas en un rango de fechas
def generar_reporte_ventas(fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, float]:
    db = SessionLocal()  

    try:
        # Consultar las ventas en el rango de fechas
        ventas = db.query(Venta).filter(Venta.fecha >= fecha_inicio, Venta.fecha <= fecha_fin).all()

        total_productos_vendidos = 0
        monto_total_ventas = 0
        monto_total_ganancias = 0
        iva_tasa = 0.19  

        for venta in ventas:
            print(f"Procesando venta ID {venta.id}, total venta: {venta.total}")  

            # Iterar sobre los detalles de la venta
            for detalle in venta.detalles:
                producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
                if producto:
                    precio_total = detalle.cantidad * producto.precio
                    iva = precio_total * iva_tasa
                    ganancia = (producto.precio - iva) * detalle.cantidad

                    total_productos_vendidos += detalle.cantidad
                    monto_total_ventas += precio_total
                    monto_total_ganancias += ganancia

        reporte = {
            "total_productos_vendidos": total_productos_vendidos,
            "monto_total_ventas": monto_total_ventas,
            "monto_total_ganancias": monto_total_ganancias
        }

        return reporte

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()


@get("/reporte-ventas")
async def obtener_reporte_ventas(fecha_inicio: str, fecha_fin: str) -> Dict[str, float]:
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        return {"error": "Formato de fecha inválido. Usa 'YYYY-MM-DD'."}
    reporte = generar_reporte_ventas(fecha_inicio, fecha_fin)

    return reporte

router = Router(
    path="/reportes",
    route_handlers=[obtener_reporte_ventas],
)
