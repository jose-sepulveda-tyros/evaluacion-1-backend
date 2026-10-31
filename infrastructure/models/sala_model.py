from __future__ import annotations

from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.database import Base


class SalaModel(Base):
    __tablename__ = "salas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    capacidad: Mapped[int] = mapped_column(Integer)
    ubicacion: Mapped[str] = mapped_column(String(120))
    equipamiento: Mapped[list[str]] = mapped_column(JSON)
    reservas: Mapped[list["ReservaModel"]] = relationship(back_populates="sala", passive_deletes="all")
    incidencias: Mapped[list["IncidenciaSalaModel"]] = relationship(back_populates="sala", passive_deletes="all")
