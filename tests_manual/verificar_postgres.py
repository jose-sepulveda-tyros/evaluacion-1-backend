"""Verificación aislada; nunca restablece la base normal del proyecto."""
import os, sys, subprocess, socket, time, json, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, inspect
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from infrastructure.database import build_database_url, Base
from infrastructure import models

url = build_database_url()
admin = psycopg2.connect(host=url.host,port=url.port,user=url.username,password=url.password,dbname='postgres')
admin.autocommit=True
name='reservas_'+uuid.uuid4().hex[:12]+'_test'
with admin.cursor() as cursor:cursor.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(name)))
env=dict(os.environ,DB_NAME=name)
engine=create_engine(url.set(database=name))
server=None
with socket.socket() as sock:
 sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
base=f'http://127.0.0.1:{port}'
def run(*args):
 p=subprocess.run([sys.executable,*args],env=env,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return p.stdout

def start():
 global server
 server=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(port)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 for _ in range(100):
  try:urlopen(base+'/openapi.json',timeout=1);return
  except Exception:time.sleep(.1)
 raise RuntimeError('El servidor de pruebas no inició')
def stop():
 global server
 if server:server.terminate();server.wait(timeout=10);server=None

def request(method,path,body=None):
 data=None if body is None else json.dumps(body).encode()
 req=Request(base+path,data=data,method=method,headers={'Content-Type':'application/json'})
 try:
  with urlopen(req,timeout=15) as r:return r.status,json.loads(r.read() or 'null')
 except HTTPError as e:return e.code,json.loads(e.read())
try:
 run('-m','alembic','upgrade','head')
 run('-m','alembic','downgrade','base')
 run('-m','alembic','upgrade','head')
 with engine.connect() as conn:
  assert MigrationContext.configure(conn).get_current_revision()=='0001'
  assert compare_metadata(MigrationContext.configure(conn),Base.metadata)==[]
 print('OK PostgreSQL: upgrade / downgrade / upgrade; esquema coincide con ORM')
 start()
 output=run('tests_manual/verificar_coleccion.py','--base-url',base)
 print(output.splitlines()[-1])
 status,before=request('GET','/reservas')
 assert status==200 and before['total']>0
 stop();start()
 assert request('GET','/reservas')==(200,before)
 print('OK PostgreSQL: reservas conservadas después de reiniciar Uvicorn')
 # Dos solicitudes paralelas no pueden ocupar el mismo horario.
 status,sala=request('POST','/salas',{'nombre':'Sala concurrencia','capacidad':10,'ubicacion':'Piso 2','equipamiento':[]})
 assert status==201
 alumnos=[]
 for n in range(2):
  status,a=request('POST','/estudiantes',{'nombre':f'Alumno paralelo {n}','carrera':'Informática','correo':f'paralelo{n}@example.com','activo':True})
  assert status==201;alumnos.append(a['id'])
 def reservar(alumno):
  return request('POST','/reservas',{'sala_id':sala['id'],'estudiante_id':alumno,'fecha':'2026-12-10','hora_inicio':'10:00','hora_fin':'11:00','cantidad_personas':2,'estado':'activa'})
 with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(reservar,alumnos))
 assert sorted(status for status,_ in results)==[201,409],results
 print('OK PostgreSQL: solicitudes simultáneas -> 201 y 409, sin superposición')
 print('Verificación PostgreSQL completada en base temporal aislada.')
finally:
 stop();engine.dispose()
 with admin.cursor() as cursor:
  cursor.execute(sql.SQL('DROP DATABASE {} WITH (FORCE)').format(sql.Identifier(name)))
 admin.close()
