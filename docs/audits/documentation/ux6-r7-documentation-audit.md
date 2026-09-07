# Auditoría documental integral UX.6 R7

**Estado:** R7 — reconciliación documental previa a R8
**Versión de aplicación revisada:** `0.1.20.01-beta`
**Candidato revision-aware:** G121/E01 (`0.1.21.01-beta`) — reservado, no aceptado
**Base auditada:** `f9cf50e0fe83e85092965562ad394271eafc52dd`
**Fecha:** 2026-09-07
**Clasificación:** Auditoría / Documentación / UX / Gobierno

## 1. Propósito

Determinar qué Markdown debe cambiar para describir UX.6 antes de R8. Esta
revisión no modifica `VERSION`, no consume G121 y no moderniza historia.

## 2. Inventario

- 166 Markdown versionables;
- 60 VIVO;
- 29 AUDITORIA;
- 64 HISTORICO;
- 9 PLANTILLA;
- 4 SOPORTE;
- 0 enlaces Markdown locales rotos;
- 118 señales heurísticas de posible obsolescencia;
- 46 documentos VIVO candidatos a revisión semántica;
- 0 contratos Developer dentro de los términos públicos.

Las 46 candidaturas **no equivalen a 46 ediciones**. `VERSIONING.md` permite
conservar metadata de la versión en que un documento fue revisado cuando su
contrato material no cambió.

## 3. Estado revision-aware

G120/E01 (`0.1.20.01-beta`) es el último estado aceptado y está publicado
mediante `v0.1.20.01-beta`. UX.6 conserva G121/E01 como candidato no aceptado:
R1–R6 implementados, R7 documental y R8 de auditoría/gate/promoción.

## 4. Documentación reconciliada

R7 actualiza estado o contrato material en:

- `README.md`, `CHANGELOG.md`, `RELEASES.md`, `SECURITY.md`, `VERSIONING.md`,
  `GOVERNANCE.md` y `CONTRIBUTING.md`;
- `docs/README.md` y `docs/audits/README.md`;
- roadmap, plan maestro y matriz maestra de pendientes;
- arquitectura general, Centro Developer y modelo de datos;
- guía de desarrollo, observabilidad, proceso de release y validación;
- especificación funcional, gestión de simulación, trazabilidad, transparencia
  e identidad visual;
- seguridad/privacidad técnica y modelo de amenazas;
- registro de decisiones en su bloque de estado vigente.

## 5. Candidatos revisados sin cambio material

No requieren modernización por UX.6 R7:

- `THIRD_PARTY_NOTICES.md`;
- motor/guía de cálculo y limitaciones no afectadas;
- licencia/distribución y dependencias de terceros;
- ledger Markdown de estados aceptados;
- documentación regulatoria SEBD/Mixto/SUCGS y Ley 81;
- procedimientos de derechos/incidentes/despliegue de terceros;
- `docs/security/privacy-policy.md` y `docs/security/terms-and-privacy.md`, ya
  reconciliados en R5–R6;
- estándares de código y estructura por extensión.

## 6. Hipervínculos

La base registra 0 enlaces locales rotos. Esta auditoría queda enlazada desde:

- [Índice de documentación](../../README.md);
- [Índice de auditorías y evidencias](../README.md).

R8 repetirá la auditoría Markdown después de la sincronización de promoción.

## 7. Frontera de promoción

R7 no modifica `VERSION`, el ledger JSON, `data/work-block-registry.json`, el
manifiesto de publicación ni el ledger Markdown de estados aceptados. Esas
superficies solo se mueven en R8 si G121/E01 supera el gate y se acepta.

## 8. Criterio de cierre R7

R7 puede cerrarse cuando la regresión documental, auditor Markdown, auditor de
identificadores y `git diff --check` queden limpios, manteniendo
`VERSION=0.1.20.01-beta` y G121/E01 como candidato no aceptado.
