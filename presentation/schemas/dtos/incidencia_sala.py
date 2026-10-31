from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from .validaciones import TextoSinNul


class IncidenciaSalaCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sala_id: int = Field(gt=0, strict=True)
    reporte: TextoSinNul = Field(min_length=5, max_length=500)
    fecha: date
    resuelto: bool = False


class IncidenciaSalaActualizar(BaseModel):
    # PUT /incidencias/{id} solo permite marcar la incidencia como resuelta o no.

    model_config = ConfigDict(extra="forbid")

    resuelto: bool


class IncidenciaSalaRespuesta(IncidenciaSalaCrear):
    id: int = Field(gt=0, strict=True)
