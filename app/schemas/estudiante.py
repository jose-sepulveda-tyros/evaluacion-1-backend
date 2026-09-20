from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EstudianteCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(min_length=3, max_length=80)
    carrera: str = Field(min_length=3, max_length=80)
    correo: EmailStr
    activo: bool = True

class EstudianteActualizar(EstudianteCrear):
    pass


class EstudianteRespuesta(EstudianteCrear):
    id: int = Field(gt=0, strict=True)