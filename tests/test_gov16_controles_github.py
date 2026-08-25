"""GOV.1.6 — controles GitHub y auditoría automática."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
GH=ROOT/'.github'
DOCS=ROOT/'docs'

class TestGov16ControlesGithub(unittest.TestCase):
    def test_security_policy_existe_y_define_canal_privado(self):
        t=(ROOT/'SECURITY.md').read_text(encoding='utf-8')
        self.assertIn('Versiones soportadas',t); self.assertIn('ruben.canizares@outlook.com',t); self.assertIn('No publique una vulnerabilidad explotable como issue público',t)
    def test_issue_forms_separan_error_mejora_y_seguridad(self):
        b=(GH/'ISSUE_TEMPLATE/bug_report.yml').read_text(encoding='utf-8'); f=(GH/'ISSUE_TEMPLATE/feature_request.yml').read_text(encoding='utf-8'); q=(GH/'ISSUE_TEMPLATE/question.yml').read_text(encoding='utf-8'); c=(GH/'ISSUE_TEMPLATE/config.yml').read_text(encoding='utf-8')
        self.assertIn('Reporte de error',b); self.assertIn('Solicitud de mejora',f); self.assertIn('Consulta / soporte',q); self.assertIn('SECURITY.md',b); self.assertIn('blank_issues_enabled: false',c); self.assertIn('/security/policy',c); self.assertIn('recm0708/mi-retiro-proyectado',c)
    def test_pr_template_exige_validacion_documentacion_y_privacidad(self):
        t=(GH/'pull_request_template.md').read_text(encoding='utf-8')
        for e in ('python -m compileall app','git diff --check','Documentación','Seguridad y privacidad','VERSION','commit está firmado'): self.assertIn(e,t)
    def test_workflow_auditoria_permisos_minimos_y_v7(self):
        t=(GH/'workflows/governance-audit.yml').read_text(encoding='utf-8')
        for e in ('name: Auditoría de gobernanza','contents: read','actions/checkout@v7','actions/setup-python@v7','tests.test_gov16_controles_github','git diff --check'): self.assertIn(e,t)
        self.assertNotIn('pull_request_target',t); self.assertNotIn('contents: write',t)
    def test_workflows_existentes_siguen_solo_lectura(self):
        for n in ('ci.yml','verificar-tags.yml'):
            t=(GH/'workflows'/n).read_text(encoding='utf-8'); self.assertIn('permissions:',t); self.assertIn('contents: read',t); self.assertNotIn('contents: write',t)
    def test_codeowners_cubre_areas_criticas(self):
        t=(GH/'CODEOWNERS').read_text(encoding='utf-8')
        for e in ('* @recm0708','/app/core/ @recm0708','/app/engines/ @recm0708','/regulations/ @recm0708','/docs/ @recm0708','/.github/ @recm0708'): self.assertIn(e,t)
    def test_documento_auditoria_registra_controles(self):
        t=(DOCS/'archive/governance/AUDITORIA_GITHUB.md').read_text(encoding='utf-8')
        for e in ('Pull Request obligatorio','Python 3.13','Python 3.14','Auditoría de gobernanza','force push','Dependency graph','Dependabot alerts','PR #17','24/24 tags','mi-retiro-proyectado'): self.assertIn(e,t)
        self.assertTrue((ROOT/'CODE_OF_CONDUCT.md').is_file()); self.assertTrue((ROOT/'SUPPORT.md').is_file()); self.assertTrue((DOCS/'archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md').is_file())
    def test_governance_enlaza_security_y_auditoria(self):
        t=(ROOT/'GOVERNANCE.md').read_text(encoding='utf-8'); self.assertIn('SECURITY.md',t); self.assertIn('Auditoría de gobernanza',t); self.assertIn('git verify-commit',t)
    def test_roadmap_cierra_gov16_sin_congelar_gov17(self):
        t=(DOCS/'governance/roadmap.md').read_text(encoding='utf-8'); self.assertIn('- [x] **GOV.1.6 — Controles GitHub y auditoría automática**',t); self.assertIn('**GOV.1.7 — Licencia**',t)
    def test_archivos_nuevos_limpios(self):
        ps=[ROOT/'SECURITY.md',ROOT/'CODE_OF_CONDUCT.md',ROOT/'SUPPORT.md',DOCS/'archive/governance/AUDITORIA_GITHUB.md',DOCS/'archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md',GH/'ISSUE_TEMPLATE/bug_report.yml',GH/'ISSUE_TEMPLATE/feature_request.yml',GH/'ISSUE_TEMPLATE/question.yml',GH/'ISSUE_TEMPLATE/config.yml',GH/'pull_request_template.md',GH/'workflows/governance-audit.yml']
        for p in ps:
            t=p.read_text(encoding='utf-8'); self.assertFalse(any(ord(c)<32 and c not in '\n\r\t' for c in t)); self.assertFalse(any(l.endswith((' ','\t')) for l in t.splitlines()))

if __name__=='__main__': unittest.main()
