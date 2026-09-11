"""Regresiones del inventario estructural NOR.3 R1."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

BASELINE = (
    ROOT
    / "docs/audits/repository/"
    "repository-ownership-baseline-nor3-r1.md"
)

INVENTORY = (
    ROOT
    / "docs/audits/repository/"
    "repository-ownership-inventory-nor3-r1.txt"
)

AUDITS_INDEX = ROOT / "docs/audits/README.md"


class TestNOR3R1RepositoryInventory(unittest.TestCase):
    """Protege la evidencia R1 sin fijar el estado de revisiones posteriores."""

    @classmethod
    def setUpClass(cls):
        cls.baseline = BASELINE.read_text(encoding="utf-8")
        cls.inventory = INVENTORY.read_text(encoding="utf-8")
        cls.index = AUDITS_INDEX.read_text(encoding="utf-8")

    def test_evidencias_r1_existen(self):
        self.assertTrue(BASELINE.is_file())
        self.assertTrue(INVENTORY.is_file())

    def test_baseline_preserva_magnitudes_auditadas(self):
        for fragment in (
            "archivos versionados: **613**",
            "rutas FastAPI detectadas: **55**",
            "rutas App Asegurado: **24**",
            "rutas Portal Developer: **29**",
            "templates runtime auditados: **29**",
            "assets runtime auditados: **44**",
            "tests auditados: **207**",
            "directorios auditados: **59**",
            "`app/main.py`: **3227 líneas**",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.baseline)

    def test_shared_no_es_cajon_de_sastre(self):
        self.assertIn(
            "`shared` no se utiliza para almacenar código",
            self.baseline,
        )
        self.assertIn("Dominio", self.baseline)
        self.assertIn("global_footer.html", self.baseline)

    def test_base_publica_no_se_clasifica_shared(self):
        self.assertIn("`base.html` **no es Shared**", self.baseline)
        self.assertIn(
            "Mover bajo `app/templates/asegurado/`",
            self.baseline,
        )

    def test_backend_developer_sale_de_core(self):
        for path in (
            "app/core/admin_security.py",
            "app/core/admin_session.py",
            "app/core/developer_identity.py",
            "app/core/developer_store.py",
            "app/core/developer_user_admin.py",
            "app/core/developer_user_audit.py",
            "app/core/developer_web_security.py",
        ):
            with self.subTest(path=path):
                self.assertIn(path, self.baseline)

        self.assertIn("Mover fuera de `core/`", self.baseline)

    def test_style_css_queda_como_mixto_para_r5(self):
        self.assertIn("`app/static/css/style.css`", self.baseline)
        self.assertIn(
            "R5 debe separar las reglas realmente comunes",
            self.baseline,
        )

    def test_data_tiene_decision_r7_sin_iniciar_persistencia(self):
        self.assertIn("data/governance/", self.baseline)
        self.assertIn("data/audits/", self.baseline)
        self.assertIn(
            "No se inicia ni se implementa `data/developer/`",
            self.baseline,
        )

    def test_r1_declara_que_no_hubo_movimientos(self):
        self.assertIn("no ejecuta movimientos físicos", self.baseline)
        self.assertIn(
            "No se realizó ningún movimiento físico en R1.",
            self.inventory,
        )

    def test_auditoria_esta_indexada(self):
        self.assertIn(
            "repository-ownership-baseline-nor3-r1.md",
            self.index,
        )


if __name__ == "__main__":
    unittest.main()
