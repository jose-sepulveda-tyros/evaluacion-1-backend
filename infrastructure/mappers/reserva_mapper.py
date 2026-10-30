from domain.reserva import Reserva
from infrastructure.models.reserva_model import ReservaModel


def a_modelo(entidad: Reserva) -> ReservaModel:
    return ReservaModel(
        id=entidad.id,
        sala_id=entidad.sala_id,
        estudiante_id=entidad.estudiante_id,
        fecha=entidad.fecha,
        hora_inicio=entidad.hora_inicio,
        hora_fin=entidad.hora_fin,
        cantidad_personas=entidad.cantidad_personas,
        estado=entidad.estado,
    )


def a_dominio(modelo: ReservaModel) -> Reserva:
    return Reserva(
        id=modelo.id,
        sala_id=modelo.sala_id,
        estudiante_id=modelo.estudiante_id,
        fecha=modelo.fecha,
        hora_inicio=modelo.hora_inicio,
        hora_fin=modelo.hora_fin,
        cantidad_personas=modelo.cantidad_personas,
        estado=modelo.estado,
    )
