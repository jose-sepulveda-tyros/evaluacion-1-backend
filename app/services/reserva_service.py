"""Casos de uso de reservas y reglas de negocio."""

from app.repositories import reserva_repository
from app.schemas.reserva import ReservaActualizar, ReservaCrear, ReservaRespuesta


class HorarioInvalidoError(ValueError):
    pass


class ReservaNoEncontradaError(LookupError):
    pass


def validar_horario(datos: ReservaCrear | ReservaActualizar) -> None:
    if datos.hora_fin <= datos.hora_inicio:
        raise HorarioInvalidoError(
            "La hora de fin debe ser estrictamente posterior a la hora de inicio"
        )


def crear_reserva(datos: ReservaCrear) -> ReservaRespuesta:
    validar_horario(datos)
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


def actualizar_reserva(reserva_id: int, datos: ReservaActualizar) -> ReservaRespuesta:
    obtener_reserva(reserva_id)
    validar_horario(datos)
    reserva = reserva_repository.actualizar(reserva_id, datos)
    if reserva is None:
        raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
    return reserva


def eliminar_reserva(reserva_id: int) -> None:
    if not reserva_repository.eliminar(reserva_id):
        raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
