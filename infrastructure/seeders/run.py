"""Uso: python -m infrastructure.seeders.run (después de alembic upgrade head).

    El comando de ejecución seria -> docker compose exec api python -m infrastructure.seeders.run
"""
from infrastructure.database import SessionLocal
from .seed import sembrar


def main() -> None:
    with SessionLocal() as session:
        resultado = sembrar(session)
    if not any(resultado.values()):
        print("Carga omitida: ya existen datos en alguna tabla. No se modificó ninguna tabla.")
        return
    for tabla, cantidad in resultado.items():
        print(f"{tabla}: {cantidad} insertadas")


if __name__ == "__main__":
    main()