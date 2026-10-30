"""Carga inicial de Benjamín, con protección global ante datos existentes.

Solo carga cuando las cuatro tablas están vacías. PostgreSQL genera los IDs;
una sola transacción confirma toda la carga o la revierte si ocurre un error.
"""
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from infrastructure.models import (
    EstudianteModel, IncidenciaSalaModel, ReservaModel, SalaModel,
)
from . import datos


def _vacia(session: Session, model) -> bool:
    return session.scalar(select(func.count()).select_from(model)) == 0


def sembrar(session: Session) -> dict[str, int]:
    """Devuelve filas insertadas; todos ceros significa carga omitida.

    Usar una sesión dedicada, sin cambios pendientes. Si cualquiera de las
    tablas tiene datos, no modifica ninguna ni mezcla registros existentes
    con los ejemplos. El bloqueo evita dos cargas iniciales simultáneas.
    """
    insertadas = {"salas": 0, "estudiantes": 0, "reservas": 0, "incidencias": 0}
    try:
        if session.get_bind().dialect.name == "postgresql":
            session.execute(text(
                "LOCK TABLE estudiantes, salas, reservas, incidencias "
                "IN SHARE ROW EXCLUSIVE MODE"
            ))

        if not all(_vacia(session, model) for model in (
            SalaModel, EstudianteModel, ReservaModel, IncidenciaSalaModel,
        )):
            session.rollback()  # Libera el bloqueo sin escribir datos.
            return insertadas

        salas = [SalaModel(**fila) for fila in datos.SALAS]
        estudiantes = [EstudianteModel(**fila) for fila in datos.ESTUDIANTES]
        session.add_all(salas + estudiantes)
        session.flush()  # Asigna los IDs antes de crear las dependientes.
        insertadas["salas"] = len(salas)
        insertadas["estudiantes"] = len(estudiantes)

        for fila in datos.RESERVAS:
            fila = dict(fila)
            fila["sala_id"] = salas[fila.pop("sala")].id
            fila["estudiante_id"] = estudiantes[fila.pop("estudiante")].id
            session.add(ReservaModel(**fila))
            insertadas["reservas"] += 1

        for fila in datos.INCIDENCIAS:
            fila = dict(fila)
            fila["sala_id"] = salas[fila.pop("sala")].id
            session.add(IncidenciaSalaModel(**fila))
            insertadas["incidencias"] += 1

        session.commit()
    except Exception:
        session.rollback()
        raise
    return insertadas
