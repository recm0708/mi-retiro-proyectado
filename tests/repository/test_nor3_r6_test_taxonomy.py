"""NOR.3 R6 — contrato permanente de taxonomía de pruebas."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tests"

MODULE_ROOTS = {
    "domain",
    "portals/asegurado",
    "portals/developer",
    "shared",
    "repository",
    "governance",
    "security",
    "regression",
}


def owner_of(path: Path) -> str:
    parts = path.relative_to(TESTS).parts
    if parts[0] == "portals":
        return "/".join(parts[:2])
    return parts[0]


class TestNOR3R6TestTaxonomy(unittest.TestCase):
    """Impide regresar al directorio tests/ plano o usar shared como descarte."""

    def test_no_hay_modulos_test_en_raiz(self):
        self.assertEqual([], sorted(TESTS.glob("test_*.py")))

    def test_todos_los_modulos_tienen_owner_permitido(self):
        unexpected = []
        for path in TESTS.rglob("test_*.py"):
            owner = owner_of(path)
            if owner not in MODULE_ROOTS:
                unexpected.append(path.relative_to(ROOT).as_posix())
        self.assertEqual([], unexpected)

    def test_helper_http_es_compartido(self):
        self.assertFalse((TESTS / "_runtime_http_source.py").exists())
        self.assertTrue(
            (TESTS / "shared" / "_runtime_http_source.py").is_file()
        )

    def test_paquetes_de_discovery_existen(self):
        required = [
            TESTS / "domain/__init__.py",
            TESTS / "portals/__init__.py",
            TESTS / "portals/asegurado/__init__.py",
            TESTS / "portals/developer/__init__.py",
            TESTS / "shared/__init__.py",
            TESTS / "repository/__init__.py",
            TESTS / "governance/__init__.py",
            TESTS / "security/__init__.py",
            TESTS / "regression/__init__.py",
        ]
        self.assertEqual([], [str(p) for p in required if not p.is_file()])

    def test_policy_declara_taxonomia_r6(self):
        policy = json.loads(
            (ROOT / "data/repository-structure-policy.json").read_text(
                encoding="utf-8"
            )
        )
        contract = policy["test_taxonomy_contract"]
        self.assertTrue(contract["enforced"])
        self.assertEqual("NOR.3 R6", contract["activation"])
        self.assertEqual(
            sorted(MODULE_ROOTS),
            sorted(contract["module_roots"]),
        )
        self.assertFalse(contract["root_test_modules_allowed"])

    def test_shared_no_contiene_modulos_ajenos_al_contrato_multiportal(self):
        expected = {
            "test_accessibility_themes.py",
            "test_accessibility_ux4.py",
            "test_responsive_ux3.py",
            "test_ux6_r3_r4_interface_polish.py",
            "test_ux6_r3_r4_motion_accessibility.py",
            "test_visual_identity_pre_r8.py",
            "test_visual_stabilization.py",
        }
        actual = {
            path.name
            for path in (TESTS / "shared").glob("test_*.py")
        }
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
