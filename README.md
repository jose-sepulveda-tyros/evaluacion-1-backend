# Evaluación 1 Backend

Base de una API de reservas con Python y FastAPI. Los datos se almacenarán exclusivamente en memoria.

## Instalación

Requiere Python 3.10 o superior. Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Si `python3` apunta a una versión anterior, utiliza `python3.12` para crear el entorno.
Pydantic se instala como dependencia de FastAPI.

## Ejecución

Con el entorno virtual activado:

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs
