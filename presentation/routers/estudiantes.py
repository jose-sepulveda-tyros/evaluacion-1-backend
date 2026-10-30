from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app import openapi_examples as doc
from presentation.schemas.dtos.error import ErrorRespuesta
from presentation.schemas.dtos.estudiante import EstudianteCrear, EstudianteRespuesta
from application.services import estudiante_service

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.post(
    "",
    response_model=EstudianteRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un estudiante",
    responses={422: {"model": ErrorRespuesta, "description": "Datos del estudiante inválidos"}},
    openapi_extra=doc.ejemplos(
        entrada=doc.ESTUDIANTE,
        codigo=201,
        salida=doc.ESTUDIANTE_RESPUESTA,
        errores={
            422: {"campo_requerido": doc.validacion("body", "nombre")},
        },
    ),
)
async def crear_estudiante(datos: EstudianteCrear, response: Response) -> EstudianteRespuesta:
    """Registra nombre, carrera, correo y estado activo en memoria; genera un ID."""
    estudiante = estudiante_service.crear_estudiante(datos)
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
async def listar_estudiantes() -> list[EstudianteRespuesta]:
    """Devuelve todos los estudiantes registrados, incluidos los inactivos."""
    return estudiante_service.listar_estudiantes()


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
async def obtener_estudiante(
    estudiante_id: Annotated[int, Path(gt=0, description="Identificador del estudiante")],
) -> EstudianteRespuesta:
    """Consulta un estudiante por su identificador; devuelve 404 si no existe."""
    return estudiante_service.obtener_estudiante(estudiante_id)
