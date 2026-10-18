# Ejecución con Docker

La API puede correr dentro de un contenedor, sin instalar Python ni crear un entorno virtual. La imagen incluye Python 3.12 y las dependencias con las versiones fijadas de `requirements.txt`.

## Requisitos

- Docker instalado y en ejecución.
- Docker Compose (opcional, simplifica los comandos). En Windows y macOS viene incluido en Docker Desktop.
- Puerto `8000` libre. Si ejecutas Uvicorn localmente, deténlo antes.

## Opción 1: Docker Compose (recomendada)

Desde la raíz del repositorio:

```bash
docker compose up --build
```

Para detenerlo, presiona `Ctrl+C` y luego:

```bash
docker compose down
```

Para dejarlo corriendo en segundo plano, agrega `-d` a `docker compose up --build`.

## Opción 2: solo Docker

```bash
docker build -t api-reservas .
docker run --rm -p 8000:8000 api-reservas
```

Se detiene con `Ctrl+C`; la opción `--rm` elimina el contenedor al salir.

## Comprobar que funciona

Con el contenedor en ejecución:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Si Swagger muestra los grupos Reservas, Salas, Estudiantes e Incidencias, la API está funcionando.

## Datos y pruebas

- Los datos viven **en memoria**: se pierden cada vez que el contenedor se detiene o reinicia. Es el comportamiento esperado, ya que el proyecto no usa base de datos.
- Para partir de una instancia vacía antes de repetir la colección de pruebas, reinicia el contenedor: `docker compose restart` (o detén y vuelve a ejecutar `docker run`).
- La colección `tests_manual/pruebas.http` apunta a `http://127.0.0.1:8000`, así que funciona igual contra el contenedor. Se ejecuta desde tu máquina, no dentro del contenedor.

## Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `port is already allocated` o `address already in use` | El puerto 8000 está ocupado. Detén Uvicorn local u otro contenedor, o cambia el mapeo a `-p 8001:8000` y abre `http://127.0.0.1:8001/docs`. |
| `Cannot connect to the Docker daemon` | Docker no está en ejecución. En Linux: `sudo systemctl start docker`. En Windows y macOS, abre Docker Desktop. |
| `permission denied ... docker.sock` (Linux) | Tu usuario no pertenece al grupo `docker`. Usa `sudo` delante del comando o agrégate con `sudo usermod -aG docker $USER` y reinicia la sesión. |
| `unknown command: docker compose` | Falta el plugin de Compose. Instálalo con el gestor de paquetes de tu distribución, o usa la opción 2. |
| Cambié el código y no veo los cambios | La imagen copia el código al construirse. Reconstruye con `docker compose up --build`. |

## Archivos relacionados

- `Dockerfile`: define la imagen de la API.
- `docker-compose.yml`: levanta la API con un solo comando.
- `.dockerignore`: excluye `.venv`, `.git`, caches y `tests_manual/` de la imagen.
