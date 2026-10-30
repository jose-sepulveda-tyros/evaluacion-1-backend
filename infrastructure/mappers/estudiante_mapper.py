from domain.estudiante import Estudiante
from infrastructure.models.estudiante_model import EstudianteModel


def a_modelo(entidad: Estudiante) -> EstudianteModel:
    return EstudianteModel(
        id=entidad.id,
        nombre=entidad.nombre,
        carrera=entidad.carrera,
        correo=entidad.correo,
        activo=entidad.activo,
    )


def a_dominio(modelo: EstudianteModel) -> Estudiante:
    return Estudiante(
        id=modelo.id,
        nombre=modelo.nombre,
        carrera=modelo.carrera,
        correo=modelo.correo,
        activo=modelo.activo,
    )
