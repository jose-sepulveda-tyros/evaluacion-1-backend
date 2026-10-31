"""Ejecuta pruebas.http sobre una API local vacía, sin dependencias adicionales.

Activar .venv, iniciar Uvicorn en otra terminal y ejecutar:
    python tests_manual/verificar_coleccion.py
Para otro puerto:
    python tests_manual/verificar_coleccion.py --base-url http://127.0.0.1:8001

Las cuatro primeras solicitudes comprueban que no existan datos antes de crear.
El verificador se detiene en el primer fallo y no borra ni reinicia datos.
"""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def leer_casos():
    texto = Path(__file__).with_name("pruebas.http").read_text(encoding="utf-8")
    casos = []
    for bloque in re.split(r"^### ", texto, flags=re.MULTILINE)[1:]:
        lineas = bloque.strip().splitlines()
        esperado = json.loads(next(line for line in lineas if line.startswith("# expect "))[9:])
        solicitud = next(line for line in lineas if "{{baseUrl}}" in line)
        metodo, ruta = solicitud.split(" {{baseUrl}}", 1)
        cuerpo = bloque.split("\n\n", 1)[1].strip() if "Content-Type:" in bloque else ""
        casos.append((lineas[0], metodo, ruta, json.loads(cuerpo) if cuerpo else None, esperado))
    return casos


def valor_en(datos, ruta):
    if ruta == "$":
        return datos
    for parte in ruta.split("."):
        datos = datos[int(parte)] if isinstance(datos, list) else datos[parte]
    return datos


def verificar(enviar):
    casos = leer_casos()
    cubiertas = set()
    for titulo, metodo, ruta, payload, esperado in casos:
        try:
            estado, cuerpo, headers = enviar(metodo, ruta, payload)
            if estado != esperado["status"]:
                raise AssertionError(f"HTTP esperado {esperado['status']}, recibido {estado}: {cuerpo!r}")
            if estado == 204:
                if cuerpo:
                    raise AssertionError("204 debe devolver un cuerpo vacío")
            else:
                datos = json.loads(cuerpo)
                for campo, valor in esperado.get("body", {}).items():
                    real = valor_en(datos, campo)
                    if real != valor:
                        raise AssertionError(f"{campo}: esperado {valor!r}, recibido {real!r}")
                if estado >= 400:
                    if set(datos) != {"error"} or set(datos["error"]) != {"code", "message", "details"}:
                        raise AssertionError("El error no conserva el contrato JSON")
                    if not isinstance(datos["error"]["details"], list):
                        raise AssertionError("error.details debe ser una lista")
            for nombre, valor in esperado.get("headers", {}).items():
                if headers.get(nombre.lower()) != valor:
                    raise AssertionError(f"Header {nombre}: se esperaba {valor!r}")
        except (AssertionError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise AssertionError(f"FALLO {titulo}: {exc}") from exc
        if estado < 300:
            ruta_normalizada = re.sub(r"/\d+(?=/|$)", "/{id}", ruta.split("?")[0])
            cubiertas.add((metodo.lower(), ruta_normalizada))
        print(f"OK {titulo} — HTTP {estado}")

    estado, cuerpo, _ = enviar("GET", "/openapi.json", None)
    if estado != 200:
        raise AssertionError("No se pudo verificar OpenAPI")
    spec = json.loads(cuerpo)
    esperadas = {
        (metodo, re.sub(r"\{[^}]+\}", "{id}", ruta))
        for ruta, operaciones in spec["paths"].items()
        for metodo in operaciones
        if metodo in {"get", "post", "put", "patch", "delete"}
    }
    faltantes = esperadas - cubiertas
    if faltantes:
        raise AssertionError(f"Operaciones sin caso exitoso: {sorted(faltantes)}")
    print(f"Resultado: {len(casos)} casos correctos; {len(esperadas)} operaciones cubiertas.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    def enviar(metodo, ruta, payload):
        datos = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            args.base_url.rstrip("/") + ruta,
            data=datos,
            headers={"Content-Type": "application/json"} if datos is not None else {},
            method=metodo,
        )
        try:
            response = urlopen(request, timeout=10)
        except HTTPError as exc:
            response = exc
        with response:
            return response.status, response.read(), {k.lower(): v for k, v in response.headers.items()}

    try:
        verificar(enviar)
    except (AssertionError, URLError, TimeoutError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
