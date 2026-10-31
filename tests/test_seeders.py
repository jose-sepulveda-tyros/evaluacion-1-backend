"""Carga inicial completa, repetición y protección de registros existentes."""
import unittest
from unittest.mock import patch
from sqlalchemy import create_engine, event, select, func
from sqlalchemy.orm import Session
from tests.test_database import _TEST_DB_CONFIG
from infrastructure.database import Base
from infrastructure.models import SalaModel, EstudianteModel, ReservaModel, IncidenciaSalaModel
from infrastructure.seeders.seed import sembrar
from infrastructure.seeders import datos


class SeedersTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        event.listen(self.engine, 'connect', lambda conn, _: conn.execute('PRAGMA foreign_keys=ON'))
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def cantidades(self):
        return [self.session.scalar(select(func.count()).select_from(model))
                for model in [SalaModel, EstudianteModel, ReservaModel, IncidenciaSalaModel]]

    def test_carga_completa_y_segunda_ejecucion_sin_duplicados(self):
        self.assertEqual(sembrar(self.session), {'salas': 3, 'estudiantes': 3, 'reservas': 5, 'incidencias': 2})
        self.assertEqual(sembrar(self.session), dict.fromkeys(['salas','estudiantes','reservas','incidencias'],0))
        self.assertEqual(self.cantidades(), [3,3,5,2])
        from application.services.reserva_service import ReservaService
        from infrastructure.repositories.reserva_repository import ReservaRepository
        from infrastructure.repositories.sala_repository import SalaRepository
        from infrastructure.repositories.estudiante_repository import EstudianteRepository
        repo = ReservaRepository(self.session)
        service = ReservaService(repo, SalaRepository(self.session), EstudianteRepository(self.session))
        for reserva in repo.listar():
            service.validar_reserva(reserva, reserva.id)
        primera = self.session.scalar(select(SalaModel).order_by(SalaModel.id))
        self.assertEqual(len(primera.reservas), 2)

    def test_una_sala_previa_no_produce_carga_parcial(self):
        self.session.add(SalaModel(nombre='Sala previa',capacidad=1,ubicacion='Piso 1',equipamiento=[]))
        self.session.commit()
        self.assertFalse(any(sembrar(self.session).values()))
        self.assertEqual(self.cantidades(), [1,0,0,0])
        self.assertEqual(self.session.scalar(select(SalaModel)).capacidad,1)

    def test_salas_previas_no_reciben_reservas_semilla(self):
        self.session.add_all([SalaModel(nombre=f'Sala previa {i}',capacidad=1,ubicacion='Piso 1',equipamiento=[]) for i in range(3)])
        self.session.commit()
        self.assertFalse(any(sembrar(self.session).values()))
        self.assertEqual(self.cantidades(), [3,0,0,0])

    def test_un_estudiante_previo_tambien_impide_carga_parcial(self):
        self.session.add(EstudianteModel(nombre='Alumno previo',carrera='Informática',correo='previo@example.com',activo=True))
        self.session.commit()
        self.assertFalse(any(sembrar(self.session).values()))
        self.assertEqual(self.cantidades(), [0,1,0,0])

    def test_error_en_datos_revierte_toda_la_carga(self):
        # Un fallo después de insertar padres debe dejar las cuatro tablas vacías.
        with patch.object(datos, 'RESERVAS', [{**datos.RESERVAS[0], 'sala': 999}]):
            with self.assertRaises(IndexError):
                sembrar(self.session)
        self.assertEqual(self.cantidades(), [0,0,0,0])
