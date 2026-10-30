from infrastructure.models import ReservaModel
from infrastructure.mappers import reserva_mapper
from .base import Repository


class ReservaRepository(Repository):
    model = ReservaModel
    mapper = reserva_mapper
