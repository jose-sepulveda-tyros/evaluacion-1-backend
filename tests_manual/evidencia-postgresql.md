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

La base normal del proyecto conserva sus datos. Las verificaciones posteriores de seeders y consultas SQL se registran en las secciones siguientes.


## Filtros, ordenamiento y paginación SQL - 30 de octubre de 2026

Tras trasladar las consultas al repositorio SQL:

- `python -m unittest discover -s tests -v`: 19 pruebas correctas.
- Seis pruebas nuevas comprueban filtros combinados, total filtrado anterior al límite, orden ascendente/descendente, desempate por ID, páginas fuera de rango y ausencia de coincidencias. También verifican que la consulta de filas incluya WHERE, ORDER BY, LIMIT y OFFSET, y que el conteo no tenga LIMIT.
- `python tests_manual/verificar_postgres.py`: 63 casos correctos, 15 operaciones cubiertas; también pasan migraciones, persistencia tras reiniciar y rechazo de reservas simultáneas superpuestas.

No cambian los parámetros de la API ni la estructura de las respuestas. Las pruebas PostgreSQL usan una base temporal y no modifican los datos de la base normal.



## Seeders - 30 de octubre de 2026

Se verificaron los seeders de Benjamín con el ajuste de carga global sobre una base PostgreSQL temporal, sin modificar la base normal:

- Primera ejecución de `python -m infrastructure.seeders.run`: 3 salas, 3 estudiantes, 5 reservas y 2 incidencias.
- Segunda ejecución: carga omitida y cantidades sin cambios.
- Todas las reservas iniciales cumplieron la validación del servicio.
- Con una sala previa de capacidad 1: carga omitida, sin estudiantes, reservas o incidencias nuevas.
- Dos cargas simultáneas sobre una base vacía: una insertó los 13 registros y la otra omitió la carga; sin duplicados.
- Suite local: 13 pruebas aprobadas, incluidas cinco de seeders (carga, repetición, bases parciales y rollback).

Los casos locales pueden repetirse con `python -m unittest tests.test_seeders -v`. El script `verificar_postgres.py` anterior prueba la API y persistencia; no incluye estos escenarios de seeders.


## Imagen Docker - 30 de octubre de 2026

Verificación reportada por Benjamín en la rama `2-dominio-datos` (commit `be21a0b`): construcción y ejecución de la API en contenedor con PostgreSQL 16, partiendo de un volumen desechable nuevo. El comando `docker compose down -v` elimina los datos; para repetir las pruebas sin borrar la base normal se recomienda `python tests_manual/verificar_postgres.py`.

Comandos: `docker compose up --build -d`, `docker compose ps`, `curl http://127.0.0.1:8000/salas` y `python tests_manual/verificar_coleccion.py`.

| Comprobación | Resultado esperado | Resultado obtenido |
|---|---|---|
| Construcción de la imagen | Imagen creada sin errores | Correcto |
| Inicio de los servicios | PostgreSQL y API en ejecución | Correcto; PostgreSQL `healthy` |
| Migraciones al iniciar el contenedor | Tablas creadas sin ejecutar Alembic manualmente | `GET /salas` respondió 200 con lista vacía |
| Estado de los servicios | `healthy` | API y PostgreSQL en `healthy` tras 2 minutos |
| Colección HTTP | 63 casos; 15 operaciones | 63 correctos; 15 cubiertas |

El `Dockerfile` ejecuta `alembic upgrade head` antes de iniciar Uvicorn, por lo que una base vacía queda lista al levantar el contenedor.

## Instalación limpia con Docker - 30 de octubre de 2026

Se verificó una copia de los archivos versionados del commit `cdd68d1`, exportada con `git archive HEAD`, sin reutilizar `.env`, `.venv` ni datos del proyecto. La API y sus dependencias se construyeron dentro de Docker con Python 3.12.

Para aislar la comprobación se usaron un nombre de proyecto Compose, nombres de contenedores y puertos temporales distintos. La copia recibió un `.env` de prueba con credenciales generadas. No se modificaron los archivos, contenedores o datos de la instancia normal.

| Comprobación | Resultado esperado | Resultado obtenido |
|---|---|---|
| Construir API desde la copia limpia | Dependencias y archivos completos | Imagen construida correctamente |
| Arrancar API y PostgreSQL desde volumen nuevo | Ambos saludables; migraciones automáticas | Ambos `healthy`; `GET /salas` devolvió 200 y lista vacía |
| Ejecutar seeders y repetir | 3 salas, 3 estudiantes, 5 reservas, 2 incidencias; sin duplicados | Cantidades correctas; segunda carga omitida |
| Consultar reservas activas, ID descendente, página 2, límite 2 | Total 4, dos páginas, IDs 2 y 1 | Valores correctos |
| Reiniciar el contenedor API | Misma colección de reservas | Igualdad comprobada antes y después |
| Verificador PostgreSQL de la copia | 63 casos; 15 operaciones; migraciones, reinicio y concurrencia | Todas las comprobaciones correctas |

Comandos principales ejecutados en la copia: `docker compose build api`, `docker compose up -d --wait`, `docker compose exec -T api python -m infrastructure.seeders.run` (dos veces), `docker compose restart api` y `python tests_manual/verificar_postgres.py`. Este último script se lanzó desde el equipo con el entorno Python 3.12 existente, apuntando al PostgreSQL temporal; su propia API de prueba es Uvicorn local. Las comprobaciones de seeders, listado y reinicio anteriores sí se realizaron contra la API del contenedor.

El primer intento del verificador de revisión conservó el puerto temporal anterior al reinicio y no pudo confirmar la respuesta. Se corrigió la lectura del puerto asignado por Docker y se repitió todo el procedimiento con éxito; no fue necesario cambiar código del proyecto.

Al terminar se eliminaron únicamente los contenedores y el volumen del proyecto temporal de revisión. La base normal se conservó. No se recomienda eliminar su volumen para repetir pruebas.

## Correcciones de validación antes del PR - 31 de octubre de 2026

Se reprodujeron dos entradas que devolvían HTTP 500: capacidad `2147483648` y texto con NUL (`U+0000`). Después de añadir restricciones Pydantic, ambas devuelven HTTP 422 con `error.code=VALIDATION_ERROR` y detalles del campo; una solicitud válida sigue devolviendo 201.

- Capacidad y cantidad de personas se limitan al máximo de INTEGER PostgreSQL: 2147483647.
- Los textos de salas, estudiantes e incidencias, incluido equipamiento, rechazan NUL sin eliminar ni transformar silenciosamente el carácter.
- `python -m unittest discover -s tests -v`: 25 pruebas correctas.
- `python tests_manual/verificar_postgres.py`: 70 casos correctos, 15 operaciones cubiertas; migraciones, reinicio y concurrencia también correctos.
- Los siete nuevos casos HTTP están al final de `pruebas.http` (64 a 70). Las pruebas se ejecutaron con una base temporal, sin modificar los datos normales.
