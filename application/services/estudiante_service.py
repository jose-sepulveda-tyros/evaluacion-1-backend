"""Casos de uso de estudiantes con almacenamiento persistente."""

from domain.estudiante import Estudiante


class EstudianteNoEncontradoError(LookupError):
    pass


class EstudianteService:
    def __init__(self, estudiante_repository):
        self.estudiante_repository = estudiante_repository

    def crear_estudiante(self, datos: Estudiante) -> Estudiante:
        return self.estudiante_repository.crear(datos)

    def listar_estudiantes(self) -> list[Estudiante]:
        return self.estudiante_repository.listar()

    def obtener_estudiante(self, estudiante_id: int) -> Estudiante:
        estudiante = self.estudiante_repository.obtener(estudiante_id)
        if estudiante is None:
            raise EstudianteNoEncontradoError(
                f"No existe un estudiante con el ID {estudiante_id}"
            )
        return estudiante
