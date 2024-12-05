from litestar import Litestar
from app.routes import productos, compras, ventas, reportes
from app.db import init_db

# Definir la función de inicialización
async def startup() -> None:
    """Inicializa la base de datos al arrancar la aplicación."""
    init_db()

# Crear la aplicación y registrar las rutas
app = Litestar(
    route_handlers=[
        productos.router,
        compras.router,
        ventas.router,
        reportes.router
    ],
    on_startup=[startup],  # Registrar el manejador de inicio
)

