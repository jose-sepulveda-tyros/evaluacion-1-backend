from infrastructure.models import IncidenciaSalaModel
from infrastructure.mappers import incidencia_mapper
from .base import Repository


class IncidenciaRepository(Repository):
    model = IncidenciaSalaModel
    mapper = incidencia_mapper
