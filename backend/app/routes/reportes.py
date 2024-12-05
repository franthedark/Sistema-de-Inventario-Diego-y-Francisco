from litestar import Router, get
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Venta, DetalleVenta, Producto
from app.utils import parse_date
from typing import Dict, Any
from litestar.exceptions import HTTPException

# Suponemos que el IVA es un porcentaje fijo. Se puede ajustar si es necesario.
IVA_PORCENTAJE = 0.19  # 19% de IVA

@get("/ventas")
async def reporte_ventas(fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
    """Genera un reporte de ventas en un rango de fechas"""
    try:
        # Parsear las fechas recibidas como parámetros
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)

        # Verificar que la fecha de inicio no sea mayor que la fecha de fin
        if fecha_inicio > fecha_fin:
            return {"error": "La fecha de inicio no puede ser mayor que la fecha de fin"}

        with SessionLocal() as session:
            # Consulta para obtener las ventas dentro del rango de fechas
            ventas = (
                session.query(Venta)
                .filter(Venta.fecha.between(fecha_inicio, fecha_fin))
                .all()
            )

            # Depuración: Ver cuántas ventas se encuentran
            print(f"Ventas encontradas: {len(ventas)}")
            for venta in ventas:
                print(f"Venta ID: {venta.id}, Fecha: {venta.fecha}, Detalles: {len(venta.detalles)}")

            total_ventas = 0
            total_productos_vendidos = 0
            total_costo_productos = 0
            total_iva = 0

            # Iterar sobre las ventas y sus detalles
            for venta in ventas:
                try:
                    # Calcular el total de la venta usando la lógica del método calcular_total_venta
                    total_venta = 0
                    for detalle in venta.detalles:
                        # Buscar el producto de la venta
                        producto = session.query(Producto).filter(Producto.id == detalle.producto_id).first()
                        if not producto:
                            raise HTTPException(status_code=404, detail=f"Producto con ID {detalle.producto_id} no encontrado")

                        # Calcular el total de la venta (sin IVA)
                        total_venta += detalle.cantidad * producto.precio

                        # Para cada detalle de la venta, contar los productos y calcular el costo
                        costo_producto = detalle.cantidad * producto.precio
                        total_costo_productos += costo_producto

                        # Calcular el IVA para cada producto vendido y acumularlo
                        iva_producto = costo_producto * IVA_PORCENTAJE
                        total_iva += iva_producto

                        total_productos_vendidos += detalle.cantidad

                    total_ventas += total_venta

                except Exception as e:
                    # Manejo de errores para cada venta en caso de que algo falle
                    print(f"Error al procesar la venta {venta.id}: {e}")
                    continue  # Saltar al siguiente registro en caso de error

            # **Corregir cálculo de ganancias**: Ganancias = Ventas sin IVA - Costos de productos sin IVA
            ganancias = total_ventas - total_costo_productos
            print(f"Ganancias: {ganancias}")

            # Preparar el reporte final con los datos calculados
            reporte = {
                "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
                "total_ventas": total_ventas,
                "total_productos_vendidos": total_productos_vendidos,
                "total_iva": total_iva,
                "total_costo_productos": total_costo_productos,
                "ganancias": ganancias,
            }

        return reporte

    except HTTPException as e:
        # Manejo de excepciones de HTTPException
        return {"status_code": e.status_code, "detail": e.detail}
    
    except Exception as e:
        # Manejo de errores generales
        return {"status_code": 500, "detail": f"Error inesperado: {str(e)}"}

# Crear el router con la ruta correspondiente para generar el reporte
router = Router(
    path="/reportes",
    route_handlers=[
        reporte_ventas  # Función que maneja el reporte de ventas
    ],
)
