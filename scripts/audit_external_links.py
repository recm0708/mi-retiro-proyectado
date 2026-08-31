"""Audita enlaces HTTP/HTTPS de la documentación vigente.

Los enlaces externos no forman parte del gate ordinario de Pull Requests.
Este auditor está diseñado para ejecución programada porque servicios externos
pueden estar temporalmente indisponibles.

No modifica documentación ni sigue referencias del archivo histórico.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

if __package__:
    from scripts import audit_repository_integrity
else:
    import audit_repository_integrity


ROOT = Path(__file__).resolve().parents[1]

URL_RE = re.compile(
    r"https?://[^\s<>\"'`()\[\]]+",
    flags=re.IGNORECASE,
)

NON_BLOCKING_HTTP_CODES = {
    401,
    403,
    429,
}


def live_markdown_files() -> list[str]:
    """Devuelve Markdown vigente sujeto a revisión externa."""

    files = audit_repository_integrity.repository_files()

    docs = set(
        audit_repository_integrity.live_document_candidates(
            files
        )
    )

    root_docs = {
        rel
        for rel in files
        if "/" not in rel and rel.lower().endswith(".md")
    }

    return sorted(docs | root_docs)


def strip_fenced_code(text: str) -> str:
    """Evita tratar ejemplos de código como URLs documentales."""

    return re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL,
    )


def normalize_url(url: str) -> str:
    """Retira puntuación Markdown terminal habitual."""

    return url.rstrip("`.,;:!?)]}")


def is_external_url(url: str) -> bool:
    """Distingue Internet público de URLs locales/internas."""

    try:
        parsed = urlsplit(url)
    except ValueError:
        return False

    host = (parsed.hostname or "").lower().rstrip(".")

    if not host:
        return False

    if host == "localhost" or host.endswith(".localhost"):
        return False

    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return True

    return not (
        address.is_loopback
        or address.is_private
        or address.is_link_local
    )


def discover_external_links() -> dict[str, list[str]]:
    """Construye URL -> documentos que la referencian."""

    found: dict[str, set[str]] = {}

    for rel in live_markdown_files():
        path = ROOT / rel

        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError:
            continue

        text = strip_fenced_code(text)

        for raw in URL_RE.findall(text):
            url = normalize_url(raw)

            if not url or not is_external_url(url):
                continue

            found.setdefault(url, set()).add(rel)

    return {
        url: sorted(sources)
        for url, sources in sorted(found.items())
    }


def request_url(
    url: str,
    *,
    timeout: float,
) -> tuple[str, int | None, str]:
    """Consulta una URL y clasifica el resultado."""

    headers = {
        "User-Agent": "Mi-Retiro-Proyectado-Link-Audit/1.0",
        "Accept": "*/*",
    }

    request = urllib.request.Request(
        url,
        headers=headers,
        method="HEAD",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            return (
                "ok",
                response.getcode(),
                "reachable",
            )

    except urllib.error.HTTPError as exc:
        if exc.code == 405:
            get_request = urllib.request.Request(
                url,
                headers={
                    **headers,
                    "Range": "bytes=0-0",
                },
                method="GET",
            )

            try:
                with urllib.request.urlopen(
                    get_request,
                    timeout=timeout,
                ) as response:
                    return (
                        "ok",
                        response.getcode(),
                        "reachable-via-get",
                    )
            except urllib.error.HTTPError as get_exc:
                exc = get_exc
            except urllib.error.URLError as get_exc:
                return (
                    "broken",
                    None,
                    str(get_exc.reason),
                )

        if exc.code in NON_BLOCKING_HTTP_CODES:
            return (
                "restricted",
                exc.code,
                "reachable-but-restricted",
            )

        return (
            "broken",
            exc.code,
            str(exc.reason),
        )

    except urllib.error.URLError as exc:
        return (
            "broken",
            None,
            str(exc.reason),
        )

    except TimeoutError:
        return (
            "broken",
            None,
            "timeout",
        )


def check_with_retries(
    url: str,
    *,
    timeout: float,
    retries: int,
) -> dict:
    """Reintenta fallos externos antes de declararlos rotos."""

    last = (
        "broken",
        None,
        "not-checked",
    )

    for attempt in range(retries + 1):
        last = request_url(
            url,
            timeout=timeout,
        )

        if last[0] != "broken":
            break

        if attempt < retries:
            time.sleep(1.0 + attempt)

    status, code, detail = last

    return {
        "url": url,
        "status": status,
        "http_code": code,
        "detail": detail,
    }


def build_report(
    *,
    timeout: float,
    retries: int,
    limit: int | None,
    list_only: bool,
) -> dict:
    """Ejecuta descubrimiento y comprobación externa."""

    links = discover_external_links()
    urls = list(links)

    if limit is not None:
        urls = urls[:limit]

    results = []

    if list_only:
        results = [
            {
                "url": url,
                "status": "not-checked",
                "http_code": None,
                "detail": "list-only",
                "sources": links[url],
            }
            for url in urls
        ]
    else:
        for index, url in enumerate(urls, start=1):
            print(
                "[external-links] "
                f"{index}/{len(urls)} {url}"
            )

            item = check_with_retries(
                url,
                timeout=timeout,
                retries=retries,
            )
            item["sources"] = links[url]
            results.append(item)

    broken = [
        item
        for item in results
        if item["status"] == "broken"
    ]
    restricted = [
        item
        for item in results
        if item["status"] == "restricted"
    ]
    ok = [
        item
        for item in results
        if item["status"] == "ok"
    ]

    return {
        "schema_version": 1,
        "result": "pass" if not broken else "fail",
        "discovered": len(links),
        "evaluated": len(results),
        "ok": len(ok),
        "restricted": len(restricted),
        "broken": len(broken),
        "results": results,
    }


def render_markdown(report: dict) -> str:
    """Genera resumen para GitHub Actions."""

    lines = [
        "# External Link Audit",
        "",
        f"- **Resultado:** `{report['result'].upper()}`",
        f"- **URLs descubiertas:** `{report['discovered']}`",
        f"- **URLs evaluadas:** `{report['evaluated']}`",
        f"- **Accesibles:** `{report['ok']}`",
        f"- **Restringidas:** `{report['restricted']}`",
        f"- **Rotas:** `{report['broken']}`",
    ]

    broken = [
        item
        for item in report["results"]
        if item["status"] == "broken"
    ]

    if broken:
        lines.extend(
            [
                "",
                "## Enlaces que requieren revisión",
                "",
            ]
        )

        for item in broken:
            lines.append(
                "- "
                + item["url"]
                + " — "
                + item["detail"]
            )

    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)

    p.add_argument(
        "--timeout",
        type=float,
        default=12.0,
    )
    p.add_argument(
        "--retries",
        type=int,
        default=2,
    )
    p.add_argument(
        "--limit",
        type=int,
    )
    p.add_argument(
        "--list-only",
        action="store_true",
    )
    p.add_argument(
        "--strict",
        action="store_true",
    )
    p.add_argument(
        "--json-out",
        type=Path,
    )
    p.add_argument(
        "--markdown-out",
        type=Path,
    )

    return p


def main() -> int:
    args = parser().parse_args()

    report = build_report(
        timeout=args.timeout,
        retries=max(args.retries, 0),
        limit=args.limit,
        list_only=args.list_only,
    )

    print(
        "[external-links] "
        f"Descubiertos: {report['discovered']}"
    )
    print(
        "[external-links] "
        f"Evaluados: {report['evaluated']}"
    )
    print(
        "[external-links] "
        f"OK: {report['ok']} | "
        f"Restringidos: {report['restricted']} | "
        f"Rotos: {report['broken']}"
    )

    if args.json_out:
        args.json_out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.json_out.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

    if args.markdown_out:
        args.markdown_out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.markdown_out.write_text(
            render_markdown(report),
            encoding="utf-8",
            newline="\n",
        )

    if args.strict and report["broken"] > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
