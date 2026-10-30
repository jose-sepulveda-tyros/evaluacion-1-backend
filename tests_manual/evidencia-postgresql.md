# Verificación de persistencia - 29 de octubre de 2026

Comando reproducible: `python tests_manual/verificar_postgres.py`.

Entorno: Python 3.12, PostgreSQL 16 en Docker y una base temporal nueva, aislada de la base del proyecto. El script configura su propio Uvicorn y elimina únicamente la base de prueba que crea. Los casos HTTP completos y sus entradas/resultados esperados están en `pruebas.http`.

| Comprobación | Resultado esperado | Resultado obtenido |
|---|---|---|
| Alembic upgrade / downgrade / upgrade | Crear, eliminar y recrear las cuatro tablas | Correcto |
| Comparación ORM contra esquema migrado | Sin diferencias | Sin diferencias |
| Colección HTTP | 63 casos; 15 operaciones | 63 correctos; 15 cubiertas |
| Reinicio del servidor | Misma colección de reservas antes y después | Igualdad comprobada, colección no vacía |
| Dos reservas paralelas, misma sala/fecha/horario | Una creación y un conflicto | HTTP 201 y HTTP 409 |

La base normal del proyecto conserva sus datos. Los seeders y la paginación ejecutada directamente en SQL pertenecen a los siguientes bloques.

## Seeders - 30 de octubre de 2026

Se verificaron los seeders de Benjamín con el ajuste de carga global sobre una base PostgreSQL temporal, sin modificar la base normal:

- Primera ejecución de `python -m infrastructure.seeders.run`: 3 salas, 3 estudiantes, 5 reservas y 2 incidencias.
- Segunda ejecución: carga omitida y cantidades sin cambios.
- Todas las reservas iniciales cumplieron la validación del servicio.
- Con una sala previa de capacidad 1: carga omitida, sin estudiantes, reservas o incidencias nuevas.
- Dos cargas simultáneas sobre una base vacía: una insertó los 13 registros y la otra omitió la carga; sin duplicados.
- Suite local: 13 pruebas aprobadas, incluidas cinco de seeders (carga, repetición, bases parciales y rollback).

Los casos locales pueden repetirse con `python -m unittest tests.test_seeders -v`. El script `verificar_postgres.py` anterior prueba la API y persistencia; no incluye estos escenarios de seeders.
