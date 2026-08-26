# Roadmap

**Estado:** vigente
**Versión vigente:** `0.1.11.01-beta` — G111/E01 aceptado para DOC.2
**Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
**Último tag formal legacy:** `v0.0.26-beta`
**Fecha de revisión:** 2026-08-25
**Estado actual:** SEC.2, AUD.SEC2 R1 y REL.GOV.1 están cerrados. DOC.2 R1 quedó aceptado mediante PR #87 y merge `1041b59`; G111/E01 se materializa como `0.1.11.01-beta` y G112/E07 (`0.1.12.07-beta`) queda reservado para NOR.1 R8 antes de PERSIST.1.


<!-- NOR1-R7-CLOSURE:START -->
## Estado NOR.1 / NOR.2

NOR.1 quedó cerrado en R7 después de consolidar los estándares de
estructura, nombres, documentación, archivos, evidencias, raíz y artefactos
locales.

La secuencia operativa previa a SEC.2 queda:

1. **NOR.1** — definición y auditoría preparatoria — cerrado en R7;
2. **NOR.2** — normalización integral del repositorio — cerrado en R8 mediante PR #74;
3. **SEC.2** — hardening integral — cerrado después de R1–R6;
4. **AUD.SEC2 R1** — saneamiento post-cierre y reconciliación revision-aware — cerrado/aceptado como G109/E01 mediante PR #83;
5. **REL.GOV.1** — preflight transversal de gobierno de Releases; cerrado/aceptado como G110/E01 mediante PR #85; no agrega un bloque funcional al plan de 14 bloques.
6. **DOC.2** — cerrado en R1; reconstrucción auditable del CHANGELOG `0.0.1-beta`–`0.0.21-beta`, aceptada como G111/E01 mediante PR #87.
7. **NOR.1 R8** — candidato transversal de gobierno de identificadores; reserva G112/E07 sin añadir un bloque funcional al plan.

NOR.2 ejecutó los movimientos, renombrados, consolidaciones y retiros que
NOR.1 deliberadamente no realizó.
<!-- NOR1-R7-CLOSURE:END -->


<!-- NOR2-R1-BASELINE:START -->
## Registro histórico NOR.2 R1 — línea base de normalización

En ese checkpoint, NOR.2 estaba activo y R1 auditaba el árbol versionado contra los estándares de NOR.1
sin ejecutar todavía renombres ni movimientos. El resultado alimentará una
matriz de migración por impacto antes de modificar rutas críticas.

SEC.2 quedó cerrado tras completar sus controles planificados durante NOR.2.
<!-- NOR2-R1-BASELINE:END -->


<!-- NOR2-R2-MATRIX:START -->
## Registro histórico NOR.2 R2 — matriz de migración

En ese checkpoint, R2 clasificaba los hallazgos de R1 y fija el orden R3–R8. El árbol operativo
quedará con rutas y documentación vigentes; Git y `docs/archive/` preservarán
la historia cuando corresponda. `README.md` se corrige desde R2 y se vuelve a
auditar en el cierre.

SEC.2 quedó cerrado tras completar sus controles planificados.
<!-- NOR2-R2-MATRIX:END -->


<!-- NOR2-R3-RUNTIME:START -->
## Registro histórico NOR.2 R3 — migración técnica

En ese checkpoint, R3 ejecutaba los movimientos de runtime/configuración aprobados en R2 y actualiza
imports, plantillas, assets y pruebas de manera atómica. Las URL públicas
permanecen estables. R4 normalizará la documentación viva.

SEC.2 quedó cerrado tras completar sus controles planificados.
<!-- NOR2-R3-RUNTIME:END -->

<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

MANT.1 quedó cerrado operativamente en R7 mediante PR #55 y commit squash `57078f2`.

Estado vigente:

- VER.2 promovió `0.0.71.01-beta` bajo la denominación original G071/E01; la reconciliación posterior sitúa ese estado en G087/E01.
- `v0.0.26-beta` permanece como tag legacy histórico e inmutable; el tag formal publicado de VER.2 es `v0.0.71.01-beta`.
- `v0.0.71.01-beta` permanece como tag histórico inmutable; fue publicado originalmente como G071/E01 y reconciliado posteriormente como G087/E01.
- MANT.1 queda cerrado después de R5H, R6 y R7.
- DOC.1 R1 está cerrado; DOC.1 R2 cierra la auditoría integral Markdown post-NOR.2, retira stubs documentales residuales y establece controles permanentes de regresión.
- La primera versión oficial objetivo sigue siendo `1.0.0.0` con `Build 000001`, sujeta a los gates del plan maestro.
<!-- DOC1-R1-POST-MANT1:END -->

Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md`, `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/governance/pre-1-0-revision-ledger.md`, `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/pre-1-0-revision-ledger.json` y `docs/archive/`.

VER.2 es un bloque transversal de reconciliación y **no añade un bloque 15** al plan maestro de producto. DEV.2 ya quedó cerrado documentalmente en R4. MANT.1 se trata como checkpoint técnico de mantenibilidad antes de SEC.2 y tampoco añade un bloque funcional de producto. MANT.1 R1 queda como auditoría inicial de alcance, MANT.1 R2 conserva la documentación de scripts y hooks antes de SEC.2, MANT.1 R3 documenta los YAML de GitHub sin cambiar CI ni formularios y MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica permanezca en documentación, MANT.1 R5A comenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla de la guía pública, MANT.1 R5C comenta JavaScript complejo sin cambiar lógica visible y MANT.1 R5D define política/plantillas por extensión con uniformidad de encabezados.

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
- DEV.2 — Centro de desarrollo sobre Developer Diagnostics cerrado documentalmente en R4;
- NOR.2 — normalización integral del repositorio cerrada en R8 mediante PR #74.

### Pendiente o incompleto

- persistencia voluntaria si permanece dentro del alcance 1.0;
- informes PDF y exportación final seleccionable;
- auditoría WCAG 2.2 ampliada con tecnologías de apoyo/dispositivos;
- revisión normativa/jurídica externa prevista;
- parámetros oficiales que la documentación identifica como no disponibles o no reconstruibles con fidelidad.

## 3. UX.4.6 — trabajo funcional cerrado

**Estado:** UX.4.6e y UX.4.6f–UX.4.6i cerrados. VER.2 ya reconcilió su representación en la historia y permanece cerrado; no reabre sus funcionalidades.

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

**VER.2:** bloque transversal cerrado. La primera promoción se publicó como `0.0.71.01-beta`; AUD.SEC2 R1 documenta que el ledger usado entonces terminaba en G070 y que la reconstrucción completa sitúa ese estado en G087 sin modificar el tag inmutable.

**Checkpoint técnico actual:** G111/E01 (`0.1.11.01-beta`) está aceptado después de DOC.2 R1 / PR #87 y revalidación post-merge; G112/E07 (`0.1.12.07-beta`) queda reservado para NOR.1 R8 antes de PERSIST.1.

Documentos canónicos de VER.2:

- `AUDITORIA_VERSIONADO_PRE_1_0.md` — criterio contable y exclusiones;
- `pre-1-0-revision-ledger.md` — ledger reconciliado G001–G111 y siguiente Global G112;
- `MATRIZ_DECISION_REVISIONES_VER2.md` — justificación de la segunda pasada;
- `../data/pre-1-0-revision-ledger.json` — ledger estructurado validable;
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
- [x] VER.2 esté cerrado como prerrequisito transversal para continuar el ledger revision-aware;
- [x] DEV.2 esté cerrado;
- [x] NOR.1 y NOR.2 estén cerrados como normalización previa a SEC.2;
- [x] SEC.2 esté cerrado;
- [x] DOC.2 esté cerrado;
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

**Versión de aplicación:** `0.0.71.01-beta`

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


## NOR.2 R4 — documentación viva canónica

R4 migra 41 documentos vivos y consolida 2 estándares heredados dentro de la estructura documental canónica. R5 tratará exclusivamente auditorías, cierres y evidencia histórica aún ubicada en la raíz de `docs/`. SEC.2 quedó cerrado tras completar sus controles planificados.

## NOR.2 R5 — archivo y consolidación histórica

**Estado:** activo.

R5 retira de la raíz de `docs/` los 36 documentos cerrados clasificados por R2
y los conserva en `docs/archive/` sin reescribir su contenido histórico. R6
queda como siguiente revisión de NOR.2.


<!-- NOR2-R6-LEDGER:START -->
## NOR.2 R6 — ledger y datos de alto impacto

R5 queda cerrado después de integrar el archivo histórico en PR #71.

R6 normaliza el ledger machine-readable a
`data/pre-1-0-revision-ledger.json` sin modificar su contenido, numeración,
esquema ni versión de aplicación.

Gate local observado:

- **977 pruebas — OK**;
- **0 referencias obsoletas no justificadas**;
- integridad SHA-256 preservada;
- G001–G070 preservados;
- `VERSION` permanece en `0.0.71.01-beta`.

R6 quedó integrado en `main` mediante PR #72 y commit squash `365ba5b`.

La revisión activa pasa a **NOR.2 R7 — artefactos locales**.
<!-- NOR2-R6-LEDGER:END -->


<!-- NOR2-R7-LOCAL-ARTIFACTS:START -->
## NOR.2 R7 — artefactos locales

R7 resuelve la excepción transitoria `_entregas/` identificada durante la
normalización del repositorio.

La línea base auditada fue:

- **29 archivos**;
- **9,874,828 bytes**;
- **20 `.txt`**;
- **8 `.patch`**;
- **1 `.zip`**.

La depuración local produjo:

- **20 evidencias únicas conservadas** en `_deliverables/`;
- **2** evidencias bajo `_deliverables/dev2/`;
- **18** evidencias bajo `_deliverables/ver2-r2/`;
- **8 duplicados SHA-256 exactos retirados**;
- **1 ZIP de 8,412,675 bytes retirado** después de demostrarse completamente
  reproducible desde Git;
- `_entregas/` retirado como ubicación local activa;
- `_deliverables/` mantenido fuera del árbol Git canónico.

El ZIP retirado fue comparado contra el commit
`929628df38d4750fb103ffc79bdb81f8405535bb`: los **329 archivos** coincidieron
sin faltantes, extras ni diferencias de contenido.

R7 permanece activo hasta su integración en `main`.

Después continúa **NOR.2 R8 — auditoría integral y cierre formal de NOR.2**.
SEC.2 quedó cerrado tras completar sus controles planificados hasta completar dicho cierre.
<!-- NOR2-R7-LOCAL-ARTIFACTS:END -->


<!-- NOR2-R8-FINAL-AUDIT:START -->
## NOR.2 R8 — auditoría integral y cierre formal

NOR.2 R7 quedó integrado mediante PR #73 y commit squash `b8ffd39`.

R8 re-audita el resultado completo de R3–R7 contra los estándares de NOR.1.

El gate local confirmó:

- estructura raíz canónica;
- `docs/` raíz reducido a `README.md`;
- retiro de dos fragmentos transitorios heredados;
- `_entregas/` inexistente;
- `_deliverables/` con 20 evidencias locales y 0 archivos trackeados;
- 115 decisiones R2 re-auditadas sin incumplimientos reales;
- 0 consumidores operativos vivos de rutas retiradas;
- 11 contradicciones de estado vivo corregidas hasta dejar 0;
- `VERSION` y `APP_VERSION` en `0.0.71.01-beta`;
- ledger G001–G070 preservado;
- regresión específica R8 y suite NOR.2 en `OK`.

El gate integral local de R8 quedó completado y la CI remota pasó en verde después de hacer reproducible el guard de artefactos locales.

R8 quedó integrado mediante PR #74 y commit squash `b4df9b7`. Esa frase describe el checkpoint histórico previo al inicio de SEC.2; el estado vigente es que **SEC.2 cerró después de R1–R6** y AUD.SEC2 R1 ejecuta el saneamiento post-cierre.
<!-- NOR2-R8-FINAL-AUDIT:END -->


**SEC.2 R6 cerrado:** hardening de sesión administrativa web y preparación para HTTPS interno completados.

## AUD.SEC2 R1 — saneamiento post-cierre

**Estado:** cerrado; G109 consumido por aceptación de PR #83 y merge `ec1842d`.

Alcance:

- corregir el kill switch y el contrato de sesión administrativa;
- auditar individualmente los 140 Markdown del snapshot `4bd7d8d`;
- reconciliar el ledger desde G070 hasta G108;
- preservar `v0.0.71.01-beta` como anomalía histórica inmutable;
- aceptar G109/E01 (`0.1.09.01-beta`) mediante PR #83 y sincronizar `VERSION` post-merge;
- reservar G110/E01 (`0.1.10.01-beta`) para REL.GOV.1 antes de DOC.2;
- habilitar DOC.2 únicamente después de gate, PR/CI y merge.

## REL.GOV.1 — gobierno de GitHub Releases

**Estado:** cerrado; G110/E01 (`0.1.10.01-beta`) consumido por aceptación de PR #85 y merge `5cd1cea`.

Alcance:

- corregir referencias vivas que aún interpretaban `v0.0.71.01-beta` como G071/E01 sin explicar su reconciliación G087/E01;
- estandarizar título, secciones, prerelease/estable y evidencia de cada GitHub Release futuro;
- exigir que todo tag formal nuevo posterior a esta política tenga GitHub Release asociado;
- no crear Releases retroactivos para estados que nunca tuvieron tag formal;
- añadir `.github/release.yml` para categorización asistida;
- añadir `scripts/release_contract.py` para validar VERSION/ledger/tag/título/notas;
- extender la verificación de tags para ejecutar el contrato local en tags futuros;
- preservar los dos Releases existentes y sus tags sin reescribir historia criptográfica.

Cierre confirmado: gate local completo, commit firmado, PR #85, CI Python 3.13/3.14 + Markdown/gobernanza en `success` e integración `5cd1cea`. La promoción post-merge materializa G110 sin consumir G111; DOC.2 continúa con G111/E01 (`0.1.11.01-beta`).

## DOC.2 — CHANGELOG histórico detallado

**Estado:** R1 en ejecución; candidato reservado G111/E01 (`0.1.11.01-beta`), todavía no consumido.

R1 materializa la reconstrucción exigida por el plan:

- 21 estados retrospectivos `0.0.1-beta`–`0.0.21-beta`;
- 80 commits reales, contiguos y únicos;
- rango Git, fecha, hito y sujetos de commit preservados por versión;
- evidencia machine-readable en `data/doc2-legacy-changelog-evidence.json`;
- auditoría en `docs/audits/documentation/changelog-reconstruction-doc2-r1.md`;
- regresiones para impedir que el CHANGELOG vuelva a degradarse a resúmenes de una sola línea;
- sincronización del estado real de G110 y del inventario **29 tags ↔ 29 GitHub Releases**.

R1 solo podrá cerrar DOC.2 y consumir G111 después de gate completo, commit firmado, PR/CI, merge y revalidación.
