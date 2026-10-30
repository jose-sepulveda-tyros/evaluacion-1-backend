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
