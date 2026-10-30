"""Casos de uso de reservas y reglas de negocio."""

from domain.reserva import Reserva
from domain.consulta_reservas import ConsultaReservas, PaginaReservas


class HorarioInvalidoError(ValueError):
    pass


class ReservaSuperpuestaError(ValueError):
    pass


class LimiteReservasError(ValueError):
    pass


class RecursoRelacionadoNoEncontradoError(LookupError):
    pass


class CapacidadExcedidaError(ValueError):
    pass


class ReservaNoEncontradaError(LookupError):
    pass


class ReservaService:
    def __init__(self, reserva_repository, sala_repository, estudiante_repository):
        self.reserva_repository = reserva_repository
        self.sala_repository = sala_repository
        self.estudiante_repository = estudiante_repository

    def validar_horario(self, datos: Reserva) -> None:
        if datos.hora_fin <= datos.hora_inicio:
            raise HorarioInvalidoError(
                "La hora de fin debe ser estrictamente posterior a la hora de inicio"
            )

    def validar_recursos_relacionados(self, datos: Reserva) -> None:
        sala = self.sala_repository.obtener(datos.sala_id)
        if sala is None:
            raise RecursoRelacionadoNoEncontradoError(
                f"No existe una sala con el ID {datos.sala_id}"
            )
        if not self.estudiante_repository.existe(datos.estudiante_id):
            raise RecursoRelacionadoNoEncontradoError(
                f"No existe un estudiante con el ID {datos.estudiante_id}"
            )
        if datos.cantidad_personas > sala.capacidad:
            raise CapacidadExcedidaError(
                f"La cantidad de personas no puede superar la capacidad de la sala ({sala.capacidad})"
            )

    def validar_reserva(
        self,
        datos: Reserva, reserva_id: int | None = None
    ) -> None:
        self.validar_horario(datos)
        self.validar_recursos_relacionados(datos)
        if datos.estado != "activa":
            return

        # Al actualizar, la reserva no debe entrar en conflicto consigo misma.
        activas_del_dia = [
            reserva
            for reserva in self.reserva_repository.listar()
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

    def crear_reserva(self, datos: Reserva) -> Reserva:
        self.reserva_repository.bloquear_reglas()
        self.validar_reserva(datos)
        return self.reserva_repository.crear(datos)

    def listar_reservas(self, consulta: ConsultaReservas) -> PaginaReservas:
        reservas = self.reserva_repository.listar()
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
        return PaginaReservas(
            items=reservas[inicio:inicio + consulta.limite],
            total=total,
            pagina=consulta.pagina,
            limite=consulta.limite,
            total_paginas=(total + consulta.limite - 1) // consulta.limite,
        )

    def obtener_reserva(self, reserva_id: int) -> Reserva:
        reserva = self.reserva_repository.obtener(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
        return reserva

    def actualizar_reserva(self, reserva_id: int, datos: Reserva) -> Reserva:
        self.reserva_repository.bloquear_reglas()
        self.obtener_reserva(reserva_id)
        self.validar_reserva(datos, reserva_id=reserva_id)
        reserva = self.reserva_repository.actualizar(reserva_id, datos)
        if reserva is None:
            raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
        return reserva

    def eliminar_reserva(self, reserva_id: int) -> None:
        self.reserva_repository.bloquear_reglas()
        if not self.reserva_repository.eliminar(reserva_id):
            raise ReservaNoEncontradaError(f"No existe una reserva con el ID {reserva_id}")
