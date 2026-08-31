"""Regresiones del motor canónico Automation Core y Automation Extended."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest
import yaml

from scripts import audit_action_references
from scripts import audit_external_links
from scripts import audit_pr_policy
from scripts import audit_repository_integrity
from scripts import audit_signed_tags
from scripts import quality_gate
from scripts import release_readiness


ROOT = Path(__file__).resolve().parents[1]


class TestAutomationCoreQualityGate(unittest.TestCase):
    def test_requirements_dev_separa_tooling_del_runtime(self):
        text = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
        self.assertIn("-r requirements.txt", text)
        self.assertIn("pytest==9.1.1", text)

    def test_modos_publicos_son_estables(self):
        self.assertEqual(
            ("fast", "pre-commit", "full", "release"),
            quality_gate.VALID_MODES,
        )

    def test_fast_no_ejecuta_suites_completas(self):
        names = quality_gate.planned_check_names("fast")
        self.assertNotIn("unittest", names)
        self.assertNotIn("pytest", names)
        self.assertIn("Documentación Markdown", names)
        self.assertIn("Identificadores de bloques", names)
        self.assertIn("Integridad del repositorio", names)

    def test_precommit_conserva_unittest_sin_duplicar_pytest(self):
        names = quality_gate.planned_check_names("pre-commit")
        self.assertIn("unittest", names)
        self.assertNotIn("pytest", names)
        self.assertIn("Integridad del repositorio", names)

    def test_full_ejecuta_unittest_y_pytest(self):
        names = quality_gate.planned_check_names("full")
        self.assertIn("unittest", names)
        self.assertIn("pytest", names)
        self.assertIn("Integridad del repositorio", names)

    def test_release_agrega_contrato_de_tag(self):
        names = quality_gate.planned_check_names("release")
        self.assertIn("Contrato de tag", names)

    def test_resolve_mode_usa_full_por_defecto(self):
        args = argparse.Namespace(
            fast=False,
            pre_commit=False,
            full=False,
            release=False,
        )
        self.assertEqual("full", quality_gate.resolve_mode(args))

    def test_metadata_refleja_version_y_siguiente_candidato(self):
        metadata = quality_gate.collect_metadata()
        self.assertEqual(
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            metadata["version"],
        )
        ledger = json.loads(
            (ROOT / "data" / "pre-1-0-revision-ledger.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(ledger["accepted_count"], metadata["accepted_count"])
        self.assertEqual(ledger["next_candidate"], metadata["next_candidate"])
        self.assertEqual(
            ledger["next_candidate_block"],
            metadata["next_candidate_block"],
        )

    def test_summary_markdown_es_legible_y_no_modifica_estado(self):
        report = {
            "result": "pass",
            "mode": "fast",
            "metadata": {
                "version": "0.1.19.05-beta",
                "git_sha": "abc123",
                "branch": "automation/test",
                "accepted_count": 119,
                "next_global": 120,
                "next_candidate": "0.1.20.01-beta",
                "next_candidate_block": "UX.5",
            },
            "summary": {"passed": 1, "failed": 0},
            "checks": [
                {
                    "name": "Ejemplo",
                    "status": "pass",
                    "duration_seconds": 0.1,
                    "summary": "OK",
                }
            ],
        }
        text = quality_gate.render_markdown_summary(report)
        self.assertIn("# Repository Quality Gate", text)
        self.assertIn("0.1.19.05-beta", text)
        self.assertIn("G120", text)
        self.assertIn("UX.5", text)
        self.assertIn("| Ejemplo | PASS |", text)

    def test_subprocess_environment_fuerza_utf8(self):
        env = quality_gate.subprocess_environment()
        self.assertEqual("1", env["PYTHONUTF8"])
        self.assertEqual("utf-8", env["PYTHONIOENCODING"])

    def test_metadata_registra_versiones_de_tooling(self):
        metadata = quality_gate.collect_metadata()
        self.assertTrue(metadata["node"].startswith("v"), metadata["node"])
        self.assertTrue(
            metadata["pytest"].startswith("pytest "),
            metadata["pytest"],
        )

    def test_precommit_delega_en_motor_canonico(self):
        text = (ROOT / "scripts" / "validate_precommit.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("scripts/quality_gate.py", text)
        self.assertIn("--pre-commit", text)
        self.assertIn("--fail-fast", text)
        self.assertNotIn("scripts/audit_markdown.py", text)
        self.assertNotIn("compileall", text)

    def test_workflow_quality_gate_existe_y_tiene_nombre_estable(self):
        path = ROOT / ".github" / "workflows" / "quality-gate.yml"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("name: Repository Quality Gate", text)

    def test_workflow_quality_gate_usa_permisos_minimos(self):
        text = (
            ROOT / ".github" / "workflows" / "quality-gate.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", text)
        self.assertNotIn("contents: write", text)
        self.assertNotIn("pull_request_target", text)
        self.assertIn("persist-credentials: false", text)

    def test_workflow_quality_gate_reutiliza_motor_canonico(self):
        text = (
            ROOT / ".github" / "workflows" / "quality-gate.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("python scripts/quality_gate.py", text)
        self.assertIn("--full", text)
        self.assertIn("--base-ref", text)
        self.assertIn("requirements-dev.txt", text)
        self.assertIn("python scripts/audit_pr_policy.py", text)

    def test_workflow_quality_gate_genera_summary_y_artifact(self):
        text = (
            ROOT / ".github" / "workflows" / "quality-gate.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("repository-health.json", text)
        self.assertIn("repository-health.md", text)
        self.assertIn("GITHUB_STEP_SUMMARY", text)
        self.assertIn("actions/upload-artifact@v7", text)
        self.assertIn("retention-days: 14", text)

    def test_workflows_canonicos_post_migracion_existen(self):
        workflows = ROOT / ".github" / "workflows"

        active = {
            "dependency-security.yml",
            "pr-labeler.yml",
            "quality-gate.yml",
            "scheduled-health.yml",
            "verificar-tags.yml",
            "visual-a11y.yml",
        }

        for name in active:
            with self.subTest(workflow=name):
                self.assertTrue(
                    (workflows / name).is_file()
                )

        for name in (
            "ci.yml",
            "governance-audit.yml",
            "markdown-audit.yml",
        ):
            with self.subTest(legacy=name):
                self.assertFalse(
                    (workflows / name).exists()
                )

    def test_scripts_readme_documenta_automation_core(self):
        text = (ROOT / "scripts" / "README.md").read_text(encoding="utf-8")
        for expected in (
            "`quality_gate.py`",
            "`audit_repository_integrity.py`",
            "`audit_pr_policy.py`",
            "`release_readiness.py`",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_readme_representa_arbol_versionable_real(self):
        files = audit_repository_integrity.repository_files()
        directories = audit_repository_integrity.canonical_directories(files)
        roots = audit_repository_integrity.root_files(files)
        readme_directories, readme_roots = (
            audit_repository_integrity.parse_readme_tree()
        )
        self.assertEqual(directories, readme_directories)
        self.assertEqual(roots, readme_roots)

    def test_integridad_repo_actual_no_tiene_bloqueadores(self):
        report = audit_repository_integrity.audit_repository()
        self.assertEqual("pass", report["result"], report["blockers"])

    def test_quality_gate_incluye_integridad_en_todos_los_modos(self):
        for mode in quality_gate.VALID_MODES:
            with self.subTest(mode=mode):
                self.assertIn(
                    "Integridad del repositorio",
                    quality_gate.planned_check_names(mode),
                )

    def test_quality_gate_delega_integridad_en_auditor_canonico(self):
        commands = dict(quality_gate.build_command_checks("fast", None))
        self.assertEqual(
            [
                quality_gate.sys.executable,
                "scripts/audit_repository_integrity.py",
            ],
            commands["Integridad del repositorio"],
        )

    def test_integridad_distingue_archivo_historico_de_documentacion_viva(self):
        self.assertFalse(
            audit_repository_integrity.link_source_is_enforced(
                "docs/archive/technical/ejemplo.md"
            )
        )
        self.assertTrue(
            audit_repository_integrity.link_source_is_enforced(
                "docs/operations/validation.md"
            )
        )
        self.assertTrue(
            audit_repository_integrity.link_source_is_enforced(
                "docs/product/functional-specification.md"
            )
        )

    def test_pr_policy_acepta_ramas_canonicas(self):
        for branch in (
            "automation/post-g119-core",
            "docs/reconciliacion",
            "fix/correccion-menor",
            "feature/nueva-capacidad",
        ):
            with self.subTest(branch=branch):
                self.assertEqual([], audit_pr_policy.branch_errors(branch))

    def test_pr_policy_rechaza_main_y_ramas_no_canonicas(self):
        for branch in (
            "main",
            "Automation/Core",
            "sin-separador",
            "automation/../main",
        ):
            with self.subTest(branch=branch):
                self.assertTrue(audit_pr_policy.branch_errors(branch))

    def test_pr_policy_dependabot_tiene_excepcion_explicita(self):
        self.assertIn("dependabot[bot]", audit_pr_policy.TRUSTED_BOTS)

    def test_pr_policy_exige_estado_revision_aware_coordinado(self):
        expected = {
            "VERSION",
            "data/pre-1-0-revision-ledger.json",
            "data/release-publication-manifest.json",
        }
        self.assertEqual(expected, set(audit_pr_policy.REVISION_STATE_FILES))

    def test_pr_policy_allowed_signers_proviene_de_base(self):
        text = (ROOT / "scripts" / "audit_pr_policy.py").read_text(
            encoding="utf-8"
        )
        self.assertIn(".github/allowed_signers", text)
        self.assertIn("git", text)
        self.assertIn("show", text)
        self.assertIn("verify-commit", text)

    def test_release_readiness_estado_actual_es_coherente(self):
        report = release_readiness.build_report()
        self.assertEqual("pass", report["result"], report["errors"])

    def test_release_readiness_distingue_tag_pendiente(self):
        self.assertEqual(
            "signed-tag-required",
            release_readiness.derive_release_action(
                tag_exists=False,
                tag_is_ancestor=False,
            ),
        )

    def test_release_readiness_distingue_tag_publicado(self):
        self.assertEqual(
            "none",
            release_readiness.derive_release_action(
                tag_exists=True,
                tag_is_ancestor=True,
            ),
        )

    def test_release_readiness_bloquea_divergencia_de_tag(self):
        self.assertEqual(
            "investigate-tag-divergence",
            release_readiness.derive_release_action(
                tag_exists=True,
                tag_is_ancestor=False,
            ),
        )

    def test_quality_gate_metadata_usa_next_global_canonico(self):
        metadata = quality_gate.collect_metadata()
        ledger = quality_gate.read_json(
            ROOT / "data" / "pre-1-0-revision-ledger.json"
        )
        self.assertEqual(
            ledger["next_global_if_ver2_accepted"],
            metadata["next_global"],
        )

    def test_action_references_rechaza_refs_mutables(self):
        for reference in (
            "actions/checkout@main",
            "owner/action@master",
            "owner/action@latest",
        ):
            with self.subTest(reference=reference):
                self.assertIsNotNone(
                    audit_action_references.validate_reference(reference)
                )

    def test_action_references_acepta_versiones_y_sha(self):
        for reference in (
            "actions/checkout@v7",
            "actions/dependency-review-action@v4",
            "owner/action@v1.2.3",
            "owner/action@" + ("a" * 40),
        ):
            with self.subTest(reference=reference):
                self.assertIsNone(
                    audit_action_references.validate_reference(reference)
                )

    def test_action_references_repo_actual_es_valido(self):
        report = audit_action_references.audit_workflows()
        self.assertEqual("pass", report["result"], report["errors"])

    def test_dependency_security_tiene_un_solo_job_principal(self):
        workflow = (
            ROOT / ".github" / "workflows" / "dependency-security.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("name: Dependency Security", workflow)
        self.assertIn("pip-audit==2.10.1", workflow)
        self.assertIn("actions/dependency-review-action@v5", workflow)
        self.assertIn("scripts/audit_action_references.py", workflow)

    def test_dependency_review_solo_corre_en_pr(self):
        workflow = (
            ROOT / ".github" / "workflows" / "dependency-security.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("if: github.event_name == 'pull_request'", workflow)

    def test_external_links_solo_usa_documentacion_vigente(self):
        files = audit_external_links.live_markdown_files()
        self.assertTrue(files)
        self.assertFalse(any(path.startswith("docs/archive/") for path in files))
        self.assertFalse(any(path.startswith("docs/audits/") for path in files))

    def test_external_links_descubre_urls_http(self):
        links = audit_external_links.discover_external_links()
        self.assertTrue(links)
        self.assertTrue(
            all(url.startswith(("http://", "https://")) for url in links)
        )

    def test_external_links_trata_restricciones_como_no_rotas(self):
        self.assertEqual(
            {401, 403, 429},
            audit_external_links.NON_BLOCKING_HTTP_CODES,
        )

    def test_signed_tags_descubre_tags_versionados(self):
        tags = audit_signed_tags.version_tags()
        self.assertTrue(tags)
        self.assertTrue(all(tag.startswith("v") for tag in tags))

    def test_scheduled_health_es_semanal_y_manual(self):
        workflow = (
            ROOT / ".github" / "workflows" / "scheduled-health.yml"
        ).read_text(encoding="utf-8")
        self.assertIn('cron: "0 14 * * 0"', workflow)
        self.assertIn("workflow_dispatch:", workflow)

    def test_scheduled_health_reutiliza_auditores_canonicos(self):
        workflow = (
            ROOT / ".github" / "workflows" / "scheduled-health.yml"
        ).read_text(encoding="utf-8")
        for expected in (
            "quality_gate.py",
            "audit_action_references.py",
            "audit_external_links.py",
            "audit_signed_tags.py",
            "release_readiness.py",
            "pip_audit",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, workflow)

    def test_scheduled_health_no_tiene_permisos_de_escritura(self):
        workflow = (
            ROOT / ".github" / "workflows" / "scheduled-health.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertNotIn("contents: write", workflow)

    def test_external_links_cli_funciona_como_script_directo(self):
        result = subprocess.run(
            [
                sys.executable,
                "scripts/audit_external_links.py",
                "--list-only",
                "--limit",
                "1",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("[external-links] Descubiertos:", result.stdout)

    def test_external_links_excluye_urls_locales_y_privadas(self):
        for url in (
            "http://127.0.0.1:8000",
            "http://localhost:8000/dev",
            "http://192.168.1.10",
            "http://10.0.0.1",
        ):
            with self.subTest(url=url):
                self.assertFalse(audit_external_links.is_external_url(url))
        self.assertTrue(
            audit_external_links.is_external_url("https://antai.gob.pa/")
        )

    def test_external_links_normaliza_backtick_markdown(self):
        self.assertEqual(
            "https://antai.gob.pa/direccion-de-proteccion-de-datos-personales/",
            audit_external_links.normalize_url(
                "https://antai.gob.pa/direccion-de-proteccion-de-datos-personales/`"
            ),
        )

    def test_external_links_descubrimiento_no_incluye_loopback(self):
        links = audit_external_links.discover_external_links()
        self.assertFalse(
            any("127.0.0.1" in url or "localhost" in url for url in links)
        )
        self.assertFalse(any(url.endswith("`") for url in links))

    def test_external_links_separa_badge_de_enlace_markdown(self):
        sample = (
            "[![CI](https://example.com/ci.svg?branch=main)]"
            "(https://example.com/actions/ci)"
        )
        urls = audit_external_links.URL_RE.findall(sample)
        self.assertEqual(
            [
                "https://example.com/ci.svg?branch=main",
                "https://example.com/actions/ci",
            ],
            urls,
        )

    def test_external_links_descubrimiento_no_contiene_sintaxis_markdown(self):
        links = audit_external_links.discover_external_links()
        for url in links:
            with self.subTest(url=url):
                self.assertNotIn("](", url)
                self.assertNotIn(")", url)
                self.assertNotIn("[", url)
                self.assertNotIn("]", url)

    def test_pr_labeler_configura_areas_canonicas(self):
        config = (
            ROOT
            / ".github"
            / "labeler.yml"
        ).read_text(
            encoding="utf-8"
        )

        for label in (
            "documentation",
            "ui",
            "security",
            "regulations",
            "backend",
            "tests",
            "github-actions",
            "maintenance",
            "dependencies",
        ):
            with self.subTest(label=label):
                self.assertIn(
                    f'"{label}":',
                    config,
                )

    def test_pr_labeler_usa_action_oficial_versionada(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "pr-labeler.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "actions/labeler@v7",
            workflow,
        )

        self.assertIn(
            "configuration-path: .github/labeler.yml",
            workflow,
        )

    def test_pr_labeler_tiene_permisos_minimos_de_etiquetado(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "pr-labeler.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "contents: read",
            workflow,
        )

        self.assertIn(
            "pull-requests: write",
            workflow,
        )

        self.assertNotIn(
            "issues: write",
            workflow,
        )

        self.assertNotIn(
            "contents: write",
            workflow,
        )

    def test_pr_labeler_pull_request_target_no_ejecuta_codigo_pr(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "pr-labeler.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "pull_request_target:",
            workflow,
        )

        self.assertNotIn(
            "actions/checkout@",
            workflow,
        )

        self.assertNotIn(
            "\n        run:",
            workflow,
        )

    def test_pr_labeler_no_sincroniza_etiquetas_manuales(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "pr-labeler.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "sync-labels: false",
            workflow,
        )



    def test_visual_a11y_fija_tooling_node_reproducible(self):
        package = (
            ROOT
            / "scripts"
            / "package.json"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            '"playwright": "1.62.1"',
            package,
        )

        self.assertIn(
            '"@axe-core/playwright": "4.13.0"',
            package,
        )

        self.assertIn(
            '"private": true',
            package,
        )

    def test_visual_a11y_cubre_viewports_temas_y_superficies(self):
        script = (
            ROOT
            / "scripts"
            / "visual_a11y_audit.mjs"
        ).read_text(
            encoding="utf-8"
        )

        for expected in (
            "360",
            "800",
            "768",
            "1024",
            "1440",
            "900",
            'theme: "light"',
            'theme: "dark"',
            'theme: "contrast"',
            '"/simulacion"',
            '"/comparar"',
            '"/metodologia"',
            '"/como-se-calcula"',
            '"/dev"',
            "miRetiroProyectado.tema",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    script,
                )

    def test_visual_a11y_es_informativo_por_defecto(self):
        script = (
            ROOT
            / "scripts"
            / "visual_a11y_audit.mjs"
        ).read_text(
            encoding="utf-8"
        )

        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "visual-a11y.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'process.env.MRP_A11Y_STRICT === "1"',
            script,
        )

        self.assertIn(
            'MRP_A11Y_STRICT: "0"',
            workflow,
        )

    def test_visual_a11y_workflow_usa_permisos_minimos_y_artifacts(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "visual-a11y.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "permissions:\n  contents: read",
            workflow,
        )

        self.assertNotIn(
            "contents: write",
            workflow,
        )

        self.assertIn(
            "actions/upload-artifact@v7",
            workflow,
        )

        self.assertIn(
            "GITHUB_STEP_SUMMARY",
            workflow,
        )

    def test_visual_a11y_workflow_arranca_fastapi_y_chromium(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "visual-a11y.yml"
        ).read_text(
            encoding="utf-8"
        )

        for expected in (
            "python -m uvicorn app.main:app",
            "npx playwright install --with-deps chromium",
            "MRP_ADMIN_ENABLED",
            "node scripts/visual_a11y_audit.mjs",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    workflow,
                )

    def test_dependency_security_audita_tooling_node(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "dependency-security.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "actions/setup-node@v7",
            workflow,
        )

        self.assertIn(
            "npm audit --prefix scripts --audit-level=high",
            workflow,
        )

        self.assertIn(
            "scripts/package*.json",
            workflow,
        )



    def test_dependabot_cubre_tooling_node_automatizacion(self):
        config = (
            ROOT
            / ".github"
            / "dependabot.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "package-ecosystem: npm",
            config,
        )
        self.assertIn(
            'directory: "/scripts"',
            config,
        )
        self.assertIn(
            "playwright",
            config,
        )
        self.assertIn(
            "@axe-core/playwright",
            config,
        )



    def test_visual_a11y_incluye_wcag_22(self):
        script = (
            ROOT
            / "scripts"
            / "visual_a11y_audit.mjs"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            '"wcag22a"',
            script,
        )
        self.assertIn(
            '"wcag22aa"',
            script,
        )



    def test_quality_gate_incluye_python_compatibility(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "quality-gate.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "python-compatibility:",
            workflow,
        )
        self.assertIn(
            "name: Python Compatibility",
            workflow,
        )
        self.assertIn(
            'python-version: "3.13"',
            workflow,
        )

    def test_python_compatibility_conserva_gate_legacy_313(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "quality-gate.yml"
        ).read_text(
            encoding="utf-8"
        )

        for expected in (
            "python -m pip check",
            "python -m compileall app scripts tests -q",
            "python -m unittest discover -s tests -q",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    workflow,
                )



    def test_python_compatibility_recupera_historial_y_tags(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "quality-gate.yml"
        ).read_text(
            encoding="utf-8"
        )

        compatibility = workflow.split(
            "  python-compatibility:",
            1,
        )[1]

        self.assertIn(
            "fetch-depth: 0",
            compatibility,
        )
        self.assertIn(
            "fetch-tags: true",
            compatibility,
        )
        self.assertIn(
            "persist-credentials: false",
            compatibility,
        )
        self.assertIn(
            "requirements-dev.txt",
            compatibility,
        )

    def test_inventario_workflows_post_migracion_es_canonico(self):
        workflows = ROOT / ".github" / "workflows"

        names = {
            path.name
            for path in workflows.glob("*.yml")
        }

        self.assertEqual(
            {
                "dependency-security.yml",
                "pr-labeler.yml",
                "quality-gate.yml",
                "scheduled-health.yml",
                "verificar-tags.yml",
                "visual-a11y.yml",
            },
            names,
        )


    def test_dependabot_coordina_pydantic_con_su_core(self):
        config = yaml.safe_load(
            (
                ROOT
                / ".github"
                / "dependabot.yml"
            ).read_text(
                encoding="utf-8"
            )
        )

        pip_update = next(
            item
            for item in config["updates"]
            if item["package-ecosystem"] == "pip"
        )

        allowed = {
            item["dependency-name"]
            for item in pip_update["allow"]
        }

        patterns = set(
            pip_update["groups"][
                "python-runtime-minor-patch"
            ]["patterns"]
        )

        for dependency in (
            "pydantic",
            "pydantic_core",
        ):
            with self.subTest(
                dependency=dependency
            ):
                self.assertIn(
                    dependency,
                    allowed,
                )
                self.assertIn(
                    dependency,
                    patterns,
                )


if __name__ == "__main__":
    unittest.main()
