from sqlalchemy import func, select

from domain.consulta_reservas import ConsultaReservas
from domain.reserva import Reserva
from infrastructure.models import ReservaModel
from infrastructure.mappers import reserva_mapper
from .base import Repository


class ReservaRepository(Repository):
    model = ReservaModel
    mapper = reserva_mapper

    def consultar(self, consulta: ConsultaReservas) -> tuple[list[Reserva], int]:
        """Filtra y pagina en SQL; cuenta todas las coincidencias antes del límite."""
        filtros = []
        for nombre in ('fecha', 'sala_id', 'estudiante_id', 'estado'):
            valor = getattr(consulta, nombre)
            if valor is not None:
                filtros.append(getattr(ReservaModel, nombre) == valor)

        # Solo se pueden ordenar columnas públicas, nunca texto SQL del cliente.
        columnas = {
            'id': ReservaModel.id,
            'fecha': ReservaModel.fecha,
            'hora_inicio': ReservaModel.hora_inicio,
            'hora_fin': ReservaModel.hora_fin,
        }
        columna = columnas[consulta.ordenar_por]
        orden = [columna, ReservaModel.id] if consulta.ordenar_por != 'id' else [columna]
        orden = [c.desc() if consulta.direccion == 'desc' else c.asc() for c in orden]

        total = self.session.scalar(
            select(func.count()).select_from(ReservaModel).where(*filtros)
        )
        sentencia = (
            select(ReservaModel)
            .where(*filtros)
            .order_by(*orden)
            .offset((consulta.pagina - 1) * consulta.limite)
            .limit(consulta.limite)
        )
        items = [reserva_mapper.a_dominio(modelo)
                 for modelo in self.session.scalars(sentencia)]
        return items, total
