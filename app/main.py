from fastapi import FastAPI

from app.routers.reservas import router as reservas_router

app = FastAPI(
    title="API de Reservas",
    version="0.1.0",
)

app.include_router(reservas_router)
