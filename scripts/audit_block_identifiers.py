#!/usr/bin/env python3
"""Audita identificadores de bloques contra el registro canónico NOR.1 R8."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "work-block-registry.json"

def tracked_files() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return [line for line in proc.stdout.splitlines() if line.strip()]

def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    if data.get("schema_version") != 1:
        print("ERROR: schema_version debe ser 1.")
        return 1

    families = [item["prefix"] for item in data["families"]]
    identifiers = [item["identifier"] for item in data["identifiers"]]
    if len(families) != len(set(families)):
        print("ERROR: familias duplicadas.")
        return 1
    if len(identifiers) != len(set(identifiers)):
        print("ERROR: identificadores duplicados.")
        return 1

    allowed = set(identifiers)
    planned = {"PLAN.2", "UX.5", "PERSIST.1", "REP.1", "A11Y.2", "REV.1", "QA.1", "REL.1"}
    if not planned.issubset(allowed):
        print("ERROR: faltan identificadores futuros reservados.")
        return 1

    family_alt = "|".join(
        sorted(map(re.escape, families), key=len, reverse=True)
    )
    token_re = re.compile(
        rf"(?<![A-Za-z0-9_.-])(?:{family_alt})"
        rf"(?:\.(?:[A-Z][A-Z0-9]*|\d+[A-Za-z0-9]*))+"
        rf"(?![A-Za-z0-9_.-])"
    )

    unknown: dict[str, list[str]] = {}
    for rel in tracked_files():
        if rel.startswith("docs/archive/"):
            continue
        path = ROOT / rel
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in raw[:8192] or len(raw) > 3_000_000:
            continue
        text = raw.decode("utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for token in token_re.findall(line):
                if token not in allowed:
                    unknown.setdefault(token, []).append(f"{rel}:{lineno}")

    if unknown:
        print("ERROR: identificadores de familia conocida no registrados:")
        for token in sorted(unknown):
            print(f"  - {token}: {', '.join(unknown[token][:8])}")
        return 1

    print(
        f"OK: {len(families)} familias y "
        f"{len(allowed)} identificadores registrados."
    )
    return 0

if __name__ == "__main__":
    sys.exit(main())
