from fastapi import FastAPI

from app.errors import registrar_manejadores
from app.routers.estudiantes import router as estudiantes_router
from app.routers.reservas import router as reservas_router
from app.routers.salas import router as salas_router

app = FastAPI(
    title="API de Reservas",
    version="0.1.0",
)

registrar_manejadores(app)
app.include_router(reservas_router)
app.include_router(salas_router)
app.include_router(estudiantes_router)
