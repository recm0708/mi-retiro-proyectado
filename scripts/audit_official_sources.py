"""Audita la colección local de fuentes oficiales preservadas.

Responsabilidad:
- validar el manifiesto machine-readable de fuentes oficiales;
- comprobar presencia, tamaño, SHA-256 y firma binaria;
- detectar archivos binarios huérfanos o entradas duplicadas.

Límites:
- no accede a la red;
- no modifica documentos preservados;
- no determina vigencia jurídica ni sustituye revisión normativa humana.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_ROOT = ROOT / "docs" / "regulatory" / "sources" / "official"
MANIFEST = OFFICIAL_ROOT / "manifest.json"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:pdf|xlsx)$")
ALLOWED_SUFFIXES = {".pdf", ".xlsx"}


def sha256_file(path: Path) -> str:
    """Calcula SHA-256 hexadecimal en mayúsculas."""

    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest().upper()


def signature_matches(path: Path) -> bool:
    """Comprueba una firma mínima coherente con PDF o XLSX."""

    prefix = path.read_bytes()[:8]

    if path.suffix.lower() == ".pdf":
        return prefix.startswith(b"%PDF-")

    if path.suffix.lower() == ".xlsx":
        return prefix.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08"))

    return False


def valid_https_url(value: str) -> bool:
    """Exige HTTPS y host explícito para procedencia oficial."""

    parsed = urlsplit(value)

    return parsed.scheme == "https" and bool(parsed.netloc)


def main() -> int:
    """Ejecuta la auditoría completa de la colección."""

    if not MANIFEST.is_file():
        raise SystemExit(
            "[official-sources] ERROR: falta "
            + MANIFEST.relative_to(ROOT).as_posix()
        )

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if payload.get("schema_version") != 1:
        raise SystemExit(
            "[official-sources] ERROR: schema_version debe ser 1."
        )

    sources = payload.get("sources")

    if not isinstance(sources, list) or not sources:
        raise SystemExit(
            "[official-sources] ERROR: sources debe ser una lista no vacía."
        )

    ids: set[str] = set()
    paths: set[str] = set()
    declared_files: set[str] = set()
    errors: list[str] = []
    total_bytes = 0

    for index, source in enumerate(sources, start=1):
        source_id = str(source.get("id", "")).strip()
        local_path = str(source.get("local_path", "")).strip()
        file_name = Path(local_path).name

        if not source_id:
            errors.append(f"entrada {index}: id vacío")
        elif source_id in ids:
            errors.append(f"id duplicado: {source_id}")
        ids.add(source_id)

        if local_path in paths:
            errors.append(f"local_path duplicado: {local_path}")
        paths.add(local_path)

        if not local_path.startswith(
            "docs/regulatory/sources/official/"
        ):
            errors.append(
                f"{source_id}: local_path fuera de la colección"
            )
            continue

        if not NAME_RE.fullmatch(file_name):
            errors.append(
                f"{source_id}: nombre no canónico: {file_name}"
            )

        path = ROOT / local_path

        try:
            resolved = path.resolve()
            resolved.relative_to(OFFICIAL_ROOT.resolve())
        except ValueError:
            errors.append(
                f"{source_id}: ruta escapa OFFICIAL_ROOT"
            )
            continue

        if not path.is_file():
            errors.append(
                f"{source_id}: falta {local_path}"
            )
            continue

        if path.suffix.lower() not in ALLOWED_SUFFIXES:
            errors.append(
                f"{source_id}: extensión no permitida"
            )

        declared_files.add(path.relative_to(OFFICIAL_ROOT).as_posix())

        actual_size = path.stat().st_size
        expected_size = int(source.get("bytes", -1))

        if actual_size != expected_size:
            errors.append(
                f"{source_id}: bytes {actual_size} != {expected_size}"
            )

        total_bytes += actual_size

        expected_hash = str(source.get("sha256", "")).upper()
        actual_hash = sha256_file(path)

        if actual_hash != expected_hash:
            errors.append(
                f"{source_id}: SHA-256 no coincide"
            )

        if not signature_matches(path):
            errors.append(
                f"{source_id}: firma binaria inválida"
            )

        for key in ("official_url", "origin_page"):
            value = str(source.get(key, "")).strip()

            if not valid_https_url(value):
                errors.append(
                    f"{source_id}: {key} no es URL HTTPS válida"
                )

    actual_files = {
        path.relative_to(OFFICIAL_ROOT).as_posix()
        for path in OFFICIAL_ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in ALLOWED_SUFFIXES
    }

    orphan_files = sorted(actual_files - declared_files)
    missing_manifest_entries = sorted(declared_files - actual_files)

    for orphan in orphan_files:
        errors.append(
            "archivo binario sin manifest: " + orphan
        )

    for missing in missing_manifest_entries:
        errors.append(
            "entrada manifest sin archivo: " + missing
        )

    print(
        f"[official-sources] Entradas: {len(sources)}"
    )
    print(
        f"[official-sources] Binarios: {len(actual_files)}"
    )
    print(
        "[official-sources] Tamaño total: "
        f"{total_bytes / (1024 * 1024):.3f} MiB"
    )
    print(
        "[official-sources] IDs únicos: "
        f"{len(ids)}"
    )
    print(
        "[official-sources] Huérfanos: "
        f"{len(orphan_files)}"
    )

    if errors:
        for error in errors:
            print(
                "[official-sources] ERROR: " + error
            )
        return 1

    print(
        "[official-sources] OK: colección íntegra, "
        "nombres canónicos y hashes verificados."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
