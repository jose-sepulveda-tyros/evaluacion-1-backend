from typing import Annotated

from fastapi import APIRouter, Path, status

from app.schemas.error import ErrorRespuesta
from app.schemas.incidencia_sala import (
    IncidenciaSalaActualizar,
    IncidenciaSalaCrear,
    IncidenciaSalaRespuesta,
)
from app.services import incidencia_service

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])


@router.post(
    "",
    response_model=IncidenciaSalaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una incidencia de sala",
    responses={
        404: {"model": ErrorRespuesta, "description": "La sala no existe"},
        422: {"model": ErrorRespuesta, "description": "Datos de incidencia inválidos"},
    },
)
async def crear_incidencia(datos: IncidenciaSalaCrear) -> IncidenciaSalaRespuesta:
    """Registra un reporte y su fecha para una sala existente; genera un ID.

    El estado resuelto es falso por defecto.
    """
    return incidencia_service.crear_incidencia(datos)


@router.get("", response_model=list[IncidenciaSalaRespuesta], summary="Listar incidencias")
async def listar_incidencias() -> list[IncidenciaSalaRespuesta]:
    """Devuelve todas las incidencias, tanto pendientes como resueltas."""
    return incidencia_service.listar_incidencias()


@router.put(
    "/{incidencia_id}",
    response_model=IncidenciaSalaRespuesta,
    summary="Actualizar el estado de una incidencia",
    responses={
        404: {"model": ErrorRespuesta, "description": "La incidencia no existe"},
        422: {"model": ErrorRespuesta, "description": "ID o estado inválido"},
    },
)
async def actualizar_incidencia(
    incidencia_id: Annotated[int, Path(gt=0, description="Identificador de la incidencia")],
    datos: IncidenciaSalaActualizar,
) -> IncidenciaSalaRespuesta:
    """Establece resuelto en true o false, conservando sala, reporte, fecha e ID.

    Solo acepta el campo resuelto.
    """
    return incidencia_service.actualizar_incidencia(incidencia_id, datos)
