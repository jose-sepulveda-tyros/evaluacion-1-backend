import os
import unittest
from unittest.mock import patch

_TEST_DB_CONFIG = {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "reservas_test",
    "DB_USER": "reservas_test",
    "DB_PASSWORD": "test_only_password",
}
with patch.dict(os.environ, _TEST_DB_CONFIG):
    from infrastructure.database import build_database_url
    from presentation import dependencies


class DatabaseConfigurationTests(unittest.TestCase):
    def test_database_url_uses_postgresql_and_preserves_password(self):
        url = build_database_url(
            {
                "DB_HOST": "localhost",
                "DB_PORT": "5432",
                "DB_NAME": "reservas",
                "DB_USER": "reservas",
                "DB_PASSWORD": "p@ss:word",
            }
        )

        self.assertEqual(
            url.render_as_string(hide_password=False),
            "postgresql+psycopg2://reservas:p%40ss%3Aword@localhost:5432/reservas",
        )

    def test_get_session_closes_session_after_response(self):
        class FakeSession:
            closed = False

            def close(self):
                self.closed = True

        session = FakeSession()
        dependency = dependencies.get_session()

        with patch.object(dependencies, "SessionLocal", return_value=session):
            yielded = next(dependency)
            dependency.close()

        self.assertIs(yielded, session)
        self.assertTrue(session.closed)


if __name__ == "__main__":
    unittest.main()
