"""Dependencias compartidas de FastAPI para solicitudes HTTP."""

from collections.abc import Iterator

from sqlalchemy.orm import Session

from infrastructure.database import SessionLocal


def get_session() -> Iterator[Session]:
    """Entrega una sesión de base de datos y la cierra al terminar la solicitud."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
