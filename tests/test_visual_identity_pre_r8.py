"""Regresiones de identidad visual y activos pre-R8."""

from __future__ import annotations

import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def dimensiones_png(ruta: Path) -> tuple[int, int]:
    """Lee ancho y alto directamente del encabezado IHDR de un PNG."""

    datos = ruta.read_bytes()
    if datos[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{ruta} no es un PNG válido")
    return struct.unpack(">II", datos[16:24])


def tamanos_ico(ruta: Path) -> list[tuple[int, int]]:
    """Obtiene las dimensiones declaradas por cada imagen de un ICO."""

    datos = ruta.read_bytes()
    reservado, tipo, cantidad = struct.unpack("<HHH", datos[:6])
    if reservado != 0 or tipo != 1:
        raise AssertionError(f"{ruta} no es un ICO válido")

    tamanos: list[tuple[int, int]] = []
    offset = 6
    for _ in range(cantidad):
        ancho_raw, alto_raw = struct.unpack("<BB", datos[offset : offset + 2])
        ancho = 256 if ancho_raw == 0 else ancho_raw
        alto = 256 if alto_raw == 0 else alto_raw
        tamanos.append((ancho, alto))
        offset += 16
    return tamanos


class TestIdentidadVisualPreR8(unittest.TestCase):
    """Protege la fuente canónica, derivados y uso visible de la marca."""

    def test_fuente_maestra_y_normalizada_tienen_dimensiones_esperadas(self):
        self.assertEqual(
            dimensiones_png(ROOT / "assets/brand/source/icono-simple-master-1254.png"),
            (1254, 1254),
        )
        self.assertEqual(
            dimensiones_png(ROOT / "assets/brand/source/icono-simple-1024.png"),
            (1024, 1024),
        )

    def test_familia_canonica_de_iconos_esta_completa(self):
        esperados = [16, 32, 48, 64, 128, 180, 192, 256, 512, 1024]
        for lado in esperados:
            with self.subTest(lado=lado):
                ruta = ROOT / f"assets/brand/icons/icon-{lado}.png"
                self.assertTrue(ruta.is_file(), ruta)
                self.assertEqual(dimensiones_png(ruta), (lado, lado))

    def test_logo_mark_canonico_conserva_derivados_grandes(self):
        for lado in (512, 1024):
            with self.subTest(lado=lado):
                ruta = ROOT / f"assets/brand/logos/logo-mark-{lado}.png"
                self.assertTrue(ruta.is_file(), ruta)
                self.assertEqual(dimensiones_png(ruta), (lado, lado))

    def test_activos_runtime_tienen_dimensiones_esperadas(self):
        esperados = {
            "logo-mark-128.png": (128, 128),
            "favicon-16x16.png": (16, 16),
            "favicon-32x32.png": (32, 32),
            "favicon-48x48.png": (48, 48),
            "apple-touch-icon.png": (180, 180),
            "app-icon-192.png": (192, 192),
            "app-icon-512.png": (512, 512),
        }
        for nombre, dimensiones in esperados.items():
            with self.subTest(nombre=nombre):
                ruta = ROOT / "app/static/img/brand" / nombre
                self.assertTrue(ruta.is_file(), ruta)
                self.assertEqual(dimensiones_png(ruta), dimensiones)

    def test_favicon_ico_conserva_resoluciones_multicapa(self):
        ruta = ROOT / "app/static/img/brand/favicon.ico"
        self.assertTrue(ruta.is_file(), ruta)
        self.assertEqual(
            tamanos_ico(ruta),
            [(16, 16), (32, 32), (48, 48), (256, 256)],
        )

    def test_social_preview_cumple_dimension_y_peso(self):
        ruta = ROOT / "assets/social/github-social-preview.png"
        self.assertTrue(ruta.is_file(), ruta)
        self.assertEqual(dimensiones_png(ruta), (1280, 640))
        self.assertLess(ruta.stat().st_size, 1024 * 1024)

    def test_plantilla_global_declara_favicons_y_apple_touch(self):
        contenido = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
        self.assertIn("/img/brand/favicon.ico", contenido)
        self.assertIn("/img/brand/favicon-32x32.png", contenido)
        self.assertIn("/img/brand/favicon-16x16.png", contenido)
        self.assertIn("/img/brand/apple-touch-icon.png", contenido)

    def test_navbar_usa_logo_oficial_y_no_marcador_mr(self):
        contenido = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
        self.assertIn("/img/brand/logo-mark-128.png", contenido)
        self.assertIn('class="app-brand-mark-image"', contenido)
        self.assertNotIn(">MR</span>", contenido)

    def test_capa_css_de_marca_es_tematica_y_no_duplica_logica(self):
        contenido = (ROOT / "app/static/css/brand.css").read_text(encoding="utf-8")
        self.assertIn(".app-brand-mark-image", contenido)
        self.assertIn('html[data-bs-theme="dark"] .app-brand-mark', contenido)
        self.assertIn('html[data-app-theme="contrast"] .app-brand-mark', contenido)
        self.assertIn("prefers-reduced-motion", contenido)

    def test_estructura_provisional_anterior_ya_no_es_fuente_de_runtime(self):
        self.assertFalse((ROOT / "app/static/img/icons").exists())
        self.assertFalse((ROOT / "app/static/img/.gitkeep").exists())


if __name__ == "__main__":
    unittest.main()
