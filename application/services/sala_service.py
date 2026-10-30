"""Casos de uso de salas y coherencia con las reservas activas."""

from domain.sala import Sala


class SalaNoEncontradaError(LookupError):
    pass


class CapacidadEnConflictoError(ValueError):
    pass


class SalaService:
    def __init__(self, sala_repository, reserva_repository):
        self.sala_repository = sala_repository
        self.reserva_repository = reserva_repository

    def crear_sala(self, datos: Sala) -> Sala:
        return self.sala_repository.crear(datos)

    def listar_salas(self) -> list[Sala]:
        return self.sala_repository.listar()

    def obtener_sala(self, sala_id: int) -> Sala:
        sala = self.sala_repository.obtener(sala_id)
        if sala is None:
            raise SalaNoEncontradaError(f"No existe una sala con el ID {sala_id}")
        return sala

    def actualizar_sala(self, sala_id: int, datos: Sala) -> Sala:
        self.sala_repository.bloquear_reglas()
        self.obtener_sala(sala_id)
        for reserva in self.reserva_repository.listar():
            if (
                reserva.sala_id == sala_id
                and reserva.estado == "activa"
                and reserva.cantidad_personas > datos.capacidad
            ):
                raise CapacidadEnConflictoError(
                    "La capacidad propuesta es menor que la cantidad de personas de una reserva activa"
                )
        sala = self.sala_repository.actualizar(sala_id, datos)
        if sala is None:
            raise SalaNoEncontradaError(f"No existe una sala con el ID {sala_id}")
        return sala
