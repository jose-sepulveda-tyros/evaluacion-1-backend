"""DTO mínimos de reservas; coordinar este contrato con el rol de dominio y datos."""

from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReservaCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sala_id: int = Field(gt=0, strict=True)
    estudiante_id: int = Field(gt=0, strict=True)
    fecha: date
    hora_inicio: time
    hora_fin: time
    cantidad_personas: int = Field(gt=0, strict=True)
    estado: Literal["activa", "cancelada"] = "activa"

    @field_validator("hora_inicio", "hora_fin")
    @classmethod
    def validar_hora_local(cls, valor: time) -> time:
        if valor.tzinfo is not None:
            raise ValueError("Utiliza la hora local del campus, sin zona horaria")
        return valor


class ReservaActualizar(ReservaCrear):
    """PUT reemplaza todos los datos editables y exige un estado explícito."""

    estado: Literal["activa", "cancelada"]


class ReservaRespuesta(ReservaCrear):
    id: int = Field(gt=0, strict=True)
