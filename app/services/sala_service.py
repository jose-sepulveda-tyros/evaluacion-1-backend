"""Casos de uso de salas y coherencia con las reservas activas."""

from app.repositories import reserva_repository, sala_repository
from app.schemas.sala import SalaActualizar, SalaCrear, SalaRespuesta


class SalaNoEncontradaError(LookupError):
    pass


class CapacidadEnConflictoError(ValueError):
    pass


def crear_sala(datos: SalaCrear) -> SalaRespuesta:
    return sala_repository.crear(datos)


def listar_salas() -> list[SalaRespuesta]:
    return sala_repository.listar()


def obtener_sala(sala_id: int) -> SalaRespuesta:
    sala = sala_repository.obtener(sala_id)
    if sala is None:
        raise SalaNoEncontradaError(f"No existe una sala con el ID {sala_id}")
    return sala


def actualizar_sala(sala_id: int, datos: SalaActualizar) -> SalaRespuesta:
    obtener_sala(sala_id)
    for reserva in reserva_repository.listar():
        if (
            reserva.sala_id == sala_id
            and reserva.estado == "activa"
            and reserva.cantidad_personas > datos.capacidad
        ):
            raise CapacidadEnConflictoError(
                "La capacidad propuesta es menor que la cantidad de personas de una reserva activa"
            )
    sala = sala_repository.actualizar(sala_id, datos)
    if sala is None:
        raise SalaNoEncontradaError(f"No existe una sala con el ID {sala_id}")
    return sala
