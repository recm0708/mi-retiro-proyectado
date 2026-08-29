"""DEV.2 R5 - Portal Developer y separación de acceso web/Bearer."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.admin_session import revocar_todas_las_sesiones_admin
from app.core.observability import ruta_log_actual
from app.main import app

ROOT = Path(__file__).resolve().parents[1]


class TestDev2R5PortalAccess(unittest.TestCase):
    def tearDown(self):
        revocar_todas_las_sesiones_admin()

    @staticmethod
    def _env(temp: str):
        return patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "test-admin-secret",
            },
            clear=True,
        )

    def test_dev_es_entrada_humana_canonica(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get("/dev")

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("Portal Developer", respuesta.text)
        self.assertIn("Ingresar al Portal Developer", respuesta.text)
        self.assertNotIn('href="/simulacion"', respuesta.text)
        self.assertNotIn('href="/comparar"', respuesta.text)
        self.assertNotIn("Cómo se calcula", respuesta.text)

    def test_login_valido_crea_cookie_acotada_a_dev(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).post(
                    "/dev",
                    data={"token": "test-admin-secret"},
                    follow_redirects=False,
                )

        self.assertEqual(303, respuesta.status_code)
        self.assertEqual("/dev", respuesta.headers["location"])
        cookie = respuesta.headers.get("set-cookie", "")
        self.assertIn("mrp_admin_session=", cookie)
        self.assertIn("HttpOnly", cookie)
        self.assertIn("Path=/dev", cookie)
        self.assertNotIn("test-admin-secret", cookie)

    def test_sesion_web_renderiza_portal_sin_navegacion_publica_ni_revisiones(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                cliente.post("/dev", data={"token": "test-admin-secret"})
                respuesta = cliente.get("/dev")

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("Centro de desarrollo", respuesta.text)
        for texto in ("Resumen", "Diagnóstico", "Eventos", "Archivos", "Privacidad"):
            self.assertIn(texto, respuesta.text)
        self.assertNotIn('href="/simulacion"', respuesta.text)
        self.assertNotIn('href="/comparar"', respuesta.text)
        self.assertNotIn(">DEV.2 R1<", respuesta.text)
        self.assertNotIn(">DEV.2 R2<", respuesta.text)
        self.assertNotIn(">DEV.2 R3<", respuesta.text)

    def test_centro_legacy_browser_redirige_sin_falso_denied(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                cliente.post("/dev", data={"token": "test-admin-secret"})
                log = ruta_log_actual()
                if log.exists():
                    log.unlink()

                respuesta = cliente.get(
                    "/dev/centro-desarrollo",
                    headers={"Accept": "text/html"},
                    follow_redirects=False,
                )
                contenido = log.read_text(encoding="utf-8") if log.exists() else ""

        self.assertEqual(303, respuesta.status_code)
        self.assertEqual("/dev", respuesta.headers["location"])
        self.assertNotIn("admin.access.denied", contenido)

    def test_bearer_legacy_sigue_disponible_para_acceso_programatico(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get(
                    "/dev/centro-desarrollo",
                    headers={"Authorization": "Bearer test-admin-secret"},
                    follow_redirects=False,
                )

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("Centro de desarrollo", respuesta.text)

    def test_login_legacy_get_redirige_a_entrada_canonica(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get("/dev/login", follow_redirects=False)

        self.assertEqual(303, respuesta.status_code)
        self.assertEqual("/dev", respuesta.headers["location"])

    def test_logout_vuelve_a_dev_y_revoca_cookie_dev(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                cliente.post("/dev", data={"token": "test-admin-secret"})
                respuesta = cliente.post("/dev/logout", follow_redirects=False)

        self.assertEqual(303, respuesta.status_code)
        self.assertEqual("/dev", respuesta.headers["location"])
        self.assertIn("Path=/dev", respuesta.headers.get("set-cookie", ""))

    def test_operaciones_dev_tienen_clasificacion_explicita(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                cliente.get("/dev")
                cliente.get("/dev/login", follow_redirects=False)
                contenido = ruta_log_actual().read_text(encoding="utf-8")
                eventos = [json.loads(line) for line in contenido.splitlines() if line.strip()]

        operaciones = {
            evento.get("metadata", {}).get("operation")
            for evento in eventos
            if evento.get("event") == "http.request"
        }
        self.assertIn("dev.portal", operaciones)
        self.assertIn("dev.login", operaciones)

    def test_shell_dev_no_arrastra_superficie_previsional(self):
        base = (ROOT / "app/templates/dev_base.html").read_text(encoding="utf-8")
        login = (ROOT / "app/templates/dev_login.html").read_text(encoding="utf-8")
        centro = (ROOT / "app/templates/dev_development_center.html").read_text(encoding="utf-8")

        self.assertNotIn('partials/data_management.html', base)
        self.assertNotIn('partials/privacy_consent.html', base)
        self.assertNotIn('href="/simulacion"', base)
        self.assertNotIn('href="/comparar"', base)
        self.assertIn('{% extends "dev_base.html" %}', login)
        self.assertIn('{% extends "dev_base.html" %}', centro)

    def test_javascript_dev_no_persiste_credenciales(self):
        texto = (ROOT / "app/static/js/developer_portal.js").read_text(encoding="utf-8").casefold()
        self.assertNotIn("localstorage", texto)
        self.assertNotIn("sessionstorage", texto)
        self.assertNotIn("token=", texto)
        self.assertNotIn("?token", texto)


    def test_documentacion_r5_describe_contrato_vigente_promovido_g118(self):
        documentacion = (
            ROOT / "docs/architecture/development-center.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Alcance de R5", documentacion)
        self.assertIn("`/dev` como entrada humana canónica", documentacion)
        self.assertIn("Path=/dev", documentacion)
        self.assertIn("Authorization: Bearer <token>", documentacion)
        self.assertIn("DEV.2 R6", documentacion)
        self.assertIn("1172 unittest OK", documentacion)
        self.assertIn("1211 pytest passed / 5747 subtests passed", documentacion)
        self.assertIn("G118/E04", documentacion)
        self.assertIn("G119/E05", documentacion)

        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.18.04-beta", version)

if __name__ == "__main__":
    unittest.main()
