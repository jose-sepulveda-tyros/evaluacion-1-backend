from dataclasses import dataclass


@dataclass
class Estudiante:
    """Entidad Estudiante; id es None antes de persistir."""

    id: int | None
    nombre: str
    carrera: str
    correo: str
    activo: bool
