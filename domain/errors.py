"""Errores independientes del motor de persistencia."""


class ConflictoPersistenciaError(ValueError):
    """Una escritura entra en conflicto con las referencias existentes."""
