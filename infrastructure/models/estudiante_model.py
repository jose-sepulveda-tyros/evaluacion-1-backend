from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.database import Base


class EstudianteModel(Base):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    carrera: Mapped[str] = mapped_column(String(80))
    correo: Mapped[str] = mapped_column(String(254))
    activo: Mapped[bool] = mapped_column(Boolean)
    reservas: Mapped[list["ReservaModel"]] = relationship(back_populates="estudiante", passive_deletes="all")
