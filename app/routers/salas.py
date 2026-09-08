from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app.schemas.error import ErrorRespuesta
from app.schemas.sala import SalaActualizar, SalaCrear, SalaRespuesta
from app.services import sala_service

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post(
    "",
    response_model=SalaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una sala",
    responses={422: {"model": ErrorRespuesta, "description": "Datos de sala inválidos"}},
)
async def crear_sala(datos: SalaCrear, response: Response) -> SalaRespuesta:
    """Registra una sala en memoria y genera su ID."""
    sala = sala_service.crear_sala(datos)
    response.headers["Location"] = f"/salas/{sala.id}"
    return sala


@router.get("", response_model=list[SalaRespuesta], summary="Listar salas")
async def listar_salas() -> list[SalaRespuesta]:
    """Devuelve todas las salas registradas en memoria."""
    return sala_service.listar_salas()


@router.get(
    "/{sala_id}",
    response_model=SalaRespuesta,
    summary="Obtener una sala por ID",
    responses={
        404: {"model": ErrorRespuesta, "description": "La sala no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
)
async def obtener_sala(
    sala_id: Annotated[int, Path(gt=0, description="Identificador de la sala")],
) -> SalaRespuesta:
    """Consulta una sala existente por su identificador."""
    return sala_service.obtener_sala(sala_id)


@router.put(
    "/{sala_id}",
    response_model=SalaRespuesta,
    summary="Actualizar una sala",
    responses={
        404: {"model": ErrorRespuesta, "description": "La sala no existe"},
        409: {"model": ErrorRespuesta, "description": "Capacidad incompatible con reservas activas"},
        422: {"model": ErrorRespuesta, "description": "Datos de sala inválidos"},
    },
)
async def actualizar_sala(
    sala_id: Annotated[int, Path(gt=0, description="Identificador de la sala")],
    datos: SalaActualizar,
) -> SalaRespuesta:
    """Reemplaza los datos conservando el ID; omitir equipamiento lo deja vacío.

    Rechaza una capacidad inferior a la cantidad de personas de una reserva activa.
    """
    return sala_service.actualizar_sala(sala_id, datos)
