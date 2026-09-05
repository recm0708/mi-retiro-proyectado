# Política de seguridad

<!-- DOC1-R1-POST-MANT1:START -->
## Estado de seguridad post-MANT.1

La versión canónica vigente es `0.1.20.01-beta`.

El estado revision-aware vigente y publicado es:

- versión canónica: `0.1.20.01-beta` (G120/E01);
- DEV.2 R6 integrado mediante PR #111 / merge `bd2accb`;
- G119/E05 está publicado mediante `v0.1.19.05-beta`, sobre
  `9424ea854f859a24fd01fe83bdf5d476b52fc213`;
- G118/E04 permanece preservado mediante `v0.1.18.04-beta`;
- G120/E01 queda aceptado para UX.5 R6; G121/E01 queda reservado para UX.6 R1;
- REL.GOV.1 mantiene la firma del tag fuera de GitHub Actions;
- las rutas de reporte responsable y revisión de vulnerabilidades
  permanecen sin cambio material.

DEV.2 R6 separa expresamente identidad humana y Bearer técnico:
el login humano usa cuentas Developer persistentes y no depende de
`MRP_ADMIN_SECRET`; ese secreto queda limitado al contrato Bearer legado.
<!-- DOC1-R1-POST-MANT1:END -->

## Versiones soportadas

Mi Retiro Proyectado se encuentra en **desarrollo beta**. Los estados históricos conservan la familia legacy `0.0.N-beta`; VER.2 adopta para candidatos y estados nuevos la familia revision-aware `0.GG.RR.EE-beta`. El repositorio de código es público, pero la aplicación no se declara todavía como versión oficial ni como despliegue de producción.

| Línea | Soporte de seguridad |
| --- | --- |
| `0.1.20.01-beta` | Beta vigente G120/E01 aceptada para UX.5 R6; publicación mediante tag formal pendiente del cierre de promoción |
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
- `data/pre-1-0-revision-ledger.json`

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
