from infrastructure.models import SalaModel
from infrastructure.mappers import sala_mapper
from .base import Repository


class SalaRepository(Repository):
    model = SalaModel
    mapper = sala_mapper
