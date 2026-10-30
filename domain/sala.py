from dataclasses import dataclass


@dataclass
class Sala:
    """Entidad Sala; id es None antes de persistir."""

    id: int | None
    nombre: str
    capacidad: int
    ubicacion: str
    equipamiento: list[str]
