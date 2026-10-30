"""Datos semilla en estructuras simples (sin SQLAlchemy).

Cumplen las mismas reglas que la API: horas válidas, sin superposición de
reservas activas por sala y fecha, máximo 2 reservas activas por estudiante y
día, y cantidad de personas <= capacidad de la sala. Las reservas e incidencias
referencian salas/estudiantes por posición (0 = primero de la lista).
"""
from datetime import date, time

SALAS = [
    {"nombre": "Sala Estudio A1", "capacidad": 6, "ubicacion": "Biblioteca, piso 1",
     "equipamiento": ["Pizarra", "Enchufes"]},
    {"nombre": "Sala Estudio B2", "capacidad": 10, "ubicacion": "Edificio B, piso 2",
     "equipamiento": ["Proyector", "Pizarra", "Aire acondicionado"]},
    {"nombre": "Sala Grupal C3", "capacidad": 4, "ubicacion": "Edificio C, piso 3",
     "equipamiento": []},
]

ESTUDIANTES = [
    {"nombre": "Camila Rojas", "carrera": "Ingeniería en Informática",
     "correo": "camila.rojas@example.com", "activo": True},
    {"nombre": "Matías Soto", "carrera": "Ingeniería Civil",
     "correo": "matias.soto@example.com", "activo": True},
    {"nombre": "Valentina Pérez", "carrera": "Diseño Gráfico",
     "correo": "valentina.perez@example.com", "activo": False},
]

RESERVAS = [
    {"sala": 0, "estudiante": 0, "fecha": date(2026, 11, 10),
     "hora_inicio": time(10, 0), "hora_fin": time(11, 0),
     "cantidad_personas": 4, "estado": "activa"},
    # Contigua a la anterior (11:00): compatible, los extremos son abiertos.
    {"sala": 0, "estudiante": 1, "fecha": date(2026, 11, 10),
     "hora_inicio": time(11, 0), "hora_fin": time(12, 0),
     "cantidad_personas": 5, "estado": "activa"},
    {"sala": 1, "estudiante": 0, "fecha": date(2026, 11, 10),
     "hora_inicio": time(15, 0), "hora_fin": time(17, 0),
     "cantidad_personas": 8, "estado": "activa"},
    {"sala": 2, "estudiante": 1, "fecha": date(2026, 11, 11),
     "hora_inicio": time(9, 0), "hora_fin": time(10, 30),
     "cantidad_personas": 3, "estado": "activa"},
    # Cancelada: no ocupa horario ni cuenta para el límite diario.
    {"sala": 1, "estudiante": 2, "fecha": date(2026, 11, 12),
     "hora_inicio": time(14, 0), "hora_fin": time(15, 0),
     "cantidad_personas": 2, "estado": "cancelada"},
]

INCIDENCIAS = [
    {"sala": 1, "reporte": "El proyector no enciende.",
     "fecha": date(2026, 11, 5), "resuelto": False},
    {"sala": 0, "reporte": "Falta un marcador para la pizarra.",
     "fecha": date(2026, 11, 3), "resuelto": True},
]