from litestar import Litestar
from litestar.static_files import StaticFilesConfig
from app.routes import users, productos, compras, ventas, reportes
from app.db import init_db, verify_user, get_db
from fastapi import FastAPI, Form, Depends
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

async def startup() -> None:
    """Inicializa la base de datos al arrancar la aplicación."""
    init_db()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


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