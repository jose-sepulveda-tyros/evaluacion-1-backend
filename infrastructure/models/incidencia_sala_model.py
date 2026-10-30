from __future__ import annotations

from datetime import date
from sqlalchemy import Date, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.database import Base


class IncidenciaSalaModel(Base):
    __tablename__ = "incidencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), index=True)
    reporte: Mapped[str] = mapped_column(String(500))
    fecha: Mapped[date] = mapped_column(Date)
    resuelto: Mapped[bool] = mapped_column(Boolean)
    sala: Mapped["SalaModel"] = relationship(back_populates="incidencias")
