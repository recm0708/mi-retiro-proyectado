# Roadmap

**Estado:** vigente
**Versión de aplicación:** `0.0.26-beta`
**Fecha de revisión:** 2026-08-21

Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md` y `docs/historico/`.

## 1. Programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta

**Estado general:** cerrado el 2026-08-18.
**Decisión de cierre:** como formulación histórica del cierre GOV.1, **UX.4.6e queda descongelada**; posteriormente fue cerrada en `0.0.25-beta`.

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
  - [x] diagnóstico documental;
  - [x] R1 — documentos de entrada, archivo histórico y estructura;
  - [x] R2 — documentación técnica vigente;
  - [x] R3 — normativa, seguridad y privacidad documental;
  - [x] R4 — capa de auditoría documental y controles de consistencia;
  - versión de cierre: `0.0.23-beta`.

- [x] **Prebloque transversal — Firma e integridad Git/GitHub**
  - [x] respaldo completo previo a la migración;
  - [x] clave SSH Ed25519 dedicada y verificación local;
  - [x] política de firma, allowed signers, ADR y workflow preparados;
  - [x] primer commit nuevo firmado y verificado por GitHub;
  - [x] materialización firmada de `v0.0.1-beta` a `v0.0.21-beta`;
  - [x] reemisión firmada única de `v0.0.22-beta` y `v0.0.23-beta`;
  - [x] auditoría local/remota 23/23 tags;
  - [x] ruleset de tags;
  - [x] protección/ruleset de `main`;
  - [x] revisión de configuración GitHub y PR de Dependabot.

- [x] **GOV.1.4 — Observabilidad y Developer Diagnostics**
  - [x] modo exclusivo de desarrollo;
  - [x] logging estructurado;
  - [x] niveles y categorías;
  - [x] correlación de operaciones;
  - [x] registro de errores, conexiones e hitos técnicos sin duplicar cálculos;
  - [x] redacción y prohibición de datos sensibles;
  - [x] rotación/retención local;
  - [x] exportación diagnóstica controlada;
  - [x] documentación de esquema y operación;
  - [x] 13 regresiones específicas y suite completa de 487 pruebas en `OK`.

- [x] **GOV.1.5 — Seguridad, privacidad y transparencia**
  - [x] threat model;
  - [x] procedimiento de incidentes;
  - [x] procedimiento de derechos del titular;
  - [x] revisión de logs y datos sensibles;
  - [x] terceros y recursos externos;
  - [x] criterios TLS/despliegue;
  - [x] gate y paquete documental para revisión jurídica externa previa a publicación.

- [x] **GOV.1.6 — Controles GitHub y auditoría automática**
  - [x] plantillas estructuradas de issues y Pull Request;
  - [x] `SECURITY.md`;
  - [x] controles documentales de repositorio;
  - [x] workflow adicional `Auditoría de gobernanza`;
  - [x] política de rama/revisión documentada y compatible con la etapa del proyecto;
  - [x] `Auditoría de gobernanza` promovido al conjunto de checks requeridos junto con Python 3.13/3.14.

- [x] **GOV.1.7 — Licencia**
  - [x] objetivo de distribución evaluado;
  - [x] compatibilidad de dependencias directas revisada;
  - [x] derechos de terceros separados del código original;
  - [x] seleccionada licencia propietaria pre-beta / todos los derechos reservados;
  - [x] añadidos `LICENSE`, `THIRD_PARTY_NOTICES.md` y gates de distribución;
  - [x] futura relicencia abierta reservada a una decisión expresa del titular.

- [x] **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**
  - [x] revisión integral de GOV.1.1–GOV.1.7;
  - [x] coherencia código/pruebas/documentación;
  - [x] versión formal de cierre `0.0.24-beta`;
  - [x] tag anotado y firmado `v0.0.24-beta` creado después de merge, validación post-merge y CI verde;
  - [x] auditoría de GitHub con `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`;
  - [x] decisión de reanudar UX.4.6e;
  - [x] gates de publicación preservados sin declarar una versión oficial lista.

## 2. Estado funcional del producto

### Implementado

- asistente de seis pasos;
- Paso 4 — proyección salarial/laboral auditado y cerrado en UX.4.6f;
- Paso 5 — escenarios de retiro auditado y cerrado en UX.4.6g;
- Paso 6 — resultados y exportación auditado y cerrado en UX.4.6h; incluye copia imprimible A4 provisional y reserva el PDF formal para REP.1;
- motores SEBD, Mixto y SUCGS para el alcance general documentado;
- comparación de escenarios;
- trazabilidad de cálculo;
- metodología y fuentes;
- resultado transversal;
- importación revisable de Mi Retiro Seguro;
- importación revisable de Ficha Digital;
- procedencia editable con fotografía documental original, copia de trabajo y exclusión explícita de períodos;
- gestión local de datos de simulación;
- temas Claro, Oscuro, Automático y Alto contraste;
- base responsive y accesible;
- identidad visual oficial, favicons y Social Preview propios;
- repositorio público con metadata, 20/20 topics, 21 labels e Issue Forms;
- Dependency graph, Dependabot, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting;
- CI y auditoría automática de gobernanza.

### Pendiente o incompleto

- sección pública «Cómo se calcula» para SEBD, Mixto y SUCGS;
- Centro de desarrollo sobre Developer Diagnostics;
- hardening integral;
- reconstrucción detallada del CHANGELOG `0.0.1-beta`–`0.0.21-beta`;
- persistencia voluntaria;
- informes PDF;
- exportación final seleccionable;
- auditoría WCAG 2.2 ampliada con tecnologías de apoyo/dispositivos;
- revisión jurídica externa previa a la primera versión oficial;
- revisión jurídica externa de estrategia de publicación/licencia;
- parámetros oficiales que la documentación identifica como no disponibles o no reconstruibles con fidelidad.

## 3. UX.4.6 — trabajo funcional

**Estado:** UX.4.6e, PLAN.1, UX.4.6f, UX.4.6g y UX.4.6h cerrados; UX.4.6i — Cómo se calcula es el bloque funcional activo.

- [x] **UX.4.6e — Estandarización técnica, comentarios y coherencia de interfaz post-GOV.1**
  - [x] R1 — auditoría integral del código y definición del patrón documental por tecnología;
  - [x] R2 — normalización Python/tests y corrección de precisión detectada durante la auditoría; 550 pruebas en `OK`;
  - [x] R3 — normalización JavaScript y cambio definitivo de almacenamiento a `miRetiroProyectado.*`; 558 pruebas en `OK`;
  - [x] R4 — normalización Python restante, HTML/Jinja/CSS y pruebas históricas sin alterar contratos funcionales ni la cascada; 566 pruebas en `OK`;
  - [x] R5 — coherencia GOV → interfaz visible y preparación pública del repositorio; 576 pruebas en `OK`;
  - [x] R6 — documentación transversal y normalización definitiva de la secuencia UX.4.6; 586 pruebas en `OK`;
  - [x] R7 — regresiones y auditoría de coherencia código/interfaz/documentación; 598 pruebas en `OK`;
  - [x] checkpoint pre-R8 — identidad visual oficial, favicon, Social Preview, visibilidad pública y revalidación de seguridad GitHub; 624 pruebas en `OK`;
  - [x] R8 — prueba funcional manual y automática completa hasta Paso 3; reconsentimiento, procedencia editable y exclusión/reinclusión documental validados; R8.2 cerró con 644 pruebas en `OK`;
  - [x] R9 — cierre técnico y publicación del hito;
    - [x] R9.1 — candidato local `0.0.25-beta` validado con 660 pruebas en `OK`, documentación coherente y `git diff --check` limpio;
    - [x] R9.2 — PR #21 integrado por squash; PR #22 completó el cierre documental; `main` final `7affa00e2530aeede066c10ecfee8c6dbd49b10b`; tag firmado `v0.0.25-beta`.
- [x] **UX.4.6f — Paso 4 · Proyección salarial/laboral**
  - [x] R1 — consistencia transversal de procedencia, decisiones explícitas y procesamiento accesible de adjuntos; gate automático 734/734 superado.
  - [x] R1.1 — bloqueo documental en vista principal, franja visual de solo lectura, iconos semánticos y selección explícita de disponibilidad del historial; R1 + R1.1 integradas por PR #28 tras **743/743 pruebas en `OK`** y validación visual manual.
  - [x] R2 — auditoría lógica, matemática, casos reales y trazabilidad del Paso 4; PR #30 integrado por squash en `9634ae4b1a0a07cc14682d315b6cdb9c1b37eb4d` tras validación manual, **756/756 pruebas en `OK`** en CI, Python 3.13/3.14 y Auditoría de gobernanza en verde.
- [x] **UX.4.6g — Paso 5 · Escenarios de retiro**
  - [x] R1 — selección contextual desde Paso 4, retiro anticipado explícito, +4 años, fechas pasadas no accionables, fecha de evaluación opcional, cobertura visible de fechas personalizadas, contrato transversal de fechas y alineación visual final; PR #32 integrado con **784 pruebas en `OK`** y CI verde.
- [x] **UX.4.6h — Paso 6 · Resultados y exportación**
  - [x] R1/R1.1 — selección salarial explícita, invalidación completa de salidas obsoletas, transición Mixto→SUCGS guiada, referencias SUCGS rotuladas y sincronización documental.
  - [x] R1.2 — claridad, jerarquía visual, comparación acreditado/proyectado, referencia personal y reducción de información redundante.
  - [x] R1.3 — informe A4 independiente para impresión; la generación/descarga directa de PDF permanece reservada a REP.1; gate de cierre **812 pruebas**.
- [ ] **UX.4.6i — Cómo se calcula**

## 4. PLAN.1 y secuencia hacia 1.0

**Último bloque transversal cerrado:** PLAN.1 — cerrado formalmente en `0.0.26-beta` con **720 pruebas en `OK`** y tag firmado `v0.0.26-beta`.

**Bloque funcional activo:** UX.4.6i — Cómo se calcula.

La secuencia completa y sus criterios se documentan en `PLAN_MAESTRO_HACIA_1_0.md`.

Estado interno de PLAN.1:

- [x] R1 — política de versionado oficial futuro, validador y plan maestro;
- [x] R2 — documentación primaria/transversal, ADR-168 y saneamiento de metadata viva;
- [x] R3 — terminología beta/oficial, privacidad/licencia y guard de referencias históricas;
- [x] R4 — auditoría final y publicación del hito;
  - [x] R4.1 — candidato local `0.0.26-beta` validado con **720 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpio;
  - [x] R4.2 — cierre remoto y tag firmado `v0.0.26-beta`:
    - [x] commit de rama firmado `7c50d989f5c6d266db26c9625367dd82e9895aba`;
    - [x] PR #23 integrado por squash;
    - [x] `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` en `success`;
    - [x] `main` integrado en `497097f720c98f6e5a7ed689cf91368011a96be1`;
    - [x] gate post-merge con **720 pruebas en `OK`**;
    - [x] corregir y revalidar sin `SyntaxWarning` la higiene pre-tag;
    - [x] crear y verificar el tag firmado `v0.0.26-beta` (`bfbb746b177ebcc577f7241fef4d6914f713739a` → `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`).

Resumen:

1. PLAN.1 — alineación maestra;
2. UX.4.6f — Paso 4;
3. UX.4.6g — Paso 5;
4. UX.4.6h — Paso 6;
5. UX.4.6i — Cómo se calcula;
6. DEV.2 — Centro de desarrollo;
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
- [ ] UX.4.6f–UX.4.6i estén cerrados;
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

La línea `0.0.N-beta` continúa durante el desarrollo. No existe una familia futura vigente `0.1.0-beta.1`.

La visibilidad pública del repositorio no cambia la etapa funcional ni convierte una beta de desarrollo en versión oficial.
