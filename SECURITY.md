# Política de seguridad


<!-- DOC1-R1-POST-MANT1:START -->
## Estado de seguridad post-MANT.1

El cierre de MANT.1 R7 no cambia la política de seguridad ni convierte candidatos de versión en releases publicadas.

Estado vigente:

- La versión canónica vigente es `0.1.11.01-beta` (G111/E01).
- `v0.0.71.01-beta` es un tag formal histórico publicado originalmente como VER.2 G071/E01 y reconciliado posteriormente como G087/E01 sin alterar el objeto firmado.
- `v0.0.26-beta` permanece como tag legacy histórico e inmutable.
- VER.2, DOC.1 R1, NOR.1 y NOR.2 están cerrados.
- DOC.1 R2 quedó cerrado tras auditar integralmente la documentación Markdown posterior a NOR.2.
- DOC.2 R1 quedó aceptado como G111/E01 mediante PR #87 y merge `1041b59`; G112/E01 queda disponible para PERSIST.1.
- SEC.2 está cerrado después de R1–R6. AUD.SEC2 R1 fue aceptado como G109/E01 y corrige la semántica del kill switch administrativo y las regresiones de sesión sin modificar motores previsionales.
- Las rutas de reporte responsable y revisión de vulnerabilidades se mantienen sin cambio material.
<!-- DOC1-R1-POST-MANT1:END -->

## Versiones soportadas

Mi Retiro Proyectado se encuentra en **desarrollo beta**. Los estados históricos conservan la familia legacy `0.0.N-beta`; VER.2 adopta para candidatos y estados nuevos la familia revision-aware `0.GG.RR.EE-beta`. El repositorio de código es público, pero la aplicación no se declara todavía como versión oficial ni como despliegue de producción.

| Línea | Soporte de seguridad |
|---|---|
| `0.1.11.01-beta` | Beta vigente G111/E01; tag/Release pendientes hasta integrar y revalidar la promoción post-merge |
| `0.1.10.01-beta` | Beta G110/E01 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.1.09.01-beta` | Beta G109/E01 publicada; tag firmado y GitHub Release prerelease preservados |
| `0.0.71.01-beta` | Beta revision-aware publicada previa; tag formal `v0.0.71.01-beta` preservado e inmutable |
| `0.0.26-beta` | Beta legacy histórica; tag formal inmutable y referencia estable para regresiones históricas |
| `0.0.25-beta` y anteriores | Históricas; no reciben correcciones independientes |

La base histórica anterior a VER.2 se reconstruye en G001–G070 sin crear tags retroactivos. La denominación G071/E01 usada originalmente para `v0.0.71.01-beta` se conserva como historia; la reconciliación vigente sitúa ese estado en G087/E01.

La primera versión oficial objetivo es `1.0.0.0` y solo podrá considerarse soportada cuando se materialice formalmente después de los gates definidos por el plan maestro.

La numeración revision-aware no mueve ni recrea tags legacy. Consultar `VERSIONING.md`, `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md` y `docs/governance/pre-1-0-revision-ledger.md`.

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
- `docs/archive/governance/AUDITORIA_GITHUB.md`
- `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`
- `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`
- `docs/governance/pre-1-0-revision-ledger.md`
- `data/pre-1-0-revision-ledger.json`

<!-- ANCLAS_HISTORICAS_VER2_SECURITY_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

| Versión | Estado de soporte |
| --- | --- |
| `0.0.71.01-beta` | Versión promovida históricamente en VER.2 R4; tag formal preservado como referencia revision-aware publicada previa |
| `0.0.26-beta` | Referencia legacy histórica preservada por pruebas de regresión; soportada como hito formal legacy etiquetado |

## Superficie administrativa post-SEC.2

La superficie `/dev/` está deshabilitada salvo que `MRP_ADMIN_ENABLED=1` y
exista un secreto administrativo configurado fuera del repositorio. No existe
una clave predeterminada. El login web usa una cookie técnica `HttpOnly` y el
logout es una operación POST. Una sesión no puede sobreponerse al kill switch ni
a un estado de autenticación no configurada. Para HTTPS interno debe activarse
`MRP_ADMIN_COOKIE_SECURE=1`; una exposición remota pública continúa fuera del
escenario soportado hasta su revisión específica.
