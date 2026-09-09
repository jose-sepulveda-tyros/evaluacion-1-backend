from typing import Annotated

from fastapi import APIRouter, Path, Response, status

from app.schemas.error import ErrorRespuesta
from app.schemas.estudiante import EstudianteCrear, EstudianteRespuesta
from app.services import estudiante_service

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.post(
    "",
    response_model=EstudianteRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un estudiante",
    responses={422: {"model": ErrorRespuesta, "description": "Datos del estudiante inválidos"}},
)
async def crear_estudiante(datos: EstudianteCrear, response: Response) -> EstudianteRespuesta:
    """Registra nombre, carrera, correo y estado activo en memoria; genera un ID."""
    estudiante = estudiante_service.crear_estudiante(datos)
    response.headers["Location"] = f"/estudiantes/{estudiante.id}"
    return estudiante


@router.get("", response_model=list[EstudianteRespuesta], summary="Listar estudiantes")
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
)
async def obtener_estudiante(
    estudiante_id: Annotated[int, Path(gt=0, description="Identificador del estudiante")],
) -> EstudianteRespuesta:
    """Consulta un estudiante por su identificador; devuelve 404 si no existe."""
    return estudiante_service.obtener_estudiante(estudiante_id)
