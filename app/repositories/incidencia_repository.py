from itertools import count

from app.schemas.incidencia_sala import (
    IncidenciaSalaActualizar,
    IncidenciaSalaCrear,
    IncidenciaSalaRespuesta,
)

_incidencias: dict[int, IncidenciaSalaRespuesta] = {}
_ids = count(1)


def crear(datos: IncidenciaSalaCrear) -> IncidenciaSalaRespuesta:
    incidencia = IncidenciaSalaRespuesta(id=next(_ids), **datos.model_dump())
    _incidencias[incidencia.id] = incidencia
    return incidencia.model_copy(deep=True)


def listar() -> list[IncidenciaSalaRespuesta]:
    return [incidencia.model_copy(deep=True) for incidencia in _incidencias.values()]


def obtener(incidencia_id: int) -> IncidenciaSalaRespuesta | None:
    incidencia = _incidencias.get(incidencia_id)
    return incidencia.model_copy(deep=True) if incidencia is not None else None


def actualizar(
    incidencia_id: int, datos: IncidenciaSalaActualizar
) -> IncidenciaSalaRespuesta | None:
    incidencia = _incidencias.get(incidencia_id)
    if incidencia is None:
        return None
    actualizada = incidencia.model_copy(update={"resuelto": datos.resuelto})
    _incidencias[incidencia_id] = actualizada
    return actualizada.model_copy(deep=True)