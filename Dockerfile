FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# mientras las dependencias no cambien.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY application ./application
COPY domain ./domain
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini
COPY infrastructure ./infrastructure
COPY presentation ./presentation

# El contenedor no necesita privilegios de root.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/docs')"

# 0.0.0.0 es obligatorio dentro del contenedor; con 127.0.0.1 no sería accesible desde fuera.
# Primero aplica las migraciones (crea/actualiza las tablas) y luego inicia la API.
# Si la migración falla, el contenedor termina y no arranca una API sin tablas.
CMD ["sh", "-c", "python -m alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]