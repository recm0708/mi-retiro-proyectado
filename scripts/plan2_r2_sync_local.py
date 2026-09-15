"""Sincronización local temporal de PLAN.2 R2.

Este archivo se elimina a sí mismo después de aplicar correctamente la
reconciliación. No materializa G126 ni cambia VERSION.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BRANCH = "plan/plan2-r2-replanificacion-maestra"
EXPECTED_VERSION = "0.1.25.01-beta"
BASE_SHA = "ee077c0d83931f140c91583fa8b2c4ae6b72dec8"


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> bool:
    target = ROOT / path
    old = target.read_text(encoding="utf-8")
    if old == text:
        return False
    target.write_text(text, encoding="utf-8", newline="\n")
    return True


def replace_marked(text: str, start: str, end: str, replacement: str) -> str:
    i = text.find(start)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise RuntimeError(f"No se encontró bloque requerido: {start} ... {end}")
    j += len(end)
    return text[:i] + replacement.rstrip() + text[j:]


def id_map(data: dict) -> dict[str, dict]:
    return {item["identifier"]: item for item in data["identifiers"]}


def ensure_identifier(
    data: dict,
    identifier: str,
    family: str,
    meaning: str,
    evidence: str,
    *,
    status: str = "planned_reserved",
    kind: str = "block",
) -> dict:
    ids = id_map(data)
    if identifier in ids:
        item = ids[identifier]
        item["family"] = family
        item["kind"] = kind
        item["status"] = status
        item["meaning"] = meaning
        item["evidence"] = evidence
        item.setdefault("global_refs", [])
        item["reusable_for_different_scope"] = False
        return item

    item = {
        "identifier": identifier,
        "family": family,
        "kind": kind,
        "status": status,
        "meaning": meaning,
        "evidence": evidence,
        "global_refs": [],
        "reusable_for_different_scope": False,
    }
    data["identifiers"].append(item)
    return item


def sync_registry() -> None:
    path = "data/governance/work-block-registry.json"
    data = json.loads(read(path))

    candidate = data["current_candidate"]
    if candidate.get("next_global_available") != 126:
        raise RuntimeError("Registry: next_global_available ya no es 126")
    candidate.update(
        {
            "global_revision": None,
            "revision_aware": None,
            "block": None,
            "revision": None,
            "revision_scope": None,
            "state": "unassigned",
            "next_functional_block_if_accepted": None,
            "next_functional_global_if_accepted": None,
            "edition": None,
            "planning_issue": 155,
            "next_global_available": 126,
        }
    )

    families = {item["prefix"]: item for item in data["families"]}
    if "DEPLOY" not in families:
        data["families"].append(
            {
                "prefix": "DEPLOY",
                "meaning": "Despliegue, runtime, hosting y operación de la aplicación.",
            }
        )

    ids = id_map(data)

    doc3 = ids["DOC.3"]
    doc3.update(
        {
            "status": "closed",
            "meaning": (
                "Auditoría documental integral periódica. R1 quedó cerrada, "
                "integrada y publicada como G125/E01 (0.1.25.01-beta)."
            ),
            "evidence": (
                "Issue #154; main@ee077c0d83931f140c91583fa8b2c4ae6b72dec8; "
                "tag firmado v0.1.25.01-beta; GitHub Release prerelease 388866555; "
                "preflight #166 CLEAN."
            ),
            "active_scope": "R1",
        }
    )

    plan2 = ids["PLAN.2"]
    plan2.update(
        {
            "status": "reopened_active_r2",
            "meaning": (
                "R1 permanece cerrado/aceptado como G114/E01. R2 está en "
                "progreso para replanificar el programa post-G125 sin Global "
                "ni VERSION preasignados."
            ),
            "evidence": (
                "G114 / PR #94 preservado; PLAN.2 R2 Issue #155; rama "
                "plan/plan2-r2-replanificacion-maestra; G126 libre."
            ),
            "active_scope": "R2",
        }
    )
    if "G114" not in plan2.get("global_refs", []):
        raise RuntimeError("Registry: PLAN.2 perdió la referencia histórica G114")
    if "G126" in plan2.get("global_refs", []):
        raise RuntimeError("Registry: PLAN.2 no puede referenciar G126 aún")

    doc4 = ids["DOC.4"]
    doc4.update(
        {
            "status": "planned_reserved",
            "meaning": (
                "Reingeniería documental canónica current-state-only. Se ejecuta "
                "después de VER.2 R6 y antes de la auditoría previsional #142; "
                "incluye lotes #172/#173/#174 y #174 absorbe #176."
            ),
            "evidence": "Issues #171–#174; decisión PLAN.2 R2/#155.",
        }
    )

    ver2 = ids["VER.2"]
    ver2.update(
        {
            "status": "reopened_planned_r6",
            "meaning": (
                "Reconciliación revision-aware y promoción. R6 será la primera "
                "fase material después de PLAN.2 R2 publicado y debe cerrar antes "
                "de DOC.4 R1."
            ),
            "evidence": "Ledger revision-aware; Issue #164; PLAN.2 R2/#155.",
        }
    )

    persist = ids["PERSIST.1"]
    persist.update(
        {
            "status": "planned_reserved",
            "meaning": (
                "Persistencia voluntaria y segura. Espera PLAN.2 publicado → "
                "VER.2 R6 → DOC.4 R1 → #142 y cualquier derivado funcional "
                "obligatorio. Toda nueva superficie visual debe recibir UX.x."
            ),
            "evidence": "Issues #130, #142, #155, #164, #171 y política UX/GOV #189.",
        }
    )

    rep = ids["REP.1"]
    rep.update(
        {
            "status": "planned_reserved",
            "meaning": (
                "Informes PDF y exportaciones finales después de PERSIST.1. Toda "
                "nueva superficie visible debe registrar la siguiente UX.x."
            ),
            "evidence": "Issue #143; PLAN.2 R2/#155; política UX/GOV #189.",
        }
    )

    sec2 = ids["SEC.2"]
    sec2.update(
        {
            "status": "reopened_planned_r7",
            "meaning": (
                "R1–R6 permanecen cerrados en G103–G108. R7 queda planificado "
                "como hardening final después de DEPLOY.1 y de toda la ola "
                "UX.7→UX.x, con #189 sin drift shared."
            ),
            "evidence": "Ledger G103-G108; Issue #144; PLAN.2 R2/#155; #189.",
        }
    )

    ensure_identifier(
        data,
        "DEPLOY.1",
        "DEPLOY",
        (
            "Arquitectura de despliegue 1.0: runtime FastAPI, hosting, HTTPS, "
            "persistencia operativa y CI/CD. Se ejecuta después de REP.1 y antes "
            "de la ola UX final."
        ),
        "Issue #157; PLAN.2 R2/#155.",
    )

    ux = {
        7: (133, "Inicio Asegurado / + Inicio/Resumen Developer /dev autenticado."),
        8: (134, "Asegurado /simulacion: entrada y selección Manual/Asistida antes del Paso 1."),
        9: (177, "Simulación Paso 1: Datos personales."),
        10: (178, "Simulación Paso 2: Cuotas."),
        11: (179, "Simulación Paso 3: Historial y base salarial."),
        12: (180, "Simulación Paso 4: Proyección y línea temporal."),
        13: (181, "Simulación Paso 5: Escenarios de retiro."),
        14: (182, "Simulación Paso 6: Resultados."),
        15: (183, "Asegurado /comparar: Escenarios/Comparación."),
        16: (184, "Asegurado /como-se-calcula."),
        17: (185, "Asegurado /metodologia: Fuentes/Metodología."),
        18: (186, "Modal Términos, privacidad y consentimiento."),
        19: (187, "Modal Gestión de datos."),
        20: (188, "Modal Mi Retiro Seguro: vista previa/importación."),
        21: (190, "Modal Ficha Digital: vista previa/revisión/importación."),
        22: (191, "Modal Vigencia de Ficha Digital."),
        23: (192, "Portal Developer: inicio de sesión."),
        24: (193, "Portal Developer: Diagnóstico."),
        25: (194, "Portal Developer: Eventos."),
        26: (195, "Portal Developer: Archivos."),
        27: (196, "Portal Developer: Mantenimiento."),
        28: (197, "Portal Developer: Usuarios/RBAC."),
        29: (198, "Portal Developer: Privacidad."),
        30: (199, "Portal Developer: Perfil y credenciales web."),
        31: (200, "Portal Developer: Acceso técnico."),
        32: (201, "Portal Developer: Centro de desarrollo legacy, si continúa soportado."),
    }
    for number, (issue, meaning) in ux.items():
        item = ensure_identifier(
            data,
            f"UX.{number}",
            "UX",
            meaning,
            f"Issue #{issue}; programa #129; política transversal #189; PLAN.2 R2/#155.",
        )
        if item.get("global_refs"):
            raise RuntimeError(f"Registry: UX.{number} no debe tener Global preasignado")

    for ident, meaning, evidence in (
        (
            "A11Y.2",
            "Auditoría WCAG 2.2 ampliada sobre todas las UX.x finales.",
            "Issue #145; programa UX #129; PLAN.2 R2/#155.",
        ),
        (
            "REV.1",
            "Revisión normativa, jurídica, privacidad y seguridad final después de A11Y.2.",
            "Issue #146; PLAN.2 R2/#155.",
        ),
        (
            "QA.1",
            "Auditoría integral de cierre beta después de DOC.1 R6 y toda UX.x final.",
            "Issue #148; PLAN.2 R2/#155.",
        ),
        (
            "REL.1",
            "Preparación y publicación de la primera versión oficial 1.0.0.0 después de QA.1.",
            "Issue #149; PLAN.2 R2/#155.",
        ),
    ):
        ids[ident].update({"status": "planned_reserved", "meaning": meaning, "evidence": evidence})

    data["post_nor3_state"].update(
        {
            "issues_reconciliation_required": True,
            "documentation_audit_issue": 154,
            "master_replanning_issue": 155,
            "next_candidate_assigned": False,
            "active_phase": "PLAN.2 R2",
            "active_phase_issue": 155,
            "active_phase_state": "in_progress",
            "next_global_available": 126,
        }
    )

    data["active_phase"] = {
        "block": "PLAN.2",
        "revision": "R2",
        "issue": 155,
        "state": "in_progress",
        "global_revision": None,
        "revision_aware": None,
        "base_global_revision": 125,
        "base_revision_aware": "0.1.25.01-beta",
        "next_phase_issue": 164,
    }

    all_refs = {
        ref
        for item in data["identifiers"]
        for ref in item.get("global_refs", [])
    }
    if "G126" in all_refs:
        raise RuntimeError("Registry: se detectó una preasignación prohibida G126")

    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sync_ledger_json() -> None:
    path = "data/governance/pre-1-0-revision-ledger.json"
    data = json.loads(read(path))

    if data["accepted_count"] != 125:
        raise RuntimeError("Ledger: accepted_count ya no es 125")
    if data["entries"][-1]["global_revision"] != 125:
        raise RuntimeError("Ledger: G125 ya no es la última entrada aceptada")
    if data.get("next_candidate") is not None:
        raise RuntimeError("Ledger: existe un candidato inesperado")

    assignment = data["next_candidate_assignment"]
    assignment["state"] = "unassigned"
    assignment["next_global_available"] = 126
    assignment["planning_issue"] = 155
    for key in ("global_revision", "revision_aware", "block", "revision", "edition"):
        if key in assignment:
            assignment[key] = None

    data["active_phase"] = {
        "block": "PLAN.2",
        "revision": "R2",
        "issue": 155,
        "state": "in_progress",
        "global_revision": None,
        "revision_aware": None,
        "base_global_revision": 125,
        "base_revision_aware": "0.1.25.01-beta",
        "next_phase_issue": 164,
    }

    if any(entry["global_revision"] == 126 for entry in data["entries"]):
        raise RuntimeError("Ledger: G126 no puede existir durante PLAN.2 R2")

    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sync_manifest() -> None:
    path = "data/governance/release-publication-manifest.json"
    data = json.loads(read(path))
    if data["version"] != EXPECTED_VERSION or data["block"] != "DOC.3":
        raise RuntimeError("Manifest: dejó de representar G125/DOC.3")

    next_step = data["next_step"]
    if next_step.get("global_revision") != 126:
        raise RuntimeError("Manifest: next_step global dejó de ser 126")
    next_step["revision_aware"] = None
    next_step["block"] = None
    next_step["description"] = (
        "G126 permanece disponible sin candidato, bloque ni VERSION preasignados. "
        "PLAN.2 R2/#155 está en progreso sobre G125 publicado. Después de validar, "
        "aceptar, integrar y publicar PLAN.2 R2 corresponde VER.2 R6/#164, sujeto "
        "a un preflight fresco #166; cualquier lote material nuevo de dependencias "
        "inserta MANT.2 R2+ antes de continuar."
    )
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


CURRENT_POST_BLOCK = """<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:START -->
## Estado vigente post-G125 / PLAN.2 R2

DOC.3 R1/#154 está cerrado, integrado y publicado como **G125/E01**
(`0.1.25.01-beta`) sobre
`main@ee077c0d83931f140c91583fa8b2c4ae6b72dec8`, con tag firmado
`v0.1.25.01-beta` y GitHub Release prerelease 388866555.

PLAN.2 R2/#155 está en progreso sobre la rama
`plan/plan2-r2-replanificacion-maestra`. G126 permanece libre: no tiene
candidato, bloque ni `VERSION` preasignados.

La continuidad material vigente es:

1. **PLAN.2 R2 / #155** — replanificación y sincronización del programa.
2. **VER.2 R6 / #164** — primera fase material después de publicar PLAN.2.
3. **DOC.4 R1 / #171** — reingeniería documental después de VER.2.
4. **Auditoría previsional / #142** y derivados funcionales obligatorios.
5. **PERSIST.1 / #130 → REP.1 / #143 → DEPLOY.1 / #157**.
6. **UX.7 → UX.x** — baseline conocido UX.7–UX.32 y expansión UX.33+ si
   aparecen nuevas superficies; #189 exige sincronización visual multiportal.
7. **SEC.2 R7 → rendimiento → A11Y.2 → REV.1 → #153 → DOC.1 R6 → QA.1 → REL.1**.

Antes y después de cada fase material se aplica #166. Un trabajo material nuevo
de dependencias antepone MANT.2 R2+ y obliga a sincronizar el árbol antes de
continuar.
<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->"""


def sync_common_live_blocks() -> None:
    paths = [
        "README.md",
        "docs/README.md",
        "GOVERNANCE.md",
        "VERSIONING.md",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "docs/operations/release-process.md",
        "docs/decisions/README.md",
        "docs/product/transparency.md",
    ]
    for path in paths:
        text = read(path)
        start = "<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:START -->"
        end = "<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->"
        if start in text:
            text = replace_marked(text, start, end, CURRENT_POST_BLOCK)
        write(path, text)


def sync_readme_status() -> None:
    path = "README.md"
    text = read(path)
    pattern = re.compile(
        r"(?ms)^## Estado del proyecto\n\n.*?(?=^La visibilidad pública del repositorio)"
    )
    replacement = """## Estado del proyecto

- **Versión canónica vigente:** `0.1.25.01-beta`, obtenida exclusivamente desde
  [`VERSION`](VERSION); corresponde a DOC.3 R1 / G125/E01.
- **Última publicación formal:** `v0.1.25.01-beta`, tag firmado sobre
  `main@ee077c0d83931f140c91583fa8b2c4ae6b72dec8`; GitHub Release prerelease
  388866555.
- **Fase material actual:** PLAN.2 R2 / #155, en progreso y **sin Global ni
  VERSION preasignados**.
- **Siguiente Global disponible:** G126, libre y sin candidato.
- **Preflight de entrada #166:** CLEAN; la verificación diferencial de apertura
  no detectó trabajo material nuevo de dependencias.
- **Próxima fase material después de PLAN.2 publicado:** VER.2 R6 / #164.
- **Secuencia posterior:** VER.2 → DOC.4 → #142/derivados → PERSIST.1 → REP.1 →
  DEPLOY.1 → UX.7→UX.x → SEC.2 R7 → rendimiento → A11Y.2 → REV.1 → #153 →
  DOC.1 R6 → QA.1 → REL.1.
- **Programa UX:** baseline conocido UX.7–UX.32; UX.33+ se crea de forma
  consecutiva cuando aparezca una superficie visual material nueva. #189 obliga
  a sincronizar todo cambio shared entre Asegurado, Developer y portales futuros.
- **Primera versión oficial objetivo:** `1.0.0.0` con `Build 000001`.
- **Etapa:** desarrollo beta; el repositorio público no equivale por sí solo a
  un despliegue oficial de producción.

"""
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("README: no se pudo reemplazar Estado del proyecto")
    write(path, text)


def sync_docs_index_status() -> None:
    path = "docs/README.md"
    text = read(path)
    text = re.sub(
        r"(?m)^\*\*Versión de aplicación:\*\*.*$",
        "**Versión de aplicación:** `0.1.25.01-beta` — G125/E01 publicado; G126 libre sin candidato",
        text,
        count=1,
    )
    text = re.sub(
        r"(?m)^\*\*Última actualización transversal:\*\*.*$",
        "**Última actualización transversal:** PLAN.2 R2/#155 — replanificación post-G125 en progreso — 2026-09-15",
        text,
        count=1,
    )
    text = re.sub(
        r"(?m)^\*\*Estado actual:\*\*.*$",
        (
            "**Estado actual:** DOC.3 R1/G125 está publicado; PLAN.2 R2/#155 está en progreso "
            "sin Global preasignado; G126 permanece libre y la siguiente fase material será "
            "VER.2 R6/#164 después de publicar PLAN.2."
        ),
        text,
        count=1,
    )
    write(path, text)


def sync_governance_status() -> None:
    path = "GOVERNANCE.md"
    text = read(path)
    text = re.sub(
        r"(?m)^\*\*Última revisión de estado:\*\*.*$",
        (
            "**Última revisión de estado:** PLAN.2 R2/#155 en progreso sobre G125/E01 "
            "publicado; G126 libre — 2026-09-15"
        ),
        text,
        count=1,
    )
    start = "<!-- DOC1-R1-POST-MANT1:START -->"
    end = "<!-- DOC1-R1-POST-MANT1:END -->"
    block = """<!-- DOC1-R1-POST-MANT1:START -->
## Estado de gobierno vigente

- `VERSION` sigue siendo la fuente única y permanece en `0.1.25.01-beta`.
- DOC.3 R1 está cerrado/publicado como G125/E01 mediante `v0.1.25.01-beta`.
- PLAN.2 R2/#155 está en progreso sin Global/VERSION preasignados.
- G126 permanece libre y `current_candidate` sigue sin asignar.
- VER.2 R6/#164 será la siguiente fase material después de publicar PLAN.2.
- DOC.4/#171 queda después de VER.2; #142/derivados preceden PERSIST.1.
- El programa UX se gobierna por #129: baseline UX.7–UX.32, expansión UX.33+
  y sincronización visual multiportal obligatoria mediante #189.
- Todo tag formal futuro exige integración, revalidación, firma y publicación
  gobernada conforme a REL.GOV.1 y #166.
<!-- DOC1-R1-POST-MANT1:END -->"""
    if start in text:
        text = replace_marked(text, start, end, block)
    write(path, text)


def sync_versioning_status() -> None:
    path = "VERSIONING.md"
    text = read(path)
    start = "<!-- DOC1-R1-POST-MANT1:START -->"
    end = "<!-- DOC1-R1-POST-MANT1:END -->"
    block = """<!-- DOC1-R1-POST-MANT1:START -->
## Estado revision-aware vigente

- `VERSION` contiene `0.1.25.01-beta` y corresponde a DOC.3 R1 / G125/E01.
- G125/E01 está integrado y publicado mediante tag firmado
  `v0.1.25.01-beta` y GitHub Release prerelease 388866555.
- G126 es el siguiente Global disponible, **sin candidato ni bloque reservado**.
- PLAN.2 R2/#155 está en progreso sin `global_revision`, `revision_aware` ni
  edición preasignados.
- La siguiente fase material después de publicar PLAN.2 será VER.2 R6/#164,
  que reformará esta política antes de DOC.4 R1.
- PR, squash, tag o Release que materializan un mismo estado no consumen otro
  Global.
<!-- DOC1-R1-POST-MANT1:END -->"""
    if start in text:
        text = replace_marked(text, start, end, block)
    write(path, text)


def sync_security_status() -> None:
    path = "SECURITY.md"
    text = read(path)
    start = "<!-- DOC1-R1-POST-MANT1:START -->"
    end = "<!-- DOC1-R1-POST-MANT1:END -->"
    block = """<!-- DOC1-R1-POST-MANT1:START -->
## Estado de seguridad vigente

La versión canónica publicada es `0.1.25.01-beta` / G125/E01.

- DOC.3 R1 está cerrado/publicado mediante `v0.1.25.01-beta`.
- El preflight #166 de entrada a PLAN.2 R2 quedó CLEAN y no apareció trabajo
  material nuevo de dependencias.
- PLAN.2 R2/#155 está en progreso sin Global/VERSION preasignados; G126 sigue
  libre.
- Login humano y Bearer técnico continúan separados.
- PERSIST.1, REP.1 y DEPLOY.1 permanecen pendientes antes de la ola UX final.
- SEC.2 R7/#144 se ejecutará únicamente después de cerrar toda UX.7→UX.x y de
  que #189 confirme ausencia de drift visual shared bloqueante.
- REL.GOV.1 mantiene la firma del tag fuera de GitHub Actions.
<!-- DOC1-R1-POST-MANT1:END -->"""
    if start in text:
        text = replace_marked(text, start, end, block)
    text = re.sub(
        r"(?m)^\| `0\.1\.25\.01-beta` \|.*$",
        "| `0.1.25.01-beta` | Beta vigente publicada G125/E01 / DOC.3 R1; PLAN.2 R2 en progreso; preflight #166 de entrada limpio |",
        text,
        count=1,
    )
    write(path, text)


def sync_contributing_status() -> None:
    path = "CONTRIBUTING.md"
    text = read(path)
    start = "<!-- DOC1-R1-POST-MANT1:START -->"
    end = "<!-- DOC1-R1-POST-MANT1:END -->"
    block = """<!-- DOC1-R1-POST-MANT1:START -->
## Estado de contribución vigente

- `VERSION` permanece en `0.1.25.01-beta` / G125/E01 publicado.
- PLAN.2 R2/#155 está en progreso y G126 sigue libre, sin candidato.
- La siguiente fase material será VER.2 R6/#164 después de publicar PLAN.2 y
  repetir #166.
- PERSIST.1 no comienza antes de VER.2 → DOC.4 → #142/derivados.
- La ola UX es dinámica (UX.7→UX.x) y todo cambio visual shared debe cumplir
  #189 en todos los portales aplicables.
- Código, pruebas, documentación y evidencia deben permanecer sincronizados.
<!-- DOC1-R1-POST-MANT1:END -->"""
    if start in text:
        text = replace_marked(text, start, end, block)
    write(path, text)


def sync_changelog() -> None:
    path = "CHANGELOG.md"
    text = read(path)
    pattern = re.compile(r"(?ms)^## \[Unreleased\]\n\n.*?(?=^## \[0\.1\.25\.01-beta\])")
    replacement = """## [Unreleased]

- PLAN.2 R2/#155 está en progreso sobre G125/E01 publicado y no materializa
  todavía G126.
- Se reconstruye el árbol pre-1.0: VER.2 → DOC.4 → #142/derivados → PERSIST →
  REP → DEPLOY → UX.7→UX.x → SEC.2 R7 → rendimiento → A11Y.2 → REV.1 → #153
  → DOC.1 R6 → QA.1 → REL.1.
- El baseline UX conocido se granulariza como UX.7–UX.32, una superficie/paso/
  modal por fase; UX.33+ se crea consecutivamente cuando aparezcan nuevas
  superficies pre-1.0.
- #189 formaliza la sincronización visual shared entre App Asegurado, Portal
  Developer y portales futuros.
- G126 permanece disponible sin candidato, bloque ni VERSION preasignados.

"""
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("CHANGELOG: no se pudo reemplazar Unreleased")
    text = text.replace(
        "- La publicación formal de G125/E01 permanece pendiente de PR/merge,\n  revalidación de `main`, tag firmado y GitHub Release prerelease.",
        (
            "- G125/E01 quedó integrado en `main@ee077c0d83931f140c91583fa8b2c4ae6b72dec8`, "
            "publicado mediante tag firmado `v0.1.25.01-beta` y GitHub Release prerelease 388866555."
        ),
    )
    write(path, text)


def sync_releases() -> None:
    path = "RELEASES.md"
    text = read(path)
    start = "<!-- DOC3-R1-G125-PROMOTION:START -->"
    end = "<!-- DOC3-R1-G125-PROMOTION:END -->"
    block = """<!-- DOC3-R1-G125-PROMOTION:START -->
## Promoción G125/E01 — DOC.3 R1

- G125/E01 (`0.1.25.01-beta`) materializa DOC.3 R1.
- Alcance: auditoría documental integral de estado vigente, gobierno,
  estructura, historia, coherencia semántica y cierre reproducible.
- Inventario auditado: 173 Markdown y 418 archivos textuales de
  código/configuración.
- Preflight final #166: 0 PRs, 0 Dependabot alerts y 0 PRs Dependabot; auditorías
  Python/npm verdes.
- Integración/publicación: `main@ee077c0d83931f140c91583fa8b2c4ae6b72dec8`,
  tag firmado `v0.1.25.01-beta`, GitHub Release prerelease 388866555.
- Revalidación final publicada: Quality Gate FULL 11 PASS / 0 FAIL; 1608
  `unittest` OK; `pytest` 1648 passed + 7844 subtests.
- DOC.4/#171 permanece planificado, ahora ubicado por PLAN.2 R2 después de
  VER.2 R6 y antes de #142/PERSIST.1.
- PLAN.2 R2/#155 está en progreso sin Global/VERSION preasignados.
- G126 permanece disponible sin candidato.
<!-- DOC3-R1-G125-PROMOTION:END -->"""
    text = replace_marked(text, start, end, block)
    write(path, text)


def sync_ledger_markdown() -> None:
    path = "docs/governance/pre-1-0-revision-ledger.md"
    text = read(path)
    text = re.sub(
        r"(?m)^\*\*Siguiente candidato disponible:\*\*.*$",
        (
            "**Siguiente candidato disponible:** **ninguno asignado** — G126 permanece libre; "
            "G125/E01 está publicado y PLAN.2 R2/#155 está en progreso sin Global preasignado"
        ),
        text,
        count=1,
    )
    start = "<!-- DOC3-G125-PROMOTION:START -->"
    end = "<!-- DOC3-G125-PROMOTION:END -->"
    block = """<!-- DOC3-G125-PROMOTION:START -->
## Estado DOC.3 R1 / G125-E01 publicado

- `VERSION` permanece en `0.1.25.01-beta` para DOC.3 R1 / G125-E01.
- G125/E01 está integrado en
  `main@ee077c0d83931f140c91583fa8b2c4ae6b72dec8`.
- Tag firmado: `v0.1.25.01-beta`.
- GitHub Release prerelease: 388866555.
- Revalidación final: Quality Gate FULL 11 PASS / 0 FAIL; 1608 unittest OK;
  pytest 1648 passed + 7844 subtests.
- G126 queda disponible sin candidato/bloque preasignado.
- PLAN.2 R2/#155 está en progreso sin Global/VERSION preasignados.
<!-- DOC3-G125-PROMOTION:END -->"""
    text = replace_marked(text, start, end, block)
    write(path, text)


def sync_misc_live_metadata() -> None:
    path = "docs/operations/release-process.md"
    text = read(path)
    text = re.sub(
        r"(?m)^\*\*Versión de aplicación:\*\*.*$",
        "**Versión de aplicación:** `0.1.25.01-beta` — G125/E01 publicado; G126 libre sin candidato; PLAN.2 R2 en progreso.",
        text,
        count=1,
    )
    write(path, text)

    path = "docs/product/transparency.md"
    text = read(path)
    text = re.sub(
        r"(?m)^\*\*Revisión transversal vigente:\*\*.*$",
        "**Revisión transversal vigente:** PLAN.2 R2/#155 — replanificación post-G125 en progreso — 2026-09-15",
        text,
        count=1,
    )
    write(path, text)

    # Reemplazos acotados en entradas vivas que todavía describían la frontera
    # pre-publicación de G125.
    for path in ("docs/decisions/README.md",):
        text = read(path)
        text = text.replace(
            "DOC.3 R1/#154 está materializado como G125/E01 y pendiente de\n  publicación; G126 queda disponible sin candidato/bloque asignado.",
            (
                "DOC.3 R1/#154 está cerrado/publicado como G125/E01; PLAN.2 R2/#155 "
                "está en progreso y G126 queda disponible sin candidato/bloque asignado."
            ),
        )
        write(path, text)


def sync_validation_inventory() -> None:
    path = "docs/operations/validation.md"
    text = read(path)
    old = "- `tests/governance/test_plan2_r1_master_pending_matrix.py`"
    new = (
        old
        + "\n- `tests/governance/test_plan2_r2_program.py`"
    )
    if "tests/governance/test_plan2_r2_program.py" not in text:
        if old not in text:
            raise RuntimeError("validation.md: no se encontró inventario PLAN.2 R1")
        text = text.replace(old, new, 1)
    write(path, text)


def post_checks() -> None:
    if read("VERSION").strip() != EXPECTED_VERSION:
        raise RuntimeError("VERSION fue modificado durante la sincronización")

    registry = json.loads(read("data/governance/work-block-registry.json"))
    ledger = json.loads(read("data/governance/pre-1-0-revision-ledger.json"))
    manifest = json.loads(read("data/governance/release-publication-manifest.json"))

    if registry["current_candidate"]["global_revision"] is not None:
        raise RuntimeError("Registry preasignó Global inesperadamente")
    if ledger["accepted_count"] != 125 or ledger["entries"][-1]["global_revision"] != 125:
        raise RuntimeError("Ledger dejó de cerrar en G125")
    if manifest["next_step"]["block"] is not None:
        raise RuntimeError("Manifest preasignó bloque G126")

    planning = "\n".join(
        read(path)
        for path in (
            "docs/governance/roadmap.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/pre-1-0-pending-matrix.md",
        )
    )
    for token in ("UX.32", "UX.33+", "#189", "UX.x final", "SEC.2 R7"):
        if token not in planning:
            raise RuntimeError(f"Planificación sin token obligatorio: {token}")
    if "UX.7–UX.20" in planning:
        raise RuntimeError("Persistió el rango UX fijo antiguo")


if __name__ == "__main__":
    branch = git("branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise SystemExit(
            f"ERROR: rama actual {branch!r}; se esperaba {EXPECTED_BRANCH!r}."
        )

    version = read("VERSION").strip()
    if version != EXPECTED_VERSION:
        raise SystemExit(
            f"ERROR: VERSION={version!r}; se esperaba {EXPECTED_VERSION!r}."
        )

    status = git("status", "--porcelain")
    # El único cambio permitido antes de ejecutar es ninguno: el script debe
    # provenir del commit remoto y el árbol debe estar limpio.
    if status:
        raise SystemExit(
            "ERROR: working tree no está limpio antes de sincronizar:\n" + status
        )

    changed_before = set(git("diff", "--name-only").splitlines())
    if changed_before:
        raise SystemExit("ERROR: existen cambios previos inesperados")

    sync_registry()
    sync_ledger_json()
    sync_manifest()
    sync_common_live_blocks()
    sync_readme_status()
    sync_docs_index_status()
    sync_governance_status()
    sync_versioning_status()
    sync_security_status()
    sync_contributing_status()
    sync_changelog()
    sync_releases()
    sync_ledger_markdown()
    sync_misc_live_metadata()
    sync_validation_inventory()
    post_checks()

    # El sincronizador es temporal: se retira del árbol final.
    Path(__file__).unlink()

    print("OK: sincronización local PLAN.2 R2 aplicada.")
    print(f"Rama: {branch}")
    print(f"Base publicada verificada: {BASE_SHA}")
    print(f"VERSION preservado: {EXPECTED_VERSION}")
    print("G126: libre / no reservado / sin candidato")
    print("UX baseline: UX.7–UX.32; expansión UX.33+ habilitada")
    print("Política UX/GOV: #189")
    print("Archivos modificados:")
    print(git("status", "--short"))
