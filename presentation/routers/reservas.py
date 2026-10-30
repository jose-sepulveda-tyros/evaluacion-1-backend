from typing import Annotated

from fastapi import APIRouter, Path, Query, Response, status

from app import openapi_examples as doc
from presentation.schemas.dtos.error import ErrorRespuesta
from presentation.schemas.dtos.reserva import (
    ReservaActualizar,
    ReservaConsulta,
    ReservaCrear,
    ReservaPagina,
    ReservaRespuesta,
)
from application.services.reserva_service import ReservaService
from presentation.dependencies import get_reserva_service
from fastapi import Depends
from domain.reserva import Reserva
from domain.consulta_reservas import ConsultaReservas, PaginaReservas

ServiceDep = Annotated[ReservaService, Depends(get_reserva_service)]

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "",
    response_model=ReservaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una reserva",
    responses={
        404: {"model": ErrorRespuesta, "description": "La sala o el estudiante no existe"},
        400: {"model": ErrorRespuesta, "description": "Horario, capacidad o límite diario inválidos"},
        409: {"model": ErrorRespuesta, "description": "La sala tiene una reserva superpuesta"},
        422: {"model": ErrorRespuesta, "description": "Datos de entrada inválidos"},
    },
    openapi_extra=doc.ejemplos(
        entrada=doc.RESERVA,
        codigo=201,
        salida=doc.RESERVA_RESPUESTA,
        errores={
            400: {"horario": doc.HORARIO, "capacidad": doc.CAPACIDAD, "limite_diario": doc.LIMITE},
            409: {"superposicion": doc.SUPERPOSICION},
            404: {"sala": doc.no_encontrado("una sala"), "estudiante": doc.no_encontrado("un estudiante")},
            422: {"campo_requerido": doc.validacion("body", "sala_id")},
        },
    ),
)
def crear_reserva(service: ServiceDep, datos: ReservaCrear, response: Response) -> Reserva:
    """Crea una reserva para una sala y un estudiante existentes.

    Valida capacidad, horarios, superposiciones y el límite diario de activas.
    """
    reserva = service.crear_reserva(Reserva(id=None, **datos.model_dump()))
    response.headers["Location"] = f"/reservas/{reserva.id}"
    return reserva


@router.get(
    "",
    response_model=ReservaPagina,
    summary="Listar reservas con filtros, ordenamiento y paginación",
    responses={422: {"model": ErrorRespuesta, "description": "Parámetros de consulta inválidos"}},
    openapi_extra=doc.ejemplos(
        salida=doc.PAGINA,
        errores={
            422: {"pagina_invalida": doc.validacion("query", "pagina")},
        },
    ),
)
def listar_reservas(service: ServiceDep, consulta: Annotated[ReservaConsulta, Query()]) -> PaginaReservas:
    """Filtra por fecha, sala, estudiante y estado; luego ordena y finalmente pagina.

    Los filtros se combinan. Por defecto ordena por ID ascendente y devuelve
    la página 1 con hasta 10 reservas. El total cuenta los resultados filtrados.
    Una página fuera de rango devuelve items vacío conservando los metadatos.
    Ejemplo: /reservas?sala_id=2&estado=activa&ordenar_por=fecha&direccion=asc&pagina=1&limite=10
    """
    return service.listar_reservas(ConsultaReservas(**consulta.model_dump()))


@router.get(
    "/{reserva_id}",
    response_model=ReservaRespuesta,
    summary="Obtener una reserva por ID",
    responses={
        404: {"model": ErrorRespuesta, "description": "La reserva no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
    openapi_extra=doc.ejemplos(
        salida=doc.RESERVA_RESPUESTA,
        errores={
            404: {"recurso": doc.no_encontrado("una reserva")},
            422: {"id_invalido": doc.validacion("path", "reserva_id")},
        },
    ),
)
def obtener_reserva(
    service: ServiceDep,
    reserva_id: Annotated[int, Path(gt=0, description="Identificador de la reserva")],
) -> Reserva:
    """Busca una reserva por su identificador; devuelve 404 si no existe."""
    return service.obtener_reserva(reserva_id)


@router.put(
    "/{reserva_id}",
    response_model=ReservaRespuesta,
    summary="Actualizar una reserva",
    responses={
        400: {"model": ErrorRespuesta, "description": "Horario, capacidad o límite diario inválidos"},
        404: {"model": ErrorRespuesta, "description": "La reserva, la sala o el estudiante no existe"},
        409: {"model": ErrorRespuesta, "description": "La sala tiene una reserva superpuesta"},
        422: {"model": ErrorRespuesta, "description": "Datos de entrada inválidos"},
    },
    openapi_extra=doc.ejemplos(
        entrada=doc.RESERVA,
        salida=doc.RESERVA_RESPUESTA,
        errores={
            400: {"horario": doc.HORARIO, "capacidad": doc.CAPACIDAD, "limite_diario": doc.LIMITE},
            409: {"superposicion": doc.SUPERPOSICION},
            404: {"recurso": doc.no_encontrado("una reserva"), "sala": doc.no_encontrado("una sala"), "estudiante": doc.no_encontrado("un estudiante")},
            422: {"campo_requerido": doc.validacion("body", "sala_id"), "id_invalido": doc.validacion("path", "reserva_id")},
        },
    ),
)
def actualizar_reserva(
    service: ServiceDep,
    reserva_id: Annotated[int, Path(gt=0, description="Identificador de la reserva")],
    datos: ReservaActualizar,
) -> Reserva:
    """Reemplaza los campos y conserva el ID, aplicando las mismas reglas de creación."""
    return service.actualizar_reserva(reserva_id, Reserva(id=reserva_id, **datos.model_dump()))


@router.delete(
    "/{reserva_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Eliminar una reserva",
    responses={409: {"model": ErrorRespuesta, "description": "Conflicto con recursos relacionados"},
        404: {"model": ErrorRespuesta, "description": "La reserva no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
    openapi_extra=doc.ejemplos(
        codigo=204,
        errores={
            404: {"recurso": doc.no_encontrado("una reserva")},
            422: {"id_invalido": doc.validacion("path", "reserva_id")},
        },
    ),
)
def eliminar_reserva(
    service: ServiceDep,
    reserva_id: Annotated[int, Path(gt=0, description="Identificador de la reserva")],
) -> Response:
    """Elimina una reserva de la base de datos; devuelve 204 sin cuerpo o 404 si no existe."""
    service.eliminar_reserva(reserva_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
