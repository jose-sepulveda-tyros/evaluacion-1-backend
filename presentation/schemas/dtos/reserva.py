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


class ReservaConsulta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fecha: date | None = None
    sala_id: int | None = Field(default=None, gt=0)
    estudiante_id: int | None = Field(default=None, gt=0)
    estado: Literal["activa", "cancelada"] | None = None
    ordenar_por: Literal["fecha", "hora_inicio", "hora_fin", "id"] = "id"
    direccion: Literal["asc", "desc"] = "asc"
    pagina: int = Field(default=1, ge=1)
    limite: int = Field(default=10, ge=1, le=100)


class ReservaPagina(BaseModel):
    items: list[ReservaRespuesta]
    total: int = Field(ge=0)
    pagina: int = Field(ge=1)
    limite: int = Field(ge=1, le=100)
    total_paginas: int = Field(ge=0)
