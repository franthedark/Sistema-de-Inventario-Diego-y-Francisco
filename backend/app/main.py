from litestar import Litestar
from app.routes import router
from app.database import init_db

init_db()  # Inicializa la base de datos
app = Litestar(route_handlers=[router])
