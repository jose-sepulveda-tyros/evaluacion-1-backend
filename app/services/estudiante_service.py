"""Casos de uso de estudiantes sobre el repositorio en memoria del rol 2."""

from app.repositories import estudiante_repository
from app.schemas.estudiante import EstudianteCrear, EstudianteRespuesta


class EstudianteNoEncontradoError(LookupError):
    pass


def crear_estudiante(datos: EstudianteCrear) -> EstudianteRespuesta:
    return estudiante_repository.crear(datos)


def listar_estudiantes() -> list[EstudianteRespuesta]:
    return estudiante_repository.listar()


def obtener_estudiante(estudiante_id: int) -> EstudianteRespuesta:
    estudiante = estudiante_repository.obtener(estudiante_id)
    if estudiante is None:
        raise EstudianteNoEncontradoError(
            f"No existe un estudiante con el ID {estudiante_id}"
        )
    return estudiante
