"""Regresiones del gate local versionado que protege la creación de commits."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestPrecommitGuard(unittest.TestCase):
    """Protege instalación, alcance y no congelación del gate de commit."""

    def test_hook_versionado_delega_en_validador_python(self):
        hook = (ROOT / ".githooks/pre-commit").read_text(encoding="utf-8")
        self.assertIn("#!/usr/bin/env sh", hook)
        self.assertIn("scripts/validar_precommit.py", hook)
        self.assertIn("exec python", hook)
        self.assertIn("exec python3", hook)
        self.assertIn("exec py -3", hook)

    def test_validador_bloquea_main_y_arbol_no_reproducible(self):
        guard = (ROOT / "scripts/validar_precommit.py").read_text(encoding="utf-8")
        self.assertIn('if rama == "main"', guard)
        self.assertIn('"diff", "--name-only"', guard)
        self.assertIn('"ls-files",', guard)
        self.assertIn('"--others",', guard)
        self.assertIn('"--exclude-standard",', guard)
        self.assertIn('"diff", "--cached", "--check"', guard)

    def test_validador_ejecuta_gate_tecnico_completo(self):
        guard = (ROOT / "scripts/validar_precommit.py").read_text(encoding="utf-8")
        self.assertIn('"pip", "check"', guard)
        self.assertIn('"compileall", "-q", "app"', guard)
        self.assertIn('shutil.which("node")', guard)
        self.assertIn('"--check", str(archivo)', guard)
        self.assertIn('"unittest", "discover", "-s", "tests", "-q"', guard)

    def test_instalador_configura_hooks_path_solo_en_el_clon(self):
        instalador = (ROOT / "scripts/configurar_hooks_git.ps1").read_text(
            encoding="utf-8"
        )
        self.assertIn("git config --local core.hooksPath .githooks", instalador)
        self.assertIn("git config --local --get core.hooksPath", instalador)
        self.assertNotIn("--global core.hooksPath", instalador)
        validacion = (ROOT / "docs/VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("tests/test_precommit_guard.py", validacion)

    def test_regresiones_historicas_no_congelan_ux46f_como_bloque_activo(self):
        rutas = (
            ROOT / "tests/test_ux46e_auditoria_coherencia.py",
            ROOT / "tests/test_ux46e_r8_cierre_funcional.py",
            ROOT / "tests/test_ux46e_r91_candidato_cierre.py",
        )
        for ruta in rutas:
            texto = ruta.read_text(encoding="utf-8")
            with self.subTest(ruta=ruta.name):
                self.assertNotIn(
                    'assertIn("**Bloque activo:** UX.4.6f",',
                    texto,
                )
                self.assertNotIn(
                    'assertIn("- [ ] **UX.4.6f — Paso 4",',
                    texto,
                )


if __name__ == "__main__":
    unittest.main()
