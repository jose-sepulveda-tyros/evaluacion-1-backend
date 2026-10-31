"""Ejecuta Alembic en una base temporal; PostgreSQL requiere verificación aparte."""
import unittest
from unittest.mock import patch
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect
from tests.test_database import _TEST_DB_CONFIG
from infrastructure.database import Base
from infrastructure import models


class MigracionInicialTests(unittest.TestCase):
    def test_upgrade_downgrade_upgrade_y_coherencia_con_modelos(self):
        engine = create_engine("sqlite://")
        config = Config("alembic.ini")
        try:
            # Se sustituye únicamente la conexión externa, se ejecuta env.py real.
            with patch("infrastructure.database.engine", engine):
                command.upgrade(config, "head")
                self.assertEqual(set(inspect(engine).get_table_names()),
                                 {"alembic_version", "salas", "estudiantes", "reservas", "incidencias"})
                with engine.connect() as connection:
                    context = MigrationContext.configure(connection)
                    self.assertEqual(context.get_current_revision(), "0001")
                    self.assertEqual(compare_metadata(context, Base.metadata), [])
                command.downgrade(config, "base")
                self.assertEqual(inspect(engine).get_table_names(), ["alembic_version"])
                command.upgrade(config, "head")
                with engine.connect() as connection:
                    self.assertEqual(MigrationContext.configure(connection).get_current_revision(), "0001")
        finally:
            engine.dispose()
