"""Gate canónico de calidad de Mi Retiro Proyectado.

Responsabilidad:
- centralizar comprobaciones reproducibles usadas por desarrollo y CI;
- reducir duplicación entre hooks locales y GitHub Actions;
- generar evidencia estructurada de salud del repositorio;
- validar código, documentación, gobierno y contrato de publicación.

Límites:
- no modifica archivos fuente;
- no crea commits, tags ni Releases;
- no implementa reglas previsionales;
- no sustituye la revisión semántica humana;
- no accede a secretos ni a datos locales ignorados.

Modos:
- fast: comprobaciones estructurales y técnicas rápidas;
- pre-commit: fast + unittest;
- full: pre-commit + pytest;
- release: full + validación explícita del tag esperado.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]

VALID_MODES = (
    "fast",
    "pre-commit",
    "full",
    "release",
)


@dataclass
class CheckResult:
    """Resultado normalizado de una comprobación del gate."""

    name: str
    status: str
    duration_seconds: float
    command: list[str]
    summary: str = ""
    output: str = ""


def configure_utf8_stdio() -> None:
    """Fija UTF-8 cuando la consola disponible permite reconfiguración."""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(
                encoding="utf-8",
                errors="replace",
            )


def subprocess_environment() -> dict[str, str]:
    """Fuerza UTF-8 en procesos Python hijos sin alterar el entorno fuente."""

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_process(
    command: list[str],
    *,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    """Ejecuta un proceso sin shell y captura su salida como UTF-8."""

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=subprocess_environment(),
        check=False,
    )


def combined_output(
    result: subprocess.CompletedProcess[str],
) -> str:
    """Combina stdout y stderr preservando texto útil."""

    parts = []

    if result.stdout:
        parts.append(result.stdout.rstrip())

    if result.stderr:
        parts.append(result.stderr.rstrip())

    return "\n".join(
        part
        for part in parts
        if part
    )


def summarize_output(text: str) -> str:
    """Obtiene una línea compacta útil para reportes."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return "OK"

    interesting = (
        "passed",
        "subtests",
        "Ran ",
        "OK",
        "familias",
        "Markdown",
        "manifiesto",
        "release-contract",
        "release-publication",
    )

    for line in reversed(lines):
        if any(token in line for token in interesting):
            return line[:500]

    return lines[-1][:500]


def execute_command_check(
    name: str,
    command: list[str],
) -> CheckResult:
    """Ejecuta un check ordinario y normaliza su resultado."""

    print()
    print(f"[quality-gate] {name}...")

    started = time.perf_counter()
    result = run_process(command)
    elapsed = time.perf_counter() - started

    output = combined_output(result)
    status = (
        "pass"
        if result.returncode == 0
        else "fail"
    )

    if output:
        print(output)

    if status == "pass":
        print(
            f"[quality-gate] PASS: {name} "
            f"({elapsed:.2f}s)"
        )
    else:
        print(
            f"[quality-gate] FAIL: {name} "
            f"({elapsed:.2f}s)",
            file=sys.stderr,
        )

    return CheckResult(
        name=name,
        status=status,
        duration_seconds=round(elapsed, 3),
        command=command,
        summary=summarize_output(output),
        output=output,
    )


def tracked_javascript_files() -> list[Path]:
    """Devuelve únicamente JavaScript rastreado por Git."""

    result = run_process(
        [
            "git",
            "ls-files",
            "--",
            ":(glob)app/static/js/**/*.js",
            "app/static/js/*.js",
        ]
    )

    if result.returncode != 0:
        raise RuntimeError(
            combined_output(result)
            or "git ls-files falló."
        )

    paths = {
        ROOT / line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    }

    return sorted(paths)


def execute_javascript_check() -> CheckResult:
    """Valida sintaxis de todo JavaScript versionado."""

    name = "JavaScript versionado"

    print()
    print(f"[quality-gate] {name}...")

    started = time.perf_counter()

    node = shutil.which("node")
    if not node:
        elapsed = time.perf_counter() - started
        message = "Node.js no está disponible en PATH."

        print(
            f"[quality-gate] FAIL: {message}",
            file=sys.stderr,
        )

        return CheckResult(
            name=name,
            status="fail",
            duration_seconds=round(elapsed, 3),
            command=["node", "--check", "<tracked-js>"],
            summary=message,
            output=message,
        )

    try:
        files = tracked_javascript_files()
    except RuntimeError as exc:
        elapsed = time.perf_counter() - started
        message = str(exc)

        print(message, file=sys.stderr)

        return CheckResult(
            name=name,
            status="fail",
            duration_seconds=round(elapsed, 3),
            command=[node, "--check", "<tracked-js>"],
            summary=message,
            output=message,
        )

    failures = []

    for path in files:
        result = run_process(
            [
                node,
                "--check",
                str(path),
            ]
        )

        if result.returncode != 0:
            failures.append(
                (
                    path.relative_to(ROOT).as_posix(),
                    combined_output(result),
                )
            )

    elapsed = time.perf_counter() - started

    if failures:
        output_lines = []

        for rel, text in failures:
            output_lines.append(
                f"{rel}:\n{text}"
            )

        output = "\n\n".join(output_lines)

        print(output, file=sys.stderr)
        print(
            f"[quality-gate] FAIL: {name} "
            f"({len(failures)} archivos con error).",
            file=sys.stderr,
        )

        return CheckResult(
            name=name,
            status="fail",
            duration_seconds=round(elapsed, 3),
            command=[node, "--check", "<tracked-js>"],
            summary=(
                f"{len(failures)} archivos con error "
                f"de {len(files)}."
            ),
            output=output,
        )

    summary = (
        f"{len(files)} archivos JavaScript válidos."
    )

    print(
        f"[quality-gate] PASS: {name} — "
        f"{summary} ({elapsed:.2f}s)"
    )

    return CheckResult(
        name=name,
        status="pass",
        duration_seconds=round(elapsed, 3),
        command=[node, "--check", "<tracked-js>"],
        summary=summary,
        output="",
    )


def execute_whitespace_check(
    base_ref: str | None,
) -> CheckResult:
    """Valida whitespace local y, opcionalmente, el rango de un PR."""

    name = "Whitespace Git"

    print()
    print(f"[quality-gate] {name}...")

    started = time.perf_counter()

    commands = [
        [
            "git",
            "diff",
            "--check",
        ],
        [
            "git",
            "diff",
            "--cached",
            "--check",
        ],
    ]

    if base_ref:
        commands.append(
            [
                "git",
                "diff",
                "--check",
                f"{base_ref}...HEAD",
            ]
        )

    outputs = []
    failure = False

    for command in commands:
        result = run_process(command)
        text = combined_output(result)

        if text:
            outputs.append(text)

        if result.returncode != 0:
            failure = True

    elapsed = time.perf_counter() - started
    output = "\n".join(outputs)

    if failure:
        if output:
            print(output, file=sys.stderr)

        print(
            f"[quality-gate] FAIL: {name}",
            file=sys.stderr,
        )

        return CheckResult(
            name=name,
            status="fail",
            duration_seconds=round(elapsed, 3),
            command=["git", "diff", "--check"],
            summary="Git detectó errores de whitespace.",
            output=output,
        )

    print(
        f"[quality-gate] PASS: {name} "
        f"({elapsed:.2f}s)"
    )

    return CheckResult(
        name=name,
        status="pass",
        duration_seconds=round(elapsed, 3),
        command=["git", "diff", "--check"],
        summary="Sin errores de whitespace.",
        output=output,
    )


def read_json(path: Path) -> dict:
    """Lee un objeto JSON UTF-8."""

    data = json.loads(
        path.read_text(
            encoding="utf-8-sig",
        )
    )

    if not isinstance(data, dict):
        raise ValueError(
            f"{path} no contiene un objeto JSON."
        )

    return data


def git_value(*args: str) -> str:
    """Obtiene un valor Git sin abortar la generación del reporte."""

    result = run_process(
        [
            "git",
            *args,
        ]
    )

    if result.returncode != 0:
        return ""

    return result.stdout.strip()


def tool_version(
    command: list[str],
) -> str:
    """Obtiene la versión compacta de una herramienta disponible."""

    result = run_process(command)

    if result.returncode != 0:
        return "unavailable"

    text = combined_output(result).strip()

    if not text:
        return "unknown"

    return text.splitlines()[0].strip()


def collect_metadata() -> dict:
    """Construye metadata reproducible del estado evaluado."""

    version = (
        ROOT
        / "VERSION"
    ).read_text(
        encoding="utf-8",
    ).strip()

    ledger = read_json(
        ROOT
        / "data"
        / "pre-1-0-revision-ledger.json"
    )

    manifest = read_json(
        ROOT
        / "data"
        / "release-publication-manifest.json"
    )

    tracked = run_process(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
        ]
    )

    tracked_count = (
        len(
            [
                line
                for line in tracked.stdout.splitlines()
                if line.strip()
            ]
        )
        if tracked.returncode == 0
        else None
    )

    branch = git_value(
        "branch",
        "--show-current",
    )

    return {
        "version": version,
        "accepted_count": ledger.get(
            "accepted_count"
        ),
        "next_global": ledger.get(
            "next_global_if_ver2_accepted"
        ),
        "next_candidate": ledger.get(
            "next_candidate"
        ),
        "next_candidate_block": ledger.get(
            "next_candidate_block"
        ),
        "published_block": manifest.get(
            "block"
        ),
        "published_revision": manifest.get(
            "revision"
        ),
        "git_sha": git_value(
            "rev-parse",
            "HEAD",
        ),
        "branch": branch or "detached",
        "tracked_files": tracked_count,
        "python": sys.version.split()[0],
        "node": (
            tool_version(
                ["node", "--version"]
            )
            if shutil.which("node")
            else "unavailable"
        ),
        "pytest": tool_version(
            [
                sys.executable,
                "-m",
                "pytest",
                "--version",
            ]
        ),
    }


def planned_check_names(
    mode: str,
) -> tuple[str, ...]:
    """Devuelve el contrato lógico de checks por modo."""

    if mode not in VALID_MODES:
        raise ValueError(
            f"Modo no válido: {mode}"
        )

    checks = [
        "Dependencias Python",
        "Documentación Markdown",
        "Identificadores de bloques",
        "Integridad del repositorio",
        "Compilación Python",
        "JavaScript versionado",
        "Contrato revision-aware",
        "Manifiesto de publicación",
        "Whitespace Git",
    ]

    if mode in {
        "pre-commit",
        "full",
        "release",
    }:
        checks.append(
            "unittest"
        )

    if mode in {
        "full",
        "release",
    }:
        checks.append(
            "pytest"
        )

    if mode == "release":
        checks.append(
            "Contrato de tag"
        )

    return tuple(checks)


def build_command_checks(
    mode: str,
    tag: str | None,
) -> list[tuple[str, list[str]]]:
    """Construye comandos ordinarios del modo solicitado."""

    compile_targets = (
        [
            "app",
            "scripts",
            "tests",
        ]
        if mode in {
            "full",
            "release",
        }
        else [
            "app",
        ]
    )

    checks = [
        (
            "Dependencias Python",
            [
                sys.executable,
                "-m",
                "pip",
                "check",
            ],
        ),
        (
            "Documentación Markdown",
            [
                sys.executable,
                "scripts/audit_markdown.py",
            ],
        ),
        (
            "Identificadores de bloques",
            [
                sys.executable,
                "scripts/audit_block_identifiers.py",
            ],
        ),
        (
            "Integridad del repositorio",
            [
                sys.executable,
                "scripts/audit_repository_integrity.py",
            ],
        ),
        (
            "Compilación Python",
            [
                sys.executable,
                "-m",
                "compileall",
                "-q",
                *compile_targets,
            ],
        ),
        (
            "Contrato revision-aware",
            [
                sys.executable,
                "scripts/release_contract.py",
            ],
        ),
        (
            "Manifiesto de publicación",
            [
                sys.executable,
                "scripts/release_publication.py",
                "--check-manifest",
            ],
        ),
    ]

    if mode in {
        "pre-commit",
        "full",
        "release",
    }:
        checks.append(
            (
                "unittest",
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tests",
                    "-q",
                ],
            )
        )

    if mode in {
        "full",
        "release",
    }:
        checks.append(
            (
                "pytest",
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "-q",
                ],
            )
        )

    if mode == "release":
        expected_tag = (
            tag
            or (
                "v"
                + (
                    ROOT
                    / "VERSION"
                ).read_text(
                    encoding="utf-8",
                ).strip()
            )
        )

        checks.append(
            (
                "Contrato de tag",
                [
                    sys.executable,
                    "scripts/release_contract.py",
                    "--check-tag",
                    expected_tag,
                ],
            )
        )

    return checks


def resolve_mode(
    args: argparse.Namespace,
) -> str:
    """Resuelve el modo solicitado por CLI."""

    selected = [
        name
        for name, enabled in (
            ("fast", args.fast),
            ("pre-commit", args.pre_commit),
            ("full", args.full),
            ("release", args.release),
        )
        if enabled
    ]

    if len(selected) > 1:
        raise ValueError(
            "Solo puede seleccionarse un modo."
        )

    if not selected:
        return "full"

    return selected[0]


def build_report(
    *,
    mode: str,
    results: list[CheckResult],
) -> dict:
    """Construye el documento repository-health."""

    metadata = collect_metadata()

    passed = sum(
        result.status == "pass"
        for result in results
    )

    failed = sum(
        result.status == "fail"
        for result in results
    )

    total_duration = round(
        sum(
            result.duration_seconds
            for result in results
        ),
        3,
    )

    return {
        "schema_version": 1,
        "project": "Mi Retiro Proyectado",
        "mode": mode,
        "result": (
            "pass"
            if failed == 0
            else "fail"
        ),
        "metadata": metadata,
        "summary": {
            "checks": len(results),
            "passed": passed,
            "failed": failed,
            "duration_seconds": total_duration,
        },
        "checks": [
            asdict(result)
            for result in results
        ],
    }


def render_markdown_summary(
    report: dict,
) -> str:
    """Renderiza un resumen legible para GitHub Actions."""

    metadata = report["metadata"]
    summary = report["summary"]

    lines = [
        "# Repository Quality Gate",
        "",
        f"- **Resultado:** `{report['result'].upper()}`",
        f"- **Modo:** `{report['mode']}`",
        f"- **Versión:** `{metadata['version']}`",
        f"- **Commit:** `{metadata['git_sha']}`",
        f"- **Rama:** `{metadata['branch']}`",
        (
            "- **Estado aceptado:** "
            f"G{int(metadata['accepted_count']):03d}"
        ),
        (
            "- **Siguiente candidato:** "
            f"G{int(metadata['next_global']):03d} — "
            f"`{metadata['next_candidate']}` — "
            f"{metadata['next_candidate_block']}"
        ),
        (
            "- **Checks:** "
            f"{summary['passed']} PASS / "
            f"{summary['failed']} FAIL"
        ),
        "",
        "| Check | Estado | Duración | Resumen |",
        "| --- | --- | ---: | --- |",
    ]

    for check in report["checks"]:
        lines.append(
            "| "
            + check["name"]
            + " | "
            + check["status"].upper()
            + " | "
            + f"{check['duration_seconds']:.2f}s"
            + " | "
            + check["summary"]
            .replace("|", "\\|")
            .replace("\n", " ")
            + " |"
        )

    return (
        "\n".join(lines).rstrip()
        + "\n"
    )


def write_report_files(
    report: dict,
    *,
    json_path: Path | None,
    summary_path: Path | None,
) -> None:
    """Escribe artifacts solo cuando la CLI lo solicita."""

    if json_path is not None:
        json_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        json_path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        print(
            "[quality-gate] Reporte JSON: "
            f"{json_path}"
        )

    if summary_path is not None:
        summary_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        summary_path.write_text(
            render_markdown_summary(
                report
            ),
            encoding="utf-8",
            newline="\n",
        )

        print(
            "[quality-gate] Resumen Markdown: "
            f"{summary_path}"
        )


def parser() -> argparse.ArgumentParser:
    """Construye la CLI pública."""

    p = argparse.ArgumentParser(
        description=__doc__,
    )

    modes = p.add_mutually_exclusive_group()

    modes.add_argument(
        "--fast",
        action="store_true",
        help="Ejecuta comprobaciones rápidas sin suites.",
    )

    modes.add_argument(
        "--pre-commit",
        dest="pre_commit",
        action="store_true",
        help="Ejecuta el contrato previsto para pre-commit.",
    )

    modes.add_argument(
        "--full",
        action="store_true",
        help="Ejecuta el gate integral.",
    )

    modes.add_argument(
        "--release",
        action="store_true",
        help="Ejecuta el gate integral más contrato de tag.",
    )

    p.add_argument(
        "--tag",
        help="Tag a validar en modo release.",
    )

    p.add_argument(
        "--base-ref",
        help=(
            "Ref base para validar whitespace "
            "del rango base...HEAD en CI."
        ),
    )

    p.add_argument(
        "--report-json",
        type=Path,
        help="Escribe repository-health.json.",
    )

    p.add_argument(
        "--summary-md",
        type=Path,
        help="Escribe resumen Markdown.",
    )

    p.add_argument(
        "--json",
        action="store_true",
        help="Imprime el reporte estructurado al finalizar.",
    )

    p.add_argument(
        "--fail-fast",
        action="store_true",
        help="Detiene el gate en el primer fallo.",
    )

    return p


def main() -> int:
    """Ejecuta el gate canónico."""

    configure_utf8_stdio()

    args = parser().parse_args()

    try:
        mode = resolve_mode(args)
    except ValueError as exc:
        print(
            f"[quality-gate] ERROR: {exc}",
            file=sys.stderr,
        )
        return 2

    if args.tag and mode != "release":
        print(
            "[quality-gate] ERROR: --tag solo puede "
            "utilizarse con --release.",
            file=sys.stderr,
        )
        return 2

    print(
        "Mi Retiro Proyectado — Repository Quality Gate"
    )
    print(
        f"Modo: {mode}"
    )
    print(
        f"Raíz: {ROOT}"
    )

    results: list[CheckResult] = []

    command_checks = build_command_checks(
        mode,
        args.tag,
    )

    before_javascript = {
        "Dependencias Python",
        "Documentación Markdown",
        "Identificadores de bloques",
        "Integridad del repositorio",
        "Compilación Python",
    }

    after_javascript = {
        "Contrato revision-aware",
        "Manifiesto de publicación",
        "unittest",
        "pytest",
        "Contrato de tag",
    }

    for name, command in command_checks:
        if name not in before_javascript:
            continue

        result = execute_command_check(
            name,
            command,
        )

        results.append(result)

        if (
            args.fail_fast
            and result.status == "fail"
        ):
            break

    if not (
        args.fail_fast
        and any(
            result.status == "fail"
            for result in results
        )
    ):
        result = execute_javascript_check()
        results.append(result)

    if not (
        args.fail_fast
        and any(
            result.status == "fail"
            for result in results
        )
    ):
        for name, command in command_checks:
            if name not in after_javascript:
                continue

            result = execute_command_check(
                name,
                command,
            )

            results.append(result)

            if (
                args.fail_fast
                and result.status == "fail"
            ):
                break

    if not (
        args.fail_fast
        and any(
            result.status == "fail"
            for result in results
        )
    ):
        result = execute_whitespace_check(
            args.base_ref
        )
        results.append(result)

    report = build_report(
        mode=mode,
        results=results,
    )

    write_report_files(
        report,
        json_path=args.report_json,
        summary_path=args.summary_md,
    )

    print()
    print("=" * 64)
    print(
        "RESULTADO: "
        + report["result"].upper()
    )
    print(
        "Checks: "
        f"{report['summary']['passed']} PASS / "
        f"{report['summary']['failed']} FAIL"
    )
    print(
        "Duración acumulada: "
        f"{report['summary']['duration_seconds']:.2f}s"
    )
    print("=" * 64)

    if args.json:
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )

    return (
        0
        if report["result"] == "pass"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
