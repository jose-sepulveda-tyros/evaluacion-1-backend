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

## Imagen Docker - 30 de octubre de 2026

Se verificó la construcción y ejecución de la API en contenedor con PostgreSQL 16, partiendo de un volumen nuevo (`docker compose down -v`).

Comandos: `docker compose up --build -d`, `docker compose ps`, `curl http://127.0.0.1:8000/salas` y `python tests_manual/verificar_coleccion.py`.

| Comprobación | Resultado esperado | Resultado obtenido |
|---|---|---|
| Construcción de la imagen | Imagen creada sin errores | Correcto |
| Inicio de los servicios | PostgreSQL y API en ejecución | Correcto; PostgreSQL `healthy` |
| Migraciones al iniciar el contenedor | Tablas creadas sin ejecutar Alembic manualmente | `GET /salas` respondió 200 con lista vacía |
| Estado de los servicios | `healthy` | API y PostgreSQL en `healthy` tras 2 minutos |
| Colección HTTP | 63 casos; 15 operaciones | 63 correctos; 15 cubiertas |

El `Dockerfile` ejecuta `alembic upgrade head` antes de iniciar Uvicorn, por lo que una base vacía queda lista al levantar el contenedor.
