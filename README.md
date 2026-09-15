# Sistema de Reservas de Salas de Estudio

Proyecto grupal de Desarrollo de Backend (ICINF1108). API REST para registrar salas, estudiantes, reservas e incidencias del campus. Usa Python, FastAPI, Pydantic y Uvicorn, con almacenamiento exclusivamente en memoria mediante diccionarios.

## Equipo y responsabilidades

El líder del grupo es **José Sepúlveda**, quien también asume el rol de API y lógica de negocio.

| Integrante | Rol | Cuenta de GitHub | Responsabilidad principal |
|---|---|---|---|
| Lissete Delgado | 1. Coordinación y documentación | `aloliss-17` | Planificación, README, P1–P7, revisión de Swagger, coordinación de integración y presentación. |
| Benjamín Leal | 2. Dominio y datos | `benjamin-leal` | Entidades, atributos, relaciones, schemas/DTO, validaciones y repositorios en memoria. |
| José Sepúlveda | 3. API y lógica de negocio; líder del grupo | `jose-sepulveda-tyros` | Liderazgo del grupo, endpoints, servicios, CRUD, reglas de negocio y manejo de errores. |
| Elías Gutiérrez | 4. Calidad y pruebas | `rosbosman` | Casos exitosos y de error, colección de pruebas y revisión de filtros, ordenamiento y paginación. |

Todos deben comprender y poder explicar el funcionamiento completo. Las responsabilidades no impiden colaborar en correcciones e integración.

## Instalación y ejecución

Requiere Python 3.10 o superior. El entorno local de desarrollo se verificó con Python 3.12. Desde la carpeta raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Si `python3` apunta a una versión anterior a 3.10, usa `python3.12 -m venv .venv`. En Windows, la activación en PowerShell es `.venv\Scripts\Activate.ps1`.

- [Swagger UI](http://127.0.0.1:8000/docs): permite consultar los modelos y ejecutar solicitudes con **Try it out**.
- [OpenAPI JSON](http://127.0.0.1:8000/openapi.json): contrato generado por FastAPI.
- `requirements.txt` fija FastAPI, Uvicorn y `email-validator`; Pydantic se instala como dependencia de FastAPI.

La aplicación inicia sin datos. Primero registra una sala y un estudiante y usa sus IDs al crear una reserva. Cada reinicio, incluido el provocado por `--reload`, borra los registros y reinicia los contadores. Ejecuta una sola instancia/proceso: los diccionarios no se comparten entre procesos.

## Problemática y alcance: P1–P7

### P1. Situación actual

Los estudiantes reservan salas de estudio presencialmente o mediante mensajes informales. No existe una consulta centralizada que permita conocer las reservas registradas y sus horarios.

### P2. Actores

- **Estudiante:** registra y consulta sus reservas.
- **Administrador del campus:** administra salas y consulta, registra o resuelve incidencias.

Estos actores describen el uso del sistema; la entrega no implementa autenticación ni permisos por rol.

### P3. Consecuencias

Se producen reservas duplicadas o superpuestas, estudiantes encuentran ocupadas salas que creían disponibles y los administradores pierden tiempo resolviendo conflictos manualmente.

### P4. Información administrada

| Entidad | Atributos |
|---|---|
| Sala | `id`, `nombre`, `capacidad`, `ubicacion`, `equipamiento` |
| Estudiante | `id`, `nombre`, `carrera`, `correo`, `activo` |
| Reserva | `id`, `sala_id`, `estudiante_id`, `fecha`, `hora_inicio`, `hora_fin`, `cantidad_personas`, `estado` |
| IncidenciaSala | `id`, `sala_id`, `reporte`, `fecha`, `resuelto` |

Cada sala puede tener muchas reservas e incidencias. Cada estudiante puede tener muchas reservas. Los servicios comprueban la existencia de los recursos relacionados antes de registrar los datos.

### P5. Acciones que permite la API

1. El sistema debe permitir registrar una reserva.
2. El sistema debe permitir listar y consultar una reserva por ID.
3. El sistema debe permitir actualizar una reserva.
4. El sistema debe permitir eliminar una reserva.
5. El sistema debe permitir registrar una sala.
6. El sistema debe permitir listar, consultar y actualizar salas.
7. El sistema debe permitir registrar estudiantes.
8. El sistema debe permitir listar y consultar estudiantes por ID.
9. El sistema debe permitir registrar incidencias para una sala.
10. El sistema debe permitir listar incidencias y cambiar su estado de resolución.
11. El sistema debe permitir filtrar, ordenar y paginar las reservas.

### P6. Fuera de alcance

No incluye frontend, aplicación móvil, autenticación, envío de correos/notificaciones, base de datos ni despliegue en Internet. Los datos no persisten después de detener el servidor.

### P7. Criterios de aceptación

- Una reserva válida para recursos existentes se crea con HTTP 201.
- Si `hora_fin <= hora_inicio`, la reserva se rechaza con 400.
- Una reserva activa superpuesta en la misma sala y fecha se rechaza con 409.
- Una tercera reserva activa del estudiante durante el mismo día se rechaza con 400.
- Si la cantidad de personas supera la capacidad de la sala, se rechaza con 400.
- Consultar un recurso inexistente devuelve 404; los datos que incumplen el schema devuelven 422.
- La colección de reservas filtra, ordena y pagina, en ese orden, devolviendo sus metadatos.
- Una operación rechazada no modifica el registro existente ni crea uno nuevo.

## Arquitectura

```text
app/
  main.py                 # Configura FastAPI y registra routers y manejadores.
  errors.py               # Traduce excepciones de servicios/validación a HTTP.
  routers/                # Entrada HTTP, DTO y respuestas.
  schemas/                # Modelos Pydantic y validaciones de datos.
  services/               # Casos de uso y reglas de negocio.
  repositories/           # Diccionarios, IDs y operaciones de almacenamiento.
  domain/                 # Paquete reservado; actualmente sin entidades separadas.
tests_manual/
  pruebas.http            # Colección ejecutable de solicitudes.
  verificar_coleccion.py  # Verifica resultados por HTTP con la biblioteca estándar.
```

Flujo: solicitud → router → schema Pydantic → servicio → repositorio → modelo de respuesta. FastAPI valida y serializa la salida. Actualmente se almacenan modelos Pydantic de respuesta en los diccionarios; no hay una segunda representación de entidades en `domain/`.

## Reglas y validaciones

**Pydantic** comprueba IDs y cantidades positivas, longitudes, fechas, horas y correos (`EmailStr`). Los estados de reserva son `activa` y `cancelada`. Los modelos de entrada rechazan campos adicionales. Las horas representan la hora local del campus, sin zona horaria.

**Los servicios** aplican las siguientes reglas:

1. La hora final debe ser estrictamente posterior a la inicial. Una reserva no cruza la medianoche.
2. No se admiten reservas activas superpuestas de una sala en la misma fecha. Los horarios contiguos, como 10:00–11:00 y 11:00–12:00, son compatibles.
3. Un estudiante puede tener como máximo dos reservas activas por fecha.
4. La cantidad de personas no puede superar la capacidad de la sala.
5. La sala y el estudiante deben existir al crear o actualizar una reserva; la sala debe existir al registrar una incidencia.
6. Actualizar la capacidad de una sala no puede dejar una reserva activa con más personas que la nueva capacidad: devuelve 409.

Al actualizar una reserva se excluye su propio ID de las comparaciones de superposición y límite diario. Las canceladas no ocupan horario ni consumen el límite, pero deben tener recursos existentes, un horario válido y una cantidad compatible con la capacidad. El campo `activo` del estudiante es informativo: no existe una regla que impida reservar por estar inactivo.

## Contrato de los 15 endpoints

Los schemas completos de entrada y salida se consultan en Swagger. Los IDs de las rutas deben ser enteros positivos.

| Método | Ruta | Entrada JSON | Respuesta exitosa | Errores controlados |
|---|---|---|---|---|
| POST | `/reservas` | `ReservaCrear` | 201, `ReservaRespuesta` | 400, 404, 409, 422 |
| GET | `/reservas` | Parámetros de consulta | 200, `ReservaPagina` | 422 |
| GET | `/reservas/{reserva_id}` | — | 200, `ReservaRespuesta` | 404, 422 |
| PUT | `/reservas/{reserva_id}` | `ReservaActualizar` | 200, `ReservaRespuesta` | 400, 404, 409, 422 |
| DELETE | `/reservas/{reserva_id}` | — | 204, sin cuerpo | 404, 422 |
| POST | `/salas` | `SalaCrear` | 201, `SalaRespuesta` | 422 |
| GET | `/salas` | — | 200, lista de `SalaRespuesta` | — |
| GET | `/salas/{sala_id}` | — | 200, `SalaRespuesta` | 404, 422 |
| PUT | `/salas/{sala_id}` | `SalaActualizar` | 200, `SalaRespuesta` | 404, 409, 422 |
| POST | `/estudiantes` | `EstudianteCrear` | 201, `EstudianteRespuesta` | 422 |
| GET | `/estudiantes` | — | 200, lista de `EstudianteRespuesta` | — |
| GET | `/estudiantes/{estudiante_id}` | — | 200, `EstudianteRespuesta` | 404, 422 |
| POST | `/incidencias` | `IncidenciaSalaCrear` | 201, `IncidenciaSalaRespuesta` | 404, 422 |
| GET | `/incidencias` | — | 200, lista de `IncidenciaSalaRespuesta` | — |
| PUT | `/incidencias/{incidencia_id}` | `IncidenciaSalaActualizar` | 200, `IncidenciaSalaRespuesta` | 404, 422 |

- La API genera los IDs; no deben enviarse en el cuerpo.
- Los POST de reservas, salas y estudiantes incluyen `Location` con la ruta de consulta del nuevo recurso.
- `PUT /reservas/{id}` exige todos los campos editables, incluido `estado`. No se implementa PATCH.
- `PUT /salas/{id}` sustituye sus datos. Omitir `equipamiento` lo deja como lista vacía.
- `equipamiento` es una lista de textos, por ejemplo `["Pizarra"]`.
- Según el DTO del equipo, `PUT /incidencias/{id}` acepta únicamente `{"resuelto": true}` o `{"resuelto": false}`. Conserva sala, reporte y fecha.

### Filtros, ordenamiento y paginación

```http
GET /reservas?sala_id=1&estado=activa&ordenar_por=fecha&direccion=asc&pagina=1&limite=10
```

| Parámetro | Valores / comportamiento |
|---|---|
| `fecha` | Fecha `AAAA-MM-DD`, opcional. |
| `sala_id`, `estudiante_id` | ID positivo, opcional. |
| `estado` | `activa` o `cancelada`, opcional. |
| `ordenar_por` | `fecha`, `hora_inicio`, `hora_fin` o `id`; predeterminado `id`. |
| `direccion` | `asc` o `desc`; predeterminado `asc`. |
| `pagina` | Entero desde 1; predeterminado 1. |
| `limite` | Entero entre 1 y 100; predeterminado 10. |

Los filtros se combinan. El ID desempata el orden. `total` se calcula después de filtrar y antes de paginar. Una página fuera de rango devuelve `items: []` y conserva los totales. Sin coincidencias, `total_paginas` es 0.

Ejemplo de respuesta sin coincidencias:

```json
{"items": [], "total": 0, "pagina": 1, "limite": 10, "total_paginas": 0}
```

### Errores

Los errores controlados de negocio, recursos y validación conservan esta estructura:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "No existe una reserva con el ID 999",
    "details": []
  }
}
```

| HTTP | Situación / códigos de error |
|---|---|
| 400 | `INVALID_TIME_RANGE`, `DAILY_RESERVATION_LIMIT`, `ROOM_CAPACITY_EXCEEDED`. |
| 404 | `RESOURCE_NOT_FOUND`. |
| 409 | `RESERVATION_OVERLAP`, `ROOM_CAPACITY_CONFLICT`. |
| 422 | `VALIDATION_ERROR`; `details` contiene `campo`, `mensaje` y `tipo`. |

Las rutas o métodos no implementados conservan los errores predeterminados de FastAPI/Starlette (por ejemplo, `{"detail": "Method Not Allowed"}` para PATCH).

## Pruebas reproducibles

La colección [tests_manual/pruebas.http](tests_manual/pruebas.http) amplía el archivo inicial del rol 4. Contiene 63 casos con resultados esperados, cobertura de los 15 endpoints, reglas de negocio, validaciones y paginación con varios registros.

1. Inicia Uvicorn sobre una instancia vacía con el comando de ejecución anterior.
2. En otra terminal, desde la raíz del proyecto y con `.venv` activado, ejecuta:

```bash
python tests_manual/verificar_coleccion.py
```

Para otro puerto:

```bash
python tests_manual/verificar_coleccion.py --base-url http://127.0.0.1:8001
```

El verificador comprueba códigos HTTP, campos esperados, headers declarados, errores uniformes, cuerpo vacío en 204 y cobertura de las operaciones publicadas en OpenAPI. Se detiene en el primer fallo con código de salida 1. Las primeras cuatro consultas exigen una API sin datos; no borra datos para preparar el entorno.

Para repetir, detén y vuelve a iniciar Uvicorn. No ejecutes solicitudes manuales entre los casos ni edites archivos mientras corre la colección con `--reload`. Los IDs de ejemplo dependen de ejecutar la secuencia completa sobre memoria vacía.

También puede ejecutarse manualmente en VS Code con la extensión REST Client, usando **Send Request** en cada bloque de `pruebas.http`, de arriba hacia abajo. Las líneas `# expect` indican qué respuesta revisar; solo el verificador Python las comprueba automáticamente.
