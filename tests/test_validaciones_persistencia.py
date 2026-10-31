"""Pydantic rechaza entradas incompatibles con el almacenamiento antes de escribir."""
import unittest
from pydantic import ValidationError
from presentation.schemas.dtos.sala import SalaCrear, SalaActualizar
from presentation.schemas.dtos.estudiante import EstudianteCrear
from presentation.schemas.dtos.incidencia_sala import IncidenciaSalaCrear
from presentation.schemas.dtos.reserva import ReservaCrear


class ValidacionesPersistenciaTests(unittest.TestCase):
    def test_capacidad_fuera_de_rango_rechazada_en_post_y_put(self):
        for modelo in (SalaCrear, SalaActualizar):
            with self.subTest(modelo=modelo.__name__), self.assertRaises(ValidationError):
                modelo(nombre='Sala normal', capacidad=2147483648, ubicacion='Piso 1')

    def test_maximo_integer_aceptado(self):
        sala = SalaCrear(nombre='Sala normal', capacidad=2147483647, ubicacion='Piso 1')
        self.assertEqual(sala.capacidad, 2147483647)

    def test_cantidad_personas_fuera_de_rango_rechazada(self):
        with self.assertRaises(ValidationError):
            ReservaCrear(sala_id=1, estudiante_id=1, fecha='2026-11-10',
                         hora_inicio='10:00', hora_fin='11:00', cantidad_personas=2147483648)

    def test_nul_rechazado_en_textos_de_las_entidades(self):
        casos = [
            (SalaCrear,dict(nombre='Sala normal',capacidad=5,ubicacion='Piso 1'),['nombre','ubicacion']),
            (SalaActualizar,dict(nombre='Sala normal',capacidad=5,ubicacion='Piso 1'),['nombre','ubicacion']),
            (EstudianteCrear,dict(nombre='Ana Pérez',carrera='Informática',correo='ana@example.com'),['nombre','carrera']),
            (IncidenciaSalaCrear,dict(sala_id=1,reporte='Falta plumón',fecha='2026-11-10'),['reporte']),
        ]
        for modelo,datos,campos in casos:
            for campo in campos:
                with self.subTest(modelo=modelo.__name__,campo=campo), self.assertRaises(ValidationError):
                    modelo(**{**datos,campo:'Texto\x00inválido'})

    def test_equipamiento_con_nul_rechazado(self):
        with self.assertRaises(ValidationError):
            SalaCrear(nombre='Sala normal',capacidad=5,ubicacion='Piso 1',equipamiento=['Pizarra\x00'])

    def test_textos_validos_con_tildes_y_saltos_se_conservan(self):
        incidencia = IncidenciaSalaCrear(sala_id=1,reporte='Proyector sin señal.\nRevisar conexión.',fecha='2026-11-10')
        self.assertEqual(incidencia.reporte, 'Proyector sin señal.\nRevisar conexión.')
