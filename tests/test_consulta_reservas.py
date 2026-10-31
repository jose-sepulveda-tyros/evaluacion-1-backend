"""Consultas SQL con filtros combinados, totales y páginas estables."""
import unittest
from datetime import date
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from tests.test_database import _TEST_DB_CONFIG
from infrastructure.database import Base
from infrastructure.seeders.seed import sembrar
from infrastructure.repositories.reserva_repository import ReservaRepository
from infrastructure.repositories.sala_repository import SalaRepository
from infrastructure.repositories.estudiante_repository import EstudianteRepository
from application.services.reserva_service import ReservaService
from domain.consulta_reservas import ConsultaReservas


class ConsultaReservasTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        sembrar(self.session)
        self.repo = ReservaRepository(self.session)
        self.service = ReservaService(self.repo, SalaRepository(self.session), EstudianteRepository(self.session))

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_filtros_combinados_se_aplican_antes_de_paginar(self):
        items, total = self.repo.consultar(ConsultaReservas(
            fecha=date(2026,11,10), sala_id=1, estudiante_id=1,
            estado='activa', pagina=1, limite=1))
        self.assertEqual([r.id for r in items], [1])
        self.assertEqual(total, 1)

    def test_total_filtrado_no_depende_del_limite(self):
        pagina = self.service.listar_reservas(ConsultaReservas(
            fecha=date(2026,11,10), estado='activa', pagina=2, limite=2))
        self.assertEqual([r.id for r in pagina.items], [3])
        self.assertEqual((pagina.total, pagina.total_paginas, pagina.pagina, pagina.limite), (3,2,2,2))

    def test_orden_descendente_desempata_por_id(self):
        items, total = self.repo.consultar(ConsultaReservas(
            fecha=date(2026,11,10), ordenar_por='fecha', direccion='desc', limite=2))
        self.assertEqual([r.id for r in items], [3,2])
        self.assertEqual(total, 3)

    def test_columnas_de_orden_y_direcciones(self):
        casos = [('id',[1,2,3,4,5]), ('fecha',[1,2,3,4,5]),
                 ('hora_inicio',[4,1,2,5,3]), ('hora_fin',[4,1,2,5,3])]
        for columna, esperado in casos:
            for direccion in ['asc','desc']:
                with self.subTest(columna=columna, direccion=direccion):
                    items, total = self.repo.consultar(ConsultaReservas(ordenar_por=columna,direccion=direccion))
                    self.assertEqual([r.id for r in items], esperado if direccion=='asc' else esperado[::-1])
                    self.assertEqual(total,5)

    def test_pagina_fuera_de_rango_conserva_total_y_sin_coincidencias_da_cero(self):
        for consulta,total,paginas in [(ConsultaReservas(estado='activa',pagina=8,limite=2),4,2),
                                      (ConsultaReservas(sala_id=999),0,0)]:
            with self.subTest(consulta=consulta):
                resultado=self.service.listar_reservas(consulta)
                self.assertEqual(resultado.items,[])
                self.assertEqual((resultado.total,resultado.total_paginas),(total,paginas))

    def test_consulta_de_filas_envia_filtro_orden_y_limite_a_sql(self):
        sentencias=[]
        def capturar(conn,cursor,statement,parameters,context,executemany):
            sentencias.append(statement.upper())
        event.listen(self.engine,'before_cursor_execute',capturar)
        self.repo.consultar(ConsultaReservas(estado='activa',pagina=2,limite=1))
        consultas=[s for s in sentencias if s.lstrip().startswith('SELECT')]
        conteos=[s for s in consultas if 'COUNT(' in s]
        filas=[s for s in consultas if 'COUNT(' not in s]
        self.assertEqual(len(conteos),1)
        self.assertEqual(len(filas),1)
        self.assertNotIn('LIMIT',conteos[0])
        for fragmento in ['WHERE','ORDER BY','LIMIT','OFFSET']:
            self.assertIn(fragmento,filas[0])
