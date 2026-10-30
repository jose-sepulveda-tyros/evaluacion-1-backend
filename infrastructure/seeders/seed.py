"""Carga los datos semilla usando los modelos ORM existentes.

Es idempotente por tabla: si la tabla ya tiene filas, no inserta nada. No se
fijan IDs a mano; PostgreSQL los genera, así la secuencia queda coherente y los
POST posteriores de la API no chocan con claves duplicadas.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from infrastructure.models import (
    EstudianteModel, IncidenciaSalaModel, ReservaModel, SalaModel,
)
from . import datos


def _vacia(session: Session, model) -> bool:
    return session.scalar(select(func.count()).select_from(model)) == 0


def sembrar(session: Session) -> dict[str, int]:
    """Inserta los datos en orden de dependencias y confirma una sola vez.

    Devuelve cuántas filas se insertaron por tabla (0 si ya había datos).
    """
    insertadas = {"salas": 0, "estudiantes": 0, "reservas": 0, "incidencias": 0}
    try:
        # 1) Tablas sin dependencias.
        salas, estudiantes = [], []
        if _vacia(session, SalaModel):
            salas = [SalaModel(**fila) for fila in datos.SALAS]
            session.add_all(salas)
            insertadas["salas"] = len(salas)
        if _vacia(session, EstudianteModel):
            estudiantes = [EstudianteModel(**fila) for fila in datos.ESTUDIANTES]
            session.add_all(estudiantes)
            insertadas["estudiantes"] = len(estudiantes)
        session.flush()  # asigna los IDs antes de crear las dependientes

        # Si ya existían, se leen en orden de ID para resolver las posiciones.
        if not salas:
            salas = list(session.scalars(select(SalaModel).order_by(SalaModel.id)))
        if not estudiantes:
            estudiantes = list(session.scalars(
                select(EstudianteModel).order_by(EstudianteModel.id)))

        # 2) Tablas con claves foráneas.
        if _vacia(session, ReservaModel) and len(salas) >= 3 and len(estudiantes) >= 3:
            for fila in datos.RESERVAS:
                fila = dict(fila)
                fila["sala_id"] = salas[fila.pop("sala")].id
                fila["estudiante_id"] = estudiantes[fila.pop("estudiante")].id
                session.add(ReservaModel(**fila))
                insertadas["reservas"] += 1
        if _vacia(session, IncidenciaSalaModel) and len(salas) >= 2:
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