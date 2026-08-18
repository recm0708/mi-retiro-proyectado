"""GOV.1.7 — licencia y estrategia de distribución."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'
class TestGov17Licencia(unittest.TestCase):
    def test_license_propietaria_existe_y_reserva_derechos(self):
        t=(ROOT/'LICENSE').read_text(encoding='utf-8'); self.assertIn('Rubén Enrique Cañizares Miranda',t); self.assertIn('All rights reserved',t); self.assertIn('PROPRIETARY LICENSE NOTICE',t); self.assertIn('No license is granted',t); self.assertIn('THIRD_PARTY_NOTICES.md',t)
    def test_avisos_terceros_cubren_directas_y_bootstrap(self):
        t=(ROOT/'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
        for e in ('FastAPI | 0.141.1 | MIT','Jinja2 | 3.1.6 | BSD-3-Clause','Pydantic | 2.13.4 | MIT','python-multipart | 0.0.32 | Apache-2.0','pypdf | 6.15.0 | BSD-3-Clause','Uvicorn | 0.52.1 | BSD-3-Clause','Bootstrap | 5.3.8 | MIT'): self.assertIn(e,t)
    def test_decision_documenta_alternativas_y_no_relicencia(self):
        t=(DOCS/'LICENCIA_Y_DISTRIBUCION.md').read_text(encoding='utf-8')
        for e in ('MIT','Apache-2.0','GPL-3.0 / AGPL-3.0','Propietaria / todos los derechos reservados','Decisión GOV.1.7','no relicencia','revisión jurídica externa'): self.assertIn(e,t)
    def test_readme_declara_licencia_y_mueve_a_gov18(self):
        t=(ROOT/'README.md').read_text(encoding='utf-8'); self.assertIn('**Bloque activo:** GOV.1.8 — Auditoría final y cierre pre-beta de gobierno',t); self.assertIn('**GOV.1.7:** Licencia propietaria pre-beta',t); self.assertIn('(LICENSE)',t); self.assertIn('(THIRD_PARTY_NOTICES.md)',t)
    def test_roadmap_cierra_gov17_y_mantiene_gov18(self):
        t=(DOCS/'ROADMAP.md').read_text(encoding='utf-8'); self.assertIn('- [x] **GOV.1.7 — Licencia**',t); self.assertIn('- [ ] **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**',t)
    def test_governance_respeta_decision_propietaria(self):
        t=(ROOT/'GOVERNANCE.md').read_text(encoding='utf-8'); self.assertIn('licencia propietaria pre-beta',t); self.assertIn('THIRD_PARTY_NOTICES.md',t); self.assertIn('relicencia',t)
    def test_release_exige_avisos_de_terceros(self):
        t=(DOCS/'PROCESO_RELEASE.md').read_text(encoding='utf-8'); self.assertIn('THIRD_PARTY_NOTICES.md',t); self.assertIn('inventario exacto del artefacto',t); self.assertIn('licencias/NOTICE upstream',t)
    def test_version_no_cambia_y_archivos_limpios(self):
        self.assertEqual('0.0.23-beta',(ROOT/'VERSION').read_text(encoding='utf-8').strip())
        for p in (ROOT/'LICENSE',ROOT/'THIRD_PARTY_NOTICES.md',DOCS/'LICENCIA_Y_DISTRIBUCION.md'):
            t=p.read_text(encoding='utf-8'); self.assertFalse(any(ord(c)<32 and c not in '\n\r\t' for c in t)); self.assertFalse(any(l.endswith((' ','\t')) for l in t.splitlines()))
if __name__=='__main__': unittest.main()
