# Plan maestro hacia Mi Retiro Proyectado 1.0

**Estado:** vigente
**Versión base al iniciar el plan:** `0.0.25-beta`
**Versión candidata de cierre de PLAN.1:** `0.0.26-beta`
**Fecha:** 2026-08-19
**Clasificación:** Producto / Arquitectura / QA / Release

## 1. Propósito

Este documento ordena el trabajo restante desde el cierre de `v0.0.25-beta`
hasta la primera versión oficial de Mi Retiro Proyectado.

La etapa vigente continúa usando:

```text
0.0.N-beta
```

La primera versión oficial objetivo será:

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

Un archivo no se modifica de forma aislada si el cambio altera contratos
descritos en otros documentos o pruebas.

Los comentarios y docstrings del runtime siguen el contrato de ADR-162:
explican responsabilidades, motivos, límites y comportamiento permanente, no
números cronológicos de fase.

## 3. Secuencia de 14 bloques

### 1. PLAN.1 — Alineación maestra post-`0.0.25-beta`

Objetivo:

- sustituir el objetivo futuro `0.1.0-beta.1` por `1.0.0.0`;
- adoptar versión oficial de cuatro componentes;
- definir Build oficial de seis dígitos;
- preparar el validador de `VERSION`;
- registrar la decisión en ADR;
- alinear documentación vigente y regresiones;
- preservar sin reescritura la documentación histórica;
- mantener `0.0.N-beta` durante la etapa de desarrollo.

**Estado de PLAN.1:** cerrado. R4.2 integró PR #23 y PR #24, superó los checks remotos, revalidó `main` con **720 pruebas en `OK`** sin `SyntaxWarning` y publicó el tag firmado `v0.0.26-beta` (`bfbb746b177ebcc577f7241fef4d6914f713739a` → `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`). El siguiente bloque funcional es UX.4.6f.

Revisiones internas:

- **R1:** política, soporte técnico futuro, plan maestro y regresiones base;
- **R2:** barrido de documentación vigente, ADR-168 y contratos dependientes;
- **R3:** proceso de release, terminología beta/oficial y control de referencias obsoletas;
- **R4:** auditoría final y publicación del hito;
  - **R4.1:** promover el candidato `0.0.26-beta`, auditar documentación viva y validar localmente;
  - **R4.2:** commit firmado, PR, CI requerida, cierre documental y tag firmado `v0.0.26-beta`.

### 2. UX.4.6f — Paso 4 · Proyección salarial/laboral

- **R1 activo:** unificar procedencia visual, decisiones explícitas sin predeterminados silenciosos, trazabilidad de valores automáticos y estado accesible de procesamiento para todos los adjuntos;
- **R1.1 en validación:** restaurar el bloqueo de datos documentales detectados en la vista principal y concentrar su edición en la revisión modal, manteniendo editables los campos originalmente no detectados;
- validar lógica y precisión;
- revisar UX y accesibilidad;
- distinguir información acreditada, datos reales recientes y proyección;
- validar el caso femenino usado en Pasos 1–3;
- conservar por separado la proyección de Mi Retiro Seguro y la información más reciente de Ficha Digital;
- revisar modalidades salariales y horizonte;
- asegurar trazabilidad hacia Pasos 5 y 6.

### 3. UX.4.6g — Paso 5 · Escenarios de retiro

- escenarios de edad/fecha;
- continuación de cotización;
- cuotas adicionales;
- selección explícita del escenario;
- validación por los tres sistemas;
- coherencia con Paso 4.

### 4. UX.4.6h — Paso 6 · Resultados y exportación

- resultados finales;
- comparación;
- trazabilidad;
- fuentes;
- advertencias y limitaciones;
- preparación de exportaciones;
- accesibilidad del resultado.

### 5. UX.4.6i — Cómo se calcula

Nueva sección pública para que el asegurado pueda reproducir manualmente los
procedimientos implementados.

Debe cubrir:

- SEBD;
- Subsistema Mixto;
- SUCGS;
- datos necesarios;
- requisitos;
- fórmulas;
- variables;
- orden de operaciones;
- redondeos;
- reglas especiales;
- ejemplos completos;
- fuentes normativas;
- limitaciones;
- vínculo desde resultados a «Ver cómo se obtuvo este cálculo».

La explicación no duplicará motores de cálculo en JavaScript.

### 6. DEV.2 — Centro de desarrollo

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

Mientras este bloque no cierre, la aplicación permanece en `0.0.N-beta`.

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

## 4. Estado al comenzar PLAN.1

La versión base permanece:

```text
0.0.25-beta
```

El tag `v0.0.25-beta` es histórico e inmutable.

PLAN.1 no mueve ese tag y R1 no modifica `VERSION`.

## 5. Criterio de salida de PLAN.1

PLAN.1 solo puede cerrarse cuando:

- no queden referencias vigentes que presenten `0.1.0-beta.1` como objetivo futuro;
- la documentación histórica conserve su contexto sin ser reescrita;
- `VERSIONING.md` y el validador Python admitan la línea oficial futura;
- ADR-168 registre la decisión;
- ROADMAP, README, RELEASES, CHANGELOG, índice, validación y documentos dependientes estén sincronizados;
- las regresiones protejan el nuevo contrato;
- compilación Python, sintaxis JavaScript y `git diff --check` estén limpios;
- la suite completa esté en `OK`;
- cualquier cierre formal siga el flujo de commit firmado, PR, CI, squash y tag aplicable.
