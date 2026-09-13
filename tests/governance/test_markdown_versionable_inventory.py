"""Regresión del inventario Markdown versionable."""

from __future__ import annotations

from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from scripts import audit_markdown


class TestMarkdownVersionableInventory(unittest.TestCase):
    """Protege la cobertura de archivos nuevos antes del staging."""

    def test_incluye_tracked_y_untracked_pero_no_ignored(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)

            subprocess.run(
                ["git", "init", "-q"],
                cwd=root,
                check=True,
            )

            (root / ".gitignore").write_text(
                "ignored.md\n",
                encoding="utf-8",
            )
            (root / "tracked.md").write_text(
                "# Rastreado\n",
                encoding="utf-8",
            )
            (root / "untracked.md").write_text(
                "# Nuevo versionable\n",
                encoding="utf-8",
            )
            (root / "ignored.md").write_text(
                "# Ignorado\n",
                encoding="utf-8",
            )

            subprocess.run(
                ["git", "add", ".gitignore", "tracked.md"],
                cwd=root,
                check=True,
            )

            files = audit_markdown.versionable_markdown(root)

            self.assertEqual(
                [".gitignore", "tracked.md"],
                sorted(
                    subprocess.run(
                        ["git", "ls-files"],
                        cwd=root,
                        text=True,
                        capture_output=True,
                        check=True,
                    ).stdout.splitlines()
                ),
            )
            self.assertEqual(
                ["tracked.md", "untracked.md"],
                files,
            )


if __name__ == "__main__":
    unittest.main()
