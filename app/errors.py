"""Convierte los errores de servicios y validación al contrato HTTP del proyecto."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.error import DetalleValidacion, ErrorDetalle, ErrorRespuesta
from app.services.reserva_service import (
    HorarioInvalidoError,
    LimiteReservasError,
    ReservaNoEncontradaError,
    ReservaSuperpuestaError,
)


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(ReservaNoEncontradaError)
    async def reserva_no_encontrada(
        request: Request, exc: ReservaNoEncontradaError
    ) -> JSONResponse:
        respuesta = ErrorRespuesta(
            error=ErrorDetalle(code="RESOURCE_NOT_FOUND", message=str(exc))
        )
        return JSONResponse(status_code=404, content=respuesta.model_dump(mode="json"))

    @app.exception_handler(HorarioInvalidoError)
    async def horario_invalido(
        request: Request, exc: HorarioInvalidoError
    ) -> JSONResponse:
        respuesta = ErrorRespuesta(
            error=ErrorDetalle(code="INVALID_TIME_RANGE", message=str(exc))
        )
        return JSONResponse(status_code=400, content=respuesta.model_dump(mode="json"))

    @app.exception_handler(ReservaSuperpuestaError)
    async def reserva_superpuesta(
        request: Request, exc: ReservaSuperpuestaError
    ) -> JSONResponse:
        respuesta = ErrorRespuesta(
            error=ErrorDetalle(code="RESERVATION_OVERLAP", message=str(exc))
        )
        return JSONResponse(status_code=409, content=respuesta.model_dump(mode="json"))

    @app.exception_handler(LimiteReservasError)
    async def limite_reservas(
        request: Request, exc: LimiteReservasError
    ) -> JSONResponse:
        respuesta = ErrorRespuesta(
            error=ErrorDetalle(code="DAILY_RESERVATION_LIMIT", message=str(exc))
        )
        return JSONResponse(status_code=400, content=respuesta.model_dump(mode="json"))

    @app.exception_handler(RequestValidationError)
    async def datos_invalidos(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        respuesta = ErrorRespuesta(
            error=ErrorDetalle(
                code="VALIDATION_ERROR",
                message="Los datos de la solicitud no son válidos",
                details=[
                    DetalleValidacion(
                        campo=list(error["loc"]),
                        mensaje=error["msg"],
                        tipo=error["type"],
                    )
                    for error in exc.errors()
                ],
            )
        )
        return JSONResponse(status_code=422, content=respuesta.model_dump(mode="json"))
