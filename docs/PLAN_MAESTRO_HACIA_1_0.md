# Plan maestro hacia Mi Retiro Proyectado 1.0

**Estado:** vigente
**Versión base al iniciar el plan:** `0.0.25-beta`
**Cierre histórico de PLAN.1:** `0.0.26-beta` / `v0.0.26-beta`
**Versión candidata transversal VER.2:** `0.0.71.01-beta` — G071/E01
**Fecha:** 2026-08-22
**Clasificación:** Producto / Arquitectura / QA / Release


<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

El plan maestro se interpreta desde la línea base documental posterior a MANT.1 R7.

Estado vigente:

- `VERSION` continúa en `0.0.26-beta`.
- `v0.0.26-beta` sigue siendo el tag formal vigente.
- VER.2 sigue pendiente como reconciliación revision-aware antes de cualquier promoción formal.
- MANT.1 está cerrado operativamente.
- DOC.1 R1 está activo para actualizar documentación Markdown vigente y separar evidencia histórica de estado actual.
- La meta `1.0.0.0` / `Build 000001` se mantiene condicionada al cierre de los gates definidos.

Las referencias históricas a bloques previos se conservan como trazabilidad, pero el estado operativo vigente debe leerse desde esta sección.
<!-- DOC1-R1-POST-MANT1:END -->

## 1. Propósito

Este documento ordena el trabajo desde el cierre de `v0.0.25-beta` hasta la primera versión oficial de Mi Retiro Proyectado.

PLAN.1 adoptó originalmente la familia beta legacy `0.0.N-beta`. VER.2, ejecutado después de UX.4.6i, conserva esa familia como historia publicada y adopta para **estados nuevos** el formato revision-aware:

```text
0.GG.RR.EE-beta
```

La primera versión oficial objetivo continúa siendo:

```text
1.0.0.0
Build 000001
```

No se utilizará `0.1.0-beta.1` como etapa futura vigente.

## 2. Regla transversal de sincronización

Todo cambio debe revisar de manera coordinada los artefactos que dependan de él:

```text
Código
↕
Pruebas
↕
Interfaz
↕
Normativa
↕
Modelo de datos
↕
Documentación técnica
↕
Documentación pública
↕
CHANGELOG / ROADMAP / RELEASES
↕
ADR cuando exista una decisión arquitectónica
↕
Git / versión / tag / Build cuando corresponda
```

Un archivo no se modifica de forma aislada si el cambio altera contratos descritos en otros documentos o pruebas.

Los comentarios y docstrings del runtime siguen el contrato de ADR-162: explican responsabilidades, motivos, límites y comportamiento permanente, no números cronológicos de fase.

La metadata `Versión de aplicación revisada` de un documento de dominio registra la base en la que ese documento fue revisado. No constituye una copia canónica de la versión vigente ni obliga a reescribir documentos no afectados por cada incremento de `VERSION`.

## 3. Prerrequisito transversal VER.2

VER.2 — Reconciliación revision-aware del historial pre-1.0 — **no es un bloque 15**. Es una corrección de gobierno necesaria antes de continuar el bloque 6, DEV.2.

Base auditada:

```text
main = 7037addd44253e528c77460b678d2b3ccd540dd5
G070 / E02 = cierre UX.4.6i
```

Candidato:

```text
G071 / E01 = 0.0.71.01-beta
```

G071 solo se considera aceptado después de gate completo, PR/CI e integración. Un candidato fallido no consume el número.

Fuentes canónicas:

- `VERSIONING.md`;
- `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`;
- `docs/LEDGER_REVISIONES_PRE_1_0.md`;
- `docs/MATRIZ_DECISION_REVISIONES_VER2.md`;
- `data/revision_ledger_pre_1_0.json`;
- ADR de gobierno correspondiente.

Mientras VER.2 permanezca abierto, **DOC.1 R1 es el bloque documental activo** para sincronizar la documentación Markdown vigente posterior a MANT.1; DEV.2 queda preservado como bloque funcional cerrado.

## 4. Secuencia de 14 bloques

### 1. PLAN.1 — Alineación maestra post-`0.0.25-beta`

Objetivo original:

- sustituir el objetivo futuro `0.1.0-beta.1` por `1.0.0.0`;
- adoptar versión oficial de cuatro componentes;
- definir Build oficial de seis dígitos;
- preparar el validador de `VERSION`;
- registrar la decisión en ADR;
- alinear documentación vigente y regresiones;
- preservar sin reescritura la documentación histórica.

**Estado de PLAN.1:** cerrado. R4.2 integró PR #23 y PR #24, superó los checks remotos, revalidó `main` con **720 pruebas en `OK`** sin `SyntaxWarning` y publicó el tag firmado `v0.0.26-beta` (`bfbb746b177ebcc577f7241fef4d6914f713739a` → `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`).

Revisiones internas preservadas:

- **R1:** política, soporte técnico futuro, plan maestro y regresiones base;
- **R2A/R2B1/R2B2/R2C:** alineación documental progresiva;
- **R3A/R3B1/R3B2:** release, terminología, seguridad, privacidad/licencia y guard histórico;
- **R4.1:** candidato local `0.0.26-beta`;
- **R4.2:** commit/PR/CI, corrección de higiene, validación y tag firmado.

### 2. UX.4.6f — Paso 4 · Proyección salarial/laboral

**Estado:** cerrado.

- **R1/R1.1 aceptadas conjuntamente:** PR #28, validación manual y **743 pruebas**;
- **mantenimiento técnico post-R1:** PR #29, actualización coordinada de `pypdf`/`uvicorn`, mismo gate funcional y estado técnico aceptado independiente;
- **R2 cerrada:** PR #30, validación manual y **756 pruebas**;
- **cierre/hardening final:** PR #31, gate `pre-commit` y **762 pruebas**;
- lógica y precisión de las cuatro modalidades salariales auditadas;
- separación de información acreditada, datos reales recientes y proyección;
- trazabilidad hacia Pasos 5 y 6.

### 3. UX.4.6g — Paso 5 · Escenarios de retiro

**Estado:** cerrado mediante PR #32 con **784 pruebas en `OK`**.

Incluye:

- escenarios de edad/fecha;
- continuación de cotización;
- cuotas adicionales;
- selección explícita/contextual del escenario;
- retiro anticipado explícito;
- cobertura por horizonte del Paso 4;
- validación transversal de fechas;
- coherencia con los tres sistemas.

Los refinamientos R1.2/R1.3/R1.4/R1.4.2/R1.4.3 permanecen documentados como evolución interna del cierre y no se reinterpretan como tags separados.

### 4. UX.4.6h — Paso 6 · Resultados y exportación

**Estado:** cerrado mediante PR #33 con **812 pruebas**.

- R1 fue un primer candidato y falló tres regresiones de gobierno/documentación; no consume revisión global aceptada;
- R1.1 corrigió el candidato y constituye el primer estado aceptado del bloque;
- R1.2 fue aceptada visualmente y depuró claridad/jerarquía;
- R1.3 creó el informe A4 imprimible independiente y cerró el bloque.

El cierre incorpora selección salarial explícita, invalidación de resultados obsoletos, transición Mixto→SUCGS guiada, presentación depurada, comparación, trazabilidad, fuentes y advertencias. La generación/descarga directa de PDF permanece reservada a REP.1.

### 5. UX.4.6i — Cómo se calcula

**Estado:** cerrado mediante PR #34 con **841 pruebas**.

La secuencia demostrada por la auditoría canónica es:

- **R1:** ruta pública, procedimientos SEBD/Mixto/SUCGS, parámetros y fuentes; estado aceptado G069;
- **R1.2:** navegación, recorrido Pasos 1–6, formato monetario y densidad de tablas; refinamiento interno sin aceptación independiente recuperada;
- **R1.3:** ejemplos sustituidos, terminología contextual y espaciado; refinamiento interno sin aceptación independiente recuperada;
- **R1.4:** etiqueta visible **Ejemplo** y cierre aceptado G070.

No existe una sección, gate ni artefacto independiente que sustente una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2; VER.2 corrige las referencias agregadas que la incluyeron por error.

La explicación pública no duplica motores de cálculo en JavaScript y mantiene las fórmulas ejecutables en los motores Python existentes.

### 6. DEV.2 — Centro de desarrollo

**Estado:** bloque documental activo; actualización Markdown vigente post-MANT.1 en curso.

> Ancla histórica preservada por pruebas de regresión: **Estado:** siguiente bloque funcional; pendiente de inicio hasta cerrar VER.2.

Evolución visible y controlada de Developer Diagnostics:

- disponible solo en modo de desarrollo;
- autenticación administrativa local;
- estado de aplicación;
- logs estructurados;
- errores y advertencias;
- correlation ID;
- salud de componentes;
- filtros y consulta;
- autodiagnóstico;
- exportación de ZIP diagnóstico sanitizado;
- ausencia de PII y valores financieros sensibles.

### 7. SEC.2 — Hardening integral

- autenticación y sesiones administrativas;
- gestión de secretos;
- CSP;
- CORS/CSRF según superficie real;
- seguridad de archivos;
- permisos locales;
- endurecimiento del servidor;
- Bootstrap local o decisión final documentada;
- dependencias;
- SBOM/inventario;
- seguridad de persistencia;
- cifrado donde exista información persistente que lo requiera;
- evaluación de despliegue remoto si se adopta.

### 8. DOC.2 — CHANGELOG detallado `0.0.1-beta`–`0.0.21-beta`

Reconstrucción basada exclusivamente en evidencia:

- rangos Git de `RELEASES.md`;
- commits reales;
- `docs/REGISTRO_CAMBIOS_HISTORICO.md`;
- documentación histórica;
- ADR;
- pruebas disponibles.

No se inventará detalle retrospectivo no sustentado.

### 9. PERSIST.1 — Persistencia voluntaria y segura

- guardado solo por decisión del asegurado;
- modelo de datos versionado;
- migraciones;
- cifrado/protección aplicable;
- borrado;
- exportación/importación controlada;
- revisión de privacidad.

### 10. REP.1 — Informes PDF y exportaciones finales

- PDF;
- formatos seleccionables;
- versión de aplicación y metodología;
- trazabilidad;
- accesibilidad;
- metadatos mínimos;
- protección de datos.

### 11. A11Y.2 — Auditoría WCAG 2.2 ampliada

- teclado;
- lector de pantalla;
- zoom;
- alto contraste;
- colores forzados;
- navegadores;
- dispositivos;
- exportaciones;
- formularios;
- modales y navegación.

### 12. REV.1 — Revisión normativa, jurídica, privacidad y seguridad final

- fuentes oficiales;
- interpretación de los tres motores;
- parámetros;
- limitaciones;
- privacidad;
- licencia;
- terceros;
- revisión jurídica externa cuando corresponda.

### 13. QA.1 — Auditoría integral de cierre de la etapa beta

Gate transversal:

```text
Código
↔ pruebas
↔ documentación
↔ normativa
↔ UX
↔ seguridad
↔ accesibilidad
↔ release
```

Mientras este bloque no cierre, la aplicación permanece en la familia beta revision-aware `0.GG.RR.EE-beta`.

### 14. REL.1 — Preparación de la primera versión oficial

Objetivo inicial:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

Debe incluir:

- congelación funcional;
- build reproducible;
- fuente canónica de Build;
- empaquetado;
- inventario/SBOM;
- licencias y avisos;
- hashes;
- firma;
- documentación de instalación/uso/soporte;
- release notes;
- validación en entorno limpio;
- CI final;
- tag firmado;
- política de distribución.

## 5. Estado al comenzar PLAN.1

La versión base fue:

```text
0.0.25-beta
```

El tag `v0.0.25-beta` es histórico e inmutable. PLAN.1 no movió ese tag.

## 6. Criterio histórico de salida de PLAN.1

PLAN.1 quedó cerrado porque:

- las referencias vigentes dejaron de presentar `0.1.0-beta.1` como objetivo futuro;
- la documentación histórica conservó su contexto sin reescritura;
- `VERSIONING.md` y el validador Python admitieron la línea oficial futura;
- ADR-168 registró la decisión;
- ROADMAP, README, RELEASES, CHANGELOG, índice, validación y documentos dependientes quedaron sincronizados;
- compilación Python, sintaxis JavaScript, `git diff --check` y suite completa quedaron limpios;
- el cierre formal siguió commit, PR, CI, squash, revalidación y tag aplicable.

VER.2 no invalida ese cierre: corrige únicamente la granularidad y trazabilidad de la etapa beta posterior.

<!-- ANCLAS_HISTORICAS_VER2_PLAN_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

- **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico previo a PLAN.1.
- R4.1 — candidato local `0.0.26-beta`.
- R4.2 integró el cierre de PLAN.1 mediante PR protegido y preservó `v0.0.26-beta`.
- R4.2 — PR #23/#24 preservan la integración y saneamiento final de PLAN.1 antes del tag `v0.0.26-beta`.
- Después de su cierre se habilitó UX.4.6g.
