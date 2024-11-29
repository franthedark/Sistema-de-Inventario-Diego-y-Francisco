from litestar import Litestar
from app.routes import router
from app.database import init_db

# Inicializa la base de datos
init_db()

# Crear la app
app = Litestar(route_handlers=[router])

# Si es necesario, puedes ejecutar la app aquí o con el comando uvicorn
if __name__ == "__main__":
    app.run()
