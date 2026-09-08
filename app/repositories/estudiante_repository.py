from itertools import count

from app.schemas.estudiante import EstudianteActualizar, EstudianteCrear, EstudianteRespuesta

_estudiantes: dict[int, EstudianteRespuesta] = {}
_ids = count(1)


def crear(datos: EstudianteCrear) -> EstudianteRespuesta:
    estudiante = EstudianteRespuesta(id=next(_ids), **datos.model_dump())
    _estudiantes[estudiante.id] = estudiante
    return estudiante.model_copy(deep=True)


def listar() -> list[EstudianteRespuesta]:
    return [estudiante.model_copy(deep=True) for estudiante in _estudiantes.values()]


def obtener(estudiante_id: int) -> EstudianteRespuesta | None:
    estudiante = _estudiantes.get(estudiante_id)
    return estudiante.model_copy(deep=True) if estudiante is not None else None


def actualizar(estudiante_id: int, datos: EstudianteActualizar) -> EstudianteRespuesta | None:
    if estudiante_id not in _estudiantes:
        return None
    estudiante = EstudianteRespuesta(id=estudiante_id, **datos.model_dump())
    _estudiantes[estudiante_id] = estudiante
    return estudiante.model_copy(deep=True)


def existe(estudiante_id: int) -> bool:
    # Para que el rol de reglas de negocio valide estudiante_id antes de crear reservas.
    return estudiante_id in _estudiantes