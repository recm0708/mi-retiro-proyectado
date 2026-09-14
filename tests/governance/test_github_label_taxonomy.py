'Guard permanente de la taxonomía GitHub del repositorio.'

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]

CANONICAL = {
    "planning",
    "governance",
    "architecture",
    "post-1.0",
    "blocked",
    "ui",
    "accessibility",
    "security",
    "privacy",
    "documentation",
    "tests",
    "backend",
    "regulations",
    "dependencies",
    "github-actions",
    "maintenance",
}

SUPPLEMENTARY = {
    "bug",
    "enhancement",
    "question",
    "needs-triage",
    "duplicate",
    "good first issue",
    "help wanted",
    "invalid",
    "wontfix",
    "python",
    "javascript",
    "release",
}

ALLOWED = CANONICAL | SUPPLEMENTARY

DISALLOWED_ALIASES = {
    "ux",
    "technical-debt",
    "qa",
    "testing",
    "github_actions",
    "normativa",
    "needs-review",
}


def _section(text: str, start: str, end: str) -> str:
    pattern = (
        rf"(?ms)^{re.escape(start)}\s*$"
        rf"(.*?)"
        rf"(?=^{re.escape(end)}\s*$)"
    )
    match = re.search(pattern, text)
    if not match:
        raise AssertionError(f"No se encontró sección {start!r} -> {end!r}")
    return match.group(1)


def _inline_issue_form_labels(text: str) -> set[str]:
    result: set[str] = set()
    for match in re.finditer(r"(?m)^labels:\s*\[(.*?)\]\s*$", text):
        result.update(re.findall(r'["\']([^"\']+)["\']', match.group(1)))
    return result


def _labeler_keys(text: str) -> set[str]:
    return set(re.findall(r'(?m)^"([^"]+)":\s*$', text))


def _yaml_label_lists(text: str) -> set[str]:
    labels: set[str] = set()
    active_indent: int | None = None

    for line in text.splitlines():
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))

        if stripped == "labels:":
            active_indent = indent
            continue

        if active_indent is None:
            continue

        if not stripped:
            continue

        if indent <= active_indent:
            active_indent = None
            continue

        if stripped.startswith("- "):
            value = stripped[2:].strip().strip('"').strip("'")
            if value != "*":
                labels.add(value)

    return labels


class TestGitHubLabelTaxonomy(unittest.TestCase):
    def test_documento_gobierno_define_16_canonicos_y_prohibe_aliases(self):
        text = (
            ROOT / "docs/governance/github-issues-pr-governance.md"
        ).read_text(encoding="utf-8")
        section = _section(text, "## Labels", "## Milestones")

        canonical_paragraph = section.split(
            "GitHub conserva además 12 labels suplementarios", 1
        )[0]
        documented = set(re.findall(r"`([^`]+)`", canonical_paragraph))

        self.assertEqual(CANONICAL, documented)
        self.assertIn("28 labels", section)

        for alias in DISALLOWED_ALIASES:
            self.assertIn(f"`{alias}`", section)

    def test_documento_publico_enumera_exactamente_28_labels_activos(self):
        text = (
            ROOT / "docs/operations/github-public-repository.md"
        ).read_text(encoding="utf-8")
        section = _section(
            text,
            "## 3. Taxonomía de labels",
            "### 3.1. Contributors automatizados",
        )
        table_labels = set(
            re.findall(r"(?m)^\|\s*`([^`]+)`\s*\|", section)
        )

        self.assertEqual(ALLOWED, table_labels)
        self.assertEqual(28, len(table_labels))
        self.assertIn("16 labels canónicos", section)
        self.assertIn("12 labels suplementarios", section)

    def test_issue_forms_y_labeler_solo_consumen_labels_permitidos(self):
        form_labels: set[str] = set()
        for path in sorted(
            (ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.y*ml")
        ):
            form_labels.update(
                _inline_issue_form_labels(
                    path.read_text(encoding="utf-8")
                )
            )

        labeler_labels = _labeler_keys(
            (ROOT / ".github" / "labeler.yml").read_text(encoding="utf-8")
        )

        self.assertTrue(form_labels)
        self.assertTrue(labeler_labels)
        self.assertLessEqual(form_labels, ALLOWED)
        self.assertLessEqual(labeler_labels, ALLOWED)
        self.assertFalse(form_labels & DISALLOWED_ALIASES)
        self.assertFalse(labeler_labels & DISALLOWED_ALIASES)

    def test_release_yml_no_reintroduce_labels_inexistentes(self):
        text = (ROOT / ".github" / "release.yml").read_text(
            encoding="utf-8"
        )
        labels = _yaml_label_lists(text)

        self.assertTrue(labels)
        self.assertLessEqual(labels, ALLOWED)
        self.assertFalse(labels & DISALLOWED_ALIASES)
        self.assertNotIn("feature", labels)
        self.assertNotIn("fix", labels)
        self.assertNotIn("ignore-for-release", labels)

    def test_forms_semanticos_conservan_mapeos_canonicos(self):
        templates = ROOT / ".github" / "ISSUE_TEMPLATE"

        technical = _inline_issue_form_labels(
            (templates / "technical_debt.yml").read_text(encoding="utf-8")
        )
        ux_review = _inline_issue_form_labels(
            (templates / "ux_review.yml").read_text(encoding="utf-8")
        )
        architecture = _inline_issue_form_labels(
            (templates / "architecture.yml").read_text(encoding="utf-8")
        )

        self.assertEqual({"planning", "maintenance"}, technical)
        self.assertEqual({"planning", "ui"}, ux_review)
        self.assertEqual({"planning", "architecture"}, architecture)


if __name__ == "__main__":
    unittest.main()
