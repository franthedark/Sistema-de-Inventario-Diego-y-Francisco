from app.models import Venta, DetalleVenta, Producto
from app.db import SessionLocal
from datetime import datetime
from typing import List, Dict
from litestar import Router, get

# Función para obtener el reporte de ventas en un rango de fechas
def generar_reporte_ventas(fecha_inicio: datetime, fecha_fin: datetime) -> Dict[str, float]:
    db = SessionLocal()  # Nueva sesión para asegurar que obtenemos los datos más recientes

    try:
        # Consultar las ventas en el rango de fechas
        ventas = db.query(Venta).filter(Venta.fecha >= fecha_inicio, Venta.fecha <= fecha_fin).all()

        total_productos_vendidos = 0
        monto_total_ventas = 0
        monto_total_ganancias = 0
        iva_tasa = 0.19  # Suponiendo un IVA del 19%

        for venta in ventas:
            # Asegurarse de que el total de la venta se calcula correctamente
            print(f"Procesando venta ID {venta.id}, total venta: {venta.total}")  # Log de depuración

            # Iterar sobre los detalles de la venta
            for detalle in venta.detalles:
                producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
                if producto:
                    # Calcular el precio total de la venta (sin IVA)
                    precio_total = detalle.cantidad * producto.precio
                    # Calcular el IVA de la venta
                    iva = precio_total * iva_tasa
                    # Calcular la ganancia (precio de venta - IVA - costo del producto)
                    ganancia = (producto.precio - iva) * detalle.cantidad

                    # Acumular totales
                    total_productos_vendidos += detalle.cantidad
                    monto_total_ventas += precio_total
                    monto_total_ganancias += ganancia

        # Generar el reporte con los resultados
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

# Endpoint GET para obtener el reporte de ventas
@get("/reporte-ventas")
async def obtener_reporte_ventas(fecha_inicio: str, fecha_fin: str) -> Dict[str, float]:
    # Convertir las fechas de string a datetime
    try:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        return {"error": "Formato de fecha inválido. Usa 'YYYY-MM-DD'."}

    # Llamar a la función que genera el reporte
    reporte = generar_reporte_ventas(fecha_inicio, fecha_fin)

    return reporte

# Router para las rutas de reportes
router = Router(
    path="/reportes",
    route_handlers=[obtener_reporte_ventas],
)
