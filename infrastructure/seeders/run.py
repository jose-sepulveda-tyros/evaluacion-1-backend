"""Uso: python -m infrastructure.seeders.run (después de alembic upgrade head).

    El comando de ejecución seria -> docker compose exec api python -m infrastructure.seeders.run
"""
from infrastructure.database import SessionLocal
from .seed import sembrar


def main() -> None:
    with SessionLocal() as session:
        resultado = sembrar(session)
    for tabla, cantidad in resultado.items():
        estado = f"{cantidad} insertadas" if cantidad else "ya tenía datos, sin cambios"
        print(f"{tabla}: {estado}")


if __name__ == "__main__":
    main()