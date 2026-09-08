from pydantic import BaseModel, ConfigDict, Field, field_validator


class SalaCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(min_length=3, max_length=80)
    capacidad: int = Field(gt=0, strict=True)
    ubicacion: str = Field(min_length=3, max_length=120)
    equipamiento: list[str] = Field(default_factory=list)

    @field_validator("nombre", "ubicacion")
    @classmethod
    def sin_espacios_extremos(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("El campo no puede estar vacío")
        return valor


class SalaActualizar(SalaCrear):
    """PUT reemplaza todos los datos editables de la sala.""" # Si quitan lo de azul tirara error,
                                                              # ya que por defecto no se puede tener una clase vacia.     

class SalaRespuesta(SalaCrear):
    id: int = Field(gt=0, strict=True)