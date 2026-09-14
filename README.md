# Evaluación 1 Backend

Base de una API de reservas con Python y FastAPI. Los datos se almacenarán exclusivamente en memoria.

# Instalación

Requiere Python 3.10 o superior. Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Si `python3` apunta a una versión anterior, utiliza `python3.12` para crear el entorno.
Pydantic se instala como dependencia de FastAPI.

# Ejecución

Con el entorno virtual activado:

```bash
uvicorn app.main:app --reload
```


# API Backend - Sistema de Gestión FastAPI

# Integrantes y Responsabilidades:

* Rol N°1 (Coordinación y Documentación): Organización de tareas, creación y mantenimiento del README, especificación del contrato de endpoints (P1-P7), revisión de documentación OpenAPI/Swagger, integración de ramas Git y coordinación de la presentación final.

* Rol N°2 (Dominio y Datos): Definición de las 4 entidades del dominio, sus atributos, relaciones, schemas/DTOs, validaciones y gestión de almacenamiento en memoria.

* Rol N°3 (API y Lógica de Negocio): Implementación de endpoints, ruteo, servicios, operaciones CRUD, reglas de negocio y manejo de excepciones/errores HTTP.

* Rol N°4 (Calidad y Pruebas):Pruebas integrales de endpoints en Postman/Thunder Client, verificación de respuestas HTTP, filtros, ordenamiento y paginación.

# Tecnologías Utilizadas

* Lenguaje: Python 3.10+.
* Framework Web: FastAPI.
* Servidor ASGI: Uvicorn.
* Validación de Datos: Pydantic.
* Documentación Interactiva: Swagger UI / OpenAPI (`http://127.0.0.1:8000/docs`).

# Contrato de Endpoints y Requisitos (P1 - P7)

* P1 Documentación y Estructura Base: Configuración general del proyecto, Swagger UI accesible en `/docs` y definición de schemas/DTOs mediante Pydantic.

* P2 Definición de Entidades de Dominio: Implementación de las 4 entidades principales con tipos de datos estrictos y validaciones de atributos.

* P3 Operaciones CRUD: Endpoints para creación (`POST`), lectura (`GET`), actualización (`PUT`/`PATCH`) y eliminación (`DELETE`).

* P4 Reglas de Negocio: Validación en capa de servicios para prevenir solapamiento/conflictos de datos y control de capacidad o disponibilidad.

* P5 Manejo de Errores y Códigos HTTP: Emisión de respuestas estandarizadas usando `HTTPException` (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 422 Unprocessable Entity).

* P6 Paginación y Filtrado: Parámetros de consulta (`Query Params`) para filtrar registros por atributos específicos y limitar/paginar los resultados devueltos.

* P7 Pruebas y Validación End-to-End: Verificación del correcto funcionamiento con colecciones de pruebas en Postman / Thunder Client.
