"""Restricciones de entrada compatibles con los tipos de almacenamiento."""
from typing import Annotated
from pydantic import AfterValidator

MAX_ENTERO_POSTGRES = 2_147_483_647


def validar_texto_sin_nul(valor: str) -> str:
    if '\x00' in valor:
        raise ValueError('El texto no puede contener el carácter NUL (U+0000)')
    return valor


TextoSinNul = Annotated[str, AfterValidator(validar_texto_sin_nul)]
