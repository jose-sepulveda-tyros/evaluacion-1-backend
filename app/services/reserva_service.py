"""Casos de uso de reservas y reglas de negocio."""

from app.repositories import reserva_repository
from app.schemas.reserva import (
    ReservaActualizar,
    ReservaConsulta,
    ReservaCrear,
    ReservaPagina,
    ReservaRespuesta,
)


class HorarioInvalidoError(ValueError):
    pass


class ReservaSuperpuestaError(ValueError):
    pass


class LimiteReservasError(ValueError):
    pass


class ReservaNoEncontradaError(LookupError):
    pass


def validar_horario(datos: ReservaCrear | ReservaActualizar) -> None:
    if datos.hora_fin <= datos.hora_inicio:
        raise HorarioInvalidoError(
            "La hora de fin debe ser estrictamente posterior a la hora de inicio"
        )


def validar_reserva(
    datos: ReservaCrear | ReservaActualizar, reserva_id: int | None = None
) -> None:
    validar_horario(datos)
    if datos.estado != "activa":
        return

    # Al actualizar, la reserva no debe entrar en conflicto consigo misma.
    activas_del_dia = [
        reserva
        for reserva in reserva_repository.listar()
        if reserva.id != reserva_id
        and reserva.estado == "activa"
        and reserva.fecha == datos.fecha
    ]
    for reserva in activas_del_dia:
        # Los extremos son abiertos al comparar: 10-11 y 11-12 son compatibles.
        if (
            reserva.sala_id == datos.sala_id
            and datos.hora_inicio < reserva.hora_fin
            and datos.hora_fin > reserva.hora_inicio
        ):
            raise ReservaSuperpuestaError(
                "La sala ya tiene una reserva activa que se superpone con ese horario"
            )

    cantidad_activas = sum(
        reserva.estudiante_id == datos.estudiante_id for reserva in activas_del_dia
    )
    if cantidad_activas >= 2:
        raise LimiteReservasError(
            "Un estudiante no puede tener más de 2 reservas activas en el mismo día"
        )


def crear_reserva(datos: ReservaCrear) -> ReservaRespuesta:
    validar_reserva(datos)
    # La existencia de sala/estudiante y la capacidad se integrarán
    # cuando estén disponibles los recursos y contratos del rol 2.
    return reserva_repository.crear(datos)


def listar_reservas(consulta: ReservaConsulta) -> ReservaPagina:
    reservas = reserva_repository.listar()
    for campo in ("fecha", "sala_id", "estudiante_id", "estado"):
        valor = getattr(consulta, campo)
        if valor is not None:
            reservas = [reserva for reserva in reservas if getattr(reserva, campo) == valor]

    # El ID desempata para mantener un orden determinista entre páginas.
    reservas.sort(
        key=lambda reserva: (getattr(reserva, consulta.ordenar_por), reserva.id),
        reverse=consulta.direccion == "desc",
    )
    total = len(reservas)
    inicio = (consulta.pagina - 1) * consulta.limite
    return ReservaPagina(
        items=reservas[inicio:inicio + consulta.limite],
        total=total,
        pagina=consulta.pagina,
        limite=consulta.limite,
        total_paginas=(total + consulta.limite - 1) // consulta.limite,
    )


def obtener_reserva(reserva_id: int) -> ReservaRespuesta:
    reserva = reserva_repository.obtener(reserva_id)
    if reserva is None:
        raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
    return reserva


def actualizar_reserva(reserva_id: int, datos: ReservaActualizar) -> ReservaRespuesta:
    obtener_reserva(reserva_id)
    validar_reserva(datos, reserva_id=reserva_id)
    reserva = reserva_repository.actualizar(reserva_id, datos)
    if reserva is None:
        raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
    return reserva


def eliminar_reserva(reserva_id: int) -> None:
    if not reserva_repository.eliminar(reserva_id):
        raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
