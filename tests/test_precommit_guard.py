"""Regresiones del gate local versionado que protege la creación de commits."""

from pathlib import Path
import inspect
import unittest

from scripts import quality_gate


ROOT = Path(__file__).resolve().parents[1]


class TestPrecommitGuard(unittest.TestCase):
    """Protege instalación, alcance y no congelación del gate de commit."""

    def test_hook_versionado_delega_en_validador_python(self):
        hook = (
            ROOT / ".githooks/pre-commit"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "#!/usr/bin/env sh",
            hook,
        )
        self.assertIn(
            "scripts/validate_precommit.py",
            hook,
        )
        self.assertIn(
            "exec python",
            hook,
        )
        self.assertIn(
            "exec python3",
            hook,
        )
        self.assertIn(
            "exec py -3",
            hook,
        )

    def test_validador_bloquea_main_y_arbol_no_reproducible(self):
        guard = (
            ROOT / "scripts/validate_precommit.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'if rama == "main"',
            guard,
        )
        self.assertIn(
            '"diff", "--name-only"',
            guard,
        )
        self.assertIn(
            '"ls-files",',
            guard,
        )
        self.assertIn(
            '"--others",',
            guard,
        )
        self.assertIn(
            '"--exclude-standard",',
            guard,
        )

        whitespace_source = inspect.getsource(
            quality_gate.execute_whitespace_check
        )

        self.assertIn(
            '"--cached"',
            whitespace_source,
        )
        self.assertIn(
            '"--check"',
            whitespace_source,
        )

    def test_validador_ejecuta_gate_tecnico_completo(self):
        guard = (
            ROOT / "scripts/validate_precommit.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "scripts/quality_gate.py",
            guard,
        )
        self.assertIn(
            "--pre-commit",
            guard,
        )
        self.assertIn(
            "--fail-fast",
            guard,
        )

        names = set(
            quality_gate.planned_check_names(
                "pre-commit"
            )
        )

        expected = {
            "Dependencias Python",
            "Documentación Markdown",
            "Identificadores de bloques",
            "Integridad del repositorio",
            "Compilación Python",
            "JavaScript versionado",
            "Contrato revision-aware",
            "Manifiesto de publicación",
            "Whitespace Git",
            "unittest",
        }

        self.assertEqual(
            expected,
            names,
        )

        commands = dict(
            quality_gate.build_command_checks(
                "pre-commit",
                None,
            )
        )

        self.assertEqual(
            [
                quality_gate.sys.executable,
                "-m",
                "pip",
                "check",
            ],
            commands["Dependencias Python"],
        )

        self.assertEqual(
            [
                quality_gate.sys.executable,
                "scripts/audit_markdown.py",
            ],
            commands["Documentación Markdown"],
        )

        self.assertEqual(
            [
                quality_gate.sys.executable,
                "scripts/audit_block_identifiers.py",
            ],
            commands["Identificadores de bloques"],
        )

        self.assertIn(
            "compileall",
            commands["Compilación Python"],
        )

        self.assertEqual(
            [
                quality_gate.sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-q",
            ],
            commands["unittest"],
        )

    def test_instalador_configura_hooks_path_solo_en_el_clon(self):
        instalador = (
            ROOT / "scripts/configure_git_hooks.ps1"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "git config --local core.hooksPath .githooks",
            instalador,
        )
        self.assertIn(
            "git config --local --get core.hooksPath",
            instalador,
        )
        self.assertNotIn(
            "--global core.hooksPath",
            instalador,
        )

        validacion = (
            ROOT / "docs/operations/validation.md"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "tests/test_precommit_guard.py",
            validacion,
        )

    def test_regresiones_historicas_no_congelan_ux46f_como_bloque_activo(self):
        rutas = (
            ROOT / "tests/test_ux46e_auditoria_coherencia.py",
            ROOT / "tests/test_ux46e_r8_cierre_funcional.py",
            ROOT / "tests/test_ux46e_r91_candidato_cierre.py",
        )

        for ruta in rutas:
            texto = ruta.read_text(
                encoding="utf-8"
            )

            with self.subTest(
                ruta=ruta.name
            ):
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
