# Ejecución con Docker

Docker Compose levanta dos servicios: `api` (FastAPI) y `postgres` (PostgreSQL 16). Los datos se guardan en un volumen de Docker, por lo que sobreviven a reinicios y a `docker compose down`. No hace falta instalar Python ni PostgreSQL.

## Requisitos

- Docker y Docker Compose instalados y en ejecución. En Windows y macOS vienen incluidos en Docker Desktop.
- Puertos libres: `8000` (API) y `5432` (PostgreSQL). Si ya usas un PostgreSQL local, cambia `DB_PORT` en `.env`.

## Primera ejecución

Desde la raíz del repositorio:

```bash
cp .env.example .env
# Edita .env y define DB_PASSWORD (es obligatoria: sin ella Compose no inicia).
docker compose up --build -d
```

Al iniciar, el contenedor de la API espera a que PostgreSQL esté listo, aplica las migraciones de Alembic (`alembic upgrade head`) y arranca Uvicorn. No necesitas ejecutar las migraciones a mano.

## Comprobar que funciona

```bash
docker compose ps
```

Ambos servicios deben aparecer en estado `healthy` (la API puede tardar unos segundos). Luego abre:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Si Swagger muestra los grupos Reservas, Salas, Estudiantes e Incidencias y `GET /salas` responde 200, la API y la base de datos están conectadas.

## Datos iniciales (opcional)

Con la API en ejecución y la base vacía:

```bash
docker compose exec api python -m infrastructure.seeders.run
```

Carga 3 salas, 3 estudiantes, 5 reservas y 2 incidencias. Si la base ya tiene datos, omite la carga sin modificar nada.

## Datos y pruebas

- Los datos **persisten** en el volumen `reservas_postgres_data`. `docker compose down` conserva los datos; `docker compose down -v` **los elimina**.
- La colección `tests_manual/pruebas.http` y su verificador esperan una base **vacía**. Para repetirla: `docker compose down -v`, luego `docker compose up --build -d` y, desde tu máquina con el entorno virtual activado, `python tests_manual/verificar_coleccion.py`. No cargues los datos iniciales antes de esa prueba.
- `python tests_manual/verificar_postgres.py` prepara su propia base temporal y no modifica la base normal; requiere el servicio `postgres` en ejecución y `.env` configurado.

## Detener

```bash
docker compose down        # detiene y conserva los datos
docker compose down -v     # detiene y borra los datos
```

## Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `Copia .env.example a .env y configura DB_PASSWORD` | Falta el archivo `.env` o la variable `DB_PASSWORD`. Ejecuta `cp .env.example .env` y define la contraseña. |
| `port is already allocated` o `address already in use` | El puerto 8000 o 5432 está ocupado. Detén el otro proceso, o cambia `DB_PORT` en `.env` (PostgreSQL) o el mapeo `8000:8000` en `docker-compose.yml` (API). |
| `GET /salas` responde 500 y el log dice `relation "salas" does not exist` | Las migraciones no se aplicaron. Ejecuta `docker compose exec api python -m alembic upgrade head` y revisa `docker compose logs api`. |
| `Cannot connect to the Docker daemon` | Docker no está en ejecución. En Linux: `sudo systemctl start docker`. En Windows y macOS, abre Docker Desktop. |
| `permission denied ... docker.sock` (Linux) | Tu usuario no pertenece al grupo `docker`. Usa `sudo` delante del comando o agrégate con `sudo usermod -aG docker $USER` y reinicia la sesión. |
| `unknown command: docker compose` | Falta el plugin de Compose. Instálalo con el gestor de paquetes de tu distribución. |
| Cambié el código y no veo los cambios | La imagen copia el código al construirse. Reconstruye con `docker compose up --build -d`. |

## Archivos relacionados

- `Dockerfile`: define la imagen de la API (aplica migraciones y arranca Uvicorn).
- `docker-compose.yml`: levanta la API y PostgreSQL, con volumen persistente y credenciales por variables de entorno.
- `.env.example`: plantilla de variables `DB_*`; el archivo `.env` real no se sube al repositorio.
- `.dockerignore`: excluye `.venv`, `.git`, caches, `.env` y `tests_manual/` de la imagen.
- `migrations/` y `alembic.ini`: migraciones de la base de datos.