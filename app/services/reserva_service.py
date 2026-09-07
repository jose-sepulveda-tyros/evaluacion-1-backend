"""Casos de uso de reservas y reglas de negocio."""

from app.repositories import reserva_repository
from app.schemas.reserva import ReservaCrear, ReservaRespuesta


class HorarioInvalidoError(ValueError):
    pass


class ReservaNoEncontradaError(LookupError):
    pass


def crear_reserva(datos: ReservaCrear) -> ReservaRespuesta:
    if datos.hora_fin <= datos.hora_inicio:
        raise HorarioInvalidoError(
            "La hora de fin debe ser estrictamente posterior a la hora de inicio"
        )
    # La existencia de sala/estudiante y las demás reglas se integrarán
    # cuando estén disponibles los recursos y contratos del rol 2.
    return reserva_repository.crear(datos)


def listar_reservas() -> list[ReservaRespuesta]:
    return reserva_repository.listar()


def obtener_reserva(reserva_id: int) -> ReservaRespuesta:
    reserva = reserva_repository.obtener(reserva_id)
    if reserva is None:
        raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
    return reserva
