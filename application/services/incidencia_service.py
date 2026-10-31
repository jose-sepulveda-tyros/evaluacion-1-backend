"""Registro y seguimiento de incidencias de salas."""

from domain.incidencia_sala import IncidenciaSala

from application.services.sala_service import SalaNoEncontradaError


class IncidenciaNoEncontradaError(LookupError):
    pass


class IncidenciaService:
    def __init__(self, incidencia_repository, sala_repository):
        self.incidencia_repository = incidencia_repository
        self.sala_repository = sala_repository

    def crear_incidencia(self, datos: IncidenciaSala) -> IncidenciaSala:
        if not self.sala_repository.existe(datos.sala_id):
            raise SalaNoEncontradaError(f"No existe una sala con el ID {datos.sala_id}")
        return self.incidencia_repository.crear(datos)

    def listar_incidencias(self) -> list[IncidenciaSala]:
        return self.incidencia_repository.listar()

    def actualizar_incidencia(
        self,
        incidencia_id: int, resuelto: bool
    ) -> IncidenciaSala:
        incidencia = self.incidencia_repository.obtener(incidencia_id)
        if incidencia is None:
            raise IncidenciaNoEncontradaError(
                f"No existe una incidencia con el ID {incidencia_id}"
            )
        incidencia.resuelto = resuelto
        return self.incidencia_repository.actualizar(incidencia_id, incidencia)
