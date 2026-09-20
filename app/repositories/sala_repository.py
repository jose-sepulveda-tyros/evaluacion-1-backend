from itertools import count

from app.schemas.sala import SalaActualizar, SalaCrear, SalaRespuesta

_salas: dict[int, SalaRespuesta] = {}
_ids = count(1)


def crear(datos: SalaCrear) -> SalaRespuesta:
    sala = SalaRespuesta(id=next(_ids), **datos.model_dump())
    _salas[sala.id] = sala
    return sala.model_copy(deep=True)


def listar() -> list[SalaRespuesta]:
    return [sala.model_copy(deep=True) for sala in _salas.values()]


def obtener(sala_id: int) -> SalaRespuesta | None:
    sala = _salas.get(sala_id)
    return sala.model_copy(deep=True) if sala is not None else None


def actualizar(sala_id: int, datos: SalaActualizar) -> SalaRespuesta | None:
    if sala_id not in _salas:
        return None
    sala = SalaRespuesta(id=sala_id, **datos.model_dump())
    _salas[sala_id] = sala
    return sala.model_copy(deep=True)


def existe(sala_id: int) -> bool:
    # Para que el rol de reglas de negocio valide sala_id antes de crear reservas/incidencias.
    return sala_id in _salas