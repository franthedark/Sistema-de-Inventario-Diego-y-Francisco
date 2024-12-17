from litestar import Litestar
from litestar.static_files import StaticFilesConfig
from app.routes import users, productos, compras, ventas, reportes
from app.db import init_db
import os

# Inicialización de la base de datos
async def startup() -> None:
    """Inicializa la base de datos al arrancar la aplicación."""
    init_db()

# Ruta a la carpeta frontend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# Verificar si la carpeta existe
if not os.path.exists(FRONTEND_DIR):
    raise Exception(f"La carpeta {FRONTEND_DIR} no existe. Verifica la estructura.")

# Crear la aplicación Litestar
app = Litestar(
    route_handlers=[
        users.router,
        productos.router,
        compras.router,
        ventas.router,
        reportes.router,
    ],
    on_startup=[startup],
    static_files_config=[
        StaticFilesConfig(directories=[FRONTEND_DIR], path="/", html_mode=True)
    ],
)
