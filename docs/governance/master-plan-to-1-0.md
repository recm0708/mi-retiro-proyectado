# Plan maestro hacia Mi Retiro Proyectado 1.0

**Estado:** vigente
**Versión base al iniciar el plan:** `0.0.25-beta`
**Cierre histórico de PLAN.1:** `0.0.26-beta` / `v0.0.26-beta`
**Versión transversal vigente:** `0.1.09.01-beta` — G109/E01 aceptado y publicado
**Fecha:** 2026-08-25
**Clasificación:** Producto / Arquitectura / QA / Release


<!-- NOR1-R7-CLOSURE:START -->
## Checkpoint de normalización previo a SEC.2

NOR.1 y NOR.2 son checkpoints técnicos transversales y no agregan bloques
funcionales al plan de 14 bloques.

- **NOR.1:** cerrado en R7; estándares determinísticos establecidos.
- **NOR.2:** cerrado en R8 mediante PR #74; normalización integral completada.
- **DOC.1 R2:** auditoría integral Markdown post-NOR.2 cerrada; documentación vigente, evidencia histórica y controles permanentes quedaron reconciliados.
- **SEC.2 R1–R6:** cerrados; hardening CodeQL, autenticación/protección administrativa, auditoría, sesión web y hardening de sesión completados. AUD.SEC2 R1 quedó aceptado/publicado como G109/E01. Antes de DOC.2 se ejecuta REL.GOV.1 como preflight transversal de gobierno de GitHub Releases.

La separación evita que SEC.2 cree nuevas rutas, archivos o estructuras sobre
una base cuya nomenclatura y documentación no hayan sido normalizadas.
<!-- NOR1-R7-CLOSURE:END -->


<!-- NOR2-R1-STATUS:START -->
## Registro histórico de NOR.2 R1

En ese checkpoint, NOR.2 se encontraba activo en R1. Esta revisión establece la línea base; las
migraciones reales se ejecutarán en revisiones posteriores según una matriz de
impacto. NOR.2 sigue siendo un checkpoint transversal y no agrega un bloque
funcional al plan de 14 bloques.
<!-- NOR2-R1-STATUS:END -->


<!-- NOR2-R2-STATUS:START -->
## Registro histórico NOR.2 R2 — decisión de migración

En ese checkpoint, R2 convierte la línea base en un plan R3–R8 y adopta como gate de cierre la
sincronización completa de README, índice documental, roadmap, plan maestro,
validación, arquitectura, enlaces, imports y estado de fases.

La historia se conserva mediante Git y archivo justificado; el árbol vigente no
mantendrá copias sustituidas únicamente por compatibilidad documental.
<!-- NOR2-R2-STATUS:END -->


<!-- NOR2-R3-STATUS:START -->
## Registro histórico NOR.2 R3 — runtime/configuración

En ese checkpoint, R3 materializa la normalización técnica de bajo/medio impacto aprobada por R2.
La siguiente revisión R4 debía migrar la documentación viva y sus enlaces hacia la
estructura canónica. SEC.2 estaba pausado en ese momento; posteriormente cerró R1–R6.
<!-- NOR2-R3-STATUS:END -->

<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

El plan maestro se interpreta desde la línea base documental posterior a MANT.1 R7.

Estado vigente:

- VER.2 promovió `0.0.71.01-beta` bajo la denominación original G071/E01; la reconciliación posterior sitúa ese estado en G087/E01.
- `v0.0.26-beta` permanece como tag legacy histórico e inmutable; VER.2 publicó formalmente `v0.0.71.01-beta`.
- VER.2 está cerrado; `v0.0.71.01-beta` fue publicado originalmente como G071/E01 y reconciliado posteriormente como G087/E01 sin mover el tag.
- MANT.1 está cerrado operativamente.
- DOC.1 R1 está cerrado.
- DOC.1 R2 queda cerrado como auditoría integral Markdown post-NOR.2, con controles locales y remotos permanentes.
- NOR.1 y NOR.2 están cerrados; R8 quedó integrado mediante PR #74.
- SEC.2 quedó cerrado después de R1–R6; AUD.SEC2 R1 fue publicado como G109/E01. REL.GOV.1 es el checkpoint transversal actual previo a DOC.2.
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
- `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`;
- `docs/governance/pre-1-0-revision-ledger.md`;
- `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`;
- `data/pre-1-0-revision-ledger.json`;
- ADR de gobierno correspondiente.

Durante VER.2, DOC.1 R1 fue el bloque documental utilizado para sincronizar la documentación Markdown vigente posterior a MANT.1. Después de NOR.2, DOC.1 R2 ejecutó la auditoría integral Markdown y estableció controles permanentes de regresión. VER.2, DOC.1 R1 y DOC.1 R2 están cerrados, y DEV.2 permanece como bloque funcional cerrado.

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

**Estado:** cerrado documentalmente en R4.

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

**Estado:** cerrado después de completar R1-R6.

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

#### Checkpoint transversal REL.GOV.1 — Gobierno de GitHub Releases

**Estado:** candidato G110/E01 (`0.1.10.01-beta`); no añade un bloque funcional al programa de 14 bloques.

Objetivo previo a DOC.2:

- normalizar la interpretación viva de `v0.0.71.01-beta` como G087/E01 sin alterar su tag histórico;
- exigir un formato canónico para títulos y cuerpos de GitHub Release;
- distinguir de forma determinística prerelease beta y release estable;
- prohibir Releases retroactivos para estados aceptados que nunca tuvieron tag;
- configurar `.github/release.yml` para categorización asistida;
- validar VERSION, ledger y tag con `scripts/release_contract.py`;
- extender el workflow de tags para ejecutar el contrato en todo tag futuro;
- fijar reglas de edición posterior que preserven firma, commit objetivo y evidencia histórica.

Si REL.GOV.1 supera gate, PR/CI e integración, consumirá G110. DOC.2 continuará entonces con G111/E01 (`0.1.11.01-beta`).

### 8. DOC.2 — CHANGELOG detallado `0.0.1-beta`–`0.0.21-beta`

Reconstrucción basada exclusivamente en evidencia:

- rangos Git de `RELEASES.md`;
- commits reales;
- `docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md`;
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


## Registro histórico NOR.2 R4 — normalización documental viva

La documentación vigente queda distribuida entre `architecture/`, `decisions/`, `governance/`, `operations/`, `product/`, `regulatory/`, `security/` y `standards/`. R5 archivará o retirará del árbol vivo los documentos históricos definidos por R2.

## Registro histórico NOR.2 R5 — archivo documental histórico

NOR.2 R5 separa evidencia histórica de documentación viva mediante 36
movimientos hacia `docs/archive/`. `VERSION` no cambiaba y SEC.2 permanecía pausado
en ese checkpoint hasta completar NOR.2.


<!-- NOR2-R6-LEDGER:START -->
## Registro histórico — actualización NOR.2 R6

La normalización del ledger de alto impacto conserva como invariantes:

- `schema_version = 1`;
- 70 entradas continuas G001–G070;
- siguiente Global 71;
- candidato `0.0.71.01-beta`;
- SHA-256
  `f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e`.

El consumidor de runtime y la documentación viva utilizan
`data/pre-1-0-revision-ledger.json`.

La evidencia histórica conserva los nombres que existían cuando fue generada.
No se crean stubs ni copias de compatibilidad.

R6 quedó integrado en `main` mediante PR #72 y commit squash `365ba5b`.

R7 queda como revisión activa para resolver los artefactos locales heredados.
R8 ejecutará el cierre integral de NOR.2 antes de reanudar SEC.2.
<!-- NOR2-R6-LEDGER:END -->


<!-- NOR2-R7-LOCAL-ARTIFACTS:START -->
## Actualización NOR.2 R7

NOR.2 R7 resuelve la excepción transitoria de artefactos locales heredados bajo
`_entregas/`.

La línea base comprobada fue de **29 archivos y 9,874,828 bytes**.

La migración local conserva como invariantes:

- la evidencia local útil no se incorpora al árbol Git;
- `_deliverables/` pasa a ser la ubicación local canónica;
- **20 evidencias únicas** permanecen conservadas;
- **2** corresponden a DEV.2;
- **18** corresponden a VER.2 R2;
- **8 duplicados SHA-256 exactos** se retiran conservando una copia;
- `_entregas/` deja de existir como ubicación activa;
- `_deliverables/` y `_entregas/` permanecen ignorados por Git.

El paquete `VER2_PR35_NETO_929628d.zip`, de **8,412,675 bytes**, se retiró
únicamente después de comprobar que era completamente reproducible desde el
commit Git `929628df38d4750fb103ffc79bdb81f8405535bb`.

La comparación verificó:

- archivos Git: **329**;
- archivos ZIP: **329**;
- archivos comunes: **329**;
- solo Git: **0**;
- solo ZIP: **0**;
- diferencias de contenido: **0**.

La historia y evidencia versionada permanecen preservadas mediante Git. El
manifest detallado de los artefactos locales se mantiene fuera del repositorio.

R7 permanece activo hasta completar sus gates, PR, CI e integración en `main`.

Después de R7 solo queda **NOR.2 R8 — auditoría integral y cierre formal**.
SEC.2 quedó cerrado tras completar sus controles planificados hasta completar R8.
<!-- NOR2-R7-LOCAL-ARTIFACTS:END -->


<!-- NOR2-R8-FINAL-AUDIT:START -->
## Registro histórico — actualización NOR.2 R8

R8 constituye el gate final de normalización antes de SEC.2.

La auditoría integral confirma:

- raíz y estructura documental canónicas;
- ausencia de residuos técnicos de las migraciones R3–R7;
- retiro de dos artefactos transitorios directos de `docs/`;
- artefactos locales preservados fuera de Git;
- documentación viva sincronizada con VER.2 cerrado, NOR.1 cerrado,
  NOR.2 R7 cerrado y R8 cerrado;
- versión `0.0.71.01-beta` preservada;
- ledger G001–G070 preservado;
- regresiones específicas de normalización en `OK`;
- CI remota y auditoría de gobernanza en verde después de hacer reproducible el guard de artefactos locales.

R8 quedó integrado mediante PR #74 y commit squash `b4df9b7`. Con esa integración, **NOR.2 queda formalmente cerrado**.

En ese checkpoint, SEC.2 quedaba habilitado para reanudación y todavía no se había iniciado formalmente. El estado vigente posterior es su cierre R1–R6.
<!-- NOR2-R8-FINAL-AUDIT:END -->


**SEC.2 R6:** endurecimiento de sesión administrativa web y controles configurables de despliegue.

## Estado transversal vigente después de SEC.2

SEC.2 está cerrado después de R1–R6. Antes de abrir DOC.2, AUD.SEC2 R1 ejecuta
una auditoría integral post-cierre porque el snapshot `4bd7d8d` reveló una
regresión del kill switch administrativo y un ledger revision-aware incompleto.

La reconciliación preserva G001–G070, reconstruye G071–G108 y AUD.SEC2 R1 queda aceptado/publicado como G109/E01 (`0.1.09.01-beta`). G110/E01 (`0.1.10.01-beta`) se reserva para REL.GOV.1, preflight transversal de gobierno de GitHub Releases. El tag `v0.0.71.01-beta` se conserva inmutable aunque su estado corresponda cronológicamente a G087. Tras aceptar REL.GOV.1, el plan continúa con **DOC.2** usando el siguiente Global disponible.
