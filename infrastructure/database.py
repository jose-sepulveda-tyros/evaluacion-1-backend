"""Configuración de SQLAlchemy y conexión a PostgreSQL."""

import os
from collections.abc import Mapping

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


def build_database_url(environ: Mapping[str, str] | None = None) -> URL:
    """Construye la URL PostgreSQL desde variables DB_*, codificando símbolos."""
    values = os.environ if environ is None else environ
    required = ("DB_USER", "DB_PASSWORD", "DB_NAME")
    missing = [name for name in required if not values.get(name)]
    if missing:
        raise RuntimeError(
            "Faltan variables de base de datos: " + ", ".join(missing)
        )

    try:
        port = int(values.get("DB_PORT", "5432"))
    except ValueError as exc:
        raise RuntimeError("DB_PORT debe ser un número entero") from exc

    return URL.create(
        drivername="postgresql+psycopg2",
        username=values["DB_USER"],
        password=values["DB_PASSWORD"],
        host=values.get("DB_HOST", "localhost"),
        port=port,
        database=values["DB_NAME"],
    )


engine = create_engine(build_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base común para declarar los modelos persistentes con SQLAlchemy."""
