"""Regresión MANT.1 R6: auditoría funcional posterior a renombres técnicos."""

from __future__ import annotations

import ast
import inspect
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import get_args, get_origin
from urllib.parse import urlsplit

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import app


ROOT = Path(__file__).resolve().parents[1]
STATIC_DIR = ROOT / "app" / "static"
JS_DIR = STATIC_DIR / "js"

PAGINAS_PRINCIPALES = [
    "/",
    "/simulacion",
    "/comparar",
    "/como-se-calcula",
    "/metodologia",
]

client = TestClient(app)


class ParserHTML(HTMLParser):
    """Parser mínimo para auditar referencias estructurales renderizadas."""

    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def _rutas_fastapi():
    return {
        getattr(route, "path", ""): sorted(
            metodo
            for metodo in (getattr(route, "methods", set()) or set())
            if metodo not in {"HEAD", "OPTIONS"}
        )
        for route in app.routes
        if getattr(route, "path", "")
    }


def _ruta_a_regex(ruta: str) -> re.Pattern:
    patron = re.escape(ruta)
    patron = re.sub(r"\\\{[^/]+\\\}", r"[^/]+", patron)
    return re.compile("^" + patron + "$")


def _resolver_ruta(url: str):
    limpia = url.split("?", 1)[0].split("#", 1)[0]

    for ruta, metodos in _rutas_fastapi().items():
        if _ruta_a_regex(ruta).match(limpia):
            return ruta, metodos

    return None, []


def _texto(relativo: str) -> str:
    return (ROOT / relativo).read_text(encoding="utf-8", errors="replace")


def test_r6_paginas_principales_y_assets_renderizados_cargan():
    """Las páginas principales y los assets declarados deben responder en runtime."""

    assets_detectados = set()

    for pagina in PAGINAS_PRINCIPALES:
        respuesta = client.get(pagina)
        assert respuesta.status_code == 200, pagina

        for attr in ("href", "src"):
            patron = rf'{attr}\s*=\s*["\']([^"\']+)["\']'

            for match in re.finditer(patron, respuesta.text):
                ruta = urlsplit(match.group(1).strip()).path

                if ruta.startswith("/static/"):
                    assets_detectados.add(ruta)

    assert assets_detectados

    for asset in sorted(assets_detectados):
        respuesta = client.get(asset)
        assert respuesta.status_code == 200, asset


def test_r6_html_renderizado_no_tiene_referencias_estructurales_rotas():
    """Valida ids, labels, aria, controles Bootstrap y anclas internas."""

    for pagina in PAGINAS_PRINCIPALES:
        respuesta = client.get(pagina)
        assert respuesta.status_code == 200, pagina

        parser = ParserHTML()
        parser.feed(respuesta.text)

        ids = []
        labels_for = []
        referencias_aria = []
        referencias_controles = []
        anclas = []

        for tag, attrs in parser.tags:
            if attrs.get("id"):
                ids.append(attrs["id"])

            if tag == "label" and attrs.get("for"):
                labels_for.append(attrs["for"])

            for attr in ("aria-labelledby", "aria-describedby"):
                for destino in attrs.get(attr, "").split():
                    referencias_aria.append((attr, destino))

            for destino in attrs.get("aria-controls", "").split():
                referencias_controles.append(("aria-controls", destino))

            if attrs.get("data-bs-target", "").startswith("#"):
                referencias_controles.append(
                    ("data-bs-target", attrs["data-bs-target"].lstrip("#"))
                )

            href = attrs.get("href", "")
            if href.startswith("#") and len(href) > 1:
                anclas.append(href.lstrip("#"))

        conteo = Counter(ids)
        duplicados = [valor for valor, cantidad in conteo.items() if cantidad > 1]
        conjunto_ids = set(ids)

        assert not duplicados, (pagina, duplicados)

        for destino in labels_for:
            assert destino in conjunto_ids, (pagina, "label", destino)

        for attr, destino in referencias_aria:
            assert destino in conjunto_ids, (pagina, attr, destino)

        for attr, destino in referencias_controles:
            assert destino in conjunto_ids, (pagina, attr, destino)

        for destino in anclas:
            assert destino in conjunto_ids, (pagina, "anchor", destino)


def test_r6_fetch_api_usa_rutas_y_metodos_registrados():
    """Los fetch API estáticos del frontend deben coincidir con FastAPI."""

    patron_fetch = re.compile(r"fetch\(\s*[`'\"]([^`'\"]+)[`'\"]", re.MULTILINE)
    llamadas = []

    for ruta_js in sorted(JS_DIR.rglob("*.js")):
        texto = ruta_js.read_text(encoding="utf-8", errors="replace")
        rel = ruta_js.relative_to(ROOT).as_posix()

        for match in patron_fetch.finditer(texto):
            url = match.group(1).strip()

            if "${" in url or not url.startswith("/api/"):
                continue

            contexto = texto[match.start() : match.start() + 900]
            metodo_match = re.search(r"method\s*:\s*[`'\"]([A-Z]+)[`'\"]", contexto)
            metodo = metodo_match.group(1) if metodo_match else "GET"
            ruta_fastapi, metodos = _resolver_ruta(url)

            llamadas.append((rel, metodo, url))
            assert ruta_fastapi, (rel, url)
            assert metodo in metodos, (rel, metodo, url, metodos)

            if metodo in {"POST", "PUT", "PATCH"}:
                assert (
                    "body:" in contexto
                    or "JSON.stringify" in contexto
                    or "FormData" in contexto
                ), (rel, metodo, url)

    assert llamadas


def test_r6_formdata_frontend_coincide_con_uploadfile_backend():
    """Los campos FormData deben coincidir con parámetros UploadFile/File del backend."""

    main_py = ROOT / "app" / "main.py"
    uploads_backend = {}

    class EndpointVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            self._procesar_funcion(node)

        def visit_AsyncFunctionDef(self, node):
            self._procesar_funcion(node)

        def _procesar_funcion(self, node):
            ruta = None

            for decorador in node.decorator_list:
                if not isinstance(decorador, ast.Call):
                    continue

                if (
                    isinstance(decorador.func, ast.Attribute)
                    and decorador.func.attr in {"post", "put", "patch"}
                    and decorador.args
                    and isinstance(decorador.args[0], ast.Constant)
                    and isinstance(decorador.args[0].value, str)
                    and decorador.args[0].value.startswith("/api/")
                ):
                    ruta = decorador.args[0].value

            if not ruta:
                return

            parametros_file = []

            desplazamiento = len(node.args.args) - len(node.args.defaults)

            for indice, arg in enumerate(node.args.args):
                default_index = indice - desplazamiento

                if default_index < 0:
                    continue

                default = node.args.defaults[default_index]

                if (
                    isinstance(default, ast.Call)
                    and isinstance(default.func, ast.Name)
                    and default.func.id == "File"
                ):
                    parametros_file.append(arg.arg)

            if parametros_file:
                uploads_backend[ruta] = parametros_file

    EndpointVisitor().visit(ast.parse(main_py.read_text(encoding="utf-8")))

    assert uploads_backend == {
        "/api/simulacion/ficha-digital": ["archivo"],
        "/api/simulacion/referencia-mi-retiro-seguro": ["archivo"],
    }

    fetches_formdata = []

    for ruta_js in sorted(JS_DIR.rglob("*.js")):
        texto = ruta_js.read_text(encoding="utf-8", errors="replace")
        rel = ruta_js.relative_to(ROOT).as_posix()

        for match in re.finditer(
            r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*new\s+FormData\s*\(\s*\)",
            texto,
        ):
            variable = match.group(1)
            bloque = texto[match.start() : match.start() + 1800]

            campos = re.findall(
                rf"{re.escape(variable)}\.append\(\s*[`'\"]([^`'\"]+)[`'\"]",
                bloque,
            )

            fetch_match = re.search(
                r"fetch\(\s*[`'\"]([^`'\"]+)[`'\"]",
                bloque,
                re.MULTILINE,
            )

            if not fetch_match:
                continue

            endpoint = fetch_match.group(1)

            if endpoint.startswith("/api/"):
                fetches_formdata.append((rel, endpoint, campos))

    assert fetches_formdata

    for rel, endpoint, campos in fetches_formdata:
        esperados = uploads_backend.get(endpoint)
        assert esperados is not None, (rel, endpoint, campos)

        for campo in esperados:
            assert campo in campos, (rel, endpoint, campo, campos)


def _resolver_modelo(annotation):
    if annotation is inspect.Signature.empty:
        return None

    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return annotation

    origen = get_origin(annotation)
    if origen:
        for arg in get_args(annotation):
            modelo = _resolver_modelo(arg)
            if modelo:
                return modelo

    return None


def test_r6_endpoints_post_declaran_modelo_json_o_uploadfile():
    """Evita endpoints POST sin contrato explícito de entrada."""

    for route in app.routes:
        path = getattr(route, "path", "")
        methods = set(getattr(route, "methods", set()) or set())

        if not path.startswith("/api/") or "POST" not in methods:
            continue

        firma = inspect.signature(route.endpoint)
        tiene_modelo = False
        tiene_archivo = False

        for parametro in firma.parameters.values():
            if _resolver_modelo(parametro.annotation):
                tiene_modelo = True

            if "UploadFile" in str(parametro.annotation):
                tiene_archivo = True

        assert tiene_modelo or tiene_archivo, path


def test_r6_payloads_indirectos_conservan_campos_requeridos():
    """Cubre payloads compuestos mediante funciones antes de JSON.stringify."""

    comparator = _texto("app/static/js/comparator.js")
    detalle = _texto("app/static/js/current_year_detail.js")
    results = _texto("app/static/js/results.js")
    retirement = _texto("app/static/js/retirement.js")

    for token in [
        'sistema: "SEBD"',
        "datos_sebd:",
        'sistema: "MIXTO"',
        "datos_mixto:",
        'sistema: "SUCGS"',
        "datos_sucgs:",
        "solicitud.fechas_retiro",
        "solicitud.escenarios_salariales",
        "JSON.stringify(solicitud)",
    ]:
        assert token in comparator

    for token in [
        "anio:",
        "modo_captura:",
        "cuotas_anio_actual_referencia:",
        "registros,",
        "JSON.stringify(datos)",
    ]:
        assert token in detalle

    for token in [
        "fecha_nacimiento:",
        "sexo:",
        "historial:",
        "linea_tiempo:",
        "resumen_retiro:",
        "fecha_retiro_seleccionada:",
        "escenario_salarial_nombre:",
        "saldo_capitalizacion_solidaria:",
        "JSON.stringify(datos)",
    ]:
        assert token in results

    for token in [
        "fecha_nacimiento:",
        "sexo:",
        "cuotas_reales:",
        "cuotas_anio_actual:",
        "cuotas_esperadas_cierre_anio:",
        "continua_cotizando:",
        "cuotas_esperadas_por_anio:",
        "JSON.stringify(datos)",
    ]:
        assert token in retirement


def test_r6_como_se_calcula_anclas_dinamicas_existen():
    """La URL dinámica /como-se-calcula#${ancla} debe apuntar a ids reales."""

    html = _texto("app/templates/calculation_guide.html")
    js = _texto("app/static/js/results_orchestration.js")

    assert "/como-se-calcula#${ancla}" in js

    for ancla in ['id="sebd"', 'id="mixto"', 'id="sucgs"']:
        assert ancla in html
