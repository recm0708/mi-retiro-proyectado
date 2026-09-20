# Política de seguridad

<!-- NOR3-G122-PROMOTION:START -->
## Registro histórico — promoción G122-E01 post-NOR.3

> **Checkpoint histórico preservado.** Este bloque describe el estado inmediatamente posterior a la integración de NOR.3 y anterior a MANT.2 R1 / MANT.1 R8. No representa el estado vigente del repositorio; las secciones vigentes posteriores de este documento tienen precedencia.

- `VERSION` materializa `0.1.22.01-beta` para NOR.3 R8 / G122-E01.
- NOR.3 R1–R8 quedó integrado/aceptado mediante PR #162 / merge
  `b97cf61763479b80b8e8724b878089e8bb20fa00`.
- La revalidación automática de `main` quedó GREEN: Repository Quality Gate,
  Visual & Accessibility y CodeQL finalizaron en `success`.
- G123 es el siguiente Global disponible, pero **no tiene candidato ni bloque
  preasignado**.
- PERSIST.1 permanece planificado y no iniciado, sin Global preasignado.
- `v0.1.21.01-beta` / G121/E01 permanece como última publicación revision-aware
  hasta completar el tag/release firmado de G122/E01.
- `v0.1.22.01-beta` queda pendiente de creación/firma local y de la
  verificación/publicación gobernada por REL.GOV.1.
<!-- NOR3-G122-PROMOTION:END -->

<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:START -->
## Estado vigente post-G126 / MANT.2 R2 — candidato G127/E02

PLAN.2 R2/#155 permanece cerrado, integrado y publicado como **G126/E01**
(`0.1.26.01-beta`) sobre `main@1819f59f95731dc652ad62d84d6a5ad87ad3f8a4`,
mediante PR #202, tag firmado `v0.1.26.01-beta` y GitHub Release prerelease 390399947.

El preflight #166 previo a VER.2 detectó #204/#205 e insertó MANT.2 R2/#206.
La integración coordinada acepta `uvicorn 0.53.0`, conserva
`pydantic==2.13.5` + `pydantic_core==2.46.5`, cierra #204/#205 sin merge
directo, deja 0 PRs Dependabot, 0 ramas `dependabot/*` y 0 alerts abiertos, e
institucionaliza mediante #203 el checklist obligatorio de Issues.

MANT.2 R2/#206 queda **materializado y aceptado localmente como G127/E02**
(`0.1.27.02-beta`) en el Draft PR #207. Integración, revalidación de `main`, tag firmado
y GitHub Release prerelease todavía están pendientes.

**G128 permanece libre** y sin candidato, bloque ni `VERSION` preasignados.

La continuidad material vigente es:

1. **publicar MANT.2 R2 / G127-E02 / #206**;
2. **preflight fresco #166** después de la publicación;
3. **VER.2 R6 / #164** solo si #166 queda limpio;
4. **DOC.4 R1 / #171**;
5. **#142** y derivados funcionales obligatorios;
6. **PERSIST.1 / #130 → REP.1 / #143 → DEPLOY.1 / #157**;
7. **UX.7→UX.x / #129** bajo #189;
8. **SEC.2 R7 → rendimiento → A11Y.2 → REV.1 → #153 → DOC.1 R6 → QA.1 → REL.1**.
<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->


<!-- DOC1-R1-POST-MANT1:START -->
## Estado de seguridad vigente

La versión canónica vigente es `0.1.27.02-beta` / G127/E02 y está aceptada localmente para MANT.2 R2, pendiente de integración/publicación. La última publicación formal permanece `v0.1.26.01-beta` / G126/E01; G125/E01 se conserva como publicación histórica anterior.

- PLAN.2 R2/#155 está cerrado/publicado como G126/E01.
- El preflight fresco #166 previo a VER.2 detectó #204/#205 y activó MANT.2 R2/#206.
- MANT.2 R2/#206 está aceptado localmente como G127/E02 (`0.1.27.02-beta`), pendiente de integración/publicación; G128 sigue libre.
- Login humano y Bearer técnico continúan separados.
- PERSIST.1, REP.1 y DEPLOY.1 permanecen pendientes antes de la ola UX final.
- SEC.2 R7/#144 se ejecutará únicamente después de cerrar toda UX.7→UX.x y de
  que #189 confirme ausencia de drift visual shared bloqueante.
- REL.GOV.1 mantiene la firma del tag fuera de GitHub Actions.
<!-- DOC1-R1-POST-MANT1:END -->

## Versiones soportadas

Mi Retiro Proyectado se encuentra en **desarrollo beta**. Los estados históricos conservan la familia legacy `0.0.N-beta`; VER.2 adopta para candidatos y estados nuevos la familia revision-aware `0.GG.RR.EE-beta`. El repositorio de código es público, pero la aplicación no se declara todavía como versión oficial ni como despliegue de producción.

| Línea | Soporte de seguridad |
| --- | --- |
| `0.1.27.02-beta` | Beta vigente candidata G127/E02 / MANT.2 R2 aceptada localmente; integración/publicación pendiente; gates CP2/CP3 y reauditoría Dependabot en verde |
| `0.1.26.01-beta` | Beta previa publicada G126/E01 / PLAN.2 R2 mediante tag firmado `v0.1.26.01-beta` y GitHub Release prerelease 390399947 |
| `0.1.25.01-beta` | Beta previa publicada G125/E01 / DOC.3 R1 mediante tag firmado `v0.1.25.01-beta` y GitHub Release prerelease |
| `0.1.24.13-beta` | Beta previa G124/E13 publicada para MANT.1 R8 mediante PR #170, tag firmado `v0.1.24.13-beta` y GitHub Release prerelease |
| `0.1.23.01-beta` | Beta previa G123/E01 publicada para MANT.2 R1 mediante tag firmado `v0.1.23.01-beta` y GitHub Release prerelease |
| `0.1.22.01-beta` | Beta previa G122/E01 publicada para NOR.3; tag firmado y GitHub Release prerelease preservados |
| `0.1.21.01-beta` | Beta previa G121/E01 integrada para UX.6 R8; se conserva como estado material anterior a NOR.3 |
| `0.1.20.01-beta` | Beta previa G120/E01 publicada mediante tag firmado `v0.1.20.01-beta` y GitHub Release prerelease |
| `0.1.19.05-beta` | Beta previa G119/E05 publicada para DEV.2 R6 mediante tag firmado `v0.1.19.05-beta`, workflow de verificación en `success` y GitHub Release prerelease |
| `0.1.18.04-beta` | Beta previa G118/E04 publicada para DEV.2 R5 mediante tag firmado `v0.1.18.04-beta` y GitHub Release prerelease |
| `0.1.17.02-beta` | Beta previa G117/E02 publicada; tag firmado y GitHub Release prerelease automatizado conforme a REL.GOV.1 R2 |
| `0.1.16.05-beta` | Beta previa G116/E05 publicada; tag firmado, workflow de verificación y GitHub Release prerelease verificados |
| `0.1.15.04-beta` | Beta previa G115/E04 publicada; tag firmado, workflow de verificación y GitHub Release prerelease verificados |
| `0.1.14.01-beta` | Beta previa G114/E01 publicada; tag firmado, workflow de verificación y GitHub Release prerelease verificados |
| `0.1.13.03-beta` | Beta previa G113/E03 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.1.12.07-beta` | Beta G112/E07 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.1.11.01-beta` | Beta previa G111/E01 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.1.10.01-beta` | Beta G110/E01 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.1.09.01-beta` | Beta G109/E01 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.0.71.01-beta` | Beta revision-aware publicada previa; tag formal `v0.0.71.01-beta` preservado e inmutable |
| `0.0.26-beta` | Beta legacy histórica; tag formal inmutable y referencia estable para regresiones históricas |
| `0.0.25-beta` y anteriores | Históricas; no reciben correcciones independientes |

La base histórica anterior a VER.2 se reconstruye en G001–G070 sin crear tags retroactivos. La denominación G071/E01 usada originalmente para `v0.0.71.01-beta` se conserva como historia; la reconciliación vigente sitúa ese estado en G087/E01.

La primera versión oficial objetivo es `1.0.0.0` y solo podrá considerarse soportada cuando se materialice formalmente después de los gates definidos por el plan maestro.

La numeración revision-aware no mueve ni recrea tags legacy. Consultar `VERSIONING.md`, `docs/archive/governance/pre-1-0-versioning-audit.md`, `docs/archive/governance/ver2-revision-decision-matrix.md` y `docs/governance/pre-1-0-revision-ledger.md`.

## Reportar una vulnerabilidad

**No publique una vulnerabilidad explotable como issue público.**

Canal preferido para el repositorio público:

- **GitHub Private vulnerability reporting**, mediante la opción privada de reporte de vulnerabilidades del repositorio.

Canal privado alternativo:

`ruben.canizares@outlook.com`

Incluya, si es posible y usando evidencia sintética o sanitizada: componente/ruta, versión o SHA, impacto, pasos mínimos y mitigación conocida.

No envíe cédulas/NSS reales, PDFs personales, historiales salariales reales, secretos ni dumps completos de Developer Diagnostics sin revisión.

## Controles del repositorio público

La configuración vigente incluye, según evidencia manual del mantenedor:

- Dependency graph;
- Dependabot alerts;
- Dependabot security updates;
- CodeQL con Default setup;
- Secret Protection / secret scanning;
- Push protection;
- Private vulnerability reporting.

Estos controles reducen riesgo y facilitan detección/reporte; no constituyen una garantía de ausencia de vulnerabilidades.

## Tratamiento del reporte

El mantenedor confirma recepción cuando sea razonablemente posible, clasifica el evento, contiene exposiciones activas, preserva evidencia mínima, corrige y añade regresiones cuando proceda, y evalúa comunicaciones/notificaciones conforme a `docs/security/security-incident-procedure.md`.

No existe un SLA contractual de respuesta.

## Divulgación coordinada

Se solicita no publicar detalles explotables antes de que exista una corrección o mitigación razonable, salvo obligación legal o riesgo urgente.

## GitHub Private vulnerability reporting

Esta función está habilitada y complementa el canal privado alternativo indicado arriba. Los Issues públicos no deben utilizarse para vulnerabilidades explotables.

## Documentos relacionados

- `docs/security/threat-model.md`
- `docs/security/security-incident-procedure.md`
- `docs/security/security-and-privacy.md`
- `docs/archive/governance/github-audit.md`
- `docs/archive/governance/pre-1-0-versioning-audit.md`
- `docs/archive/governance/ver2-revision-decision-matrix.md`
- `docs/governance/pre-1-0-revision-ledger.md`
- `data/governance/pre-1-0-revision-ledger.json`

<!-- ANCLAS_HISTORICAS_VER2_SECURITY_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

| Versión | Estado de soporte |
| --- | --- |
| `0.0.71.01-beta` | Versión promovida históricamente en VER.2 R4; tag formal preservado como referencia revision-aware publicada previa |
| `0.0.26-beta` | Referencia legacy histórica preservada por pruebas de regresión; soportada como hito formal legacy etiquetado |

## Superficie administrativa post-SEC.2

La superficie Developer está deshabilitada salvo que `MRP_ADMIN_ENABLED=1`.
`/dev` es la entrada humana canónica y usa cuentas Developer persistentes,
contraseñas Argon2id y la cookie técnica `mrp_admin_session` `HttpOnly`
limitada a `Path=/dev`. El acceso humano no depende de `MRP_ADMIN_SECRET`;
`Authorization: Bearer` conserva ese secreto únicamente como contrato técnico
separado. El logout usa POST, las operaciones sensibles aplican CSRF y
revalidación cuando corresponde, y ninguna sesión puede sobreponerse al kill
switch. Para HTTPS interno debe activarse `MRP_ADMIN_COOKIE_SECURE=1`; una
exposición remota pública continúa fuera del escenario soportado.
