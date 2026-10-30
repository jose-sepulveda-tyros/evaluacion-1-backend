from dataclasses import dataclass
from datetime import date


@dataclass
class IncidenciaSala:
    """Entidad IncidenciaSala; id es None antes de persistir."""

    id: int | None
    sala_id: int
    reporte: str
    fecha: date
    resuelto: bool
