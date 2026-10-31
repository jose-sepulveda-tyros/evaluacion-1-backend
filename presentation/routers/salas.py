from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app import openapi_examples as doc
from presentation.schemas.dtos.error import ErrorRespuesta
from presentation.schemas.dtos.sala import SalaActualizar, SalaCrear, SalaRespuesta
from application.services.sala_service import SalaService
from presentation.dependencies import get_sala_service
from fastapi import Depends
from domain.sala import Sala

ServiceDep = Annotated[SalaService, Depends(get_sala_service)]

router = APIRouter(prefix="/salas", tags=["Salas"])


@router.post(
    "",
    response_model=SalaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una sala",
    responses={409: {"model": ErrorRespuesta, "description": "Conflicto con recursos relacionados"}, 422: {"model": ErrorRespuesta, "description": "Datos de sala inválidos"}},
    openapi_extra=doc.ejemplos(
        entrada=doc.SALA,
        codigo=201,
        salida=doc.SALA_RESPUESTA,
        errores={
            422: {"campo_requerido": doc.validacion("body", "nombre")},
        },
    ),
)
def crear_sala(service: ServiceDep, datos: SalaCrear, response: Response) -> Sala:
    """Registra una sala en la base de datos y genera su ID."""
    sala = service.crear_sala(Sala(id=None, **datos.model_dump()))
    response.headers["Location"] = f"/salas/{sala.id}"
    return sala


@router.get(
    "",
    response_model=list[SalaRespuesta],
    summary="Listar salas",
    openapi_extra=doc.ejemplos(
        salida=[doc.SALA_RESPUESTA],
    ),
)
def listar_salas(service: ServiceDep) -> list[Sala]:
    """Devuelve todas las salas registradas en la base de datos."""
    return service.listar_salas()


@router.get(
    "/{sala_id}",
    response_model=SalaRespuesta,
    summary="Obtener una sala por ID",
    responses={
        404: {"model": ErrorRespuesta, "description": "La sala no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
    openapi_extra=doc.ejemplos(
        salida=doc.SALA_RESPUESTA,
        errores={
            404: {"recurso": doc.no_encontrado("una sala")},
            422: {"id_invalido": doc.validacion("path", "sala_id")},
        },
    ),
)
def obtener_sala(
    service: ServiceDep,
    sala_id: Annotated[int, Path(gt=0, description="Identificador de la sala")],
) -> Sala:
    """Consulta una sala existente por su identificador."""
    return service.obtener_sala(sala_id)


@router.put(
    "/{sala_id}",
    response_model=SalaRespuesta,
    summary="Actualizar una sala",
    responses={
        404: {"model": ErrorRespuesta, "description": "La sala no existe"},
        409: {"model": ErrorRespuesta, "description": "Capacidad incompatible con reservas activas"},
        422: {"model": ErrorRespuesta, "description": "Datos de sala inválidos"},
    },
    openapi_extra=doc.ejemplos(
        entrada=doc.SALA,
        salida=doc.SALA_RESPUESTA,
        errores={
            409: {"capacidad": doc.CONFLICTO_CAPACIDAD},
            404: {"recurso": doc.no_encontrado("una sala")},
            422: {"campo_requerido": doc.validacion("body", "nombre"), "id_invalido": doc.validacion("path", "sala_id")},
        },
    ),
)
def actualizar_sala(
    service: ServiceDep,
    sala_id: Annotated[int, Path(gt=0, description="Identificador de la sala")],
    datos: SalaActualizar,
) -> Sala:
    """Reemplaza los datos conservando el ID; omitir equipamiento lo deja vacío.

    Rechaza una capacidad inferior a la cantidad de personas de una reserva activa.
    """
    return service.actualizar_sala(sala_id, Sala(id=sala_id, **datos.model_dump()))
