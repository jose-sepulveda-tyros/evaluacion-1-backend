"""Operaciones comunes de almacenamiento; los servicios reciben entidades."""
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from domain.errors import ConflictoPersistenciaError


class Repository:
    model = None
    mapper = None

    def __init__(self, session: Session):
        self.session = session

    def bloquear_reglas(self):
        """Serializa escrituras que comparten reglas de reservas en PostgreSQL.

        El bloqueo es transaccional: se libera al hacer commit/rollback o cerrar
        la sesión. Todos los servicios que cambian reservas/capacidad lo piden
        antes de leer. SQLite solo se usa para pruebas locales secuenciales.
        """
        if self.session.bind.dialect.name == "postgresql":
            self.session.execute(text("SELECT pg_advisory_xact_lock(1108, 1)"))

    def _confirmar(self):
        try:
            self.session.commit()
        except IntegrityError as exc:
            self.session.rollback()
            raise ConflictoPersistenciaError(
                "La operación entra en conflicto con los recursos relacionados"
            ) from exc
        except Exception:
            self.session.rollback()
            raise

    def crear(self, entidad):
        modelo = self.mapper.a_modelo(entidad)
        self.session.add(modelo)
        self._confirmar()
        return self.mapper.a_dominio(modelo)

    def listar(self):
        return [self.mapper.a_dominio(modelo) for modelo in
                self.session.scalars(select(self.model).order_by(self.model.id))]

    def obtener(self, identificador):
        modelo = self.session.get(self.model, identificador)
        return self.mapper.a_dominio(modelo) if modelo is not None else None

    def existe(self, identificador):
        return self.session.get(self.model, identificador) is not None

    def actualizar(self, identificador, entidad):
        modelo = self.session.get(self.model, identificador)
        if modelo is None:
            return None
        reemplazo = self.mapper.a_modelo(entidad)
        for columna in self.model.__table__.columns:
            if columna.name != "id":
                setattr(modelo, columna.name, getattr(reemplazo, columna.name))
        self._confirmar()
        return self.mapper.a_dominio(modelo)

    def eliminar(self, identificador):
        modelo = self.session.get(self.model, identificador)
        if modelo is None:
            return False
        self.session.delete(modelo)
        self._confirmar()
        return True
