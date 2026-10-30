"""Persistencia entre sesiones y recuperación tras un error de integridad."""
import tempfile
import unittest
from datetime import date, time
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from tests.test_database import _TEST_DB_CONFIG
from infrastructure.database import Base
from infrastructure.repositories.sala_repository import SalaRepository
from infrastructure.repositories.estudiante_repository import EstudianteRepository
from infrastructure.repositories.reserva_repository import ReservaRepository
from infrastructure.repositories.incidencia_repository import IncidenciaRepository
from domain.sala import Sala
from domain.estudiante import Estudiante
from domain.reserva import Reserva
from domain.incidencia_sala import IncidenciaSala
from domain.errors import ConflictoPersistenciaError


class RepositoriosTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.engine = create_engine('sqlite:///' + str(Path(self.temp.name) / 'pruebas.db'))
        event.listen(self.engine, 'connect', lambda conn, _: conn.execute('PRAGMA foreign_keys=ON'))
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()
        self.temp.cleanup()

    def test_crud_persiste_entre_sesiones_para_las_cuatro_entidades(self):
        sala = SalaRepository(self.session).crear(Sala(None,'Sala Norte',6,'Piso uno',['Pizarra']))
        alumno = EstudianteRepository(self.session).crear(Estudiante(None,'Ana Pérez','Informática','ana@example.com',True))
        reserva = ReservaRepository(self.session).crear(Reserva(None,sala.id,alumno.id,date(2026,11,3),time(10),time(11),2,'activa'))
        incidencia = IncidenciaRepository(self.session).crear(IncidenciaSala(None,sala.id,'Falta plumón',date(2026,11,3),False))
        self.session.close()
        self.session = Session(self.engine)
        for cls, entidad, campo, nuevo in [(SalaRepository,sala,'capacidad',8),(EstudianteRepository,alumno,'activo',False),(ReservaRepository,reserva,'estado','cancelada'),(IncidenciaRepository,incidencia,'resuelto',True)]:
            with self.subTest(repositorio=cls.__name__):
                repo = cls(self.session)
                self.assertEqual(repo.obtener(entidad.id),entidad)
                self.assertEqual(repo.listar(),[entidad])
                setattr(entidad,campo,nuevo)
                self.assertEqual(repo.actualizar(entidad.id,entidad),entidad)
                with Session(self.engine) as otra:
                    self.assertEqual(getattr(cls(otra).obtener(entidad.id),campo),nuevo)
                self.assertIsNone(repo.obtener(999))
                self.assertIsNone(repo.actualizar(999,entidad))
        for cls,entidad in [(ReservaRepository,reserva),(IncidenciaRepository,incidencia),(SalaRepository,sala),(EstudianteRepository,alumno)]:
            repo = cls(self.session)
            self.assertTrue(repo.eliminar(entidad.id))
            self.assertFalse(repo.eliminar(entidad.id))
            with Session(self.engine) as otra:
                self.assertEqual(cls(otra).listar(),[])

    def test_error_de_fk_hace_rollback_y_permite_siguiente_operacion(self):
        repo = IncidenciaRepository(self.session)
        with self.assertRaises(ConflictoPersistenciaError):
            repo.crear(IncidenciaSala(None,999,'Falta plumón',date(2026,11,3),False))
        self.assertEqual(repo.listar(),[])
        sala = SalaRepository(self.session).crear(Sala(None,'Sala Norte',6,'Piso uno',[]))
        creada = repo.crear(IncidenciaSala(None,sala.id,'Falta plumón',date(2026,11,3),False))
        with Session(self.engine) as otra:
            self.assertEqual(IncidenciaRepository(otra).obtener(creada.id),creada)
