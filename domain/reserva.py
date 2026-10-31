from dataclasses import dataclass
from datetime import date, time
from typing import Literal


@dataclass
class Reserva:
    """Entidad Reserva; id es None antes de persistir."""

    id: int | None
    sala_id: int
    estudiante_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cantidad_personas: int
    estado: Literal["activa", "cancelada"]
