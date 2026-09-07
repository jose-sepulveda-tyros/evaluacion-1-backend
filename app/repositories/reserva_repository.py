"""Almacenamiento mínimo en memoria, pendiente de integración con el rol 2."""

from itertools import count

from app.schemas.reserva import ReservaActualizar, ReservaCrear, ReservaRespuesta

_reservas: dict[int, ReservaRespuesta] = {}
_ids = count(1)


def crear(datos: ReservaCrear) -> ReservaRespuesta:
    reserva = ReservaRespuesta(id=next(_ids), **datos.model_dump())
    _reservas[reserva.id] = reserva
    return reserva.model_copy(deep=True)


def listar() -> list[ReservaRespuesta]:
    return [reserva.model_copy(deep=True) for reserva in _reservas.values()]


def obtener(reserva_id: int) -> ReservaRespuesta | None:
    reserva = _reservas.get(reserva_id)
    return reserva.model_copy(deep=True) if reserva is not None else None


def actualizar(reserva_id: int, datos: ReservaActualizar) -> ReservaRespuesta | None:
    if reserva_id not in _reservas:
        return None
    reserva = ReservaRespuesta(id=reserva_id, **datos.model_dump())
    _reservas[reserva_id] = reserva
    return reserva.model_copy(deep=True)


def eliminar(reserva_id: int) -> bool:
    return _reservas.pop(reserva_id, None) is not None
