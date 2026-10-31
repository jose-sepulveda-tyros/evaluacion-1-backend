"""Prueba el contrato de almacenamiento, sin usar la base de desarrollo."""
import unittest
from datetime import date, time
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tests.test_database import _TEST_DB_CONFIG
from infrastructure.database import Base
from infrastructure.models import SalaModel, EstudianteModel, ReservaModel, IncidenciaSalaModel
from domain.sala import Sala
from domain.estudiante import Estudiante
from domain.reserva import Reserva
from domain.incidencia_sala import IncidenciaSala
from infrastructure.mappers import sala_mapper, estudiante_mapper, reserva_mapper, incidencia_mapper


class ModelosTests(unittest.TestCase):
    def setUp(self):
        # SQLite solo verifica el contrato local; no sustituye la prueba PostgreSQL.
        self.engine = create_engine("sqlite://")
        event.listen(self.engine, "connect", lambda conn, _: conn.execute("PRAGMA foreign_keys=ON"))
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_modelos_conservan_datos_y_mappers_no_comparten_listas(self):
        sala = Sala(id=None, nombre="Sala Norte", capacidad=6, ubicacion="Piso 1", equipamiento=["Pizarra"])
        modelo = sala_mapper.a_modelo(sala)
        self.session.add(modelo)
        self.session.flush()
        estudiante = Estudiante(id=None, nombre="Ana Pérez", carrera="Informática", correo="ana@example.com", activo=True)
        alumno = estudiante_mapper.a_modelo(estudiante)
        self.session.add(alumno)
        self.session.flush()
        reserva = Reserva(id=None, sala_id=modelo.id, estudiante_id=alumno.id, fecha=date(2026,11,3), hora_inicio=time(10), hora_fin=time(11), cantidad_personas=3, estado="activa")
        incidencia = IncidenciaSala(id=None, sala_id=modelo.id, reporte="Falta un plumón", fecha=date(2026,11,3), resuelto=False)
        reservada = reserva_mapper.a_modelo(reserva)
        reportada = incidencia_mapper.a_modelo(incidencia)
        self.session.add_all([reservada, reportada])
        self.session.commit()
        self.session.expire_all()
        copia = sala_mapper.a_dominio(self.session.get(SalaModel, modelo.id))
        self.assertEqual((copia.nombre, copia.capacidad, copia.ubicacion, copia.equipamiento), ("Sala Norte",6,"Piso 1",["Pizarra"]))
        copia.equipamiento.append("Proyector")
        self.assertEqual(modelo.equipamiento, ["Pizarra"])
        self.assertEqual(sala.equipamiento, ["Pizarra"])
        for original, orm, mapper in [(estudiante, alumno, estudiante_mapper), (reserva, reservada, reserva_mapper), (incidencia, reportada, incidencia_mapper)]:
            with self.subTest(tipo=type(original).__name__):
                original.id = orm.id
                self.assertEqual(mapper.a_dominio(orm), original)
        self.assertEqual([r.id for r in modelo.reservas], [reservada.id])
        self.assertEqual([r.id for r in alumno.reservas], [reservada.id])
        self.assertEqual([r.id for r in modelo.incidencias], [reportada.id])

    def test_relaciones_rechazan_referencias_inexistentes(self):
        casos = [
            ReservaModel(sala_id=999, estudiante_id=999, fecha=date(2026,11,3), hora_inicio=time(10), hora_fin=time(11), cantidad_personas=2, estado="activa"),
            IncidenciaSalaModel(sala_id=999, reporte="Sin luz en la sala", fecha=date(2026,11,3), resuelto=False),
        ]
        for modelo in casos:
            with self.subTest(tabla=modelo.__tablename__):
                self.session.add(modelo)
                with self.assertRaises(IntegrityError):
                    self.session.commit()
                self.session.rollback()

    def test_claves_foraneas_apuntan_a_las_entidades_correctas(self):
        inspector = inspect(self.engine)
        self.assertEqual(set(inspector.get_table_names()), {"salas", "estudiantes", "reservas", "incidencias"})
        self.assertEqual({(tuple(f["constrained_columns"]), f["referred_table"]) for f in inspector.get_foreign_keys("reservas")}, {(("sala_id",), "salas"), (("estudiante_id",), "estudiantes")})
        self.assertEqual(inspector.get_foreign_keys("incidencias")[0]["referred_table"], "salas")
