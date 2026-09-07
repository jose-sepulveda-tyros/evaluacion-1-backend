from typing import Annotated

from fastapi import APIRouter, Path, Query, Response, status

from app.schemas.error import ErrorRespuesta
from app.schemas.reserva import (
    ReservaActualizar,
    ReservaConsulta,
    ReservaCrear,
    ReservaPagina,
    ReservaRespuesta,
)
from app.services import reserva_service

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "",
    response_model=ReservaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una reserva",
    responses={
        400: {"model": ErrorRespuesta, "description": "Horario inválido o límite diario de reservas excedido"},
        409: {"model": ErrorRespuesta, "description": "La sala tiene una reserva superpuesta"},
        422: {"model": ErrorRespuesta, "description": "Datos de entrada inválidos"},
    },
)
async def crear_reserva(datos: ReservaCrear, response: Response) -> ReservaRespuesta:
    """Crea una reserva; valida horarios, superposiciones y el límite diario de activas."""
    reserva = reserva_service.crear_reserva(datos)
    response.headers["Location"] = f"/reservas/{reserva.id}"
    return reserva


@router.get(
    "",
    response_model=ReservaPagina,
    summary="Listar reservas con filtros, ordenamiento y paginación",
    responses={422: {"model": ErrorRespuesta, "description": "Parámetros de consulta inválidos"}},
)
async def listar_reservas(consulta: Annotated[ReservaConsulta, Query()]) -> ReservaPagina:
    """Filtra por fecha, sala, estudiante y estado; luego ordena y finalmente pagina.

    Los filtros se combinan. Por defecto ordena por ID ascendente y devuelve
    la página 1 con hasta 10 reservas. El total cuenta los resultados filtrados.
    Una página fuera de rango devuelve items vacío conservando los metadatos.
    Ejemplo: /reservas?sala_id=2&estado=activa&ordenar_por=fecha&direccion=asc&pagina=1&limite=10
    """
    return reserva_service.listar_reservas(consulta)


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


@router.put(
    "/{reserva_id}",
    response_model=ReservaRespuesta,
    summary="Actualizar una reserva",
    responses={
        400: {"model": ErrorRespuesta, "description": "Horario inválido o límite diario de reservas excedido"},
        404: {"model": ErrorRespuesta, "description": "La reserva no existe"},
        409: {"model": ErrorRespuesta, "description": "La sala tiene una reserva superpuesta"},
        422: {"model": ErrorRespuesta, "description": "Datos de entrada inválidos"},
    },
)
async def actualizar_reserva(
    reserva_id: Annotated[int, Path(gt=0, description="Identificador de la reserva")],
    datos: ReservaActualizar,
) -> ReservaRespuesta:
    """Reemplaza los campos y conserva el ID, aplicando las mismas reglas de creación."""
    return reserva_service.actualizar_reserva(reserva_id, datos)


@router.delete(
    "/{reserva_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Eliminar una reserva",
    responses={
        404: {"model": ErrorRespuesta, "description": "La reserva no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
)
async def eliminar_reserva(
    reserva_id: Annotated[int, Path(gt=0, description="Identificador de la reserva")],
) -> Response:
    """Elimina una reserva de la memoria; devuelve 204 sin cuerpo o 404 si no existe."""
    reserva_service.eliminar_reserva(reserva_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
