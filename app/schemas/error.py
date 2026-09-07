from pydantic import BaseModel, Field


class DetalleValidacion(BaseModel):
    campo: list[str | int]
    mensaje: str
    tipo: str


class ErrorDetalle(BaseModel):
    code: str
    message: str
    details: list[DetalleValidacion] = Field(default_factory=list)


class ErrorRespuesta(BaseModel):
    error: ErrorDetalle
