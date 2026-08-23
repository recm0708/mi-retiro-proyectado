# Roadmap

**Estado:** vigente
**Versión candidata:** `0.0.71.01-beta` — VER.2 G071/E01
**Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
**Último tag formal legacy:** `v0.0.26-beta`
**Fecha de revisión:** 2026-08-22
**Mantenimiento técnico en curso:** MANT.1 R5E — estandarización de nombres de carpetas antes de SEC.2; MANT.1 R5D conserva la política, plantillas y uniformidad por extensión; MANT.1 R1 conserva la auditoría inicial, MANT.1 R2 conserva la documentación de scripts y hooks antes de SEC.2, MANT.1 R3 conserva encabezados funcionales para YAML de GitHub, MANT.1 R4 limpia encabezados operativos, MANT.1 R5A documenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla y MANT.1 R5C comenta JavaScript complejo

Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md`, `docs/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/ledger_revisiones_pre_1_0.json` y `docs/archive/`.

VER.2 es un bloque transversal de reconciliación y **no añade un bloque 15** al plan maestro de producto. DEV.2 ya quedó cerrado documentalmente en R4. MANT.1 se trata como checkpoint técnico de mantenibilidad antes de SEC.2 y tampoco añade un bloque funcional de producto. MANT.1 R1 queda como auditoría inicial de alcance, MANT.1 R2 materializa los primeros cambios documentales en scripts y hooks, MANT.1 R3 documenta los YAML de GitHub sin cambiar CI ni formularios y MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica permanezca en documentación, MANT.1 R5A comenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla de la guía pública, MANT.1 R5C comenta JavaScript complejo sin cambiar lógica visible y MANT.1 R5D define política/plantillas por extensión con uniformidad de encabezados.

## 1. Programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta

**Estado general:** cerrado el 2026-08-18.

- [x] **GOV.1.1 — Inventario y reconstrucción histórica**
  - inventario del repositorio;
  - reconstrucción de 80 commits;
  - clasificación retrospectiva `0.0.1-beta` a `0.0.21-beta`.

- [x] **GOV.1.2 — Gobierno y versionado**
  - `VERSION`;
  - `VERSIONING.md`;
  - `GOVERNANCE.md`;
  - `RELEASES.md`;
  - `.github/CODEOWNERS`;
  - primera versión formal `0.0.22-beta`;
  - tag `v0.0.22-beta`.

- [x] **GOV.1.3 — Reorganización y alineación integral de documentación**
  - [x] R1 — documentos de entrada, archivo histórico y estructura;
  - [x] R2 — documentación técnica vigente;
  - [x] R3 — normativa, seguridad y privacidad documental;
  - [x] R4 — capa de auditoría documental y controles de consistencia;
  - versión de cierre: `0.0.23-beta`.

- [x] **Prebloque transversal — Firma e integridad Git/GitHub**
  - [x] materialización y auditoría criptográfica de tags;
  - [x] CI y protecciones GitHub;
  - [x] corrección PowerShell/control characters;
  - [x] actualización controlada a `pypdf 6.15.0`;
  - [x] cierre formal del prebloque;
  - cinco estados aceptados G027–G031 según la segunda auditoría de VER.2.

- [x] **GOV.1.4 — Observabilidad y Developer Diagnostics**
  - [x] modo exclusivo de desarrollo;
  - [x] logging estructurado, correlación, redacción y retención local;
  - [x] exportación diagnóstica controlada sin telemetría remota;
  - [x] 13 regresiones específicas y suite de 487 pruebas en `OK`.

- [x] **GOV.1.5 — Seguridad, privacidad y transparencia**
  - [x] R1 — modelo de amenazas;
  - [x] R2 — derechos del titular e incidentes;
  - [x] R3 — cierre integral;
  - tres estados aceptados G033–G035.

- [x] **GOV.1.6 — Controles GitHub y auditoría automática** — G036.
- [x] **GOV.1.7 — Licencia** — derechos de distribución — G037.
- [x] **Hotfix de formato de licencia** — G038.
- [x] **GOV.1.8 — Auditoría final y cierre de gobierno** — G039; `v0.0.24-beta`.
- [x] **Saneamiento post-GOV.1** — G040.

## 2. Estado funcional del producto

### Implementado

- asistente de seis pasos;
- Paso 4 — proyección salarial/laboral auditado y cerrado en UX.4.6f;
- Paso 5 — escenarios de retiro auditado y cerrado en UX.4.6g;
- Paso 6 — resultados y exportación auditado y cerrado en UX.4.6h, con copia imprimible A4 provisional;
- sección pública **Cómo se calcula** cerrada en UX.4.6i;
- motores SEBD, Mixto y SUCGS para el alcance general documentado;
- comparación y trazabilidad de cálculo;
- metodología y fuentes;
- importación revisable de Mi Retiro Seguro y Ficha Digital;
- procedencia editable con fotografía documental original, copia de trabajo y exclusión explícita de períodos;
- gestión local de datos de simulación;
- temas Claro, Oscuro, Automático y Alto contraste;
- base responsive y accesible;
- identidad visual oficial, favicons y Social Preview;
- repositorio público con metadata, topics, labels e Issue Forms;
- Dependency graph, Dependabot, CodeQL, Secret Protection, Push protection y Private vulnerability reporting;
- CI y auditoría automática de gobernanza;
- DEV.2 — Centro de desarrollo sobre Developer Diagnostics cerrado documentalmente en R4.

### Pendiente o incompleto

- VER.2 — cerrar reconciliación revision-aware y promover G071 si el gate completo, PR/CI e integración son satisfactorios;
- MANT.1 — documentación, encabezados operativos y comentarios internos de mantenibilidad en Python, CSS, plantillas y JavaScript antes de SEC.2;
- hardening integral SEC.2;
- reconstrucción detallada del CHANGELOG `0.0.1-beta`–`0.0.21-beta` en DOC.2;
- persistencia voluntaria si permanece dentro del alcance 1.0;
- informes PDF y exportación final seleccionable;
- auditoría WCAG 2.2 ampliada con tecnologías de apoyo/dispositivos;
- revisión normativa/jurídica externa prevista;
- parámetros oficiales que la documentación identifica como no disponibles o no reconstruibles con fidelidad.

## 3. UX.4.6 — trabajo funcional cerrado

**Estado:** UX.4.6e y UX.4.6f–UX.4.6i cerrados. VER.2 reconcilia ahora su representación en la historia; no reabre sus funcionalidades.

- [x] **UX.4.6e — Estandarización técnica, comentarios y coherencia de interfaz post-GOV.1**
  - [x] R1–R7 — G041–G047;
  - [x] checkpoint pre-R8 — identidad visual/repositorio público, PR #20, 624 pruebas; estado material e independiente G048;
  - [x] R8 — validación funcional/procedencia editable; R8.1 fue intermedia y R8.2/cierre documental materializa G049;
  - [x] R9.2 — cierre formal mediante PR #21/#22 y tag `v0.0.25-beta`; R9.1 se conserva como candidato local histórico; el cierre se contabiliza una vez como G050.

- [x] **PLAN.1 — alineación maestra hacia 1.0**
  - [x] R1, R2A, R2B1, R2B2, R2C, R3A, R3B1 y R3B2 — G051–G058;
  - [x] R4.1 — cierre local aceptado con 720 pruebas, G059;
  - [x] R4.2 — higiene post-merge y cierre pre-tag, G060; tag `v0.0.26-beta`.

- [x] **UX.4.6f — Paso 4 · Proyección salarial/laboral**
  - [x] R1/R1.1 — aceptadas conjuntamente por PR #28 tras validación manual y 743 pruebas; G061;
  - [x] mantenimiento coordinado de dependencias — PR #29, `pypdf 6.16.1` y `uvicorn 0.52.3`; G062;
  - [x] R2 — auditoría lógica/matemática; PR #30 y 756 pruebas; G063;
  - [x] cierre/hardening — PR #31, gate `pre-commit`, cinco regresiones nuevas y 762 pruebas; G064.

- [x] **UX.4.6g — Paso 5 · Escenarios de retiro**
  - [x] cierre PR #32 con 784 pruebas; G065. Los refinamientos R1.2/R1.3/R1.4/R1.4.2/R1.4.3 se preservan como evolución interna del mismo estado aceptado.

- [x] **UX.4.6h — Paso 6 · Resultados y exportación**
  - [x] R1 — candidato fallido; no consume Global;
  - [x] R1.1 — corrección aceptada; G066;
  - [x] R1.2 — claridad y jerarquía aceptadas; G067;
  - [x] R1.3 — informe A4 independiente y cierre PR #33 con 812 pruebas; G068.

- [x] **UX.4.6i — Cómo se calcula**
  - [x] R1 — ruta pública, estructura inicial y gate de 826 pruebas; G069;
  - [x] R1.2 — navegación, recorrido Pasos 1–6 y densidad visual; refinamiento interno;
  - [x] R1.3 — ejemplos sustituidos, terminología y espaciado; refinamiento interno;
  - [x] R1.4 — etiqueta **Ejemplo** y cierre PR #34 con 841 pruebas; G070.

No existe una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2 demostrada por sección, gate o artefacto independiente; las referencias agregadas que la incluían se corrigen en VER.2.

## 4. PLAN.1, VER.2 y secuencia hacia 1.0

**PLAN.1:** cerrado formalmente en `0.0.26-beta` con **720 pruebas en `OK`** y tag firmado `v0.0.26-beta`. La segunda auditoría reconoce diez estados aceptados G051–G060 dentro de su evolución.

**VER.2:** bloque transversal activo. La base anterior al cambio contiene **70 estados aceptados (G001–G070)**. El candidato `0.0.71.01-beta` representa G071/E01 y solo se acepta después del gate completo, PR/CI e integración.

**Checkpoint técnico actual:** MANT.1 R5D — política, plantillas y uniformidad por extensión antes de SEC.2.

Documentos canónicos de VER.2:

- `AUDITORIA_VERSIONADO_PRE_1_0.md` — criterio contable y exclusiones;
- `LEDGER_REVISIONES_PRE_1_0.md` — ledger G001–G070 y reserva G071;
- `MATRIZ_DECISION_REVISIONES_VER2.md` — justificación de la segunda pasada;
- `../data/ledger_revisiones_pre_1_0.json` — ledger estructurado validable;
- `../VERSIONING.md` — política de numeración.

Secuencia funcional de 14 bloques hacia 1.0, sin contar VER.2 como bloque adicional:

1. PLAN.1 — alineación maestra — **cerrado**;
2. UX.4.6f — Paso 4 — **cerrado**;
3. UX.4.6g — Paso 5 — **cerrado**;
4. UX.4.6h — Paso 6 — **cerrado**;
5. UX.4.6i — Cómo se calcula — **cerrado**;
6. DEV.2 — Centro de desarrollo — **cerrado**;
   - Checkpoint técnico intermedio: MANT.1 documenta scripts, hooks, YAML de GitHub, encabezados operativos y comentarios internos de mantenibilidad en Python, CSS, plantillas y JavaScript antes de SEC.2, sin añadir un bloque funcional de producto.
7. SEC.2 — Hardening integral;
8. DOC.2 — CHANGELOG histórico detallado;
9. PERSIST.1 — Persistencia voluntaria y segura;
10. REP.1 — Informes y exportaciones;
11. A11Y.2 — WCAG 2.2 ampliada;
12. REV.1 — revisión normativa/jurídica/privacidad/seguridad;
13. QA.1 — auditoría integral de cierre beta;
14. REL.1 — preparación de la primera versión oficial.

## 5. Persistencia e informes

Fase futura:

- SQLite o mecanismo equivalente solo si existe una necesidad aprobada;
- guardado voluntario;
- versionado/migración de esquema;
- importación/exportación controlada;
- informes PDF;
- separación configurable de identificadores personales;
- inclusión de versión de aplicación/metodología en salidas auditables.

Cualquier persistencia modifica el análisis de privacidad y exige revisión antes de implementarse.

## 6. Normativa y motores

Trabajo continuo:

- revalidar parámetros que cambien oficialmente;
- mantener historial de valores normativos por fecha;
- incorporar regímenes especiales únicamente con fuente y pruebas propias;
- no reconstruir saldos/bonos actuariales sin fuente suficiente;
- mantener visibles las limitaciones del modelo.

## 7. Accesibilidad y calidad

Antes de una publicación oficial amplia de la aplicación:

- auditoría WCAG 2.2 más completa;
- pruebas con lector de pantalla;
- matriz real de dispositivos/navegadores;
- revisión de alto contraste y colores forzados;
- pruebas de teclado completas;
- revisión de exportaciones e informes accesibles.

## 8. Criterio para primera versión oficial

La primera versión oficial objetivo será:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

Solo podrá materializarse cuando:

- [x] GOV.1 esté cerrado;
- [x] exista una licencia decidida para la etapa actual;
- [x] seguridad y privacidad tengan procedimientos internos base;
- [x] repositorio, metadata, identidad y controles de seguridad pública básicos estén configurados;
- [x] UX.4.6e esté cerrado;
- [x] PLAN.1 esté cerrado;
- [x] UX.4.6f–UX.4.6i estén cerrados;
- [ ] VER.2 esté cerrado como prerrequisito transversal para continuar el ledger revision-aware;
- [ ] DEV.2 esté cerrado;
- [ ] SEC.2 esté cerrado;
- [ ] DOC.2 esté cerrado;
- [ ] PERSIST.1 esté cerrado si forma parte del alcance 1.0;
- [ ] REP.1 esté cerrado si forma parte del alcance 1.0;
- [ ] A11Y.2 esté cerrado;
- [ ] REV.1 esté cerrado;
- [ ] QA.1 esté cerrado;
- [ ] REL.1 complete build reproducible, hashes, firma, documentación y empaquetado;
- [ ] se decida expresamente el alcance definitivo de `1.0.0.0`.

Los estados nuevos durante beta usan la familia revision-aware `0.GG.RR.EE-beta`. La familia legacy `0.0.N-beta` permanece como historia publicada y no se extiende después de VER.2. No existe una familia futura vigente `0.1.0-beta.1`.

La visibilidad pública del repositorio no cambia la etapa funcional ni convierte una beta de desarrollo en versión oficial.

<!-- ANCLAS_HISTORICAS_VER2_ROADMAP_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

Estas referencias preservan contratos documentales de regresión histórica sin reabrir funcionalidades cerradas ni convertir referencias legacy en estado vigente.

**Versión de aplicación:** `0.0.26-beta`

- [x] **GOV.1.5 — Seguridad, privacidad y transparencia**
- [x] **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**
- [x] **Prebloque transversal — Firma e integridad Git/GitHub**
- [x] primer commit nuevo firmado y verificado por GitHub;
- [x] materialización firmada de `v0.0.1-beta` a `v0.0.21-beta`;
- [x] reemisión firmada única de `v0.0.22-beta` y `v0.0.23-beta`;
- [x] auditoría local/remota 23/23 tags;
- [x] ruleset de tags;
- [x] protección/ruleset de `main`;
- [x] revisión de configuración GitHub y PR de Dependabot.
- revisión jurídica externa preservada como requisito externo pendiente.
- checkpoint pre-R8 — identidad visual oficial.
- [x] R5 — coherencia GOV.
- [x] R6 — renumeración/metadata.
- [x] R6 — documentación transversal.
- R6 — renumeración/metadata; 586 pruebas.
- R6 cerrada con 586 pruebas en `OK`.
- [x] R7 — auditoría transversal; 598 pruebas.
- R7 — regresiones y auditoría.
- [x] R8 — prueba funcional.
- [x] R9 — cierre técnico y publicación del hito;
- R9 queda en cierre documental y formal de UX.4.6e.
- [x] R9.1 — candidato local `0.0.25-beta` validado con 660 pruebas en `OK`
- [x] R9.2 — PR #21 integrado por squash.
- UX.4.6e R9.2 cerró la versión formal `0.0.25-beta`.
- UX.4.6e queda descongelada después del cierre de GOV.1 y continúa su secuencia histórica hasta `0.0.25-beta`.
- R4.1 — candidato local `0.0.26-beta`.
- R4.2 — PR #23/#24 preservan el cierre de PLAN.1 y el tag `v0.0.26-beta`.
- UX.4.6i cerró la guía pública `/como-se-calcula` con **841 pruebas**.

## 4. PLAN.1 y secuencia hacia 1.0

Esta referencia conserva el encabezado histórico esperado por las regresiones de PLAN.1, aunque VER.2 reordene el resumen vigente.
