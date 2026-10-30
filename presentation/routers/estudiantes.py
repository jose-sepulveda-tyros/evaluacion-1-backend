from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app import openapi_examples as doc
from presentation.schemas.dtos.error import ErrorRespuesta
from presentation.schemas.dtos.estudiante import EstudianteCrear, EstudianteRespuesta
from application.services.estudiante_service import EstudianteService
from presentation.dependencies import get_estudiante_service
from fastapi import Depends
from domain.estudiante import Estudiante

ServiceDep = Annotated[EstudianteService, Depends(get_estudiante_service)]

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.post(
    "",
    response_model=EstudianteRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un estudiante",
    responses={409: {"model": ErrorRespuesta, "description": "Conflicto con recursos relacionados"}, 422: {"model": ErrorRespuesta, "description": "Datos del estudiante inválidos"}},
    openapi_extra=doc.ejemplos(
        entrada=doc.ESTUDIANTE,
        codigo=201,
        salida=doc.ESTUDIANTE_RESPUESTA,
        errores={
            422: {"campo_requerido": doc.validacion("body", "nombre")},
        },
    ),
)
def crear_estudiante(service: ServiceDep, datos: EstudianteCrear, response: Response) -> Estudiante:
    """Registra nombre, carrera, correo y estado activo en la base de datos; genera un ID."""
    estudiante = service.crear_estudiante(Estudiante(id=None, **datos.model_dump()))
    response.headers["Location"] = f"/estudiantes/{estudiante.id}"
    return estudiante


@router.get(
    "",
    response_model=list[EstudianteRespuesta],
    summary="Listar estudiantes",
    openapi_extra=doc.ejemplos(
        salida=[doc.ESTUDIANTE_RESPUESTA],
    ),
)
def listar_estudiantes(service: ServiceDep) -> list[Estudiante]:
    """Devuelve todos los estudiantes registrados, incluidos los inactivos."""
    return service.listar_estudiantes()


@router.get(
    "/{estudiante_id}",
    response_model=EstudianteRespuesta,
    summary="Obtener un estudiante por ID",
    responses={
        404: {"model": ErrorRespuesta, "description": "El estudiante no existe"},
        422: {"model": ErrorRespuesta, "description": "ID inválido"},
    },
    openapi_extra=doc.ejemplos(
        salida=doc.ESTUDIANTE_RESPUESTA,
        errores={
            404: {"recurso": doc.no_encontrado("un estudiante")},
            422: {"id_invalido": doc.validacion("path", "estudiante_id")},
        },
    ),
)
def obtener_estudiante(
    service: ServiceDep,
    estudiante_id: Annotated[int, Path(gt=0, description="Identificador del estudiante")],
) -> Estudiante:
    """Consulta un estudiante por su identificador; devuelve 404 si no existe."""
    return service.obtener_estudiante(estudiante_id)
