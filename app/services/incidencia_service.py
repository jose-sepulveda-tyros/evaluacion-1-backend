"""Registro y seguimiento de incidencias de salas."""

from app.repositories import incidencia_repository
from app.schemas.incidencia_sala import (
    IncidenciaSalaActualizar,
    IncidenciaSalaCrear,
    IncidenciaSalaRespuesta,
)
from app.services.sala_service import obtener_sala


class IncidenciaNoEncontradaError(LookupError):
    pass


def crear_incidencia(datos: IncidenciaSalaCrear) -> IncidenciaSalaRespuesta:
    obtener_sala(datos.sala_id)
    return incidencia_repository.crear(datos)


def listar_incidencias() -> list[IncidenciaSalaRespuesta]:
    return incidencia_repository.listar()


def actualizar_incidencia(
    incidencia_id: int, datos: IncidenciaSalaActualizar
) -> IncidenciaSalaRespuesta:
    incidencia = incidencia_repository.actualizar(incidencia_id, datos)
    if incidencia is None:
        raise IncidenciaNoEncontradaError(
            f"No existe una incidencia con el ID {incidencia_id}"
        )
    return incidencia
