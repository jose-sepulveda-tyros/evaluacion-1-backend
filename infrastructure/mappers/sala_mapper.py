from domain.sala import Sala
from infrastructure.models.sala_model import SalaModel


def a_modelo(entidad: Sala) -> SalaModel:
    return SalaModel(
        id=entidad.id,
        nombre=entidad.nombre,
        capacidad=entidad.capacidad,
        ubicacion=entidad.ubicacion,
        equipamiento=list(entidad.equipamiento),
    )


def a_dominio(modelo: SalaModel) -> Sala:
    return Sala(
        id=modelo.id,
        nombre=modelo.nombre,
        capacidad=modelo.capacidad,
        ubicacion=modelo.ubicacion,
        equipamiento=list(modelo.equipamiento),
    )
