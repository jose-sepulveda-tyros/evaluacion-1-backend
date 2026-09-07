from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app.schemas.error import ErrorRespuesta
from app.schemas.reserva import ReservaCrear, ReservaRespuesta
from app.services import reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "",
    response_model=ReservaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una reserva",
    responses={
        400: {"model": ErrorRespuesta, "description": "El horario viola una regla de negocio"},
        422: {"model": ErrorRespuesta, "description": "Datos de entrada inválidos"},
    },
)
async def crear_reserva(datos: ReservaCrear, response: Response) -> ReservaRespuesta:
    """Registra una reserva en memoria y genera su ID; valida el orden de las horas."""
    reserva = reserva_service.crear_reserva(datos)
    response.headers["Location"] = f"/reservas/{reserva.id}"
    return reserva


@router.get("", response_model=list[ReservaRespuesta], summary="Listar reservas")
async def listar_reservas() -> list[ReservaRespuesta]:
    """Devuelve las reservas en memoria. La consulta avanzada se agregará posteriormente."""
    return reserva_service.listar_reservas()


@router.get(
    "/{reserva_id}",
    response_model=ReservaRespuesta,
    summary="Obtener una reserva por ID",
    responses={
        404: {"model": ErrorRespuesta, "description": "La reserva no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
)
async def obtener_reserva(
    reserva_id: Annotated[int, Path(gt=0, description="Identificador de la reserva")],
) -> ReservaRespuesta:
    """Busca una reserva por su identificador; devuelve 404 si no existe."""
    return reserva_service.obtener_reserva(reserva_id)
