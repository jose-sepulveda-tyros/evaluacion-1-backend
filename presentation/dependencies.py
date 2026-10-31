"""Dependencias compartidas de FastAPI para solicitudes HTTP."""

from collections.abc import Iterator

from sqlalchemy.orm import Session

from infrastructure.database import SessionLocal

from typing import Annotated
from fastapi import Depends
from application.services.reserva_service import ReservaService
from infrastructure.repositories.reserva_repository import ReservaRepository
from application.services.sala_service import SalaService
from infrastructure.repositories.sala_repository import SalaRepository
from application.services.estudiante_service import EstudianteService
from infrastructure.repositories.estudiante_repository import EstudianteRepository
from application.services.incidencia_service import IncidenciaService
from infrastructure.repositories.incidencia_repository import IncidenciaRepository


def get_session() -> Iterator[Session]:
    """Entrega una sesión de base de datos y la cierra al terminar la solicitud."""
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

SessionDep = Annotated[Session, Depends(get_session)]


def get_reserva_service(session: SessionDep) -> ReservaService:
    return ReservaService(ReservaRepository(session), SalaRepository(session), EstudianteRepository(session))


def get_sala_service(session: SessionDep) -> SalaService:
    return SalaService(SalaRepository(session), ReservaRepository(session))


def get_estudiante_service(session: SessionDep) -> EstudianteService:
    return EstudianteService(EstudianteRepository(session))


def get_incidencia_service(session: SessionDep) -> IncidenciaService:
    return IncidenciaService(IncidenciaRepository(session), SalaRepository(session))
