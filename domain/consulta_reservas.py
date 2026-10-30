from dataclasses import dataclass
from datetime import date
from typing import Literal
from domain.reserva import Reserva


@dataclass
class ConsultaReservas:
    fecha: date | None = None
    sala_id: int | None = None
    estudiante_id: int | None = None
    estado: Literal["activa", "cancelada"] | None = None
    ordenar_por: Literal["fecha", "hora_inicio", "hora_fin", "id"] = "id"
    direccion: Literal["asc", "desc"] = "asc"
    pagina: int = 1
    limite: int = 10


@dataclass
class PaginaReservas:
    items: list[Reserva]
    total: int
    pagina: int
    limite: int
    total_paginas: int
