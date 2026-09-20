"""Ejemplos de documentación; no crean registros ni cambian las validaciones."""

SALA = {
    "nombre": "Sala A1", "capacidad": 6,
    "ubicacion": "Biblioteca Piso 2", "equipamiento": ["Pizarra"],
}
ESTUDIANTE = {
    "nombre": "Juan Pérez", "carrera": "Psicología",
    "correo": "juan@example.com", "activo": True,
}
RESERVA = {
    "sala_id": 1, "estudiante_id": 1, "fecha": "2026-09-20",
    "hora_inicio": "10:00:00", "hora_fin": "12:00:00",
    "cantidad_personas": 4, "estado": "activa",
}
INCIDENCIA = {
    "sala_id": 1, "reporte": "La pizarra está rota",
    "fecha": "2026-09-20", "resuelto": False,
}
SALA_RESPUESTA = {**SALA, "id": 1}
ESTUDIANTE_RESPUESTA = {**ESTUDIANTE, "id": 1}
RESERVA_RESPUESTA = {**RESERVA, "id": 1}
INCIDENCIA_RESPUESTA = {**INCIDENCIA, "id": 1}
PAGINA = {
    "items": [RESERVA_RESPUESTA], "total": 1,
    "pagina": 1, "limite": 10, "total_paginas": 1,
}


def error(codigo: str, mensaje: str, detalles: list | None = None) -> dict:
    return {"error": {"code": codigo, "message": mensaje, "details": detalles or []}}


HORARIO = error("INVALID_TIME_RANGE", "La hora de fin debe ser estrictamente posterior a la hora de inicio")
CAPACIDAD = error("ROOM_CAPACITY_EXCEEDED", "La cantidad de personas no puede superar la capacidad de la sala (6)")
LIMITE = error("DAILY_RESERVATION_LIMIT", "Un estudiante no puede tener más de 2 reservas activas en el mismo día")
SUPERPOSICION = error("RESERVATION_OVERLAP", "La sala ya tiene una reserva activa que se superpone con ese horario")
CONFLICTO_CAPACIDAD = error("ROOM_CAPACITY_CONFLICT", "La capacidad propuesta es menor que la cantidad de personas de una reserva activa")


def no_encontrado(recurso: str) -> dict:
    return error("RESOURCE_NOT_FOUND", f"No existe {recurso} con el ID 999")


def validacion(ubicacion: str, campo: str) -> dict:
    if ubicacion == "body":
        detalle = {"campo": [ubicacion, campo], "mensaje": "Field required", "tipo": "missing"}
    else:
        detalle = {
            "campo": [ubicacion, campo],
            "mensaje": "Input should be greater than 0" if ubicacion == "path" else "Input should be greater than or equal to 1",
            "tipo": "greater_than" if ubicacion == "path" else "greater_than_equal",
        }
    return error("VALIDATION_ERROR", "Los datos de la solicitud no son válidos", [detalle])


def ejemplos(*, entrada=None, salida=None, codigo=200, errores=None) -> dict:
    """Metadatos OpenAPI que FastAPI combina con los schemas y códigos del router."""
    contenido = {}
    if entrada is not None:
        contenido["requestBody"] = {
            "content": {"application/json": {"example": entrada}}
        }
    respuestas = {}
    if codigo != 204:
        respuestas[str(codigo)] = {"content": {"application/json": {"example": salida}}}
    else:
        respuestas["204"] = {"description": "Reserva eliminada. La respuesta no tiene cuerpo."}
    for estado, casos in (errores or {}).items():
        respuestas[str(estado)] = {
            "content": {"application/json": {
                "examples": {nombre: {"value": valor} for nombre, valor in casos.items()}
            }}
        }
    contenido["responses"] = respuestas
    return contenido
