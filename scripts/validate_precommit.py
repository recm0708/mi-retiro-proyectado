"""Gate local que impide confirmar cambios si el repositorio no está validado.

Responsabilidad:
- proteger el árbol de trabajo antes de crear commits locales;
- impedir commits directos en ``main``;
- exigir que el contenido preparado sea reproducible;
- ejecutar auditoría Markdown y validaciones técnicas de Python, JavaScript y pruebas.

Límites:
- no corrige archivos automáticamente;
- no reemplaza los checks remotos de GitHub Actions;
- no contiene reglas previsionales ni modifica motores de cálculo.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def _ejecutar(
    comando: list[str],
    *,
    raiz: Path,
    descripcion: str,
    capturar: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Ejecuta una comprobación y aborta el commit si devuelve error."""

    print(f"[pre-commit] {descripcion}...")
    resultado = subprocess.run(
        comando,
        cwd=raiz,
        text=True,
        capture_output=capturar,
        check=False,
    )
    if resultado.returncode != 0:
        if capturar:
            if resultado.stdout:
                print(resultado.stdout, end="")
            if resultado.stderr:
                print(resultado.stderr, end="", file=sys.stderr)
        print(
            f"[pre-commit] ERROR: falló «{descripcion}». Commit cancelado.",
            file=sys.stderr,
        )
        raise SystemExit(resultado.returncode or 1)
    return resultado


def _salida_git(raiz: Path, *argumentos: str) -> str:
    """Devuelve stdout de Git o cancela el commit si la consulta falla."""

    resultado = _ejecutar(
        ["git", *argumentos],
        raiz=raiz,
        descripcion=f"git {' '.join(argumentos)}",
        capturar=True,
    )
    return resultado.stdout.strip()


def _fallar(mensaje: str) -> None:
    """Muestra un error de gate y termina con código no cero."""

    print(f"[pre-commit] ERROR: {mensaje}", file=sys.stderr)
    raise SystemExit(1)


def _validar_estado_git(raiz: Path) -> None:
    """Exige una rama de trabajo y un árbol reproducible respecto del staging."""

    rama = _salida_git(raiz, "branch", "--show-current")
    if not rama:
        _fallar("HEAD está separado; no se permite crear el commit desde detached HEAD.")
    if rama == "main":
        _fallar("no se permiten commits directos en main; usa una rama de trabajo.")

    cambios_sin_preparar = _salida_git(raiz, "diff", "--name-only")
    if cambios_sin_preparar:
        print(cambios_sin_preparar, file=sys.stderr)
        _fallar(
            "hay cambios rastreados sin preparar. Prepara o revierte esos archivos "
            "antes de confirmar para que las pruebas correspondan al commit real."
        )

    no_rastreados = _salida_git(
        raiz,
        "ls-files",
        "--others",
        "--exclude-standard",
    )
    if no_rastreados:
        print(no_rastreados, file=sys.stderr)
        _fallar(
            "hay archivos no rastreados. Añádelos, ignóralos o retíralos antes de confirmar."
        )

    _ejecutar(
        ["git", "diff", "--cached", "--check"],
        raiz=raiz,
        descripcion="validar whitespace del contenido preparado",
    )


def _validar_entorno_y_codigo(raiz: Path) -> None:
    """Ejecuta el gate técnico completo del proyecto antes de cada commit."""

    _ejecutar(
        [sys.executable, "-m", "pip", "check"],
        raiz=raiz,
        descripcion="verificar dependencias Python",
    )
    _ejecutar(
        [sys.executable, "scripts/audit_markdown.py"],
        raiz=raiz,
        descripcion="auditar documentación Markdown",
    )
    _ejecutar(
        [sys.executable, "-m", "compileall", "-q", "app"],
        raiz=raiz,
        descripcion="compilar Python",
    )

    node = shutil.which("node")
    if not node:
        _fallar(
            "Node.js no está disponible en PATH; es necesario para validar la sintaxis "
            "JavaScript antes del commit."
        )

    archivos_js = sorted((raiz / "app" / "static" / "js").rglob("*.js"))
    for archivo in archivos_js:
        _ejecutar(
            [node, "--check", str(archivo)],
            raiz=raiz,
            descripcion=f"validar JavaScript {archivo.relative_to(raiz)}",
        )

    _ejecutar(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q"],
        raiz=raiz,
        descripcion="ejecutar suite completa",
    )


def main() -> int:
    """Ejecuta el gate pre-commit y devuelve cero únicamente si todo está correcto."""

    resultado_raiz = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if resultado_raiz.returncode != 0:
        _fallar("no se pudo determinar la raíz del repositorio Git.")

    raiz = Path(resultado_raiz.stdout.strip()).resolve()
    print(f"[pre-commit] Mi Retiro Proyectado — gate local en {raiz}")

    _validar_estado_git(raiz)
    _validar_entorno_y_codigo(raiz)

    print("[pre-commit] OK: gate completo superado. Git puede crear el commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
