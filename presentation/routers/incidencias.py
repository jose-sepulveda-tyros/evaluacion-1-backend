from typing import Annotated

from fastapi import APIRouter, Path, status

from app import openapi_examples as doc
from presentation.schemas.dtos.error import ErrorRespuesta
from presentation.schemas.dtos.incidencia_sala import (
    IncidenciaSalaActualizar,
    IncidenciaSalaCrear,
    IncidenciaSalaRespuesta,
)
from application.services.incidencia_service import IncidenciaService
from presentation.dependencies import get_incidencia_service
from fastapi import Depends
from domain.incidencia_sala import IncidenciaSala

ServiceDep = Annotated[IncidenciaService, Depends(get_incidencia_service)]

router = APIRouter(prefix="/incidencias", tags=["Incidencias"])


@router.post(
    "",
    response_model=IncidenciaSalaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una incidencia de sala",
    responses={409: {"model": ErrorRespuesta, "description": "Conflicto con recursos relacionados"},
        404: {"model": ErrorRespuesta, "description": "La sala no existe"},
        422: {"model": ErrorRespuesta, "description": "Datos de incidencia inválidos"},
    },
    openapi_extra=doc.ejemplos(
        entrada=doc.INCIDENCIA,
        codigo=201,
        salida=doc.INCIDENCIA_RESPUESTA,
        errores={
            404: {"sala": doc.no_encontrado("una sala")},
            422: {"campo_requerido": doc.validacion("body", "sala_id")},
        },
    ),
)
def crear_incidencia(service: ServiceDep, datos: IncidenciaSalaCrear) -> IncidenciaSala:
    """Registra un reporte y su fecha para una sala existente; genera un ID.

    El estado resuelto es falso por defecto.
    """
    return service.crear_incidencia(IncidenciaSala(id=None, **datos.model_dump()))


@router.get(
    "",
    response_model=list[IncidenciaSalaRespuesta],
    summary="Listar incidencias",
    openapi_extra=doc.ejemplos(
        salida=[doc.INCIDENCIA_RESPUESTA],
    ),
)
def listar_incidencias(service: ServiceDep) -> list[IncidenciaSala]:
    """Devuelve todas las incidencias, tanto pendientes como resueltas."""
    return service.listar_incidencias()


@router.put(
    "/{incidencia_id}",
    response_model=IncidenciaSalaRespuesta,
    summary="Actualizar el estado de una incidencia",
    responses={409: {"model": ErrorRespuesta, "description": "Conflicto con recursos relacionados"},
        404: {"model": ErrorRespuesta, "description": "La incidencia no existe"},
        422: {"model": ErrorRespuesta, "description": "ID o estado inválido"},
    },
    openapi_extra=doc.ejemplos(
        entrada={"resuelto": True},
        salida={**doc.INCIDENCIA_RESPUESTA, "resuelto": True},
        errores={
            404: {"recurso": doc.no_encontrado("una incidencia")},
            422: {"campo_requerido": doc.validacion("body", "resuelto"), "id_invalido": doc.validacion("path", "incidencia_id")},
        },
    ),
)
def actualizar_incidencia(
    service: ServiceDep,
    incidencia_id: Annotated[int, Path(gt=0, description="Identificador de la incidencia")],
    datos: IncidenciaSalaActualizar,
) -> IncidenciaSala:
    """Establece resuelto en true o false, conservando sala, reporte, fecha e ID.

    Solo acepta el campo resuelto.
    """
    return service.actualizar_incidencia(incidencia_id, datos.resuelto)
