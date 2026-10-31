from __future__ import annotations

from datetime import date, time
from sqlalchemy import Date, Time, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.database import Base


class ReservaModel(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True)
    sala_id: Mapped[int] = mapped_column(ForeignKey("salas.id"), index=True)
    estudiante_id: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"), index=True)
    fecha: Mapped[date] = mapped_column(Date)
    hora_inicio: Mapped[time] = mapped_column(Time)
    hora_fin: Mapped[time] = mapped_column(Time)
    cantidad_personas: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(9))
    sala: Mapped["SalaModel"] = relationship(back_populates="reservas")
    estudiante: Mapped["EstudianteModel"] = relationship(back_populates="reservas")
