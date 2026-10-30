from infrastructure.models import EstudianteModel
from infrastructure.mappers import estudiante_mapper
from .base import Repository


class EstudianteRepository(Repository):
    model = EstudianteModel
    mapper = estudiante_mapper
