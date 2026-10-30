from domain.incidencia_sala import IncidenciaSala
from infrastructure.models.incidencia_sala_model import IncidenciaSalaModel


def a_modelo(entidad: IncidenciaSala) -> IncidenciaSalaModel:
    return IncidenciaSalaModel(
        id=entidad.id,
        sala_id=entidad.sala_id,
        reporte=entidad.reporte,
        fecha=entidad.fecha,
        resuelto=entidad.resuelto,
    )


def a_dominio(modelo: IncidenciaSalaModel) -> IncidenciaSala:
    return IncidenciaSala(
        id=modelo.id,
        sala_id=modelo.sala_id,
        reporte=modelo.reporte,
        fecha=modelo.fecha,
        resuelto=modelo.resuelto,
    )
