# DOC.1 R1 — Contexto de actualización Markdown post-MANT.1

Este documento extrae contexto de los Markdown candidatos antes de editarlos.

## Documentos marcados ACTUALIZAR

## CHANGELOG.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Changelog
0002:
0003: Este archivo registra **cambios notables por versión**. No sustituye el historial Git, `RELEASES.md` ni las bitácoras históricas conservadas en `docs/archive/`.
0004:
0005: Las versiones `0.0.1-beta` a `0.0.21-beta` fueron reconstruidas retrospectivamente en GOV.1.1 a partir del historial real. `0.0.22-beta` es la primera versión formal adoptada bajo la política de GOV.1.2.
0006:
0007: ## [Unreleased]
0008: - MANT.1 R5H: se completa la auditoría de nombres técnicos restantes, con normalización de módulos, assets, plantillas, workflow y pruebas, sin cambios en cálculo, normativa ni versión.
0009:
0010: ### MANT.1 R5G
0011:
0012: - Agrega auditoría documental R5G para revisar índice, enlaces internos y coherencia documental vigente.
0013: - Actualiza `docs/INDICE.md` para incluir documentos raíz que existían en `docs/` pero no estaban listados.
0014: - Conserva expresiones de dominio como normativa/privacidad, normativa/código y normativa/jurídica porque no son rutas obsoletas.
0015: - Mantiene sin cambios la lógica de cálculo, valores normativos, `VERSION`, `APP_VERSION`, `SEC.2` y `_entregas/`.
0016: ## MANT.1 R5F
0017:
0018: - Normaliza nombres de archivos técnicos en `scripts`, `data`, `regulations` y pruebas seleccionadas.
0019: - Actualiza referencias documentales, hooks, rutas internas y pruebas relacionadas.
0020: - Agrega `docs/AUDITORIA_ARCHIVOS_R5F.md` y `tests/test_mant1_r5f_nombres_archivos.py` para documentar y proteger el cambio.
0021: - Mantiene sin renombrar archivos de dominio como `mixto.json`, `sebd.json` y `sucgs.json`, y preserva archivos históricos con trazabilidad `UX46`, `VER2` o `revision-aware`.
0022:
0023: ## MANT.1 R5E — estandarización de nombres de carpetas
0024:
0025: - renombra carpetas técnicas en español a rutas en inglés: `app/models/`, `app/engines/`, `app/services/`, `regulations/`, `tests/validation_cases/` y `docs/archive/`;
0026: - actualiza imports Python, rutas de pruebas, enlaces documentales, CODEOWNERS, `.gitignore` y referencias a parámetros JSON;
0027: - documenta la auditoría de carpetas en `docs/AUDITORIA_CARPETAS_R5E.md`;
0028: - agrega regresión para impedir que reaparezcan carpetas técnicas antiguas o referencias a rutas obsoletas;
0029: - mantiene sin cambios `_entregas/`, carpetas convencionales con punto inicial, `VERSION`, `APP_VERSION`, motores previsionales, valores JSON, rutas públicas, selectores y SEC.2.
0030:
0031: ### MANT.1 R5D — política, plantillas y uniformidad por extensión
0032:
0033: - documenta la política formal de estructura por extensión para archivos no Markdown;
0034: - agrega auditoría de inventario por extensión y hallazgos de uniformidad;
0035: - incorpora plantillas oficiales por extensión en `docs/templates/file-structure/`;
0036: - uniforma encabezados de `app/static/js/*.js` y `app/static/css/*.css` con propósito y alcance permanente;
0037: - agrega regresión para proteger política, plantillas y encabezados de presentación sin cambiar lógica, storage, selectores, rutas ni textos visibles;
0038: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, ledger VER.2 ni SEC.2.
0039:
0040: ### MANT.1 R5C — comentarios internos en JavaScript complejo
0041:
0042: - agrega comentarios internos de intención en JavaScript de alto impacto: comparador, simulación, resultados, orquestación del Paso 6, gestión de datos, privacidad, procesamiento de adjuntos e importación de documentos oficiales;
0043: - documenta flujos de storage, invalidación descendente, borradores revisables, transición Mixto/SUCGS, comparación acreditado/proyectado y estado accesible de adjuntos;
0044: - mantiene comentarios de `app/static/js/` libres de identificadores de revisión, PR o bloques históricos;
0045: - agrega regresión para proteger comentarios funcionales en los ocho módulos revisados sin cambiar claves de storage, selectores, ids, clases, textos visibles ni lógica;
0046: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.
0047:
0048: ### MANT.1 R5B — comentarios internos en CSS y plantilla Cómo se calcula
0049:
0050: - agrega comentarios estructurales en `app/static/css/como-se-calcula.css` para delimitar hero, navegación, secciones, fórmulas, tablas, factores, accesibilidad y responsive;
0051: - agrega comentarios Jinja en `app/templates/como_se_calcula.html` para ubicar recorrido general, bloques SEBD/Mixto/SUCGS, fuentes y cierre de la guía;
0052: - mantiene los comentarios de `app/` libres de identificadores de revisión, PR o bloques históricos;
0053: - agrega regresión para proteger comentarios funcionales en CSS y plantilla sin cambiar clases, ids, textos visibles ni lógica Jinja;
0054: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.
0055:
0056: ### MANT.1 R5A — comentarios internos en servicios Python de aplicación
0057:
0058: - agrega comentarios internos de intención en servicios Python de alto tamaño: trazabilidad, comparador, guía de cálculo, fuentes normativas, detalle del año actual y Ficha Digital;
0059: - mantiene los comentarios dentro de `app/services/` libres de identificadores de revisión, PR o bloques históricos;
0060: - agrega regresión para exigir comentarios internos útiles en los servicios revisados sin cambiar lógica funcional;
0061: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.
0062:
0063: ### MANT.1 R4 — limpieza de trazabilidad en encabezados operativos
0064:
0065: - limpia encabezados de YAML GitHub para que describan propósito y alcance permanente, sin declarar MANT.1 dentro de archivos operativos;
0066: - elimina metadatos de bloque/origen de los README operativos de `.githooks/` y `scripts/`;
0067: - ajusta la regresión de MANT.1 R3 para exigir encabezados funcionales en YAML, no encabezados con nombre de revisión;
0068: - agrega regresión MANT.1 R4 para impedir trazabilidad de revisión en encabezados operativos;
0069: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, workflows, formularios, Dependabot ni SEC.2.
0070:
0071: ### MANT.1 R3 — encabezados YAML de GitHub
0072:
0073: - documenta los YAML de GitHub antes de SEC.2 sin modificar triggers, jobs, permisos, formularios, labels ni cadencias;
0074: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa ni ledger VER.2;
0075: - agrega encabezados semánticos a Dependabot, workflows e Issue Forms para explicar propósito, límites y privacidad operacional;
0076: - sincroniza `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`, `docs/VALIDACION.md`, `docs/ARQUITECTURA.md` y `docs/ROADMAP.md`;
0077: - agrega regresión documental para proteger encabezados funcionales en `.github/` y que MANT.1 R1/R2/R3 queden visibles en la documentación transversal.
0078:
0079: ### MANT.1 R2 — documentación de scripts y hooks
0080:
0081: - materializa los primeros cambios de mantenimiento técnico derivados de MANT.1 R1, sin cambiar `VERSION`, `APP_VERSION`, motores previsionales ni normativa;
0082: - documenta `.githooks/pre-commit`, `scripts/configure_git_hooks.ps1` y `scripts/validate_precommit.py`;
0083: - agrega `scripts/README.md` y `.githooks/README.md` para explicar propósito, alcance, límites y relación con CI;
0084: - sincroniza `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`, `docs/VALIDACION.md`, `docs/ARQUITECTURA.md` y `docs/ROADMAP.md`;
0085: - agrega regresión documental para proteger el contrato de scripts y hooks;
0086: - absorbe la corrección de higiene textual detectada durante la validación local previa al commit.
0087:
0088: ### MANT.1 R1 — auditoría inicial y plan de mantenimiento
0089:
0090: - inicia MANT.1 como mantenimiento técnico previo a SEC.2;
```

### Coincidencias con contexto

```text
0006:
0007: ## [Unreleased]
0008: - MANT.1 R5H: se completa la auditoría de nombres técnicos restantes, con normalización de módulos, assets, plantillas, workflow y pruebas, sin cambios en cálculo, normativa ni versión.
0009:
0010: ### MANT.1 R5G
```

```text
0008: - MANT.1 R5H: se completa la auditoría de nombres técnicos restantes, con normalización de módulos, assets, plantillas, workflow y pruebas, sin cambios en cálculo, normativa ni versión.
0009:
0010: ### MANT.1 R5G
0011:
0012: - Agrega auditoría documental R5G para revisar índice, enlaces internos y coherencia documental vigente.
```

```text
0014: - Conserva expresiones de dominio como normativa/privacidad, normativa/código y normativa/jurídica porque no son rutas obsoletas.
0015: - Mantiene sin cambios la lógica de cálculo, valores normativos, `VERSION`, `APP_VERSION`, `SEC.2` y `_entregas/`.
0016: ## MANT.1 R5F
0017:
0018: - Normaliza nombres de archivos técnicos en `scripts`, `data`, `regulations` y pruebas seleccionadas.
```

```text
0021: - Mantiene sin renombrar archivos de dominio como `mixto.json`, `sebd.json` y `sucgs.json`, y preserva archivos históricos con trazabilidad `UX46`, `VER2` o `revision-aware`.
0022:
0023: ## MANT.1 R5E — estandarización de nombres de carpetas
0024:
0025: - renombra carpetas técnicas en español a rutas en inglés: `app/models/`, `app/engines/`, `app/services/`, `regulations/`, `tests/validation_cases/` y `docs/archive/`;
```

```text
0029: - mantiene sin cambios `_entregas/`, carpetas convencionales con punto inicial, `VERSION`, `APP_VERSION`, motores previsionales, valores JSON, rutas públicas, selectores y SEC.2.
0030:
0031: ### MANT.1 R5D — política, plantillas y uniformidad por extensión
0032:
0033: - documenta la política formal de estructura por extensión para archivos no Markdown;
```

```text
0036: - uniforma encabezados de `app/static/js/*.js` y `app/static/css/*.css` con propósito y alcance permanente;
0037: - agrega regresión para proteger política, plantillas y encabezados de presentación sin cambiar lógica, storage, selectores, rutas ni textos visibles;
0038: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, ledger VER.2 ni SEC.2.
0039:
0040: ### MANT.1 R5C — comentarios internos en JavaScript complejo
```

```text
0038: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, ledger VER.2 ni SEC.2.
0039:
0040: ### MANT.1 R5C — comentarios internos en JavaScript complejo
0041:
0042: - agrega comentarios internos de intención en JavaScript de alto impacto: comparador, simulación, resultados, orquestación del Paso 6, gestión de datos, privacidad, procesamiento de adjuntos e importación de documentos oficiales;
```

```text
0046: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.
0047:
0048: ### MANT.1 R5B — comentarios internos en CSS y plantilla Cómo se calcula
0049:
0050: - agrega comentarios estructurales en `app/static/css/como-se-calcula.css` para delimitar hero, navegación, secciones, fórmulas, tablas, factores, accesibilidad y responsive;
```

```text
0054: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.
0055:
0056: ### MANT.1 R5A — comentarios internos en servicios Python de aplicación
0057:
0058: - agrega comentarios internos de intención en servicios Python de alto tamaño: trazabilidad, comparador, guía de cálculo, fuentes normativas, detalle del año actual y Ficha Digital;
```

```text
0061: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.
0062:
0063: ### MANT.1 R4 — limpieza de trazabilidad en encabezados operativos
0064:
0065: - limpia encabezados de YAML GitHub para que describan propósito y alcance permanente, sin declarar MANT.1 dentro de archivos operativos;
```

```text
0063: ### MANT.1 R4 — limpieza de trazabilidad en encabezados operativos
0064:
0065: - limpia encabezados de YAML GitHub para que describan propósito y alcance permanente, sin declarar MANT.1 dentro de archivos operativos;
0066: - elimina metadatos de bloque/origen de los README operativos de `.githooks/` y `scripts/`;
0067: - ajusta la regresión de MANT.1 R3 para exigir encabezados funcionales en YAML, no encabezados con nombre de revisión;
```

```text
0065: - limpia encabezados de YAML GitHub para que describan propósito y alcance permanente, sin declarar MANT.1 dentro de archivos operativos;
0066: - elimina metadatos de bloque/origen de los README operativos de `.githooks/` y `scripts/`;
0067: - ajusta la regresión de MANT.1 R3 para exigir encabezados funcionales en YAML, no encabezados con nombre de revisión;
0068: - agrega regresión MANT.1 R4 para impedir trazabilidad de revisión en encabezados operativos;
0069: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, workflows, formularios, Dependabot ni SEC.2.
```

```text
0066: - elimina metadatos de bloque/origen de los README operativos de `.githooks/` y `scripts/`;
0067: - ajusta la regresión de MANT.1 R3 para exigir encabezados funcionales en YAML, no encabezados con nombre de revisión;
0068: - agrega regresión MANT.1 R4 para impedir trazabilidad de revisión en encabezados operativos;
0069: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, workflows, formularios, Dependabot ni SEC.2.
0070:
```

```text
0069: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, workflows, formularios, Dependabot ni SEC.2.
0070:
0071: ### MANT.1 R3 — encabezados YAML de GitHub
0072:
0073: - documenta los YAML de GitHub antes de SEC.2 sin modificar triggers, jobs, permisos, formularios, labels ni cadencias;
```

```text
0072:
0073: - documenta los YAML de GitHub antes de SEC.2 sin modificar triggers, jobs, permisos, formularios, labels ni cadencias;
0074: - no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa ni ledger VER.2;
0075: - agrega encabezados semánticos a Dependabot, workflows e Issue Forms para explicar propósito, límites y privacidad operacional;
0076: - sincroniza `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`, `docs/VALIDACION.md`, `docs/ARQUITECTURA.md` y `docs/ROADMAP.md`;
```

```text
0075: - agrega encabezados semánticos a Dependabot, workflows e Issue Forms para explicar propósito, límites y privacidad operacional;
0076: - sincroniza `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`, `docs/VALIDACION.md`, `docs/ARQUITECTURA.md` y `docs/ROADMAP.md`;
0077: - agrega regresión documental para proteger encabezados funcionales en `.github/` y que MANT.1 R1/R2/R3 queden visibles en la documentación transversal.
0078:
0079: ### MANT.1 R2 — documentación de scripts y hooks
```

```text
0077: - agrega regresión documental para proteger encabezados funcionales en `.github/` y que MANT.1 R1/R2/R3 queden visibles en la documentación transversal.
0078:
0079: ### MANT.1 R2 — documentación de scripts y hooks
0080:
0081: - materializa los primeros cambios de mantenimiento técnico derivados de MANT.1 R1, sin cambiar `VERSION`, `APP_VERSION`, motores previsionales ni normativa;
```

```text
0079: ### MANT.1 R2 — documentación de scripts y hooks
0080:
0081: - materializa los primeros cambios de mantenimiento técnico derivados de MANT.1 R1, sin cambiar `VERSION`, `APP_VERSION`, motores previsionales ni normativa;
0082: - documenta `.githooks/pre-commit`, `scripts/configure_git_hooks.ps1` y `scripts/validate_precommit.py`;
0083: - agrega `scripts/README.md` y `.githooks/README.md` para explicar propósito, alcance, límites y relación con CI;
```

## CONTRIBUTING.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Guía de contribución
0002:
0003: Este documento define el flujo mínimo para modificar Mi Retiro Proyectado sin perder trazabilidad técnica, normativa, documental o de pruebas.
0004:
0005: ## 1. Antes de comenzar
0006:
0007: Actualizar primero la rama predeterminada:
0008:
0009: ```powershell
0010: git switch main
0011: git fetch origin
0012: git pull --ff-only origin main
0013: ```
0014:
0015: Comprobar que la copia de trabajo esté limpia:
0016:
0017: ```powershell
0018: git status
0019: ```
0020:
0021: Crear una rama específica antes de modificar:
0022:
0023: ```powershell
0024: git switch -c <tipo>/<descripcion>
0025: ```
0026:
0027: No aplicar un paquete de cambios sobre modificaciones locales no revisadas.
0028:
0029: Toda participación en issues, Pull Requests o revisiones debe respetar `CODE_OF_CONDUCT.md` -> CODE_OF_CONDUCT.md. Para dudas de uso, reportes, privacidad o seguridad, consultar primero `SUPPORT.md` -> SUPPORT.md.
0030:
0031: ## 2. Principios obligatorios
0032:
0033: - Las fórmulas previsionales principales viven en Python.
0034: - JavaScript no debe duplicar motores legales.
0035: - Los parámetros normativos modificables deben residir en `regulations/` o estar aislados y documentados.
0036: - Datos acreditados y proyectados permanecen diferenciados.
0037: - Pagos únicos y pensiones mensuales permanecen separados.
0038: - Un dato oficial desconocido no se inventa.
0039: - Toda interpretación normativa relevante debe ser trazable a una fuente y, cuando corresponda, a un ADR.
0040: - Los documentos personales reales no se versionan.
0041: - Código, pruebas y documentación se actualizan dentro de la misma unidad de trabajo.
0042: - Comentarios y docstrings siguen `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md` -> docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md; explican intención y contratos, no la sintaxis obvia.
0043:
0044: ## 3. Fuente de versión
0045:
0046: `VERSION` es la única fuente canónica de versión de aplicación.
0047:
0048: No escribir versiones independientes en:
0049:
0050: - `app/core/config.py`;
0051: - plantillas;
0052: - JavaScript;
0053: - motores;
0054: - documentación que pretenda definir una segunda fuente.
0055:
0056: Consultar `VERSIONING.md` -> VERSIONING.md.
0057:
0058: ## 4. Flujo de cambios
0059:
0060: Antes de editar:
0061:
0062: ```powershell
0063: git status
0064: git diff
0065: ```
0066:
0067: Después de editar, revisar únicamente los archivos afectados y agruparlos por propósito. Evitar `git add .` como hábito cuando existan cambios heterogéneos.
0068:
0069: Ejemplos de tipos de commit:
0070:
0071: ```text
0072: feat(ux): describir cambio funcional
0073: fix(data): corregir reconciliación
0074: test(ux): agregar regresiones
0075: docs(gov): actualizar documentación
0076: chore(gov): ajustar configuración
0077: refactor(core): reorganizar implementación
0078: ```
0079:
0080: Los commits deben ser legibles de forma independiente y no deben ocultar cambios no relacionados.
0081:
0082: `main` está protegida. El flujo ordinario es rama de trabajo → commit firmado → push de la rama → Pull Request → checks requeridos → `Squash and merge`. No se usa `git push origin main` como flujo normal.
0083:
0084: Cuando `main` exige firmas verificadas, el PR que se integre mediante squash debe ser creado por el mantenedor que realizará esa integración, salvo recuperación administrativa excepcional documentada.
0085:
0086: ## 5. Validación mínima
0087:
0088: El repositorio incluye un gate `pre-commit` versionado. Debe activarse **una sola vez por cada clon local**:
0089:
0090: ```powershell
```

### Coincidencias con contexto

- Sin coincidencias de riesgo detectadas.

## docs/ARQUITECTURA.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Arquitectura
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.23-beta`
0006: **Revisión documental:** GOV.1.4 — 2026-08-17
0007: **Última actualización técnica:** DEV.2 R4 — cierre final documental — 2026-08-23
0008: **Última actualización de mantenimiento:** MANT.1 R5E — estandarización de nombres de carpetas — 2026-08-23
0009: **Clasificación:** Técnica / Pública
0010:
0011: Mi Retiro Proyectado es una aplicación web local basada en FastAPI, Jinja2 y JavaScript del navegador. La arquitectura separa presentación, contratos de datos, servicios de integración, motores previsionales, parámetros normativos y observabilidad de desarrollo.
0012:
0013: MANT.1 R1 dejó la auditoría inicial de mantenibilidad, MANT.1 R2 documenta
0014: la infraestructura local de scripts/hooks que protege commits reproducibles antes
0015: de los checks remotos y MANT.1 R3 documenta los YAML de GitHub sin cambiar CI,
0016: Issue Forms ni Dependabot. MANT.1 R4 limpia encabezados operativos para separar
0017: comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
0018: de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
0019: y plantilla de la guía pública, MANT.1 R5C documenta JavaScript complejo sin
0020: alterar lógica, storage, selectores ni contratos de datos, MANT.1 R5D formaliza política/plantillas por extensión con uniformidad de encabezados JS/CSS y MANT.1 R5E estandariza nombres de carpetas técnicas en inglés sin cambiar contratos funcionales. Este mantenimiento no
0021: introduce nuevas capas de producto.
0022:
0023: Índice -> INDICE.md · Modelo de datos -> MODELO_DE_DATOS.md · Motor -> MOTOR_DE_CALCULO.md · Normativa -> NORMATIVA.md · Observabilidad -> OBSERVABILIDAD_LOGS.md · Política de estructura -> POLITICA_ESTRUCTURA_ARCHIVOS.md · Auditoría de carpetas -> AUDITORIA_CARPETAS_R5E.md
0024:
0025: ## 1. Principios
0026:
0027: 1. **Fuente única del cálculo:** las fórmulas previsionales principales viven en Python.
0028: 2. **Normativa separada:** parámetros legales modificables se mantienen en `regulations/`.
0029: 3. **Histórico y proyección separados:** una estimación futura no sustituye silenciosamente información acreditada.
0030: 4. **Datos faltantes explícitos:** un parámetro que no puede determinarse no se inventa.
0031: 5. **Trazabilidad:** motores y servicios exponen advertencias, fuentes y resultados intermedios cuando corresponde.
0032: 6. **Procesamiento local por defecto:** el estado de simulación se conserva en el navegador y no existe persistencia permanente automática.
0033: 7. **Importación revisable:** extraer un PDF no equivale a confirmar ni calcular.
0034: 8. **Versión única:** `VERSION` es la fuente canónica consumida por `app/core/version.py`.
0035: 9. **Interfaz desacoplada:** JavaScript administra experiencia, estado temporal y comunicación HTTP; no constituye una segunda implementación de los motores.
0036: 10. **Observabilidad lateral:** Developer Diagnostics observa operaciones ya ejecutadas; no vuelve a invocar motores ni replica fórmulas.
0037: 11. **Minimización de logs:** los eventos técnicos no contienen cuerpos HTTP, documentos, identificadores ni valores financieros.
0038: 12. **Historia preservada:** la documentación vigente describe el contrato actual; bitácoras anteriores se conservan en `docs/archive/`.
0039:
0040: ## 2. Inventario relevante del paquete `app`
0041:
0042: ### Núcleo
0043:
0044: - `app/core/pdf_files.py`
0045: - `app/core/config.py`
0046: - `app/core/constants.py`
0047: - `app/core/money.py`
0048: - `app/core/normativa.py`
0049: - `app/core/observability.py`
0050: - `app/core/version.py`
0051:
0052: ### Modelos
0053:
0054: - `app/models/comparacion.py`
0055: - `app/models/pension.py`
0056: - `app/models/unified_result.py`
0057: - `app/models/simulation.py`
0058: - `app/models/traceability.py`
0059:
0060: ### Motores
0061:
0062: - `app/engines/elegibilidad.py`
0063: - `app/engines/mixto.py`
0064: - `app/engines/sebd.py`
0065: - `app/engines/sebd_modalidades.py`
0066: - `app/engines/sucgs.py`
0067:
0068: ### Servicios principales
0069:
0070: - `app/services/comparator.py` — construye matrices retiro × salario sin recalcular fórmulas fuera de los servicios integrados
0071: - `app/services/como_se_calcula.py` — estructura parámetros normativos para la guía pública sin ejecutar motores
0072: - `app/services/detalle_anio_actual.py` — normaliza salarios mensuales/quincenales y separa salario visible de cuota acreditada
0073: - `app/services/reference_date.py`
0074: - `app/services/ficha_digital.py` — extrae salarios recientes desde PDF en memoria con límites de seguridad y minimización
0075: - `app/services/regulatory_sources.py` — arma catálogo metodológico de fuentes oficiales desde parámetros versionados
0076: - `app/services/salary_history.py`
0077: - `app/services/timeline.py`
0078: - `app/services/contribution_projection.py`
0079: - `app/services/salary_projection.py`
0080: - `app/services/referencia_mi_retiro_seguro.py`
0081: - `app/services/unified_result.py`
0082: - `app/services/results.py`
0083: - `app/services/mixto_results.py`
0084: - `app/services/sebd_results.py`
0085: - `app/services/sucgs_results.py`
0086: - `app/services/retirement.py`
0087: - `app/services/traceability.py` — transforma resultados ya calculados en pasos explicables y fuentes auditables
0088:
0089: ### Presentación CSS y plantillas documentadas
0090:
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.23-beta`
0006: **Revisión documental:** GOV.1.4 — 2026-08-17
```

```text
0006: **Revisión documental:** GOV.1.4 — 2026-08-17
0007: **Última actualización técnica:** DEV.2 R4 — cierre final documental — 2026-08-23
0008: **Última actualización de mantenimiento:** MANT.1 R5E — estandarización de nombres de carpetas — 2026-08-23
0009: **Clasificación:** Técnica / Pública
0010:
```

```text
0011: Mi Retiro Proyectado es una aplicación web local basada en FastAPI, Jinja2 y JavaScript del navegador. La arquitectura separa presentación, contratos de datos, servicios de integración, motores previsionales, parámetros normativos y observabilidad de desarrollo.
0012:
0013: MANT.1 R1 dejó la auditoría inicial de mantenibilidad, MANT.1 R2 documenta
0014: la infraestructura local de scripts/hooks que protege commits reproducibles antes
0015: de los checks remotos y MANT.1 R3 documenta los YAML de GitHub sin cambiar CI,
```

```text
0013: MANT.1 R1 dejó la auditoría inicial de mantenibilidad, MANT.1 R2 documenta
0014: la infraestructura local de scripts/hooks que protege commits reproducibles antes
0015: de los checks remotos y MANT.1 R3 documenta los YAML de GitHub sin cambiar CI,
0016: Issue Forms ni Dependabot. MANT.1 R4 limpia encabezados operativos para separar
0017: comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
```

```text
0014: la infraestructura local de scripts/hooks que protege commits reproducibles antes
0015: de los checks remotos y MANT.1 R3 documenta los YAML de GitHub sin cambiar CI,
0016: Issue Forms ni Dependabot. MANT.1 R4 limpia encabezados operativos para separar
0017: comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
0018: de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
```

```text
0015: de los checks remotos y MANT.1 R3 documenta los YAML de GitHub sin cambiar CI,
0016: Issue Forms ni Dependabot. MANT.1 R4 limpia encabezados operativos para separar
0017: comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
0018: de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
0019: y plantilla de la guía pública, MANT.1 R5C documenta JavaScript complejo sin
```

```text
0016: Issue Forms ni Dependabot. MANT.1 R4 limpia encabezados operativos para separar
0017: comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
0018: de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
0019: y plantilla de la guía pública, MANT.1 R5C documenta JavaScript complejo sin
0020: alterar lógica, storage, selectores ni contratos de datos, MANT.1 R5D formaliza política/plantillas por extensión con uniformidad de encabezados JS/CSS y MANT.1 R5E estandariza nombres de carpetas técnicas en inglés sin cambiar contratos funcionales. Este mantenimiento no
```

```text
0017: comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
0018: de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
0019: y plantilla de la guía pública, MANT.1 R5C documenta JavaScript complejo sin
0020: alterar lógica, storage, selectores ni contratos de datos, MANT.1 R5D formaliza política/plantillas por extensión con uniformidad de encabezados JS/CSS y MANT.1 R5E estandariza nombres de carpetas técnicas en inglés sin cambiar contratos funcionales. Este mantenimiento no
0021: introduce nuevas capas de producto.
```

```text
0018: de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
0019: y plantilla de la guía pública, MANT.1 R5C documenta JavaScript complejo sin
0020: alterar lógica, storage, selectores ni contratos de datos, MANT.1 R5D formaliza política/plantillas por extensión con uniformidad de encabezados JS/CSS y MANT.1 R5E estandariza nombres de carpetas técnicas en inglés sin cambiar contratos funcionales. Este mantenimiento no
0021: introduce nuevas capas de producto.
0022:
```

```text
0351: DEV.2 quedó cerrado documentalmente en R4 después de integrar R1, R2 y R3. R1 abrió la ruta interna, R2 añadió el visor diagnóstico seguro y la exportación ZIP sanitizada, R3 añadió el autodiagnóstico técnico local y R4 sincroniza la documentación viva del bloque.
0352:
0353: La ruta usa `MRP_DEV_MODE` solo como indicador de activación diagnóstica, conserva `0.0.26-beta` como versión visible, no añade rutas públicas nuevas, no modifica motores previsionales, no crea tags y no adelanta el cierre transversal de VER.2.
0354:
0355: ## Política de estructura por extensión
```

## docs/ESPECIFICACION_FUNCIONAL.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Especificación funcional
0002:
0003: **Estado:** Vigente con registro RF histórico integrado
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.23-beta`
0006: **Revisión documental:** GOV.1.3 R2 — 2026-08-17
0007: **Actualización funcional vigente:** UX.4.6e R8 — procedencia editable — 2026-08-19
0008: **Clasificación:** Funcional / Auditoría
0009:
0010: Este documento tiene dos capas:
0011:
0012: 1. **Contrato funcional vigente consolidado**, que describe el comportamiento actual.
0013: 2. **Registro cronológico RF preservado**, que mantiene los identificadores históricos sin renumerarlos.
0014:
0015: Cuando una descripción cronológica antigua contradiga el contrato consolidado o una regla posterior explícitamente identificada, prevalece la regla vigente más reciente. La trazabilidad RF completa se ampliará en GOV.1.3 R4.
0016:
0017: ## 1. Alcance vigente
0018:
0019: Mi Retiro Proyectado permite capturar/revisar datos, construir escenarios y estimar prestaciones para los tres sistemas generales implementados:
0020:
0021: - SEBD;
0022: - Subsistema Mixto;
0023: - SUCGS.
0024:
0025: La herramienta es independiente de la CSS y no sustituye una determinación oficial.
0026:
0027: ## 2. Asistente de seis pasos
0028:
0029: ### Paso 1 — Datos personales
0030:
0031: Debe permitir:
0032:
0033: - captura manual;
0034: - importación revisable de Mi Retiro Seguro;
0035: - identificación opcional;
0036: - fecha de nacimiento, sexo y sistema como datos necesarios para continuar;
0037: - apellido de casada opcional/condicionado;
0038: - consentimiento vigente de privacidad antes de tratar datos del asistente.
0039:
0040: Solo los campos realmente aportados por un documento conservan procedencia documental. Después de confirmar una importación, el Asegurado(a) puede ajustar la copia de trabajo; la aplicación conserva la referencia original y cambia inmediatamente el estado a `Editado por ti`, `Completado manualmente`, `Excluido por ti`, `Detectado` o `No detectado` según corresponda.
0041:
0042: ### Paso 2 — Cuotas
0043:
0044: Debe distinguir:
0045:
0046: - cuotas acreditadas;
0047: - cuotas del año actual;
0048: - continuidad futura;
0049: - cierre esperado del año;
0050: - densidad futura.
0051:
0052: Los supuestos futuros requieren una decisión explícita. Limpiar Paso 2 elimina esa decisión y sus valores.
0053:
0054: Una importación puede completar campos de cuotas por procedencia; los campos no detectados siguen manuales. Los valores documentales confirmados pueden ajustarse explícitamente y deben conservar su referencia original.
0055:
0056: ### Paso 3 — Historial y salario reciente
0057:
0058: Debe permitir:
0059:
0060: - historial anual;
0061: - detalle opcional mensual/quincenal del año actual;
0062: - Ficha Digital;
0063: - bases salariales manuales/derivadas;
0064: - separación entre salario disponible y acreditado.
0065:
0066: Una cuota manual del detalle puede actualizar el agregado del Paso 2. Una Ficha Digital confirmada puede **aumentar** la referencia de cuotas del año actual si identifica más meses; no debe reducir automáticamente una referencia superior. Después de confirmar, el usuario puede excluir o reincluir explícitamente un período detectado; esa decisión sí puede reconciliar el Paso 2 a la baja o al alza y debe quedar visible como procedencia, sin alterar el documento original.
0067:
0068: ### Paso 4 — Proyección
0069:
0070: Debe construir:
0071:
0072: - salario constante;
0073: - variación porcentual;
0074: - salario futuro conocido;
0075: - escenarios porcentuales;
0076: - línea temporal separando real y proyectado.
0077:
0078: ### Paso 5 — Retiro
0079:
0080: Debe construir escenarios de retiro usando fechas, cuotas y horizonte salarial. El último mes acreditado se maneja con granularidad mensual visible.
0081:
0082: ### Paso 6 — Resultados
0083:
0084: Debe:
0085:
0086: - ejecutar el motor correspondiente;
0087: - separar pensión mensual y pago único;
0088: - mostrar advertencias/datos no confirmados;
0089: - ofrecer trazabilidad;
0090: - generar un resumen transversal;
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente con registro RF histórico integrado
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.23-beta`
0006: **Revisión documental:** GOV.1.3 R2 — 2026-08-17
```

```text
0822:
0823:
0824: ### UX.4.6d R6 — gestión de datos del asistente
0825:
0826: **RF-240.** La barra superior del asistente debe incluir un menú **Opciones** con acciones para limpiar el paso activo y reiniciar la simulación.
```

```text
0840: **RF-247.** La versión vigente de Términos/Privacidad debe describir de forma comprensible las diferencias entre limpiar un paso, reiniciar la simulación y borrar los datos locales de la aplicación.
0841:
0842: ### UX.4.6d R7 — consulta posterior de privacidad
0843:
0844: **RF-248.** El botón **Revisar términos de privacidad** de Fuentes debe abrir el documento legal en la misma página y no navegar a Simular.
```

## docs/INDICE.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Índice de documentación
0002:
0003: **Estado:** vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Última actualización transversal:** VER.2 — segunda pasada contable y materialización del ledger — 2026-08-22
0007: **Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`
0008:
0009: Este archivo es el punto de entrada para la documentación técnica, funcional, normativa, de privacidad, validación y auditoría de Mi Retiro Proyectado.
0010:
0011: ## 1. Producto y alcance
0012:
0013: - `../README.md` -> ../README.md — presentación, alcance, instalación y estado general.
0014: - `ESPECIFICACION_FUNCIONAL.md` -> ESPECIFICACION_FUNCIONAL.md — requisitos funcionales.
0015: - `ROADMAP.md` -> ROADMAP.md — estado actual y próximos hitos.
0016: - `PLAN_MAESTRO_HACIA_1_0.md` -> PLAN_MAESTRO_HACIA_1_0.md — secuencia transversal de 14 bloques hasta la primera versión oficial.
0017: - `IDENTIDAD_VISUAL.md` -> IDENTIDAD_VISUAL.md — logo oficial, activos canónicos, favicons y Social Preview.
0018: - `COMO_SE_CALCULA.md` -> COMO_SE_CALCULA.md — contrato público de explicación de SEBD, Mixto y SUCGS sin duplicar motores.
0019:
0020: ## 2. Gobierno y versionado
0021:
0022: - `../GOVERNANCE.md` -> ../GOVERNANCE.md — gobierno del proyecto.
0023: - `../VERSIONING.md` -> ../VERSIONING.md — política legacy, beta revision-aware `0.GG.RR.EE-beta`, versión oficial de cuatro componentes y Build independiente.
0024: - `../VERSION` -> ../VERSION — fuente canónica de la versión candidata de aplicación.
0025: - `AUDITORIA_VERSIONADO_PRE_1_0.md` -> AUDITORIA_VERSIONADO_PRE_1_0.md — auditoría del historial, criterio contable y exclusiones de VER.2.
0026: - `ADR_179_VERSIONADO_REVISION_AWARE.md` -> ADR_179_VERSIONADO_REVISION_AWARE.md — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
0027: - `AUDITORIA_VER2_SEGUNDA_PASADA.md` -> AUDITORIA_VER2_SEGUNDA_PASADA.md — bitácora de la segunda pasada y correcciones sobre la primera reconstrucción.
0028: - `AUDITORIA_VER2_CONTEO_PROVISIONAL.md` -> AUDITORIA_VER2_CONTEO_PROVISIONAL.md — cierre del conteo de segunda pasada en G070 antes de VER.2.
0029: - `MATRIZ_DECISION_REVISIONES_VER2.md` -> MATRIZ_DECISION_REVISIONES_VER2.md — decisión fila por fila sobre qué consume Global y por qué.
0030: - `LEDGER_REVISIONES_PRE_1_0.md` -> LEDGER_REVISIONES_PRE_1_0.md — ledger Markdown G001–G070 y candidato G071.
0031: - `../data/revision_ledger_pre_1_0.json` -> ../data/revision_ledger_pre_1_0.json — ledger machine-readable canónico de la reconstrucción.
0032: - `../app/core/version_ledger.py` -> ../app/core/version_ledger.py — validador de continuidad, unicidad y codificación del ledger estructurado.
0033: - `../RELEASES.md` -> ../RELEASES.md — versiones, tags y reconstrucción histórica.
0034: - `../CHANGELOG.md` -> ../CHANGELOG.md — cambios notables por versión.
0035: - `../CONTRIBUTING.md` -> ../CONTRIBUTING.md — flujo de contribución.
0036: - `../CODE_OF_CONDUCT.md` -> ../CODE_OF_CONDUCT.md — normas de participación.
0037: - `../SUPPORT.md` -> ../SUPPORT.md — canales de soporte, privacidad y seguridad.
0038: - `PLAN_MAESTRO_HACIA_1_0.md` -> PLAN_MAESTRO_HACIA_1_0.md — dependencias y gates previos a `1.0.0.0`.
0039: - `MIGRACION_FIRMAS_GIT_2026-08-17.md` -> MIGRACION_FIRMAS_GIT_2026-08-17.md — firma SSH y migración histórica controlada.
0040: - `../.github/allowed_signers` -> ../.github/allowed_signers — claves públicas autorizadas.
0041: - `AUDITORIA_GITHUB.md` -> AUDITORIA_GITHUB.md — controles GitHub, seguridad y auditoría automática.
0042: - `PREPARACION_PUBLICA_GITHUB.md` -> PREPARACION_PUBLICA_GITHUB.md — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público.
0043: - `AUDITORIA_REPOSITORIO_2026-08-18.md` -> AUDITORIA_REPOSITORIO_2026-08-18.md — auditoría integral local/remota post-GOV.1.
0044: - `AUDITORIA_UX46E_R7_2026-08-18.md` -> AUDITORIA_UX46E_R7_2026-08-18.md — auditoría transversal de coherencia de UX.4.6e.
0045: - `AUDITORIA_PLAN1_R4_2026-08-20.md` -> AUDITORIA_PLAN1_R4_2026-08-20.md — auditoría integral y gates R4.1/R4.2 de PLAN.1.
0046: - `CIERRE_GOV1.md` -> CIERRE_GOV1.md — evidencia definitiva del cierre GOV.1.
0047: - `../LICENSE` -> ../LICENSE — licencia propietaria de materiales originales.
0048: - `LICENCIA_Y_DISTRIBUCION.md` -> LICENCIA_Y_DISTRIBUCION.md — evaluación y decisión de licencia.
0049: - `../THIRD_PARTY_NOTICES.md` -> ../THIRD_PARTY_NOTICES.md — avisos de componentes de terceros.
0050:
0051: ## 3. Arquitectura
0052:
0053: - `ARQUITECTURA.md` -> ARQUITECTURA.md — capas, módulos, endpoints y flujo.
0054: - `AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md` -> AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md — auditoría de política y plantillas por extensión.
0055: - `AUDITORIA_CARPETAS_R5E.md` -> AUDITORIA_CARPETAS_R5E.md — auditoría de nombres de carpetas técnicas y rutas sincronizadas.
0056: - `AUDITORIA_ARCHIVOS_R5F.md` -> AUDITORIA_ARCHIVOS_R5F.md — auditoría de nombres de archivos técnicos y referencias sincronizadas.
0057: - `AUDITORIA_DOCUMENTACION_R5G.md` -> AUDITORIA_DOCUMENTACION_R5G.md — auditoría de cobertura documental, índice y referencias internas.
0058: - `MODELO_DE_DATOS.md` -> MODELO_DE_DATOS.md — modelos y contratos.
0059: - `GESTION_DATOS_SIMULACION.md` -> GESTION_DATOS_SIMULACION.md — estado local, limpieza, restauración e invalidación.
0060: - `OBSERVABILIDAD_LOGS.md` -> OBSERVABILIDAD_LOGS.md — Developer Diagnostics, esquema JSONL, correlación, redacción, retención y exportación.
0061:
0062: ## 4. Especificación funcional
0063:
0064: - `ESPECIFICACION_FUNCIONAL.md` -> ESPECIFICACION_FUNCIONAL.md — RF y comportamiento del producto.
0065: - `GUIA_INTERNA_DESARROLLO.md` -> GUIA_INTERNA_DESARROLLO.md — convenciones de ingeniería e interfaz.
0066:
0067: ## 5. Motores previsionales
0068:
0069: - `MOTOR_DE_CALCULO.md` -> MOTOR_DE_CALCULO.md — flujo común de cálculo.
0070: - `MODALIDADES_SEBD.md` -> MODALIDADES_SEBD.md — SEBD.
0071: - `MODALIDADES_MIXTO.md` -> MODALIDADES_MIXTO.md — Subsistema Mixto.
0072: - `MODALIDADES_SUCGS.md` -> MODALIDADES_SUCGS.md — SUCGS.
0073:
0074: ## 6. Normativa y fuentes
0075:
0076: - `NORMATIVA.md` -> NORMATIVA.md — interpretación y aplicación normativa.
0077: - `FUENTES_NORMATIVAS.md` -> FUENTES_NORMATIVAS.md — catálogo de fuentes oficiales.
0078: - `../regulations/*.json` — parámetros legales versionados.
0079:
0080: ## 7. Datos y trazabilidad
0081:
0082: - `MODELO_DE_DATOS.md` -> MODELO_DE_DATOS.md — contratos y procedencia.
0083: - `GESTION_DATOS_SIMULACION.md` -> GESTION_DATOS_SIMULACION.md — ciclo de vida del estado local.
0084: - `DECISIONES.md` -> DECISIONES.md — decisiones ADR históricas y vigentes.
0085:
0086: ## 8. Seguridad y privacidad
0087:
0088: - `SEGURIDAD_PRIVACIDAD.md` -> SEGURIDAD_PRIVACIDAD.md — controles técnicos.
0089: - `MODELO_AMENAZAS.md` -> MODELO_AMENAZAS.md — threat model y matriz de riesgos.
0090: - `PROCEDIMIENTO_DERECHOS_TITULAR.md` -> PROCEDIMIENTO_DERECHOS_TITULAR.md — ejercicio de derechos.
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Última actualización transversal:** VER.2 — segunda pasada contable y materialización del ledger — 2026-08-22
```

```text
0003: **Estado:** vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Última actualización transversal:** VER.2 — segunda pasada contable y materialización del ledger — 2026-08-22
0007: **Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`
```

```text
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Última actualización transversal:** VER.2 — segunda pasada contable y materialización del ledger — 2026-08-22
0007: **Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`
0008:
```

```text
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Última actualización transversal:** VER.2 — segunda pasada contable y materialización del ledger — 2026-08-22
0007: **Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`
0008:
0009: Este archivo es el punto de entrada para la documentación técnica, funcional, normativa, de privacidad, validación y auditoría de Mi Retiro Proyectado.
```

```text
0022: - `../GOVERNANCE.md` -> ../GOVERNANCE.md — gobierno del proyecto.
0023: - `../VERSIONING.md` -> ../VERSIONING.md — política legacy, beta revision-aware `0.GG.RR.EE-beta`, versión oficial de cuatro componentes y Build independiente.
0024: - `../VERSION` -> ../VERSION — fuente canónica de la versión candidata de aplicación.
0025: - `AUDITORIA_VERSIONADO_PRE_1_0.md` -> AUDITORIA_VERSIONADO_PRE_1_0.md — auditoría del historial, criterio contable y exclusiones de VER.2.
0026: - `ADR_179_VERSIONADO_REVISION_AWARE.md` -> ADR_179_VERSIONADO_REVISION_AWARE.md — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
```

```text
0023: - `../VERSIONING.md` -> ../VERSIONING.md — política legacy, beta revision-aware `0.GG.RR.EE-beta`, versión oficial de cuatro componentes y Build independiente.
0024: - `../VERSION` -> ../VERSION — fuente canónica de la versión candidata de aplicación.
0025: - `AUDITORIA_VERSIONADO_PRE_1_0.md` -> AUDITORIA_VERSIONADO_PRE_1_0.md — auditoría del historial, criterio contable y exclusiones de VER.2.
0026: - `ADR_179_VERSIONADO_REVISION_AWARE.md` -> ADR_179_VERSIONADO_REVISION_AWARE.md — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
0027: - `AUDITORIA_VER2_SEGUNDA_PASADA.md` -> AUDITORIA_VER2_SEGUNDA_PASADA.md — bitácora de la segunda pasada y correcciones sobre la primera reconstrucción.
```

```text
0026: - `ADR_179_VERSIONADO_REVISION_AWARE.md` -> ADR_179_VERSIONADO_REVISION_AWARE.md — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
0027: - `AUDITORIA_VER2_SEGUNDA_PASADA.md` -> AUDITORIA_VER2_SEGUNDA_PASADA.md — bitácora de la segunda pasada y correcciones sobre la primera reconstrucción.
0028: - `AUDITORIA_VER2_CONTEO_PROVISIONAL.md` -> AUDITORIA_VER2_CONTEO_PROVISIONAL.md — cierre del conteo de segunda pasada en G070 antes de VER.2.
0029: - `MATRIZ_DECISION_REVISIONES_VER2.md` -> MATRIZ_DECISION_REVISIONES_VER2.md — decisión fila por fila sobre qué consume Global y por qué.
0030: - `LEDGER_REVISIONES_PRE_1_0.md` -> LEDGER_REVISIONES_PRE_1_0.md — ledger Markdown G001–G070 y candidato G071.
```

```text
0042: - `PREPARACION_PUBLICA_GITHUB.md` -> PREPARACION_PUBLICA_GITHUB.md — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público.
0043: - `AUDITORIA_REPOSITORIO_2026-08-18.md` -> AUDITORIA_REPOSITORIO_2026-08-18.md — auditoría integral local/remota post-GOV.1.
0044: - `AUDITORIA_UX46E_R7_2026-08-18.md` -> AUDITORIA_UX46E_R7_2026-08-18.md — auditoría transversal de coherencia de UX.4.6e.
0045: - `AUDITORIA_PLAN1_R4_2026-08-20.md` -> AUDITORIA_PLAN1_R4_2026-08-20.md — auditoría integral y gates R4.1/R4.2 de PLAN.1.
0046: - `CIERRE_GOV1.md` -> CIERRE_GOV1.md — evidencia definitiva del cierre GOV.1.
```

```text
0115: - `../tests/test_ver2_ledger_estructurado.py` -> ../tests/test_ver2_ledger_estructurado.py — regresiones del ledger JSON y sus invariantes.
0116: - `../tests/test_ver2_version_revision_aware.py` -> ../tests/test_ver2_version_revision_aware.py — regresiones del esquema revision-aware.
0117: - `../tests/test_ver2_documentacion_vigente.py` -> ../tests/test_ver2_documentacion_vigente.py — coherencia de superficies vigentes durante VER.2.
0118: - `../tests/validation_cases/README.md` -> ../tests/validation_cases/README.md — reglas de casos sintéticos/anonimizados.
0119: - `../.github/workflows/ci.yml` — CI funcional.
```

```text
0157: - `../CHANGELOG.md` -> ../CHANGELOG.md — cambios notables.
0158: - `../VERSIONING.md` -> ../VERSIONING.md — reglas de incremento y tags.
0159: - `AUDITORIA_VERSIONADO_PRE_1_0.md` -> AUDITORIA_VERSIONADO_PRE_1_0.md — reconciliación VER.2.
0160: - `LEDGER_REVISIONES_PRE_1_0.md` -> LEDGER_REVISIONES_PRE_1_0.md — contador global.
0161: - `../data/revision_ledger_pre_1_0.json` -> ../data/revision_ledger_pre_1_0.json — representación estructurada del contador.
```

```text
0181: <!-- ANCLAS_HISTORICAS_VER2_INDICE_CONSOLIDADAS -->
0182:
0183: ## Compatibilidad histórica preservada por VER.2
0184:
0185: - **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico de gobierno.
```

```text
0185: - **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico de gobierno.
0186: - UX.4.6e R9.2 queda preservado como cierre histórico asociado a `0.0.25-beta`.
0187: - La familia `0.0.N-beta` permanece como línea legacy histórica hasta `v0.0.26-beta`.
0188: - **Versión candidata de aplicación:** `0.0.26-beta` — referencia legacy preservada para las regresiones históricas de PLAN.1.
0189: - El contrato histórico mantiene versiones oficiales de cuatro componentes para la línea estable futura.
```

```text
0186: - UX.4.6e R9.2 queda preservado como cierre histórico asociado a `0.0.25-beta`.
0187: - La familia `0.0.N-beta` permanece como línea legacy histórica hasta `v0.0.26-beta`.
0188: - **Versión candidata de aplicación:** `0.0.26-beta` — referencia legacy preservada para las regresiones históricas de PLAN.1.
0189: - El contrato histórico mantiene versiones oficiales de cuatro componentes para la línea estable futura.
0190: - GOV.1.3 R3 preservó el snapshot archive/regulatory-privacy/ como evidencia histórica normativa y de privacidad.
```

```text
0190: - GOV.1.3 R3 preservó el snapshot archive/regulatory-privacy/ como evidencia histórica normativa y de privacidad.
0191:
0192: - AUDITORIA_NOMBRES_RESTANTES_R5H.md -> AUDITORIA_NOMBRES_RESTANTES_R5H.md — Auditoría MANT.1 R5H de nombres técnicos restantes.
0193:
0194: ## MANT.1 R6 — Auditoría funcional post-renombres
```

```text
0192: - AUDITORIA_NOMBRES_RESTANTES_R5H.md -> AUDITORIA_NOMBRES_RESTANTES_R5H.md — Auditoría MANT.1 R5H de nombres técnicos restantes.
0193:
0194: ## MANT.1 R6 — Auditoría funcional post-renombres
0195:
0196: - `AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md`: auditoría funcional posterior a los renombres técnicos de MANT.1 R5. Verifica rutas, plantillas, assets, contratos frontend/backend, formularios, cargas de archivo y estructura HTML renderizada.
```

```text
0194: ## MANT.1 R6 — Auditoría funcional post-renombres
0195:
0196: - `AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md`: auditoría funcional posterior a los renombres técnicos de MANT.1 R5. Verifica rutas, plantillas, assets, contratos frontend/backend, formularios, cargas de archivo y estructura HTML renderizada.
0197:
0198: ## MANT.1 R7 — Cierre operativo post-auditoría
```

```text
0196: - `AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md`: auditoría funcional posterior a los renombres técnicos de MANT.1 R5. Verifica rutas, plantillas, assets, contratos frontend/backend, formularios, cargas de archivo y estructura HTML renderizada.
0197:
0198: ## MANT.1 R7 — Cierre operativo post-auditoría
0199:
0200: - `CIERRE_OPERATIVO_POST_AUDITORIA_R7.md`: cierre operativo posterior a R5H/R6. Verifica estado de ramas, evidencias documentales, pruebas focalizadas y protección de archivos sensibles.
```

```text
0198: ## MANT.1 R7 — Cierre operativo post-auditoría
0199:
0200: - `CIERRE_OPERATIVO_POST_AUDITORIA_R7.md`: cierre operativo posterior a R5H/R6. Verifica estado de ramas, evidencias documentales, pruebas focalizadas y protección de archivos sensibles.
```

## docs/MATRIZ_TRAZABILIDAD.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Matriz de trazabilidad
0002:
0003: **Estado:** Vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Base histórica:** GOV.1.3 R4 — 2026-08-17
0007: **Revisión transversal:** VER.2 — 2026-08-21
0008: **Clasificación:** Técnica / Auditoría
0009:
0010: Esta matriz conecta contratos críticos del producto con su fuente, decisión, implementación y evidencia de prueba. No sustituye `ESPECIFICACION_FUNCIONAL.md` ni pretende afirmar cobertura granular completa de todos los RF históricos.
0011:
0012: ## 1. Convención
0013:
0014: | Campo | Significado |
0015: |---|---|
0016: | ID | identificador estable dentro de esta matriz |
0017: | Requisito/contrato | propiedad que el proyecto afirma |
0018: | Fuente/criterio | norma, fuente o `N/A — técnico/UX` |
0019: | ADR | decisión relevante |
0020: | Implementación | archivos principales |
0021: | Prueba | regresión principal |
0022: | Estado | nivel actual de trazabilidad |
0023:
0024: ## 2. Núcleo trazable
0025:
0026: | ID | Requisito/contrato | Fuente/criterio | ADR | Implementación | Prueba | Estado |
0027: |---|---|---|---|---|---|---|
0028: | TR-001 | Identidad independiente de la CSS | N/A — gobierno/producto | ADR-045 | `app/core/config.py`, `app/templates/base.html` | `tests/test_identidad_interfaz.py` | Verificado |
0029: | TR-002 | `VERSION` es fuente canónica | N/A — gobierno | ADR-157, ADR-158 | `VERSION`, `app/core/version.py`, `app/core/config.py` | `tests/test_gov12_versionado.py` | Verificado |
0030: | TR-003 | Datos históricos y proyectados permanecen separados | N/A — integridad de datos | ADR-006, ADR-073 | `app/services/timeline.py`, `app/services/results.py` | `tests/test_timeline.py`, `tests/test_results.py` | Verificado |
0031: | TR-004 | Precisión monetaria usa `Decimal` en operaciones sensibles | N/A — técnico | ADR-016 | `app/core/money.py` | `tests/test_money.py` | Verificado |
0032: | TR-005 | PDF se valida antes del parser y no se persiste por el endpoint | N/A — seguridad | ADR-074 | `app/core/pdf_files.py`, `app/main.py` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
0033: | TR-006 | Importación documental requiere vista previa/confirmación | N/A — UX/integridad | ADR-071 | `app/static/js/official_data_import.js` | `tests/test_ux44_importacion_oficial.py`, `tests/test_ux46b_paso1_datos_personales.py` | Verificado |
0034: | TR-007 | Ficha Digital limita el contexto importado al año objetivo y reconcilia al alza sin reducir silenciosamente | N/A — integridad de datos | ADR-072, ADR-103, ADR-155, ADR-156 | `app/services/ficha_digital.py`, `app/static/js/official_data_import.js` | `tests/test_ux46d_revision23_ficha_actualiza_cuotas.py` | Verificado |
0035: | TR-008 | SEBD mantiene clasificación/modalidades y parámetros versionados | Ley 51 / reglamentos CSS | ADR-023 a ADR-026 | `app/engines/sebd.py`, `app/engines/sebd_modalidades.py`, `regulations/sebd.json` | `tests/test_sebd.py`, `tests/test_sebd_modalidades.py` | Verificado técnico |
0036: | TR-009 | CAP Mixto no se reconstruye desde historial anual insuficiente | Ley 51 / normativa Mixto | ADR-027 a ADR-033 | `app/engines/mixto.py`, `regulations/mixto.json` | `tests/test_mixto.py`, `tests/test_mixto_prestaciones_cap.py` | Verificado técnico |
0037: | TR-010 | SUCGS separa contributivo, capa solidaria y garantía | Ley 51, arts. documentados | ADR-036 a ADR-040 | `app/engines/sucgs.py`, `regulations/sucgs.json` | `tests/test_sucgs.py`, `tests/test_sucgs_capa_solidaria.py`, `tests/test_sucgs_reemplazo.py` | Verificado técnico |
0038: | TR-011 | Trazabilidad explica el resultado y no recalcula | N/A — arquitectura/auditoría | ADR-042, ADR-043 | `app/models/traceability.py`, `app/services/traceability.py` | `tests/test_traceability.py` | Verificado |
0039: | TR-012 | Resultado final usa contrato transversal común | N/A — arquitectura | ADR-044 | `app/models/unified_result.py`, `app/services/unified_result.py` | `tests/test_unified_result.py` | Verificado |
0040: | TR-013 | Consentimiento es versionado y la sesión activa debe coincidir | Ley 81 / Decreto 285 como marco; control técnico interno | ADR-110, ADR-111, ADR-118 | `app/static/js/privacy.js` | `tests/test_ux46b_revision2_privacidad.py`, `tests/test_gov13_documentacion_r3.py` | Verificado técnico; revisión jurídica pendiente |
0041: | TR-014 | APIs de simulación usan `no-store` y cabeceras defensivas | N/A — seguridad | ADR-074 | `app/main.py` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
0042: | TR-015 | CI reproduce instalación, sintaxis y suite en Python 3.13/3.14 | N/A — calidad | ADR-075, ADR-076 | `.github/workflows/ci.yml`, `.github/dependabot.yml` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
0043: | TR-016 | Documentación vigente y evidencia histórica están separadas | N/A — gobierno | ADR-158 + GOV.1.3 | `docs/INDICE.md`, `docs/archive/` | `tests/test_gov13_documentacion.py`, `tests/test_gov13_documentacion_r2.py`, `tests/test_gov13_documentacion_r3.py` | Verificado |
0044: | TR-017 | Decisiones del Paso 3 y valores derivados distinguen ausencia de decisión, cálculo automático y edición del usuario | N/A — UX/integridad | ADR-169 | `app/static/js/simulation.js`, `app/static/js/salary_history.js`, `app/static/js/detalle_anio_actual.js`, `app/templates/simulation.html` | `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py` | Verificado UX.4.6f R1 |
0045: | TR-018 | El análisis de adjuntos comunica estado ocupado, evita duplicados y reutiliza un contrato global accesible | N/A — UX/accesibilidad | ADR-170 | `app/static/js/attachment_processing.js`, `app/static/js/official_data_import.js`, `app/static/js/referencia_mi_retiro_seguro.js` | `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py` | Verificado UX.4.6f R1 |
0046: | TR-019 | Los datos documentales detectados quedan bloqueados en la vista principal y se corrigen desde la revisión editable; los no detectados siguen completables | N/A — UX/integridad | ADR-171 | `app/static/js/procedencia_editable.js`, `app/static/css/design-system.css`, `app/static/css/procedencia-editable.css`, `app/static/js/salary_history.js` | `tests/test_ux46f_r11_bloqueo_documental_vista_principal.py` | Verificado UX.4.6f R1.1 |
0047: | TR-020 | La línea temporal valida coherencia Pasos 2–4, conserva salario mensual proyectado y distingue ausencia de cotización futura | N/A — técnico/integridad | ADR-172 | `app/models/simulation.py`, `app/services/timeline.py`, `app/static/js/timeline.js` | `tests/test_ux46f_r2_auditoria_paso4.py` | Verificado UX.4.6f R2 / PR #30 |
0048: | TR-021 | Las hipótesis salariales compuestas, la selección explícita de porcentajes, el salario futuro conocido y la procedencia del horizonte son explícitas | N/A — técnico/UX | ADR-173 | `app/models/simulation.py`, `app/services/salary_projection.py`, `app/static/js/simulation.js`, `app/static/js/retirement.js`, `app/templates/simulation.html` | `tests/test_ux46f_r2_auditoria_paso4.py` | Verificado UX.4.6f R2 / PR #30 |
0049: | TR-022 | Paso 5 deriva únicamente los escenarios posteriores cubiertos por Paso 4 y conserva las ediciones del usuario | N/A — técnico/UX | ADR-174 | `app/static/js/retirement.js`, `app/templates/partials/retirement.html`, `app/models/simulation.py` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
0050: | TR-023 | Retiro anticipado se solicita explícitamente, bloquea fechas transcurridas y la fecha de evaluación solo se admite dentro de la banda estándar | Ley 51 / reglamento CSS para componente SEBD aplicable | ADR-175 | `app/services/retirement.py`, `app/engines/elegibilidad.py`, `regulations/sebd.json`, `app/static/js/retirement.js` | `tests/test_ux46g_r1_retirement_scenarios.py`, `tests/test_retirement.py` | Verificado UX.4.6g / PR #32 |
0051: | TR-024 | Los controles de fecha validan año/calendario de forma transversal y Paso 5 muestra cobertura salarial de una fecha personalizada | N/A — técnico/UX | ADR-176 | `app/static/js/accessibility.js`, `app/static/css/accessibility.css`, `app/static/js/retirement.js`, `app/templates/partials/retirement.html` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
0052: | TR-025 | Alineación y densidad visual de períodos y resumen de retiro | N/A — UX/responsive | ADR-177 | `app/templates/partials/salary_history.html`, `app/templates/simulation.html`, `app/templates/partials/retirement.html`, `app/static/css/design-system.css` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
0053: | TR-026 | La guía pública explica cómo se transforman los datos de los Pasos 1–6 y los tres sistemas con parámetros versionados, fórmula general + sustitución numérica y términos definidos en contexto, sin duplicar motores; navbar, Metodología y Paso 6 enlazan sin transportar datos personales | N/A — transparencia/UX; normativa versionada existente | ADR-178 | `app/services/como_se_calcula.py`, `app/templates/como_se_calcula.html`, `app/static/css/como-se-calcula.css`, `app/templates/base.html`, `app/static/js/results_orchestration.js`, `app/templates/metodologia.html` | `tests/test_ux46i_r1_como_se_calcula.py` | Verificado UX.4.6i / PR #34 |
0054: | TR-027 | La beta revision-aware cuenta estados aceptados, preserva tags legacy y mantiene ledger continuo sin convertir commits/candidatos en revisiones | N/A — gobierno/versionado | ADR-179 | `VERSION`, `VERSIONING.md`, `app/core/version.py`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md` | `tests/test_ver2_version_revision_aware.py`, `tests/test_ver2_documentacion_vigente.py` | Candidato VER.2 G071/E01 |
0055:
0056: ## 3. Cobertura de RF
0057:
0058: `ESPECIFICACION_FUNCIONAL.md` conserva el ledger RF histórico. Esta matriz **no declara** que cada RF individual tenga ya una fila única requisito → ADR → archivo → test.
0059:
0060: El estado actual es:
0061:
0062: - contratos críticos: trazados en esta matriz;
0063: - ledger RF: preservado;
0064: - cobertura RF granular completa: **parcial / pendiente de ampliación**.
0065:
0066: Esta declaración evita confundir preservación histórica con cobertura de prueba demostrada.
0067:
0068: ## 4. Mantenimiento
0069:
0070: Una nueva fila debe usar una fuente normativa solo cuando exista relación real. Para UX, arquitectura, seguridad técnica o gobierno se utiliza `N/A — técnico/UX` o una descripción equivalente.
0071:
0072: No se inventan artículos legales para completar la tabla.
0073:
0074: Los estados `Candidato` deben promoverse a `Verificado` únicamente después del gate y cierre que corresponda. VER.2 debe actualizar TR-027 al integrar G071.
0075:
0076: <!-- ANCLAS_HISTORICAS_VER2_MATRIZ -->
0077:
0078: ## Anclas históricas preservadas por VER.2
0079:
0080: - Base histórica documental preservada: `0.0.23-beta`.
0081: - VER.2 añade TR-027 sin eliminar la evidencia de GOV.1.3 R4 ni la matriz previa.
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Base histórica:** GOV.1.3 R4 — 2026-08-17
```

```text
0003: **Estado:** Vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Base histórica:** GOV.1.3 R4 — 2026-08-17
0007: **Revisión transversal:** VER.2 — 2026-08-21
```

```text
0005: **Último tag formal legacy:** `v0.0.26-beta`
0006: **Base histórica:** GOV.1.3 R4 — 2026-08-17
0007: **Revisión transversal:** VER.2 — 2026-08-21
0008: **Clasificación:** Técnica / Auditoría
0009:
```

```text
0052: | TR-025 | Alineación y densidad visual de períodos y resumen de retiro | N/A — UX/responsive | ADR-177 | `app/templates/partials/salary_history.html`, `app/templates/simulation.html`, `app/templates/partials/retirement.html`, `app/static/css/design-system.css` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
0053: | TR-026 | La guía pública explica cómo se transforman los datos de los Pasos 1–6 y los tres sistemas con parámetros versionados, fórmula general + sustitución numérica y términos definidos en contexto, sin duplicar motores; navbar, Metodología y Paso 6 enlazan sin transportar datos personales | N/A — transparencia/UX; normativa versionada existente | ADR-178 | `app/services/como_se_calcula.py`, `app/templates/como_se_calcula.html`, `app/static/css/como-se-calcula.css`, `app/templates/base.html`, `app/static/js/results_orchestration.js`, `app/templates/metodologia.html` | `tests/test_ux46i_r1_como_se_calcula.py` | Verificado UX.4.6i / PR #34 |
0054: | TR-027 | La beta revision-aware cuenta estados aceptados, preserva tags legacy y mantiene ledger continuo sin convertir commits/candidatos en revisiones | N/A — gobierno/versionado | ADR-179 | `VERSION`, `VERSIONING.md`, `app/core/version.py`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md` | `tests/test_ver2_version_revision_aware.py`, `tests/test_ver2_documentacion_vigente.py` | Candidato VER.2 G071/E01 |
0055:
0056: ## 3. Cobertura de RF
```

```text
0072: No se inventan artículos legales para completar la tabla.
0073:
0074: Los estados `Candidato` deben promoverse a `Verificado` únicamente después del gate y cierre que corresponda. VER.2 debe actualizar TR-027 al integrar G071.
0075:
0076: <!-- ANCLAS_HISTORICAS_VER2_MATRIZ -->
```

```text
0076: <!-- ANCLAS_HISTORICAS_VER2_MATRIZ -->
0077:
0078: ## Anclas históricas preservadas por VER.2
0079:
0080: - Base histórica documental preservada: `0.0.23-beta`.
```

```text
0079:
0080: - Base histórica documental preservada: `0.0.23-beta`.
0081: - VER.2 añade TR-027 sin eliminar la evidencia de GOV.1.3 R4 ni la matriz previa.
```

## docs/PLAN_MAESTRO_HACIA_1_0.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Plan maestro hacia Mi Retiro Proyectado 1.0
0002:
0003: **Estado:** vigente
0004: **Versión base al iniciar el plan:** `0.0.25-beta`
0005: **Cierre histórico de PLAN.1:** `0.0.26-beta` / `v0.0.26-beta`
0006: **Versión candidata transversal VER.2:** `0.0.71.01-beta` — G071/E01
0007: **Fecha:** 2026-08-22
0008: **Clasificación:** Producto / Arquitectura / QA / Release
0009:
0010: ## 1. Propósito
0011:
0012: Este documento ordena el trabajo desde el cierre de `v0.0.25-beta` hasta la primera versión oficial de Mi Retiro Proyectado.
0013:
0014: PLAN.1 adoptó originalmente la familia beta legacy `0.0.N-beta`. VER.2, ejecutado después de UX.4.6i, conserva esa familia como historia publicada y adopta para **estados nuevos** el formato revision-aware:
0015:
0016: ```text
0017: 0.GG.RR.EE-beta
0018: ```
0019:
0020: La primera versión oficial objetivo continúa siendo:
0021:
0022: ```text
0023: 1.0.0.0
0024: Build 000001
0025: ```
0026:
0027: No se utilizará `0.1.0 beta 1` como etapa futura vigente.
0028:
0029: ## 2. Regla transversal de sincronización
0030:
0031: Todo cambio debe revisar de manera coordinada los artefactos que dependan de él:
0032:
0033: ```text
0034: Código
0035: ↕
0036: Pruebas
0037: ↕
0038: Interfaz
0039: ↕
0040: Normativa
0041: ↕
0042: Modelo de datos
0043: ↕
0044: Documentación técnica
0045: ↕
0046: Documentación pública
0047: ↕
0048: CHANGELOG / ROADMAP / RELEASES
0049: ↕
0050: ADR cuando exista una decisión arquitectónica
0051: ↕
0052: Git / versión / tag / Build cuando corresponda
0053: ```
0054:
0055: Un archivo no se modifica de forma aislada si el cambio altera contratos descritos en otros documentos o pruebas.
0056:
0057: Los comentarios y docstrings del runtime siguen el contrato de ADR-162: explican responsabilidades, motivos, límites y comportamiento permanente, no números cronológicos de fase.
0058:
0059: La metadata `Versión de aplicación revisada` de un documento de dominio registra la base en la que ese documento fue revisado. No constituye una copia canónica de la versión vigente ni obliga a reescribir documentos no afectados por cada incremento de `VERSION`.
0060:
0061: ## 3. Prerrequisito transversal VER.2
0062:
0063: VER.2 — Reconciliación revision-aware del historial pre-1.0 — **no es un bloque 15**. Es una corrección de gobierno necesaria antes de continuar el bloque 6, DEV.2.
0064:
0065: Base auditada:
0066:
0067: ```text
0068: main = 7037addd44253e528c77460b678d2b3ccd540dd5
0069: G070 / E02 = cierre UX.4.6i
0070: ```
0071:
0072: Candidato:
0073:
0074: ```text
0075: G071 / E01 = 0.0.71.01-beta
0076: ```
0077:
0078: G071 solo se considera aceptado después de gate completo, PR/CI e integración. Un candidato fallido no consume el número.
0079:
0080: Fuentes canónicas:
0081:
0082: - `VERSIONING.md`;
0083: - `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`;
0084: - `docs/LEDGER_REVISIONES_PRE_1_0.md`;
0085: - `docs/MATRIZ_DECISION_REVISIONES_VER2.md`;
0086: - `data/revision_ledger_pre_1_0.json`;
0087: - ADR de gobierno correspondiente.
0088:
0089: Mientras VER.2 permanezca abierto, **DEV.2 es el siguiente bloque funcional, no el bloque funcional iniciado**.
0090:
```

### Coincidencias con contexto

```text
0003: **Estado:** vigente
0004: **Versión base al iniciar el plan:** `0.0.25-beta`
0005: **Cierre histórico de PLAN.1:** `0.0.26-beta` / `v0.0.26-beta`
0006: **Versión candidata transversal VER.2:** `0.0.71.01-beta` — G071/E01
0007: **Fecha:** 2026-08-22
```

```text
0004: **Versión base al iniciar el plan:** `0.0.25-beta`
0005: **Cierre histórico de PLAN.1:** `0.0.26-beta` / `v0.0.26-beta`
0006: **Versión candidata transversal VER.2:** `0.0.71.01-beta` — G071/E01
0007: **Fecha:** 2026-08-22
0008: **Clasificación:** Producto / Arquitectura / QA / Release
```

```text
0012: Este documento ordena el trabajo desde el cierre de `v0.0.25-beta` hasta la primera versión oficial de Mi Retiro Proyectado.
0013:
0014: PLAN.1 adoptó originalmente la familia beta legacy `0.0.N-beta`. VER.2, ejecutado después de UX.4.6i, conserva esa familia como historia publicada y adopta para **estados nuevos** el formato revision-aware:
0015:
0016: ```text
```

```text
0057: Los comentarios y docstrings del runtime siguen el contrato de ADR-162: explican responsabilidades, motivos, límites y comportamiento permanente, no números cronológicos de fase.
0058:
0059: La metadata `Versión de aplicación revisada` de un documento de dominio registra la base en la que ese documento fue revisado. No constituye una copia canónica de la versión vigente ni obliga a reescribir documentos no afectados por cada incremento de `VERSION`.
0060:
0061: ## 3. Prerrequisito transversal VER.2
```

```text
0059: La metadata `Versión de aplicación revisada` de un documento de dominio registra la base en la que ese documento fue revisado. No constituye una copia canónica de la versión vigente ni obliga a reescribir documentos no afectados por cada incremento de `VERSION`.
0060:
0061: ## 3. Prerrequisito transversal VER.2
0062:
0063: VER.2 — Reconciliación revision-aware del historial pre-1.0 — **no es un bloque 15**. Es una corrección de gobierno necesaria antes de continuar el bloque 6, DEV.2.
```

```text
0061: ## 3. Prerrequisito transversal VER.2
0062:
0063: VER.2 — Reconciliación revision-aware del historial pre-1.0 — **no es un bloque 15**. Es una corrección de gobierno necesaria antes de continuar el bloque 6, DEV.2.
0064:
0065: Base auditada:
```

```text
0073:
0074: ```text
0075: G071 / E01 = 0.0.71.01-beta
0076: ```
0077:
```

```text
0087: - ADR de gobierno correspondiente.
0088:
0089: Mientras VER.2 permanezca abierto, **DEV.2 es el siguiente bloque funcional, no el bloque funcional iniciado**.
0090:
0091: ## 4. Secuencia de 14 bloques
```

```text
0103: - preservar sin reescritura la documentación histórica.
0104:
0105: **Estado de PLAN.1:** cerrado. R4.2 integró PR #23 y PR #24, superó los checks remotos, revalidó `main` con **720 pruebas en `OK`** sin `SyntaxWarning` y publicó el tag firmado `v0.0.26-beta` (`bfbb746b177ebcc577f7241fef4d6914f713739a` → `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`).
0106:
0107: Revisiones internas preservadas:
```

```text
0110: - **R2A/R2B1/R2B2/R2C:** alineación documental progresiva;
0111: - **R3A/R3B1/R3B2:** release, terminología, seguridad, privacidad/licencia y guard histórico;
0112: - **R4.1:** candidato local `0.0.26-beta`;
0113: - **R4.2:** commit/PR/CI, corrección de higiene, validación y tag firmado.
0114:
```

```text
0155: ### 5. UX.4.6i — Cómo se calcula
0156:
0157: **Estado:** cerrado mediante PR #34 con **841 pruebas**.
0158:
0159: La secuencia demostrada por la auditoría canónica es:
```

```text
0164: - **R1.4:** etiqueta visible **Ejemplo** y cierre aceptado G070.
0165:
0166: No existe una sección, gate ni artefacto independiente que sustente una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2; VER.2 corrige las referencias agregadas que la incluyeron por error.
0167:
0168: La explicación pública no duplica motores de cálculo en JavaScript y mantiene las fórmulas ejecutables en los motores Python existentes.
```

```text
0170: ### 6. DEV.2 — Centro de desarrollo
0171:
0172: **Estado:** siguiente bloque funcional; pendiente de inicio hasta cerrar VER.2.
0173:
0174: Evolución visible y controlada de Developer Diagnostics:
```

```text
0325: - el cierre formal siguió commit, PR, CI, squash, revalidación y tag aplicable.
0326:
0327: VER.2 no invalida ese cierre: corrige únicamente la granularidad y trazabilidad de la etapa beta posterior.
0328:
0329: <!-- ANCLAS_HISTORICAS_VER2_PLAN_CONSOLIDADAS -->
```

```text
0329: <!-- ANCLAS_HISTORICAS_VER2_PLAN_CONSOLIDADAS -->
0330:
0331: ## Compatibilidad histórica preservada por VER.2
0332:
0333: - **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico previo a PLAN.1.
```

```text
0332:
0333: - **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico previo a PLAN.1.
0334: - R4.1 — candidato local `0.0.26-beta`.
0335: - R4.2 integró el cierre de PLAN.1 mediante PR protegido y preservó `v0.0.26-beta`.
0336: - R4.2 — PR #23/#24 preservan la integración y saneamiento final de PLAN.1 antes del tag `v0.0.26-beta`.
```

```text
0333: - **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico previo a PLAN.1.
0334: - R4.1 — candidato local `0.0.26-beta`.
0335: - R4.2 integró el cierre de PLAN.1 mediante PR protegido y preservó `v0.0.26-beta`.
0336: - R4.2 — PR #23/#24 preservan la integración y saneamiento final de PLAN.1 antes del tag `v0.0.26-beta`.
0337: - Después de su cierre se habilitó UX.4.6g.
```

```text
0334: - R4.1 — candidato local `0.0.26-beta`.
0335: - R4.2 integró el cierre de PLAN.1 mediante PR protegido y preservó `v0.0.26-beta`.
0336: - R4.2 — PR #23/#24 preservan la integración y saneamiento final de PLAN.1 antes del tag `v0.0.26-beta`.
0337: - Después de su cierre se habilitó UX.4.6g.
```

## docs/PROCESO_RELEASE.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Proceso de release
0002:
0003: **Estado:** Vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Versión base histórica preservada:** `0.0.23-beta`
0008: **Base documental:** GOV.1.3 R4 — 2026-08-17
0009: **Revisión transversal:** VER.2 — versionado revision-aware — 2026-08-22
0010: **Clasificación:** Gobierno / Release / Auditoría
0011:
0012: Este procedimiento complementa `VERSIONING.md`, `RELEASES.md`, `CHANGELOG.md`, `GOVERNANCE.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `docs/LICENCIA_Y_DISTRIBUCION.md`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md`, `docs/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/revision_ledger_pre_1_0.json` y `docs/PLAN_MAESTRO_HACIA_1_0.md`.
0013:
0014: ## 1. Principio
0015:
0016: Un tag formal identifica un estado **cerrado, reproducible y validado**. No se etiqueta un árbol que todavía está pendiente de validación.
0017:
0018: La historia beta publicada conserva la familia legacy:
0019:
0020: ```text
0021: 0.0.N-beta
0022: ```
0023:
0024: Los estados beta nuevos posteriores a VER.2 usan:
0025:
0026: ```text
0027: 0.GG.RR.EE-beta
0028: ```
0029:
0030: La primera versión oficial objetivo usa cuatro componentes y se prevé inicialmente como `1.0.0.0`.
0031:
0032: El identificador `Build` es independiente de `VERSION`. No se inventa ni se incrementa por commit; se materializa cuando REL.1 disponga de un proceso reproducible de generación de artefactos oficiales.
0033:
0034: ## 2. Qué constituye una revisión aceptada
0035:
0036: Antes de preparar una nueva beta revision-aware debe verificarse que el cambio representa un **estado aceptado** según `VERSIONING.md` y el ledger.
0037:
0038: No consumen un nuevo `G` por sí solos:
0039:
0040: - commits separados de implementación, pruebas y documentación del mismo estado;
0041: - candidatos todavía pendientes de validación manual o automática;
0042: - un intento que falla su gate;
0043: - el PR, squash, CI o tag que únicamente materializa el mismo estado;
0044: - un checkpoint que solo consolida estados ya contabilizados y deja pendiente la siguiente revisión funcional.
0045:
0046: Sí puede consumir un nuevo `G` un estado de mantenimiento, seguridad, gobierno, dependencias o documentación cuando sea materialmente independiente, tenga evidencia propia de aceptación y constituya una configuración auditable distinta.
0047:
0048: El candidato reserva el siguiente número global, pero ese número solo queda consumido después del cierre satisfactorio. Si falla, se corrige conservando el mismo identificador reservado.
0049:
0050: ## 3. Precondiciones
0051:
0052: Antes del cierre:
0053:
0054: - hito funcional/técnico/documental terminado;
0055: - código, pruebas y documentación dependiente coherentes;
0056: - working tree controlado;
0057: - versión anterior y último `G` aceptado trazables;
0058: - siguiente `G` sin duplicados ni huecos en el ledger;
0059: - limitaciones conocidas actualizadas cuando corresponda;
0060: - licencia del proyecto coherente con el objetivo de distribución;
0061: - `THIRD_PARTY_NOTICES.md` revisado si el artefacto incluye componentes de terceros.
0062:
0063: ## 4. Validación del hito antes del incremento
0064:
0065: Ejecutar, como mínimo:
0066:
0067: ```powershell
0068: python -m pip check
0069: git diff --check
0070: python -m compileall app
0071:
0072: Get-ChildItem .\app\static\js\*.js | ForEach-Object {
0073:     node --check $_.FullName
0074:     if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
0075: }
0076:
0077: python -m unittest discover -s tests -q
0078: ```
0079:
0080: No se registra como “validado” un conteo que no se haya ejecutado realmente.
0081:
0082: Cuando una fase requiere validación manual, esa aceptación debe registrarse antes de declarar el estado cerrado.
0083:
0084: ## 5. Preparación del candidato
0085:
0086: Cuando el alcance está listo para gate:
0087:
0088: 1. confirmar el último estado aceptado del ledger;
0089: 2. reservar el siguiente `G` y el `EE` correspondiente al bloque;
0090: 3. construir el identificador según `VERSIONING.md`;
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
```

```text
0003: **Estado:** Vigente
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Versión base histórica preservada:** `0.0.23-beta`
```

```text
0004: **Versión candidata de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Versión base histórica preservada:** `0.0.23-beta`
0008: **Base documental:** GOV.1.3 R4 — 2026-08-17
```

```text
0007: **Versión base histórica preservada:** `0.0.23-beta`
0008: **Base documental:** GOV.1.3 R4 — 2026-08-17
0009: **Revisión transversal:** VER.2 — versionado revision-aware — 2026-08-22
0010: **Clasificación:** Gobierno / Release / Auditoría
0011:
```

```text
0022: ```
0023:
0024: Los estados beta nuevos posteriores a VER.2 usan:
0025:
0026: ```text
```

```text
0039:
0040: - commits separados de implementación, pruebas y documentación del mismo estado;
0041: - candidatos todavía pendientes de validación manual o automática;
0042: - un intento que falla su gate;
0043: - el PR, squash, CI o tag que únicamente materializa el mismo estado;
```

```text
0109: - comprobar `VERSION`, `APP_VERSION`, FastAPI y footer;
0110: - ejecutar el validador del ledger estructurado y comprobar que preserve G001–G070 sin huecos ni duplicados;
0111: - comprobar que `0.0.71.01-beta` siga identificado como candidato reservado mientras VER.2 no esté integrado;
0112: - comprobar README, ROADMAP, SECURITY, CHANGELOG, RELEASES y proceso de release;
0113: - comprobar que un candidato no se presente como tag/release ya publicado;
```

```text
0179:
0180: ```text
0181: v0.0.26-beta       # último tag legacy histórico
0182: v0.0.71.01-beta    # candidato VER.2, solo si corresponde etiquetarlo tras cierre
0183: v1.0.0.0
```

```text
0180: ```text
0181: v0.0.26-beta       # último tag legacy histórico
0182: v0.0.71.01-beta    # candidato VER.2, solo si corresponde etiquetarlo tras cierre
0183: v1.0.0.0
0184: v1.0.0.1
```

```text
0259: <!-- ANCLAS_HISTORICAS_VER2_PROCESO_CONSOLIDADAS -->
0260:
0261: ## Compatibilidad histórica preservada por VER.2
0262:
0263: - El cierre formal usa tag anotado y firmado cuando corresponde publicar un hito.
```

```text
0262:
0263: - El cierre formal usa tag anotado y firmado cuando corresponde publicar un hito.
0264: - La política de tags conserva la inmutabilidad de `v0.0.25-beta` y `v0.0.26-beta`.
0265: - Todo release con artefacto distribuible debe conservar inventario exacto del artefacto, avisos de terceros y correspondencia entre versión, Build, tag, hashes y contenido publicado.
0266: - Los releases con artefactos distribuibles deben revisar licencias/NOTICE upstream antes de publicar.
```

## docs/ROADMAP.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Roadmap
0002:
0003: **Estado:** vigente
0004: **Versión candidata:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Fecha de revisión:** 2026-08-22
0008: **Mantenimiento técnico en curso:** MANT.1 R5E — estandarización de nombres de carpetas antes de SEC.2; MANT.1 R5D conserva la política, plantillas y uniformidad por extensión; MANT.1 R1 conserva la auditoría inicial, MANT.1 R2 conserva la documentación de scripts y hooks antes de SEC.2, MANT.1 R3 conserva encabezados funcionales para YAML de GitHub, MANT.1 R4 limpia encabezados operativos, MANT.1 R5A documenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla y MANT.1 R5C comenta JavaScript complejo
0009:
0010: Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md`, `docs/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/revision_ledger_pre_1_0.json` y `docs/archive/`.
0011:
0012: VER.2 es un bloque transversal de reconciliación y **no añade un bloque 15** al plan maestro de producto. DEV.2 ya quedó cerrado documentalmente en R4. MANT.1 se trata como checkpoint técnico de mantenibilidad antes de SEC.2 y tampoco añade un bloque funcional de producto. MANT.1 R1 queda como auditoría inicial de alcance, MANT.1 R2 materializa los primeros cambios documentales en scripts y hooks, MANT.1 R3 documenta los YAML de GitHub sin cambiar CI ni formularios y MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica permanezca en documentación, MANT.1 R5A comenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla de la guía pública, MANT.1 R5C comenta JavaScript complejo sin cambiar lógica visible y MANT.1 R5D define política/plantillas por extensión con uniformidad de encabezados.
0013:
0014: ## 1. Programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta
0015:
0016: **Estado general:** cerrado el 2026-08-18.
0017:
0018: - [x] **GOV.1.1 — Inventario y reconstrucción histórica**
0019:   - inventario del repositorio;
0020:   - reconstrucción de 80 commits;
0021:   - clasificación retrospectiva `0.0.1-beta` a `0.0.21-beta`.
0022:
0023: - [x] **GOV.1.2 — Gobierno y versionado**
0024:   - `VERSION`;
0025:   - `VERSIONING.md`;
0026:   - `GOVERNANCE.md`;
0027:   - `RELEASES.md`;
0028:   - `.github/CODEOWNERS`;
0029:   - primera versión formal `0.0.22-beta`;
0030:   - tag `v0.0.22-beta`.
0031:
0032: - [x] **GOV.1.3 — Reorganización y alineación integral de documentación**
0033:   - [x] R1 — documentos de entrada, archivo histórico y estructura;
0034:   - [x] R2 — documentación técnica vigente;
0035:   - [x] R3 — normativa, seguridad y privacidad documental;
0036:   - [x] R4 — capa de auditoría documental y controles de consistencia;
0037:   - versión de cierre: `0.0.23-beta`.
0038:
0039: - [x] **Prebloque transversal — Firma e integridad Git/GitHub**
0040:   - [x] materialización y auditoría criptográfica de tags;
0041:   - [x] CI y protecciones GitHub;
0042:   - [x] corrección PowerShell/control characters;
0043:   - [x] actualización controlada a `pypdf 6.15.0`;
0044:   - [x] cierre formal del prebloque;
0045:   - cinco estados aceptados G027–G031 según la segunda auditoría de VER.2.
0046:
0047: - [x] **GOV.1.4 — Observabilidad y Developer Diagnostics**
0048:   - [x] modo exclusivo de desarrollo;
0049:   - [x] logging estructurado, correlación, redacción y retención local;
0050:   - [x] exportación diagnóstica controlada sin telemetría remota;
0051:   - [x] 13 regresiones específicas y suite de 487 pruebas en `OK`.
0052:
0053: - [x] **GOV.1.5 — Seguridad, privacidad y transparencia**
0054:   - [x] R1 — modelo de amenazas;
0055:   - [x] R2 — derechos del titular e incidentes;
0056:   - [x] R3 — cierre integral;
0057:   - tres estados aceptados G033–G035.
0058:
0059: - [x] **GOV.1.6 — Controles GitHub y auditoría automática** — G036.
0060: - [x] **GOV.1.7 — Licencia** — derechos de distribución — G037.
0061: - [x] **Hotfix de formato de licencia** — G038.
0062: - [x] **GOV.1.8 — Auditoría final y cierre de gobierno** — G039; `v0.0.24-beta`.
0063: - [x] **Saneamiento post-GOV.1** — G040.
0064:
0065: ## 2. Estado funcional del producto
0066:
0067: ### Implementado
0068:
0069: - asistente de seis pasos;
0070: - Paso 4 — proyección salarial/laboral auditado y cerrado en UX.4.6f;
0071: - Paso 5 — escenarios de retiro auditado y cerrado en UX.4.6g;
0072: - Paso 6 — resultados y exportación auditado y cerrado en UX.4.6h, con copia imprimible A4 provisional;
0073: - sección pública **Cómo se calcula** cerrada en UX.4.6i;
0074: - motores SEBD, Mixto y SUCGS para el alcance general documentado;
0075: - comparación y trazabilidad de cálculo;
0076: - metodología y fuentes;
0077: - importación revisable de Mi Retiro Seguro y Ficha Digital;
0078: - procedencia editable con fotografía documental original, copia de trabajo y exclusión explícita de períodos;
0079: - gestión local de datos de simulación;
0080: - temas Claro, Oscuro, Automático y Alto contraste;
0081: - base responsive y accesible;
0082: - identidad visual oficial, favicons y Social Preview;
0083: - repositorio público con metadata, topics, labels e Issue Forms;
0084: - Dependency graph, Dependabot, CodeQL, Secret Protection, Push protection y Private vulnerability reporting;
0085: - CI y auditoría automática de gobernanza;
0086: - DEV.2 — Centro de desarrollo sobre Developer Diagnostics cerrado documentalmente en R4.
0087:
0088: ### Pendiente o incompleto
0089:
0090: - VER.2 — cerrar reconciliación revision-aware y promover G071 si el gate completo, PR/CI e integración son satisfactorios;
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** vigente
0004: **Versión candidata:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
```

```text
0003: **Estado:** vigente
0004: **Versión candidata:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Fecha de revisión:** 2026-08-22
```

```text
0004: **Versión candidata:** `0.0.71.01-beta` — VER.2 G071/E01
0005: **Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Fecha de revisión:** 2026-08-22
0008: **Mantenimiento técnico en curso:** MANT.1 R5E — estandarización de nombres de carpetas antes de SEC.2; MANT.1 R5D conserva la política, plantillas y uniformidad por extensión; MANT.1 R1 conserva la auditoría inicial, MANT.1 R2 conserva la documentación de scripts y hooks antes de SEC.2, MANT.1 R3 conserva encabezados funcionales para YAML de GitHub, MANT.1 R4 limpia encabezados operativos, MANT.1 R5A documenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla y MANT.1 R5C comenta JavaScript complejo
```

```text
0006: **Último tag formal legacy:** `v0.0.26-beta`
0007: **Fecha de revisión:** 2026-08-22
0008: **Mantenimiento técnico en curso:** MANT.1 R5E — estandarización de nombres de carpetas antes de SEC.2; MANT.1 R5D conserva la política, plantillas y uniformidad por extensión; MANT.1 R1 conserva la auditoría inicial, MANT.1 R2 conserva la documentación de scripts y hooks antes de SEC.2, MANT.1 R3 conserva encabezados funcionales para YAML de GitHub, MANT.1 R4 limpia encabezados operativos, MANT.1 R5A documenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla y MANT.1 R5C comenta JavaScript complejo
0009:
0010: Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md`, `docs/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/revision_ledger_pre_1_0.json` y `docs/archive/`.
```

```text
0010: Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md`, `docs/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/revision_ledger_pre_1_0.json` y `docs/archive/`.
0011:
0012: VER.2 es un bloque transversal de reconciliación y **no añade un bloque 15** al plan maestro de producto. DEV.2 ya quedó cerrado documentalmente en R4. MANT.1 se trata como checkpoint técnico de mantenibilidad antes de SEC.2 y tampoco añade un bloque funcional de producto. MANT.1 R1 queda como auditoría inicial de alcance, MANT.1 R2 materializa los primeros cambios documentales en scripts y hooks, MANT.1 R3 documenta los YAML de GitHub sin cambiar CI ni formularios y MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica permanezca en documentación, MANT.1 R5A comenta servicios Python grandes, MANT.1 R5B comenta CSS/plantilla de la guía pública, MANT.1 R5C comenta JavaScript complejo sin cambiar lógica visible y MANT.1 R5D define política/plantillas por extensión con uniformidad de encabezados.
0013:
0014: ## 1. Programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta
```

```text
0043:   - [x] actualización controlada a `pypdf 6.15.0`;
0044:   - [x] cierre formal del prebloque;
0045:   - cinco estados aceptados G027–G031 según la segunda auditoría de VER.2.
0046:
0047: - [x] **GOV.1.4 — Observabilidad y Developer Diagnostics**
```

```text
0088: ### Pendiente o incompleto
0089:
0090: - VER.2 — cerrar reconciliación revision-aware y promover G071 si el gate completo, PR/CI e integración son satisfactorios;
0091: - MANT.1 — documentación, encabezados operativos y comentarios internos de mantenibilidad en Python, CSS, plantillas y JavaScript antes de SEC.2;
0092: - hardening integral SEC.2;
```

```text
0089:
0090: - VER.2 — cerrar reconciliación revision-aware y promover G071 si el gate completo, PR/CI e integración son satisfactorios;
0091: - MANT.1 — documentación, encabezados operativos y comentarios internos de mantenibilidad en Python, CSS, plantillas y JavaScript antes de SEC.2;
0092: - hardening integral SEC.2;
0093: - reconstrucción detallada del CHANGELOG `0.0.1-beta`–`0.0.21-beta` en DOC.2;
```

```text
0100: ## 3. UX.4.6 — trabajo funcional cerrado
0101:
0102: **Estado:** UX.4.6e y UX.4.6f–UX.4.6i cerrados. VER.2 reconcilia ahora su representación en la historia; no reabre sus funcionalidades.
0103:
0104: - [x] **UX.4.6e — Estandarización técnica, comentarios y coherencia de interfaz post-GOV.1**
```

```text
0103:
0104: - [x] **UX.4.6e — Estandarización técnica, comentarios y coherencia de interfaz post-GOV.1**
0105:   - [x] R1–R7 — G041–G047;
0106:   - [x] checkpoint pre-R8 — identidad visual/repositorio público, PR #20, 624 pruebas; estado material e independiente G048;
0107:   - [x] R8 — validación funcional/procedencia editable; R8.1 fue intermedia y R8.2/cierre documental materializa G049;
```

```text
0111:   - [x] R1, R2A, R2B1, R2B2, R2C, R3A, R3B1 y R3B2 — G051–G058;
0112:   - [x] R4.1 — cierre local aceptado con 720 pruebas, G059;
0113:   - [x] R4.2 — higiene post-merge y cierre pre-tag, G060; tag `v0.0.26-beta`.
0114:
0115: - [x] **UX.4.6f — Paso 4 · Proyección salarial/laboral**
```

```text
0132:   - [x] R1.2 — navegación, recorrido Pasos 1–6 y densidad visual; refinamiento interno;
0133:   - [x] R1.3 — ejemplos sustituidos, terminología y espaciado; refinamiento interno;
0134:   - [x] R1.4 — etiqueta **Ejemplo** y cierre PR #34 con 841 pruebas; G070.
0135:
0136: No existe una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2 demostrada por sección, gate o artefacto independiente; las referencias agregadas que la incluían se corrigen en VER.2.
```

```text
0134:   - [x] R1.4 — etiqueta **Ejemplo** y cierre PR #34 con 841 pruebas; G070.
0135:
0136: No existe una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2 demostrada por sección, gate o artefacto independiente; las referencias agregadas que la incluían se corrigen en VER.2.
0137:
0138: ## 4. PLAN.1, VER.2 y secuencia hacia 1.0
```

```text
0136: No existe una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2 demostrada por sección, gate o artefacto independiente; las referencias agregadas que la incluían se corrigen en VER.2.
0137:
0138: ## 4. PLAN.1, VER.2 y secuencia hacia 1.0
0139:
0140: **PLAN.1:** cerrado formalmente en `0.0.26-beta` con **720 pruebas en `OK`** y tag firmado `v0.0.26-beta`. La segunda auditoría reconoce diez estados aceptados G051–G060 dentro de su evolución.
```

```text
0138: ## 4. PLAN.1, VER.2 y secuencia hacia 1.0
0139:
0140: **PLAN.1:** cerrado formalmente en `0.0.26-beta` con **720 pruebas en `OK`** y tag firmado `v0.0.26-beta`. La segunda auditoría reconoce diez estados aceptados G051–G060 dentro de su evolución.
0141:
0142: **VER.2:** bloque transversal activo. La base anterior al cambio contiene **70 estados aceptados (G001–G070)**. El candidato `0.0.71.01-beta` representa G071/E01 y solo se acepta después del gate completo, PR/CI e integración.
```

```text
0140: **PLAN.1:** cerrado formalmente en `0.0.26-beta` con **720 pruebas en `OK`** y tag firmado `v0.0.26-beta`. La segunda auditoría reconoce diez estados aceptados G051–G060 dentro de su evolución.
0141:
0142: **VER.2:** bloque transversal activo. La base anterior al cambio contiene **70 estados aceptados (G001–G070)**. El candidato `0.0.71.01-beta` representa G071/E01 y solo se acepta después del gate completo, PR/CI e integración.
0143:
0144: **Checkpoint técnico actual:** MANT.1 R5D — política, plantillas y uniformidad por extensión antes de SEC.2.
```

```text
0142: **VER.2:** bloque transversal activo. La base anterior al cambio contiene **70 estados aceptados (G001–G070)**. El candidato `0.0.71.01-beta` representa G071/E01 y solo se acepta después del gate completo, PR/CI e integración.
0143:
0144: **Checkpoint técnico actual:** MANT.1 R5D — política, plantillas y uniformidad por extensión antes de SEC.2.
0145:
0146: Documentos canónicos de VER.2:
```

```text
0144: **Checkpoint técnico actual:** MANT.1 R5D — política, plantillas y uniformidad por extensión antes de SEC.2.
0145:
0146: Documentos canónicos de VER.2:
0147:
0148: - `AUDITORIA_VERSIONADO_PRE_1_0.md` — criterio contable y exclusiones;
```

## docs/VALIDACION.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Validación
0002:
0003: **Estado:** Vigente
0004: **Versión candidata revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Base documental histórica:** GOV.1.3 R4 — 2026-08-17
0007: **Revisión transversal histórica preservada:** UX.4.6e R8 — validación funcional y procedencia editable — 2026-08-19
0008: **Última revisión transversal:** UX.4.6f R2 integrada y cierre del Paso 4 — 2026-08-20
0009: **Revisión de mantenimiento:** MANT.1 R5D — política, plantillas y uniformidad por extensión — 2026-08-23
0010: **Clasificación:** Técnica / Calidad
0011:
0012: La estrategia combina pruebas automatizadas, CI, casos sintéticos/anonimizados y validación manual cuando una propiedad no puede demostrarse suficientemente con código.
0013:
0014: ## Validación MANT.1 R5H — nombres técnicos restantes
0015:
0016: MANT.1 R5H completa una segunda pasada sobre nombres técnicos restantes,
0017: sincronizando imports, rutas de assets, referencias de plantillas,
0018: documentación viva y pruebas automatizadas.
0019:
0020: Comandos ejecutados para el cierre local:
0021:
0022: ```powershell
0023: python -m compileall app tests -q
0024: python -m pytest -q --tb=short
0025: python -m unittest discover -s tests -q
0026: git diff --check
0027: ```
0028:
0029: Resultado observado:
0030:
0031: ```text
0032: 924 passed, 4749 subtests passed
0033: Ran 924 tests
0034: OK
0035: git diff --check: OK
0036: ```
0037:
0038: La revisión no cambia `VERSION`, `APP_VERSION`, motores previsionales,
0039: parámetros normativos, contratos JSON regulatorios, rutas públicas
0040: funcionales, claves de almacenamiento, ids, clases ni `_entregas/`.
0041:
0042: ## Validación MANT.1 R5E — nombres de carpetas técnicas
0043:
0044: MANT.1 R5E valida que las carpetas técnicas en español hayan sido renombradas a
0045: inglés y que las referencias internas queden sincronizadas.
0046:
0047: Comandos mínimos para el cierre local:
0048:
0049: ```powershell
0050: python -m pytest tests\test_mant1_r5e_nombres_carpetas.py -q
0051: python -m pytest tests\test_mant1_r5d_politica_extensiones.py tests\test_mant1_r5e_nombres_carpetas.py -q
0052: git diff --check
0053: python -m pytest -q
0054: python -m unittest discover -s tests -q
0055: ```
0056:
0057: La revisión no cambia `VERSION`, `APP_VERSION`, fórmulas previsionales, valores
0058: JSON, rutas públicas, ids, clases, selectores ni `_entregas/`.
0059:
0060: ## Validación MANT.1 R5D — política, plantillas y uniformidad por extensión
0061:
0062: MANT.1 R5D valida que exista una política formal por extensión, que las
0063: plantillas oficiales estén presentes con su extensión correspondiente y que los
0064: encabezados de JavaScript/CSS operativo sigan un patrón uniforme de propósito y
0065: alcance permanente.
0066:
0067: Comandos previstos:
0068:
0069: ```powershell
0070: python -m pytest tests\test_mant1_r5d_politica_extensiones.py -q
0071: python -m pytest tests\test_mant1_r5c_comentarios_js_app.py tests\test_mant1_r5d_politica_extensiones.py -q
0072: git diff --check
0073: python -m pytest -q
0074: ```
0075:
0076: La revisión no cambia `VERSION`, `APP_VERSION`, motores previsionales,
0077: normativa, rutas públicas, contratos JSON, claves de almacenamiento, selectores,
0078: ids, clases, textos visibles ni SEC.2.
0079:
0080: ## Validación MANT.1 R5C — comentarios internos en JavaScript complejo
0081:
0082: MANT.1 R5C valida que los módulos JavaScript revisados tengan comentarios
0083: internos de intención para almacenamiento, invalidación, borradores revisables,
0084: privacidad, adjuntos, comparación y resultados, sin cambiar claves, selectores,
0085: ids, clases, textos visibles ni lógica funcional.
0086:
0087: Comandos usados:
0088:
0089: ```powershell
0090: python -m pytest tests\test_mant1_r5c_comentarios_js_app.py -q
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión candidata revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Base documental histórica:** GOV.1.3 R4 — 2026-08-17
```

```text
0007: **Revisión transversal histórica preservada:** UX.4.6e R8 — validación funcional y procedencia editable — 2026-08-19
0008: **Última revisión transversal:** UX.4.6f R2 integrada y cierre del Paso 4 — 2026-08-20
0009: **Revisión de mantenimiento:** MANT.1 R5D — política, plantillas y uniformidad por extensión — 2026-08-23
0010: **Clasificación:** Técnica / Calidad
0011:
```

```text
0012: La estrategia combina pruebas automatizadas, CI, casos sintéticos/anonimizados y validación manual cuando una propiedad no puede demostrarse suficientemente con código.
0013:
0014: ## Validación MANT.1 R5H — nombres técnicos restantes
0015:
0016: MANT.1 R5H completa una segunda pasada sobre nombres técnicos restantes,
```

```text
0014: ## Validación MANT.1 R5H — nombres técnicos restantes
0015:
0016: MANT.1 R5H completa una segunda pasada sobre nombres técnicos restantes,
0017: sincronizando imports, rutas de assets, referencias de plantillas,
0018: documentación viva y pruebas automatizadas.
```

```text
0040: funcionales, claves de almacenamiento, ids, clases ni `_entregas/`.
0041:
0042: ## Validación MANT.1 R5E — nombres de carpetas técnicas
0043:
0044: MANT.1 R5E valida que las carpetas técnicas en español hayan sido renombradas a
```

```text
0042: ## Validación MANT.1 R5E — nombres de carpetas técnicas
0043:
0044: MANT.1 R5E valida que las carpetas técnicas en español hayan sido renombradas a
0045: inglés y que las referencias internas queden sincronizadas.
0046:
```

```text
0058: JSON, rutas públicas, ids, clases, selectores ni `_entregas/`.
0059:
0060: ## Validación MANT.1 R5D — política, plantillas y uniformidad por extensión
0061:
0062: MANT.1 R5D valida que exista una política formal por extensión, que las
```

```text
0060: ## Validación MANT.1 R5D — política, plantillas y uniformidad por extensión
0061:
0062: MANT.1 R5D valida que exista una política formal por extensión, que las
0063: plantillas oficiales estén presentes con su extensión correspondiente y que los
0064: encabezados de JavaScript/CSS operativo sigan un patrón uniforme de propósito y
```

```text
0078: ids, clases, textos visibles ni SEC.2.
0079:
0080: ## Validación MANT.1 R5C — comentarios internos en JavaScript complejo
0081:
0082: MANT.1 R5C valida que los módulos JavaScript revisados tengan comentarios
```

```text
0080: ## Validación MANT.1 R5C — comentarios internos en JavaScript complejo
0081:
0082: MANT.1 R5C valida que los módulos JavaScript revisados tengan comentarios
0083: internos de intención para almacenamiento, invalidación, borradores revisables,
0084: privacidad, adjuntos, comparación y resultados, sin cambiar claves, selectores,
```

```text
0098: normativa, rutas públicas, contratos JSON, claves de almacenamiento ni SEC.2.
0099:
0100: ## Validación MANT.1 R5B — comentarios internos en CSS y plantilla Cómo se calcula
0101:
0102: MANT.1 R5B valida que la hoja de estilos y la plantilla principal de la guía
```

```text
0100: ## Validación MANT.1 R5B — comentarios internos en CSS y plantilla Cómo se calcula
0101:
0102: MANT.1 R5B valida que la hoja de estilos y la plantilla principal de la guía
0103: pública tengan comentarios estructurales útiles, sin cambiar clases, ids, textos
0104: visibles, rutas ni lógica Jinja.
```

```text
0117: normativa, rutas públicas, contratos JSON ni SEC.2.
0118:
0119: ## Validación MANT.1 R5A — comentarios internos en servicios Python
0120:
0121: MANT.1 R5A valida que los servicios Python de aplicación revisados contengan
```

```text
0119: ## Validación MANT.1 R5A — comentarios internos en servicios Python
0120:
0121: MANT.1 R5A valida que los servicios Python de aplicación revisados contengan
0122: comentarios internos de intención para flujos complejos, sin introducir
0123: identificadores de revisión dentro del código operativo.
```

```text
0136: `VERSION`, `APP_VERSION` ni SEC.2.
0137:
0138: ## Validación MANT.1 R4 — encabezados operativos limpios
0139:
0140: MANT.1 R4 corrige la ubicación de trazabilidad histórica en archivos operativos.
```

```text
0138: ## Validación MANT.1 R4 — encabezados operativos limpios
0139:
0140: MANT.1 R4 corrige la ubicación de trazabilidad histórica en archivos operativos.
0141: La validación esperada debe confirmar que YAML, hooks y README técnicos conserven
0142: encabezados funcionales, sin declarar MANT.1 en sus primeras líneas.
```

```text
0140: MANT.1 R4 corrige la ubicación de trazabilidad histórica en archivos operativos.
0141: La validación esperada debe confirmar que YAML, hooks y README técnicos conserven
0142: encabezados funcionales, sin declarar MANT.1 en sus primeras líneas.
0143:
0144: Comandos mínimos para el cierre local:
```

```text
0208: UX.4.6e R4 cerró con **566 pruebas en `OK`** después de añadir 8 regresiones de documentación permanente del runtime. R5 añade **10 regresiones** sobre ayuda/contacto visible, repositorio, footer, botones de fuentes, badges, topics/labels documentados, Issue Forms y terceros de presentación. El objetivo de R5 es **576 pruebas en `OK`**, sin cambio de `VERSION`.
0209:
0210: UX.4.6e R5 cerró con **576 pruebas en `OK`**, YAML/Python/JavaScript válidos y `git diff --check` limpio. R6 añade **10 regresiones** de renumeración y metadata: secuencia vigente UX.4.6e–h, preservación de evidencia histórica, topics prioritariamente en español, alternativa controlada para SEBD y taxonomía de 21 labels. El objetivo de R6 es **586 pruebas en `OK`**, sin cambio de `VERSION`.
0211:
0212: UX.4.6e R6 cerró con **586 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios. R7 añade **12 regresiones de auditoría transversal** sobre secuencia documental vigente, docstrings, comentarios de runtime, namespace Web Storage, superficie visible post-GOV, enlaces Markdown, higiene textual/JSON y continuidad ADR. El objetivo de R7 es **598 pruebas en `OK`**, sin cambio de `VERSION`.
```

## GOVERNANCE.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Gobierno del proyecto
0002:
0003: **Proyecto:** Mi Retiro Proyectado
0004: **Estado:** vigente desde GOV.1.2
0005: **Fecha de adopción:** 2026-08-18
0006: **Última revisión:** PLAN.1 / ADR-168 — 2026-08-20
0007:
0008: ## 1. Propósito
0009:
0010: Este documento define quién mantiene el proyecto, cómo se adoptan decisiones y qué controles mínimos deben cumplirse antes de integrar cambios. Su finalidad es facilitar mantenimiento, revisión independiente y auditoría.
0011:
0012: ## 2. Mantenimiento actual
0013:
0014: El mantenedor y responsable de revisión actual del repositorio es:
0015:
0016: - **Rubén Enrique Cañizares Miranda** (`@recm0708`).
0017:
0018: `.github/CODEOWNERS` refleja esta responsabilidad técnica. CODEOWNERS no constituye una certificación jurídica ni una aprobación de la Caja de Seguro Social de Panamá.
0019:
0020: ## 3. Principios de gobierno
0021:
0022: 1. **Trazabilidad:** todo cambio relevante debe poder rastrearse desde Git hasta código, pruebas y documentación.
0023: 2. **Separación normativa:** las decisiones técnicas no deben presentarse como requisitos legales sin una fuente oficial.
0024: 3. **Transparencia:** no se introducen comportamientos deliberadamente ocultos al modelo documental y de auditoría del proyecto.
0025: 4. **Privacidad por defecto:** observabilidad y pruebas no justifican almacenar datos personales reales innecesarios.
0026: 5. **Reproducibilidad:** una afirmación técnica importante debe poder verificarse mediante código, prueba, fuente o procedimiento documentado.
0027: 6. **Historia preservada:** una decisión sustituida se marca como tal; no se elimina para aparentar que nunca existió.
0028: 7. **Independencia institucional:** el proyecto no debe presentarse como producto oficial de la CSS.
0029: 8. **Sincronización transversal:** cuando evoluciona un contrato compartido, se revisan conjuntamente código, pruebas, interfaz, normativa, documentación y evidencia de release que dependan de él.
0030:
0031: ## 4. Tipos de cambio
0032:
0033: ### 4.1. Funcionalidad y UX
0034:
0035: Requieren:
0036:
0037: - implementación;
0038: - regresiones automatizadas cuando sean razonables;
0039: - validación manual cuando el comportamiento sea visual o interactivo;
0040: - actualización de documentación dependiente.
0041:
0042: ### 4.2. Motores y normativa
0043:
0044: Todo cambio de fórmula, parámetro, fecha, tabla o interpretación previsional requiere:
0045:
0046: - fuente oficial identificable;
0047: - prueba de regresión;
0048: - actualización de `regulations/` cuando corresponda;
0049: - documentación técnica/normativa;
0050: - ADR cuando exista interpretación o decisión no trivial.
0051:
0052: ### 4.3. Seguridad, privacidad y observabilidad
0053:
0054: Requieren revisión de:
0055:
0056: - datos tratados;
0057: - datos registrados;
0058: - retención;
0059: - exposición externa;
0060: - mensajes de error;
0061: - documentación pública y técnica;
0062: - pruebas de no regresión.
0063:
0064: ### 4.4. Gobierno y releases
0065:
0066: Cambios en versionado, licencia, gobernanza, CI o proceso de publicación deben quedar documentados y no pueden depender únicamente de una convención oral.
0067:
0068: ## 5. Decisiones
0069:
0070: Las decisiones relevantes se documentan mediante ADR consecutivos en `docs/DECISIONES.md`.
0071:
0072: Un ADR puede estar:
0073:
0074: - vigente;
0075: - sustituido parcialmente;
0076: - sustituido;
0077: - rechazado, cuando resulte útil conservar la alternativa evaluada.
0078:
0079: Una decisión antigua no se borra solo porque una revisión posterior cambie el criterio.
0080:
0081: ## 6. Integración a `main`
0082:
0083: Antes de integrar un hito cerrado se exige, como mínimo:
0084:
0085: ```powershell
0086: python -m compileall app
0087: python -m unittest discover -s tests -q
0088: git diff --check
0089: ```
0090:
```

### Coincidencias con contexto

- Sin coincidencias de riesgo detectadas.

## README.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: <p align="center">
0002:   <img
0003:     src="assets/brand/logos/logo-mark-512.png"
0004:     alt="Logo de Mi Retiro Proyectado"
0005:     width="132"
0006:   >
0007: </p>
0008:
0009: # Mi Retiro Proyectado
0010:
0011: ![Validación continua -> https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/ci.yml/badge.svg?branch=main](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/ci.yml)
0012: ![Auditoría de gobernanza -> https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/governance-audit.yml/badge.svg?branch=main](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/governance-audit.yml)
0013: !Versión -> https://img.shields.io/badge/versi%C3%B3n-0.0.71.01--beta-2563eb
0014: !Python -> https://img.shields.io/badge/Python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white
0015: !Licencia -> https://img.shields.io/badge/licencia-propietaria-6B7280
0016:
0017: Mi Retiro Proyectado es una aplicación web local e independiente para **estimar, explicar y comparar escenarios de retiro** de personas aseguradas de la Caja de Seguro Social (CSS) de Panamá.
0018:
0019: > **No es una aplicación oficial de la CSS.** No emite certificaciones, no sustituye una resolución administrativa y sus resultados dependen de los datos suministrados, de las reglas implementadas y de la normativa aplicable a cada caso.
0020:
0021: ## Estado del proyecto
0022:
0023: - **Versión candidata de VER.2:** `0.0.71.01-beta` — G071/E01; solo se considera aceptada después de ledger/validador, gate completo, PR/CI e integración.
0024: - **Último estado aceptado reconstruido antes de VER.2:** G070/E02 — cierre UX.4.6i sobre `7037addd44253e528c77460b678d2b3ccd540dd5` con **841 pruebas en `OK`**.
0025: - **Última versión formal legacy etiquetada:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
0026: - **Etapa:** desarrollo beta; repositorio de código público y ejecución de aplicación orientada actualmente a entorno local.
0027: - **Programa GOV.1:** cerrado — Auditoría, Gobierno y Trazabilidad Pre-Beta.
0028: - **Programa PLAN.1:** cerrado — Alineación maestra hacia la primera versión oficial.
0029: - **PLAN.1:** cerrado en el esquema legacy `0.0.26-beta`; PR #23 y PR #24 integrados, **720 pruebas en `OK`** en el gate final y tag firmado `v0.0.26-beta` publicado.
0030: - **Bloque funcional cerrado:** DEV.2 — Centro de desarrollo integrado por PR #37–#40 y cerrado documentalmente en R4.
0031: - **Siguiente bloque funcional:** DEV.2 — referencia histórica preservada para regresiones VER.2; el estado vigente de DEV.2 es cerrado documentalmente en R4.
0032: - **Bloque transversal activo:** VER.2 — cierre transversal de versionado revision-aware todavía pendiente de integración final.
0033: - **Bloque transversal pendiente:** VER.2 — cierre final de versionado revision-aware y sincronización de ledger, `VERSIONING.md`, `README`, `CHANGELOG` y documentación relacionada.
0034:
0035: - **UX.4.6e:** cerrada históricamente en `0.0.25-beta`; la segunda auditoría distribuye R1–R7, identidad/publicación, R8 y R9/cierre en G041–G050.
0036: - **UX.4.6f:** cerrado — R1/R1.1 integradas mediante PR #28, mantenimiento de dependencias por PR #29, R2 por PR #30 y hardening `pre-commit` por PR #31; **762 pruebas** en el último estado del tramo, G061–G064.
0037: - **Mantenimiento post-R1:** `pypdf 6.16.1` y `Uvicorn 0.52.3` integrados mediante PR #29; PR Dependabot #26/#27 cerrados como sustituidos, con los tres checks requeridos en verde.
0038: - **UX.4.6g:** cerrado — PR #32; selección contextual desde Paso 4, retiro anticipado explícito, +4 años, cobertura de fechas personalizadas, controles de fecha transversales y alineación visual final; **784 pruebas en `OK`**, G065.
0039: - **UX.4.6h:** cerrado — R1 fue candidato fallido; R1.1, R1.2 y R1.3 son los estados aceptados G066–G068; PR #33 cerró el informe A4 con **812 pruebas**.
0040: - **UX.4.6i:** cerrado — la secuencia demostrada es R1 → R1.2 → R1.3 → R1.4; R1 y R1.4 son los estados con aceptación diferenciada contabilizados G069–G070; PR #34 cerró la guía pública `/como-se-calcula` con **841 pruebas**. No existe una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2 independiente.
0041: - **Preparación pública del repositorio:** 21 labels y 20/20 topics configurados; `sebd-panama` adoptado como topic SEBD; Social Preview e identidad visual oficial configurados.
0042: - **Seguridad del repositorio público:** Dependency graph, Dependabot, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting habilitados; revisión manual del 2026-08-19 sin alertas abiertas.
0043: - **Primera versión oficial objetivo:** `1.0.0.0` con `Build 000001`, únicamente después de cerrar todos los gates definidos en el plan maestro.
0044:
0045: La visibilidad pública del repositorio **no convierte una beta de desarrollo en versión oficial, no constituye un despliegue de producción y no modifica por sí sola la licencia vigente**.
0046:
0047: La versión se obtiene exclusivamente del archivo `VERSION` -> VERSION. La política completa se documenta en `VERSIONING.md` -> VERSIONING.md. La reconciliación actual se audita en `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` -> docs/AUDITORIA_VERSIONADO_PRE_1_0.md y `docs/MATRIZ_DECISION_REVISIONES_VER2.md` -> docs/MATRIZ_DECISION_REVISIONES_VER2.md; el contador global se materializa en `docs/LEDGER_REVISIONES_PRE_1_0.md` -> docs/LEDGER_REVISIONES_PRE_1_0.md y `data/revision_ledger_pre_1_0.json` -> data/revision_ledger_pre_1_0.json. La secuencia restante hacia 1.0 se mantiene en `docs/PLAN_MAESTRO_HACIA_1_0.md` -> docs/PLAN_MAESTRO_HACIA_1_0.md.
0048:
0049: ## Capacidades implementadas
0050:
0051: La aplicación dispone de un asistente de seis pasos para:
0052:
0053: 1. registrar datos personales y previsionales;
0054: 2. analizar cuotas acreditadas y supuestos de cotización futura;
0055: 3. construir y revisar historial salarial, detalle del año actual e información proveniente de documentos compatibles;
0056: 4. proyectar escenarios salariales;
0057: 5. construir escenarios de retiro;
0058: 6. calcular, explicar y comparar resultados previsionales.
0059:
0060: Los tres motores generales principales implementados son:
0061:
0062: - **SEBD — Subsistema Exclusivamente de Beneficio Definido**;
0063: - **Subsistema Mixto**;
0064: - **SUCGS — Sistema Único de Capitalización con Garantía Solidaria**.
0065:
0066: El alcance jurídico y matemático exacto de cada motor se encuentra en la documentación normativa y técnica. No debe asumirse que el motor general cubre regímenes especiales no documentados.
0067:
0068: La aplicación dispone además de **Developer Diagnostics** para desarrollo. Está desactivado por defecto y solo se activa mediante `MRP_DEV_MODE=1`; no constituye telemetría de producto ni envía logs automáticamente a terceros.
0069:
0070: ## Principios de diseño
0071:
0072: El proyecto aplica estos criterios:
0073:
0074: - fórmulas previsionales en Python, no duplicadas en JavaScript;
0075: - parámetros normativos versionados en `regulations/`;
0076: - separación explícita entre datos acreditados y proyectados;
0077: - trazabilidad de fuentes, decisiones e hipótesis;
0078: - datos faltantes explícitos en vez de parámetros inventados;
0079: - procesamiento local y minimización de datos personales;
0080: - observabilidad de desarrollo sin logging de PII ni valores financieros;
0081: - pruebas automatizadas y CI antes de cerrar hitos;
0082: - documentación como parte obligatoria de cada cambio;
0083: - sincronización de código, pruebas, interfaz, normativa y documentación cuando un cambio altera contratos compartidos.
0084:
0085: ## Documentación
0086:
0087: El punto de entrada de la documentación es `docs/INDICE.md` -> docs/INDICE.md.
0088:
0089: Documentos principales:
0090:
```

### Coincidencias con contexto

```text
0019: > **No es una aplicación oficial de la CSS.** No emite certificaciones, no sustituye una resolución administrativa y sus resultados dependen de los datos suministrados, de las reglas implementadas y de la normativa aplicable a cada caso.
0020:
0021: ## Estado del proyecto
0022:
0023: - **Versión candidata de VER.2:** `0.0.71.01-beta` — G071/E01; solo se considera aceptada después de ledger/validador, gate completo, PR/CI e integración.
```

```text
0021: ## Estado del proyecto
0022:
0023: - **Versión candidata de VER.2:** `0.0.71.01-beta` — G071/E01; solo se considera aceptada después de ledger/validador, gate completo, PR/CI e integración.
0024: - **Último estado aceptado reconstruido antes de VER.2:** G070/E02 — cierre UX.4.6i sobre `7037addd44253e528c77460b678d2b3ccd540dd5` con **841 pruebas en `OK`**.
0025: - **Última versión formal legacy etiquetada:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
```

```text
0022:
0023: - **Versión candidata de VER.2:** `0.0.71.01-beta` — G071/E01; solo se considera aceptada después de ledger/validador, gate completo, PR/CI e integración.
0024: - **Último estado aceptado reconstruido antes de VER.2:** G070/E02 — cierre UX.4.6i sobre `7037addd44253e528c77460b678d2b3ccd540dd5` con **841 pruebas en `OK`**.
0025: - **Última versión formal legacy etiquetada:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
0026: - **Etapa:** desarrollo beta; repositorio de código público y ejecución de aplicación orientada actualmente a entorno local.
```

```text
0023: - **Versión candidata de VER.2:** `0.0.71.01-beta` — G071/E01; solo se considera aceptada después de ledger/validador, gate completo, PR/CI e integración.
0024: - **Último estado aceptado reconstruido antes de VER.2:** G070/E02 — cierre UX.4.6i sobre `7037addd44253e528c77460b678d2b3ccd540dd5` con **841 pruebas en `OK`**.
0025: - **Última versión formal legacy etiquetada:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
0026: - **Etapa:** desarrollo beta; repositorio de código público y ejecución de aplicación orientada actualmente a entorno local.
0027: - **Programa GOV.1:** cerrado — Auditoría, Gobierno y Trazabilidad Pre-Beta.
```

```text
0027: - **Programa GOV.1:** cerrado — Auditoría, Gobierno y Trazabilidad Pre-Beta.
0028: - **Programa PLAN.1:** cerrado — Alineación maestra hacia la primera versión oficial.
0029: - **PLAN.1:** cerrado en el esquema legacy `0.0.26-beta`; PR #23 y PR #24 integrados, **720 pruebas en `OK`** en el gate final y tag firmado `v0.0.26-beta` publicado.
0030: - **Bloque funcional cerrado:** DEV.2 — Centro de desarrollo integrado por PR #37–#40 y cerrado documentalmente en R4.
0031: - **Siguiente bloque funcional:** DEV.2 — referencia histórica preservada para regresiones VER.2; el estado vigente de DEV.2 es cerrado documentalmente en R4.
```

```text
0029: - **PLAN.1:** cerrado en el esquema legacy `0.0.26-beta`; PR #23 y PR #24 integrados, **720 pruebas en `OK`** en el gate final y tag firmado `v0.0.26-beta` publicado.
0030: - **Bloque funcional cerrado:** DEV.2 — Centro de desarrollo integrado por PR #37–#40 y cerrado documentalmente en R4.
0031: - **Siguiente bloque funcional:** DEV.2 — referencia histórica preservada para regresiones VER.2; el estado vigente de DEV.2 es cerrado documentalmente en R4.
0032: - **Bloque transversal activo:** VER.2 — cierre transversal de versionado revision-aware todavía pendiente de integración final.
0033: - **Bloque transversal pendiente:** VER.2 — cierre final de versionado revision-aware y sincronización de ledger, `VERSIONING.md`, `README`, `CHANGELOG` y documentación relacionada.
```

```text
0030: - **Bloque funcional cerrado:** DEV.2 — Centro de desarrollo integrado por PR #37–#40 y cerrado documentalmente en R4.
0031: - **Siguiente bloque funcional:** DEV.2 — referencia histórica preservada para regresiones VER.2; el estado vigente de DEV.2 es cerrado documentalmente en R4.
0032: - **Bloque transversal activo:** VER.2 — cierre transversal de versionado revision-aware todavía pendiente de integración final.
0033: - **Bloque transversal pendiente:** VER.2 — cierre final de versionado revision-aware y sincronización de ledger, `VERSIONING.md`, `README`, `CHANGELOG` y documentación relacionada.
0034:
```

```text
0031: - **Siguiente bloque funcional:** DEV.2 — referencia histórica preservada para regresiones VER.2; el estado vigente de DEV.2 es cerrado documentalmente en R4.
0032: - **Bloque transversal activo:** VER.2 — cierre transversal de versionado revision-aware todavía pendiente de integración final.
0033: - **Bloque transversal pendiente:** VER.2 — cierre final de versionado revision-aware y sincronización de ledger, `VERSIONING.md`, `README`, `CHANGELOG` y documentación relacionada.
0034:
0035: - **UX.4.6e:** cerrada históricamente en `0.0.25-beta`; la segunda auditoría distribuye R1–R7, identidad/publicación, R8 y R9/cierre en G041–G050.
```

```text
0033: - **Bloque transversal pendiente:** VER.2 — cierre final de versionado revision-aware y sincronización de ledger, `VERSIONING.md`, `README`, `CHANGELOG` y documentación relacionada.
0034:
0035: - **UX.4.6e:** cerrada históricamente en `0.0.25-beta`; la segunda auditoría distribuye R1–R7, identidad/publicación, R8 y R9/cierre en G041–G050.
0036: - **UX.4.6f:** cerrado — R1/R1.1 integradas mediante PR #28, mantenimiento de dependencias por PR #29, R2 por PR #30 y hardening `pre-commit` por PR #31; **762 pruebas** en el último estado del tramo, G061–G064.
0037: - **Mantenimiento post-R1:** `pypdf 6.16.1` y `Uvicorn 0.52.3` integrados mediante PR #29; PR Dependabot #26/#27 cerrados como sustituidos, con los tres checks requeridos en verde.
```

```text
0038: - **UX.4.6g:** cerrado — PR #32; selección contextual desde Paso 4, retiro anticipado explícito, +4 años, cobertura de fechas personalizadas, controles de fecha transversales y alineación visual final; **784 pruebas en `OK`**, G065.
0039: - **UX.4.6h:** cerrado — R1 fue candidato fallido; R1.1, R1.2 y R1.3 son los estados aceptados G066–G068; PR #33 cerró el informe A4 con **812 pruebas**.
0040: - **UX.4.6i:** cerrado — la secuencia demostrada es R1 → R1.2 → R1.3 → R1.4; R1 y R1.4 son los estados con aceptación diferenciada contabilizados G069–G070; PR #34 cerró la guía pública `/como-se-calcula` con **841 pruebas**. No existe una una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2 independiente.
0041: - **Preparación pública del repositorio:** 21 labels y 20/20 topics configurados; `sebd-panama` adoptado como topic SEBD; Social Preview e identidad visual oficial configurados.
0042: - **Seguridad del repositorio público:** Dependency graph, Dependabot, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting habilitados; revisión manual del 2026-08-19 sin alertas abiertas.
```

```text
0108: - `docs/PREPARACION_PUBLICA_GITHUB.md` -> docs/PREPARACION_PUBLICA_GITHUB.md — metadata, topics, labels, badges, seguridad y mantenimiento del repositorio público;
0109: - `docs/AUDITORIA_REPOSITORIO_2026-08-18.md` -> docs/AUDITORIA_REPOSITORIO_2026-08-18.md — auditoría integral post-GOV.1 del repositorio;
0110: - `docs/AUDITORIA_UX46E_R7_2026-08-18.md` -> docs/AUDITORIA_UX46E_R7_2026-08-18.md — auditoría transversal de coherencia de UX.4.6e;
0111: - `docs/CIERRE_GOV1.md` -> docs/CIERRE_GOV1.md — auditoría final y decisión de cierre de GOV.1;
0112: - `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` -> docs/AUDITORIA_VERSIONADO_PRE_1_0.md — criterio contable y reconciliación VER.2;
```

```text
0110: - `docs/AUDITORIA_UX46E_R7_2026-08-18.md` -> docs/AUDITORIA_UX46E_R7_2026-08-18.md — auditoría transversal de coherencia de UX.4.6e;
0111: - `docs/CIERRE_GOV1.md` -> docs/CIERRE_GOV1.md — auditoría final y decisión de cierre de GOV.1;
0112: - `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` -> docs/AUDITORIA_VERSIONADO_PRE_1_0.md — criterio contable y reconciliación VER.2;
0113: - `docs/MATRIZ_DECISION_REVISIONES_VER2.md` -> docs/MATRIZ_DECISION_REVISIONES_VER2.md — decisiones de inclusión/exclusión del contador;
0114: - `docs/LEDGER_REVISIONES_PRE_1_0.md` -> docs/LEDGER_REVISIONES_PRE_1_0.md — secuencia global G001–G070 y candidato G071;
```

```text
0129: `0.0.1-beta` a `0.0.21-beta` son **estados reconstruidos retrospectivamente** a partir del historial Git. No fueron tags publicados en sus fechas originales.
0130:
0131: `0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.
0132:
0133: Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.
```

```text
0131: `0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.
0132:
0133: Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.
0134:
0135: La nueva familia beta usa `0.GG.RR.EE-beta`. El candidato actual de reconciliación es `0.0.71.01-beta` (G071/E01). Solo se convierte en estado aceptado si supera el ledger/validador, gate completo, PR/CI e integración; no se crean tags revision-aware retrospectivos para G001–G070.
```

```text
0133: Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.
0134:
0135: La nueva familia beta usa `0.GG.RR.EE-beta`. El candidato actual de reconciliación es `0.0.71.01-beta` (G071/E01). Solo se convierte en estado aceptado si supera el ledger/validador, gate completo, PR/CI e integración; no se crean tags revision-aware retrospectivos para G001–G070.
0136:
0137: Objetivo de release estable:
```

```text
0303: <!-- ANCLAS_HISTORICAS_VER2_README_CONSOLIDADAS -->
0304:
0305: ## Compatibilidad histórica preservada por VER.2
0306:
0307: Estas referencias conservan evidencia de regresiones históricas sin cambiar el estado vigente de VER.2.
```

```text
0305: ## Compatibilidad histórica preservada por VER.2
0306:
0307: Estas referencias conservan evidencia de regresiones históricas sin cambiar el estado vigente de VER.2.
0308:
0309: - **Versión candidata de VER.2:** `0.0.26-beta` — referencia legacy preservada para las pruebas históricas previas a la reconciliación revision-aware.
```

```text
0307: Estas referencias conservan evidencia de regresiones históricas sin cambiar el estado vigente de VER.2.
0308:
0309: - **Versión candidata de VER.2:** `0.0.26-beta` — referencia legacy preservada para las pruebas históricas previas a la reconciliación revision-aware.
0310: - **GOV.1.8:** Auditoría final y cierre pre-beta de gobierno preservado como cierre histórico del programa GOV.1.
0311: - **GOV.1.4:** Observabilidad y Developer Diagnostics cerrado.
```

## RELEASES.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Registro de versiones y estados del proyecto
0002:
0003: **Fecha de reconstrucción histórica:** 2026-08-17
0004: **Fuente:** historial Git de `recm0708/mi-retiro-proyectado`
0005: **Revisión de planificación hacia 1.0:** 2026-08-20
0006: **Reconciliación revision-aware:** 2026-08-22
0007:
0008: ## 1. Naturaleza del registro
0009:
0010: Las versiones `0.0.1-beta` a `0.0.21-beta` fueron asignadas retrospectivamente en GOV.1.1 para organizar estados funcionales que ya existían en Git. No fueron tags ni GitHub Releases publicados en sus fechas originales. La migración criptográfica del 2026-08-17 permitió materializarlas posteriormente como tags firmados, conservando explícitamente esa naturaleza retrospectiva.
0011:
0012: Git conserva la evidencia primaria: hashes, fechas, autores, mensajes y contenido. Este documento añade una clasificación legible sin reescribir esa evidencia.
0013:
0014: El commit raíz real es `a0a9e09` (`tipo: descripción del cambio`). Su mensaje es una anomalía histórica previa a la convención posterior y se conserva sin modificar.
0015:
0016: VER.2 añade una segunda capa de auditoría: `docs/LEDGER_REVISIONES_PRE_1_0.md` y `data/revision_ledger_pre_1_0.json` reconstruyen los **estados aceptados** como G001–G070 sobre la base `7037addd44253e528c77460b678d2b3ccd540dd5`. Esos identificadores revision-aware no sustituyen versiones/tags históricos ni autorizan tags retroactivos. `0.0.71.01-beta` es únicamente el candidato de VER.2 mientras no complete gate, PR/CI e integración.
0017:
0018: ## 2. Estados retrospectivos
0019:
0020: | Versión | Fecha de cierre | Rango Git | Commits | Hito |
0021: |---|---|---|---:|---|
0022: | `0.0.1-beta` | 2026-08-10 | `a0a9e09` → `13ce028` | 6 | Base técnica, FastAPI, primera interfaz, asistente, cuotas, salario y documentación inicial. |
0023: | `0.0.2-beta` | 2026-08-11 | `ae45943` → `eafe54d` | 3 | Historial salarial, proyección y línea temporal. |
0024: | `0.0.3-beta` | 2026-08-11 | `a7e1ed4` → `78e5188` | 4 | Retiro, precisión monetaria, pruebas y protección de datos de validación. |
0025: | `0.0.4-beta` | 2026-08-11 | `563d6c4` → `2d4dfd0` | 7 | Motor SEBD, modalidades e Indemnización por Vejez. |
0026: | `0.0.5-beta` | 2026-08-11 | `d41682c` → `8a7e381` | 3 | Motores Mixto y SUCGS. |
0027: | `0.0.6-beta` | 2026-08-11 | `fa5348f` → `e087d6e` | 4 | Organización del repositorio, centralización normativa y casos de validación. |
0028: | `0.0.7-beta` | 2026-08-12 | `c442ec2` → `e956ea9` | 4 | Comparador, trazabilidad, resultado unificado y cierre funcional de Fase 6. |
0029: | `0.0.8-beta` | 2026-08-12 | `6d4c2d8` → `d599ee2` | 3 | UX.3: responsive y precisión del corte mensual de cuotas. |
0030: | `0.0.9-beta` | 2026-08-12 | `376a967` → `e6b02dc` | 4 | Identidad, temas, accesibilidad y terminología pública. |
0031: | `0.0.10-beta` | 2026-08-12 | `3f2f5d7` → `8feb682` | 6 | Mantenimiento técnico: LF, favicon temporal, estructura y respaldos. |
0032: | `0.0.11-beta` | 2026-08-12 | `c2da494` → `1f350f6` | 3 | UX.4.1: accesibilidad y ayudas contextuales. |
0033: | `0.0.12-beta` | 2026-08-12 | `5607cc1` → `6e6b33b` | 3 | UX.4.2: estados activos y selección perceptible. |
0034: | `0.0.13-beta` | 2026-08-12 | `b671c9a` → `9f849d0` | 2 | UX.4.3: validación accesible, teclado, errores y estabilidad. |
0035: | `0.0.14-beta` | 2026-08-13 | `5ca39ac` → `f4a0d45` | 6 | UX.4.4: edad anual, detalle salarial e importación documental. |
0036: | `0.0.15-beta` | 2026-08-13 | `88a1d14` → `3430f2e` | 3 | UX.4.5: información acreditada frente a proyectada y cierre accesible. |
0037: | `0.0.16-beta` | 2026-08-13 | `338db37` → `6f138da` | 4 | Hardening PDF, privacidad, regresión E2E, CI y Dependabot. |
0038: | `0.0.17-beta` | 2026-08-13 | `488aff5` → `e55190b` | 3 | Estrategia reproducible de dependencias pre-beta. |
0039: | `0.0.18-beta` | 2026-08-13 | `429201a` → `11aefca` | 3 | UX.4.6a: rediseño visual integral. |
0040: | `0.0.19-beta` | 2026-08-13 | `e6c2310` → `83a67ed` | 3 | UX.4.6b: Paso 1, datos personales, privacidad e importación. |
0041: | `0.0.20-beta` | 2026-08-13 | `e80d15e` → `2a69fb8` | 3 | UX.4.6c: Paso 2, cuotas e importación contextual. |
0042: | `0.0.21-beta` | 2026-08-17 | `05232df` → `7941f58` | 3 | UX.4.6d: Paso 3, Ficha Digital, sincronización de Pasos 1–3 y cierre integral. |
0043:
0044: **Total reconstruido:** 80 commits en 21 estados documentales.
0045:
0046: ## 3. Marcador histórico `0.1.0`
0047:
0048: El repositorio nació con `0.1.0` escrito en la configuración, README y CHANGELOG. No existió un tag ni una GitHub Release que materializara ese número. GOV.1 lo clasifica como **marcador de desarrollo no publicado**.
0049:
0050: No se elimina esta evidencia de la historia Git. El estado actual se corrige hacia una política explícita sin alterar commits antiguos.
0051:
0052: ## 4. Versiones formales legacy desde GOV.1.2
0053:
0054: ### `0.0.22-beta` — 2026-08-17
0055:
0056: Primera versión adoptada conscientemente bajo `VERSIONING.md`.
0057:
0058: Alcance del hito:
0059:
0060: - política formal de gobierno;
0061: - política formal de versionado;
0062: - archivo canónico `VERSION`;
0063: - carga centralizada de versión en Python;
0064: - CODEOWNERS;
0065: - registro histórico de releases/estados;
0066: - regresiones para impedir divergencias entre archivo canónico, FastAPI y footer;
0067: - validación final con compilación Python, JavaScript válido, `git diff --check` limpio y **403 pruebas automatizadas en OK**.
0068:
0069: El tag formal asociado es `v0.0.22-beta`.
0070:
0071: ### `0.0.23-beta` — 2026-08-17
0072:
0073: Segunda versión formal y cierre de GOV.1.3.
0074:
0075: Alcance del hito:
0076:
0077: - R1: reorganización de documentos de entrada y archivo histórico;
0078: - R2: consolidación de documentación técnica vigente;
0079: - R3: consolidación normativa, seguridad y privacidad documental;
0080: - R4: transparencia, matriz de trazabilidad, auditoría de cálculos, limitaciones conocidas, dependencias/terceros y proceso de release;
0081: - `DECISIONES.md` indexado sin reescribir sus 158 ADR;
0082: - ADR-086 registrada como anomalía histórica de metadata;
0083: - regresiones antiguas de gobierno/documentación endurecidas para seguir la versión canónica.
0084:
0085: Validación de cierre:
0086:
0087: - **458 pruebas automatizadas en `OK`**;
0088: - compilación Python correcta;
0089: - sintaxis JavaScript correcta;
0090: - `git diff --check` limpio.
```

### Coincidencias con contexto

```text
0014: El commit raíz real es `a0a9e09` (`tipo: descripción del cambio`). Su mensaje es una anomalía histórica previa a la convención posterior y se conserva sin modificar.
0015:
0016: VER.2 añade una segunda capa de auditoría: `docs/LEDGER_REVISIONES_PRE_1_0.md` y `data/revision_ledger_pre_1_0.json` reconstruyen los **estados aceptados** como G001–G070 sobre la base `7037addd44253e528c77460b678d2b3ccd540dd5`. Esos identificadores revision-aware no sustituyen versiones/tags históricos ni autorizan tags retroactivos. `0.0.71.01-beta` es únicamente el candidato de VER.2 mientras no complete gate, PR/CI e integración.
0017:
0018: ## 2. Estados retrospectivos
```

```text
0133: No se declara una versión oficial de producto con este hito.
0134:
0135: ### `0.0.26-beta` — 2026-08-20 — cierre formal de PLAN.1
0136:
0137: Quinta versión formal legacy.
```

```text
0141: - `v0.0.25-beta` permanece inmutable;
0142: - R1–R3 cerraron progresivamente con 665, 670, 676, 684, 689, 695, 702 y **710 pruebas**;
0143: - R4.1 promovió `VERSION`/`APP_VERSION` a `0.0.26-beta` y cerró localmente con **720 pruebas**;
0144: - commit firmado: `7c50d989f5c6d266db26c9625367dd82e9895aba`;
0145: - PR #23 integrado por squash en `497097f720c98f6e5a7ed689cf91368011a96be1`;
```

```text
0148: - checks Python 3.13, Python 3.14 y Auditoría de gobernanza en `success`;
0149: - gate final post-merge: **720 pruebas en `OK`** sin `SyntaxWarning`;
0150: - tag formal: `v0.0.26-beta`;
0151: - objeto tag firmado: `bfbb746b177ebcc577f7241fef4d6914f713739a`;
0152: - target: `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`.
```

```text
0152: - target: `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`.
0153:
0154: `v0.0.26-beta` es inmutable y no debe moverse ni recrearse.
0155:
0156: La segunda pasada de VER.2 reconoce dentro de PLAN.1 diez estados aceptados G051–G060: R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2. Esta granularidad revision-aware no crea ni mueve tags históricos.
```

```text
0154: `v0.0.26-beta` es inmutable y no debe moverse ni recrearse.
0155:
0156: La segunda pasada de VER.2 reconoce dentro de PLAN.1 diez estados aceptados G051–G060: R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2. Esta granularidad revision-aware no crea ni mueve tags históricos.
0157:
0158: ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2
```

```text
0156: La segunda pasada de VER.2 reconoce dentro de PLAN.1 diez estados aceptados G051–G060: R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2. Esta granularidad revision-aware no crea ni mueve tags históricos.
0157:
0158: ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2
0159:
0160: UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.
```

```text
0158: ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2
0159:
0160: UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.
0161:
0162: La base inmediatamente anterior a VER.2 es:
```

```text
0160: UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.
0161:
0162: La base inmediatamente anterior a VER.2 es:
0163:
0164: ```text
```

```text
0164: ```text
0165: 7037addd44253e528c77460b678d2b3ccd540dd5
0166: G070 / E02 — cierre UX.4.6i — 841 pruebas
0167: ```
0168:
```

```text
0167: ```
0168:
0169: VER.2 usa como **candidato**, no como release publicada:
0170:
0171: ```text
```

```text
0170:
0171: ```text
0172: 0.0.71.01-beta
0173: G071 / E01
0174: ```
```

```text
0174: ```
0175:
0176: Mientras el PR de VER.2 no supere el gate completo y se integre:
0177:
0178: - G071 permanece reservado, no aceptado;
```

```text
0177:
0178: - G071 permanece reservado, no aceptado;
0179: - no existe tag `v0.0.71.01-beta`;
0180: - `v0.0.26-beta` continúa siendo el último tag formal legacy;
0181: - no se crean tags revision-aware retrospectivos para G001–G070.
```

```text
0178: - G071 permanece reservado, no aceptado;
0179: - no existe tag `v0.0.71.01-beta`;
0180: - `v0.0.26-beta` continúa siendo el último tag formal legacy;
0181: - no se crean tags revision-aware retrospectivos para G001–G070.
0182:
```

```text
0181: - no se crean tags revision-aware retrospectivos para G001–G070.
0182:
0183: Si VER.2 se integra satisfactoriamente, `0.0.71.01-beta` pasa a ser el primer estado nuevo gobernado por la familia revision-aware. La creación de su tag, si corresponde al cierre, se realizará únicamente después de merge y revalidación.
0184:
0185: La distribución del contador aceptado hasta G070 se conserva de forma auditable en `docs/MATRIZ_DECISION_REVISIONES_VER2.md`, `docs/LEDGER_REVISIONES_PRE_1_0.md` y `data/revision_ledger_pre_1_0.json`; los intentos fallidos, refinamientos sin aceptación independiente y checkpoints absorbidos se preservan como evidencia sin consumir un `G` adicional.
```

```text
0197: - 23/23 targets remotos comprobados;
0198: - `v0.0.22-beta`: `31accfc9a6014367179c97cfe54c5a223be8988f` → `bda764edb84ccaeb610a629fca1283bbd97e69a4`, conservando `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5`;
0199: - `v0.0.23-beta`: `609edf4bfed33c64770c88fab401002cd90f8e66` → `06b9260dadbcb2f0a7711841e1fad228e1badee8`, conservando `07278f7a193ce964612d9697da57350691bf62c0`.
0200:
0201: Desde entonces los tags publicados son inmutables. `v0.0.24-beta`, `v0.0.25-beta` y `v0.0.26-beta` fueron creados posteriormente bajo la política formal y elevan el inventario a 26 tags firmados legacy/retrospectivos.
```

```text
0199: - `v0.0.23-beta`: `609edf4bfed33c64770c88fab401002cd90f8e66` → `06b9260dadbcb2f0a7711841e1fad228e1badee8`, conservando `07278f7a193ce964612d9697da57350691bf62c0`.
0200:
0201: Desde entonces los tags publicados son inmutables. `v0.0.24-beta`, `v0.0.25-beta` y `v0.0.26-beta` fueron creados posteriormente bajo la política formal y elevan el inventario a 26 tags firmados legacy/retrospectivos.
0202:
0203: ## 7. Línea beta revision-aware y versión oficial futura
```

## SECURITY.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Política de seguridad
0002:
0003: ## Versiones soportadas
0004:
0005: Mi Retiro Proyectado se encuentra en **desarrollo beta**. Los estados históricos conservan la familia legacy `0.0.N-beta`; VER.2 adopta para candidatos y estados nuevos la familia revision-aware `0.GG.RR.EE-beta`. El repositorio de código es público, pero la aplicación no se declara todavía como versión oficial ni como despliegue de producción.
0006:
0007: | Línea | Soporte de seguridad |
0008: |---|---|
0009: | `0.0.71.01-beta` | Candidata vigente de VER.2; recibe correcciones sobre la rama de reconciliación hasta cerrar su gate |
0010: | `0.0.26-beta` | Soportada como beta vigente legacy/candidata de VER.2 para regresiones históricas; último hito formal legacy etiquetado |
0011: | `0.0.25-beta` y anteriores | Históricas; no reciben correcciones independientes |
0012:
0013: La base histórica anterior a VER.2 se reconstruye en G001–G070 sin crear tags retroactivos. G071 solo se considera aceptado después del ledger/validador, gate completo, PR/CI e integración.
0014:
0015: La primera versión oficial objetivo es `1.0.0.0` y solo podrá considerarse soportada cuando se materialice formalmente después de los gates definidos por el plan maestro.
0016:
0017: La numeración revision-aware no mueve ni recrea tags legacy. Consultar `VERSIONING.md`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/MATRIZ_DECISION_REVISIONES_VER2.md` y `docs/LEDGER_REVISIONES_PRE_1_0.md`.
0018:
0019: ## Reportar una vulnerabilidad
0020:
0021: **No publique una vulnerabilidad explotable como issue público.**
0022:
0023: Canal preferido para el repositorio público:
0024:
0025: - **GitHub Private vulnerability reporting**, mediante la opción privada de reporte de vulnerabilidades del repositorio.
0026:
0027: Canal privado alternativo:
0028:
0029: `ruben.canizares@outlook.com`
0030:
0031: Incluya, si es posible y usando evidencia sintética o sanitizada: componente/ruta, versión o SHA, impacto, pasos mínimos y mitigación conocida.
0032:
0033: No envíe cédulas/NSS reales, PDFs personales, historiales salariales reales, secretos ni dumps completos de Developer Diagnostics sin revisión.
0034:
0035: ## Controles del repositorio público
0036:
0037: La configuración vigente incluye, según evidencia manual del mantenedor:
0038:
0039: - Dependency graph;
0040: - Dependabot alerts;
0041: - Dependabot security updates;
0042: - CodeQL con Default setup;
0043: - Secret Protection / secret scanning;
0044: - Push protection;
0045: - Private vulnerability reporting.
0046:
0047: Estos controles reducen riesgo y facilitan detección/reporte; no constituyen una garantía de ausencia de vulnerabilidades.
0048:
0049: ## Tratamiento del reporte
0050:
0051: El mantenedor confirma recepción cuando sea razonablemente posible, clasifica el evento, contiene exposiciones activas, preserva evidencia mínima, corrige y añade regresiones cuando proceda, y evalúa comunicaciones/notificaciones conforme a `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`.
0052:
0053: No existe un SLA contractual de respuesta.
0054:
0055: ## Divulgación coordinada
0056:
0057: Se solicita no publicar detalles explotables antes de que exista una corrección o mitigación razonable, salvo obligación legal o riesgo urgente.
0058:
0059: ## GitHub Private vulnerability reporting
0060:
0061: Esta función está habilitada y complementa el canal privado alternativo indicado arriba. Los Issues públicos no deben utilizarse para vulnerabilidades explotables.
0062:
0063: ## Documentos relacionados
0064:
0065: - `docs/MODELO_AMENAZAS.md`
0066: - `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`
0067: - `docs/SEGURIDAD_PRIVACIDAD.md`
0068: - `docs/AUDITORIA_GITHUB.md`
0069: - `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`
0070: - `docs/MATRIZ_DECISION_REVISIONES_VER2.md`
0071: - `docs/LEDGER_REVISIONES_PRE_1_0.md`
0072: - `data/revision_ledger_pre_1_0.json`
0073:
0074: <!-- ANCLAS_HISTORICAS_VER2_SECURITY_CONSOLIDADAS -->
0075:
0076: ## Compatibilidad histórica preservada por VER.2
0077:
0078: | Versión | Estado de soporte |
0079: | --- | --- |
0080: | `0.0.71.01-beta` | Candidata vigente de VER.2; Soportada durante la rama de reconciliación hasta cerrar su gate |
0081: | `0.0.26-beta` | Candidata vigente de VER.2 como referencia legacy preservada por las pruebas históricas; último hito formal legacy etiquetado |
```

### Coincidencias con contexto

```text
0003: ## Versiones soportadas
0004:
0005: Mi Retiro Proyectado se encuentra en **desarrollo beta**. Los estados históricos conservan la familia legacy `0.0.N-beta`; VER.2 adopta para candidatos y estados nuevos la familia revision-aware `0.GG.RR.EE-beta`. El repositorio de código es público, pero la aplicación no se declara todavía como versión oficial ni como despliegue de producción.
0006:
0007: | Línea | Soporte de seguridad |
```

```text
0007: | Línea | Soporte de seguridad |
0008: |---|---|
0009: | `0.0.71.01-beta` | Candidata vigente de VER.2; recibe correcciones sobre la rama de reconciliación hasta cerrar su gate |
0010: | `0.0.26-beta` | Soportada como beta vigente legacy/candidata de VER.2 para regresiones históricas; último hito formal legacy etiquetado |
0011: | `0.0.25-beta` y anteriores | Históricas; no reciben correcciones independientes |
```

```text
0008: |---|---|
0009: | `0.0.71.01-beta` | Candidata vigente de VER.2; recibe correcciones sobre la rama de reconciliación hasta cerrar su gate |
0010: | `0.0.26-beta` | Soportada como beta vigente legacy/candidata de VER.2 para regresiones históricas; último hito formal legacy etiquetado |
0011: | `0.0.25-beta` y anteriores | Históricas; no reciben correcciones independientes |
0012:
```

```text
0011: | `0.0.25-beta` y anteriores | Históricas; no reciben correcciones independientes |
0012:
0013: La base histórica anterior a VER.2 se reconstruye en G001–G070 sin crear tags retroactivos. G071 solo se considera aceptado después del ledger/validador, gate completo, PR/CI e integración.
0014:
0015: La primera versión oficial objetivo es `1.0.0.0` y solo podrá considerarse soportada cuando se materialice formalmente después de los gates definidos por el plan maestro.
```

```text
0074: <!-- ANCLAS_HISTORICAS_VER2_SECURITY_CONSOLIDADAS -->
0075:
0076: ## Compatibilidad histórica preservada por VER.2
0077:
0078: | Versión | Estado de soporte |
```

```text
0078: | Versión | Estado de soporte |
0079: | --- | --- |
0080: | `0.0.71.01-beta` | Candidata vigente de VER.2; Soportada durante la rama de reconciliación hasta cerrar su gate |
0081: | `0.0.26-beta` | Candidata vigente de VER.2 como referencia legacy preservada por las pruebas históricas; último hito formal legacy etiquetado |
```

```text
0079: | --- | --- |
0080: | `0.0.71.01-beta` | Candidata vigente de VER.2; Soportada durante la rama de reconciliación hasta cerrar su gate |
0081: | `0.0.26-beta` | Candidata vigente de VER.2 como referencia legacy preservada por las pruebas históricas; último hito formal legacy etiquetado |
```

## VERSIONING.md

- Categoría DOC.1 R1: `ACTUALIZAR`
- Existe: `True`

### Primeras líneas

```text
0001: # Política de versionado
0002:
0003: **Proyecto:** Mi Retiro Proyectado
0004: **Estado:** vigente desde GOV.1.2; revisada por PLAN.1 y VER.2
0005: **Fecha de adopción:** 2026-08-17
0006: **Revisión de transición a versión oficial:** 2026-08-19
0007: **Revisión revision-aware:** 2026-08-22
0008:
0009: ## 1. Objetivo
0010:
0011: Esta política identifica de forma auditable cada estado aceptado de Mi Retiro Proyectado y evita que versión visible, API, documentación, artefactos y Git describan estados diferentes.
0012:
0013: VER.2 corrige una limitación de la política original `0.0.N-beta`: los hitos formales estaban bien identificados, pero las revisiones internas aceptadas entre releases no podían expresarse sin inventar betas retrospectivas o confundir commits con revisiones.
0014:
0015: ## 2. Fuentes canónicas
0016:
0017: La fuente canónica de la versión de aplicación es el archivo raíz `VERSION`.
0018:
0019: - `VERSION` contiene una sola línea con la versión de la aplicación.
0020: - `app/core/version.py` valida y expone ese valor a Python.
0021: - `app/core/config.py` importa `APP_VERSION`; no mantiene una copia literal.
0022: - FastAPI usa `APP_VERSION` como versión de la aplicación.
0023: - Jinja2 recibe `app_version` y el footer muestra el mismo valor.
0024: - El contador y la procedencia de revisiones aceptadas se auditan en `docs/LEDGER_REVISIONES_PRE_1_0.md` y `data/revision_ledger_pre_1_0.json`.
0025: - `app/core/version_ledger.py` valida continuidad, unicidad y codificación del ledger estructurado.
0026: - La regla que determina qué cuenta y qué no cuenta se documenta en `docs/MATRIZ_DECISION_REVISIONES_VER2.md` y `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`.
0027: - README, CHANGELOG, RELEASES, ROADMAP y el ledger deben corresponder al estado vigente cuando lo describan como actual.
0028: - Los documentos de dominio pueden conservar la versión en la que fueron revisados; esa metadata es histórica de revisión documental y no una segunda fuente de la versión vigente.
0029: - La numeración de **Build** es independiente de `VERSION` y solo se materializa cuando exista un proceso reproducible de generación de artefactos oficiales.
0030:
0031: No se deben introducir versiones independientes en plantillas, JavaScript, motores o normativa.
0032:
0033: ## 3. Familias admitidas
0034:
0035: Mi Retiro Proyectado reconoce tres familias de identificadores.
0036:
0037: ### 3.1. Familia beta legacy histórica
0038:
0039: La historia ya publicada conserva:
0040:
0041: ```text
0042: 0.0.N-beta
0043: ```
0044:
0045: Ejemplos:
0046:
0047: ```text
0048: 0.0.22-beta
0049: 0.0.25-beta
0050: 0.0.26-beta
0051: ```
0052:
0053: Esta familia sigue siendo válida para leer y auditar estados históricos. Los tags `v0.0.1-beta` a `v0.0.26-beta` no se renombran ni se mueven.
0054:
0055: Después del cierre de VER.2, **los estados beta nuevos no continúan incrementando esta familia legacy**.
0056:
0057: ### 3.2. Familia beta revision-aware
0058:
0059: Los candidatos y estados nuevos gobernados por VER.2 usan:
0060:
0061: ```text
0062: 0.GG.RR.EE-beta
0063: ```
0064:
0065: Donde:
0066:
0067: - `G` es el contador global de estados aceptados;
0068: - `GG = G // 100`;
0069: - `RR = G % 100`, siempre con dos dígitos;
0070: - `EE` es el ordinal aceptado dentro del bloque vigente, siempre con dos dígitos entre `01` y `99`.
0071:
0072: Ejemplos:
0073:
0074: ```text
0075: G001 / E01 -> 0.0.01.01-beta
0076: G070 / E02 -> 0.0.70.02-beta
0077: G071 / E01 -> 0.0.71.01-beta
0078: G100 / E03 -> 0.1.00.03-beta
0079: G425 / E12 -> 0.4.25.12-beta
0080: ```
0081:
0082: Los identificadores revision-aware usados en el ledger para G001–G070 son **identificadores de reconstrucción/auditoría**. No existieron como versiones publicadas y no autorizan tags retroactivos.
0083:
0084: ### 3.3. Versiones oficiales
0085:
0086: Cuando todos los gates de producto se hayan cerrado, la primera versión oficial prevista sigue siendo:
0087:
0088: ```text
0089: 1.0.0.0
0090: ```
```

### Coincidencias con contexto

```text
0002:
0003: **Proyecto:** Mi Retiro Proyectado
0004: **Estado:** vigente desde GOV.1.2; revisada por PLAN.1 y VER.2
0005: **Fecha de adopción:** 2026-08-17
0006: **Revisión de transición a versión oficial:** 2026-08-19
```

```text
0011: Esta política identifica de forma auditable cada estado aceptado de Mi Retiro Proyectado y evita que versión visible, API, documentación, artefactos y Git describan estados diferentes.
0012:
0013: VER.2 corrige una limitación de la política original `0.0.N-beta`: los hitos formales estaban bien identificados, pero las revisiones internas aceptadas entre releases no podían expresarse sin inventar betas retrospectivas o confundir commits con revisiones.
0014:
0015: ## 2. Fuentes canónicas
```

```text
0048: 0.0.22-beta
0049: 0.0.25-beta
0050: 0.0.26-beta
0051: ```
0052:
```

```text
0051: ```
0052:
0053: Esta familia sigue siendo válida para leer y auditar estados históricos. Los tags `v0.0.1-beta` a `v0.0.26-beta` no se renombran ni se mueven.
0054:
0055: Después del cierre de VER.2, **los estados beta nuevos no continúan incrementando esta familia legacy**.
```

```text
0053: Esta familia sigue siendo válida para leer y auditar estados históricos. Los tags `v0.0.1-beta` a `v0.0.26-beta` no se renombran ni se mueven.
0054:
0055: Después del cierre de VER.2, **los estados beta nuevos no continúan incrementando esta familia legacy**.
0056:
0057: ### 3.2. Familia beta revision-aware
```

```text
0057: ### 3.2. Familia beta revision-aware
0058:
0059: Los candidatos y estados nuevos gobernados por VER.2 usan:
0060:
0061: ```text
```

```text
0075: G001 / E01 -> 0.0.01.01-beta
0076: G070 / E02 -> 0.0.70.02-beta
0077: G071 / E01 -> 0.0.71.01-beta
0078: G100 / E03 -> 0.1.00.03-beta
0079: G425 / E12 -> 0.4.25.12-beta
```

```text
0136: ```
0137:
0138: Ese identificador **no reemplaza** el valor histórico que el árbol todavía mostraba (`0.0.26-beta`) ni crea un tag retrospectivo.
0139:
0140: VER.2 R1 usa como candidato el siguiente estado:
```

```text
0138: Ese identificador **no reemplaza** el valor histórico que el árbol todavía mostraba (`0.0.26-beta`) ni crea un tag retrospectivo.
0139:
0140: VER.2 R1 usa como candidato el siguiente estado:
0141:
0142: ```text
```

```text
0141:
0142: ```text
0143: G071 / E01 -> 0.0.71.01-beta
0144: ```
0145:
```

```text
0144: ```
0145:
0146: G071 solo queda consumido como estado aceptado cuando VER.2 supera su ledger estructurado, validador, gate completo, PR/CI e integración. Si el candidato falla, se corrige manteniendo el mismo identificador candidato mientras no se acepte un estado distinto.
0147:
0148: ## 6. Reconstrucción histórica
```

```text
0160: El antiguo valor `0.1.0` continúa clasificado como marcador histórico de desarrollo no publicado.
0161:
0162: La reconstrucción revision-aware de G001–G070 es exclusivamente documental. No se crean tags `v0.GG.RR.EE-beta` para estados anteriores a VER.2.
0163:
0164: ## 7. Versiones formales legacy
```

```text
0173: v0.0.24-beta
0174: v0.0.25-beta
0175: v0.0.26-beta
0176: ```
0177:
```

```text
0176: ```
0177:
0178: Todos permanecen inmutables. Las fases UX.4.6f–UX.4.6i se desarrollaron históricamente manteniendo `VERSION = 0.0.26-beta`; VER.2 no falsea tags retroactivos para ellas. Su posición se conserva en el ledger mediante G061–G070.
0179:
0180: ## 8. Tags nuevos
```

```text
0185:
0186: ```text
0187: v0.0.71.01-beta
0188: v1.0.0.0
0189: v1.0.0.1
```

```text
0197: - `.github/allowed_signers` contiene las claves públicas autorizadas.
0198:
0199: Los tags publicados son inmutables. No se crea `v0.0.71.01-beta` mientras VER.2 sea candidato/draft y no haya completado su gate post-integración.
0200:
0201: ## 9. Build oficial
```

```text
0230: ## 10. Metadata documental
0231:
0232: VER.2 separa dos conceptos que antes se confundían:
0233:
0234: - **versión vigente/candidata de la aplicación:** únicamente `VERSION` y las superficies de estado actual;
```

```text
0235: - **versión en la que un documento fue revisado:** metadata histórica válida del propio documento.
0236:
0237: Por tanto, un documento técnico que diga `Versión de aplicación revisada: 0.0.26-beta` puede conservar esa línea si realmente documenta la base sobre la que fue revisado. No tiene que reescribirse en cada incremento global si su contenido no cambió.
0238:
0239: Los documentos que sí describen el estado actual —README, ROADMAP, SECURITY, índice operativo, CHANGELOG/RELEASES vigentes y ledger— deben actualizarse cuando corresponda.
```


## Documentos marcados REVISAR_MANUALMENTE

## docs/DECISIONES.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # Registro de decisiones técnicas
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Base documental histórica:** `0.0.23-beta` — GOV.1.3 R4 — 2026-08-17
0007: **Revisión documental:** GOV.1.3 R4 — 2026-08-17
0008: **Última actualización de gobierno:** PLAN.1 / ADR-168 — 2026-08-20
0009: **Última actualización técnica:** UX.4.6i R1.4 / ADR-178 — 2026-08-21
0010: **Clasificación:** Técnica / Gobierno / Auditoría
0011: **ADR indexadas:** 178 (`ADR-001` a `ADR-178`)
0012:
0013: Este registro conserva decisiones de arquitectura, modelado, UX, precisión, seguridad y aplicación normativa. Una ADR explica por qué el proyecto adoptó una decisión; no crea una norma jurídica.
0014:
0015: ## 1. Reglas de lectura
0016:
0017: - La numeración es única y consecutiva.
0018: - El campo **Estado** dentro de cada ADR es la fuente de vigencia de esa decisión.
0019: - Una decisión sustituida no se elimina.
0020: - Las relaciones de sustitución se conservan en el texto de las ADR implicadas.
0021: - Una ADR normativa debe leerse junto con la fuente oficial correspondiente.
0022: - El snapshot pre-R4 se conserva en `docs/archive/governance/DECISIONES_PRE_GOV1_3_R4.md`.
0023:
0024: ## 2. Anomalías históricas de metadata
0025:
0026: Las ADR siguientes no declaraban una línea `**Estado:**` en el registro inmediatamente anterior a R4:
0027:
0028: `ADR-086`
0029:
0030: R4 **no inventa un estado retroactivo** para esas decisiones. El índice las marca como `No declarado explícitamente en el registro pre-R4` y el registro íntegro inferior conserva su contenido original sin alterarlo.
0031:
0032: ## 3. Índice de decisiones
0033:
0034: | ADR | Decisión | Estado declarado |
0035: |---|---|---|
0036: | ADR-001 | Aplicación web local | Aceptada |
0037: | ADR-002 | FastAPI como backend | Aceptada |
0038: | ADR-003 | Separación del motor de cálculo | Aceptada |
0039: | ADR-004 | Normativa separada del código | Aceptada |
0040: | ADR-005 | Fechas reales | Aceptada |
0041: | ADR-006 | Historial y proyección separados | Aceptada |
0042: | ADR-007 | GitHub como repositorio principal | Aceptada |
0043: | ADR-008 | Estado temporal del asistente en `sessionStorage` | Aceptada |
0044: | ADR-009 | API como frontera entre interfaz y cálculos | Aceptada |
0045: | ADR-010 | Normalización salarial mediante valor anual común | Aceptada |
0046: | ADR-011 | Proyecciones salariales por escenarios | Aceptada |
0047: | ADR-012 | Proyección anual no sustituye cálculos por fecha exacta | Aceptada |
0048: | ADR-013 | Historial anual separado del salario actual | Aceptada |
0049: | ADR-014 | Línea temporal única con separación entre realidad y proyección | Aceptada |
0050: | ADR-015 | Salario cotizado futuro proporcional a las cuotas proyectadas | Aceptada |
0051: | ADR-016 | Precisión monetaria con `Decimal` y redondeo al materializar | Aceptada |
0052: | ADR-017 | El cierre del año actual precede a la densidad futura | Aceptada |
0053: | ADR-018 | El horizonte salarial debe cubrir el escenario de retiro | Aceptada |
0054: | ADR-019 | Navegación rápida `sticky` sin duplicar lógica de negocio | Aceptada |
0055: | ADR-020 | Clasificar explícitamente cuotas excedentes por edad de referencia | Aceptada |
0056: | ADR-021 | Selección explícita del escenario que alimenta el Paso 6 | Aceptada |
0057: | ADR-022 | Capa de integración entre el asistente y los motores legales | Aceptada |
0058: | ADR-023 | Clasificación automática de modalidad SEBD | Aceptada |
0059: | ADR-024 | Años calendario parciales dentro de los mejores años | Aceptada |
0060: | ADR-025 | Factores anticipados versionados por mes | Aceptada |
0061: | ADR-026 | Indemnización por Vejez como pago único separado | Aceptada |
0062: | ADR-027 | No reconstruir el saldo CAP desde historial anual | Aceptada |
0063: | ADR-028 | Reutilizar clasificación SEBD en el componente BD del Mixto | Aceptada |
0064: | ADR-029 | Frontera operativa del Mixto en 01/03/2032 | Aceptada con discrepancia normativa documentada |
0065: | ADR-030 | La opción del CAP no se decide automáticamente | Aceptada |
0066: | ADR-031 | La garantía de renta vitalicia no incrementa la pensión inicial | Aceptada |
0067: | ADR-032 | El bono de reconocimiento requiere un monto oficial o validado | Aceptada |
0068: | ADR-033 | Pagos únicos y pensiones mensuales permanecen separados | Aceptada |
0069: | ADR-034 | La interfaz Mixto consume el motor integrado y no replica fórmulas | Aceptada |
0070: | ADR-035 | Navegación directa condicionada entre pasos del asistente | Aceptada |
0071: | ADR-036 | Separar saldo SUCGS y garantías | Aceptada |
0072: | ADR-037 | Versionar referencias solidarias y permitir valores vigentes | Aceptada |
0073: | ADR-038 | Prioridad del artículo 195 en el límite exacto de 240 cuotas | Aceptada |
0074: | ADR-039 | Preevaluación conservadora del artículo 197 | Aceptada |
0075: | ADR-040 | Integrar SUCGS al Paso 6 sin duplicar fórmulas | Aceptada |
0076: | ADR-041 | El comparador coordina motores y no recalcula fórmulas | Aceptada |
0077: | ADR-042 | La trazabilidad explica resultados y no recalcula prestaciones | Aceptada |
0078: | ADR-043 | Las fuentes visibles usan nombres humanos y metadatos versionados | Aceptada |
0079: | ADR-044 | Contrato transversal común para el resultado final | Aceptada |
0080: | ADR-045 | Adoptar una identidad de producto independiente | Aceptada |
0081: | ADR-046 | Denominar Asegurado(a) al público de la aplicación | Aceptada |
0082: | ADR-047 | Unificar la escala tipográfica visible | Aceptada |
0083: | ADR-048 | Separar información del Asegurado(a) y documentación interna | Aceptada |
0084: | ADR-049 | Preferencia visual local e independiente de la simulación | Aceptada |
0085: | ADR-050 | Accesibilidad base transversal en la plantilla global | Aceptada |
0086: | ADR-051 | Pie de página compacto como información legal global | Aceptada |
0087: | ADR-052 | Usar tokens semánticos para todos los colores visibles | Aceptada |
0088: | ADR-053 | Tratar Alto contraste como tema oscuro de contraste máximo | Aceptada |
0089: | ADR-054 | Convertir Inicio en una portada orientada al Asegurado(a) | Aceptada |
0090: | ADR-055 | Reservar detalles de implementación para documentación interna | Aceptada |
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Base documental histórica:** `0.0.23-beta` — GOV.1.3 R4 — 2026-08-17
```

```text
0140: | ADR-105 | Las casillas importadas deben conservar una marca visual inequívoca | Aceptada en la marca visual; el bloqueo permanente queda sustituido por ADR-167 |
0141: | ADR-106 | Estado seleccionado de casillas documentales independiente del pintado nativo | Sustituida parcialmente por ADR-167: la metadata conserva procedencia, pero la inclusión puede cambiar por decisión explícita |
0142: | ADR-107 | Borrado por paso con invalidación descendente | Aceptada para validación UX.4.6d R6. |
0143: | ADR-108 | Reinicio integral separado de preferencias y consentimiento | Aceptada para validación UX.4.6d R6. |
0144: | ADR-109 | Borrado local integral desde Privacidad | Aceptada para validación UX.4.6d R6. |
```

```text
0141: | ADR-106 | Estado seleccionado de casillas documentales independiente del pintado nativo | Sustituida parcialmente por ADR-167: la metadata conserva procedencia, pero la inclusión puede cambiar por decisión explícita |
0142: | ADR-107 | Borrado por paso con invalidación descendente | Aceptada para validación UX.4.6d R6. |
0143: | ADR-108 | Reinicio integral separado de preferencias y consentimiento | Aceptada para validación UX.4.6d R6. |
0144: | ADR-109 | Borrado local integral desde Privacidad | Aceptada para validación UX.4.6d R6. |
0145: | ADR-110 | Nueva versión de términos por controles de conservación y eliminación | Aceptada para validación UX.4.6d R6. |
```

```text
0142: | ADR-107 | Borrado por paso con invalidación descendente | Aceptada para validación UX.4.6d R6. |
0143: | ADR-108 | Reinicio integral separado de preferencias y consentimiento | Aceptada para validación UX.4.6d R6. |
0144: | ADR-109 | Borrado local integral desde Privacidad | Aceptada para validación UX.4.6d R6. |
0145: | ADR-110 | Nueva versión de términos por controles de conservación y eliminación | Aceptada para validación UX.4.6d R6. |
0146: | ADR-111 | Consulta posterior de términos no modifica el consentimiento | Aceptada para validación UX.4.6d R7. |
```

```text
0143: | ADR-108 | Reinicio integral separado de preferencias y consentimiento | Aceptada para validación UX.4.6d R6. |
0144: | ADR-109 | Borrado local integral desde Privacidad | Aceptada para validación UX.4.6d R6. |
0145: | ADR-110 | Nueva versión de términos por controles de conservación y eliminación | Aceptada para validación UX.4.6d R6. |
0146: | ADR-111 | Consulta posterior de términos no modifica el consentimiento | Aceptada para validación UX.4.6d R7. |
0147: | ADR-112 | El estado de una fila editable deriva de sus datos actuales | Aceptada para UX.4.6d R8. |
```

```text
0144: | ADR-109 | Borrado local integral desde Privacidad | Aceptada para validación UX.4.6d R6. |
0145: | ADR-110 | Nueva versión de términos por controles de conservación y eliminación | Aceptada para validación UX.4.6d R6. |
0146: | ADR-111 | Consulta posterior de términos no modifica el consentimiento | Aceptada para validación UX.4.6d R7. |
0147: | ADR-112 | El estado de una fila editable deriva de sus datos actuales | Aceptada para UX.4.6d R8. |
0148: | ADR-113 | El resumen anual debe ser visible antes de terminar todo el Paso 3 | Aceptada para UX.4.6d R8. |
```

```text
0197: | ADR-162 | Los comentarios de runtime son semánticos y no cronológicos | Aceptada para UX.4.6e R4. |
0198: | ADR-163 | La preparación pública separa información útil al usuario de gobierno interno | Aceptada para UX.4.6e R5. |
0199: | ADR-164 | La renumeración vigente no reescribe la historia UX anterior | Aceptada para UX.4.6e R6. |
0200: | ADR-165 | La auditoría transversal es un gate antes de la validación funcional manual | Aceptada para UX.4.6e R7. |
0201: | ADR-166 | El borrado integral invalida también residuos pre-beta y fuerza reconsentimiento | Aceptada para UX.4.6e R8. |
```

```text
0198: | ADR-163 | La preparación pública separa información útil al usuario de gobierno interno | Aceptada para UX.4.6e R5. |
0199: | ADR-164 | La renumeración vigente no reescribe la historia UX anterior | Aceptada para UX.4.6e R6. |
0200: | ADR-165 | La auditoría transversal es un gate antes de la validación funcional manual | Aceptada para UX.4.6e R7. |
0201: | ADR-166 | El borrado integral invalida también residuos pre-beta y fuerza reconsentimiento | Aceptada para UX.4.6e R8. |
0202: | ADR-167 | Los datos documentales confirmados son editables sin perder la referencia original | Sustituida parcialmente por ADR-171: la edición de datos detectados se concentra en la ventana de revisión; se preservan referencia original y copia de trabajo |
```

```text
1238: ## ADR-107 — Borrado por paso con invalidación descendente
1239:
1240: **Estado:** Aceptada para validación UX.4.6d R6.
1241:
1242: **Decisión:** cada paso puede limpiarse sin alterar los anteriores, pero debe eliminar o invalidar todos los estados posteriores dependientes. Esto impide conservar resultados calculados con datos que ya no existen.
```

```text
1244: ## ADR-108 — Reinicio integral separado de preferencias y consentimiento
1245:
1246: **Estado:** Aceptada para validación UX.4.6d R6.
1247:
1248: **Decisión:** **Reiniciar simulación** elimina la simulación completa, pero no cambia el tema visual ni la aceptación vigente de términos. Estos estados no forman parte del caso previsional.
```

```text
1250: ## ADR-109 — Borrado local integral desde Privacidad
1251:
1252: **Estado:** Aceptada para validación UX.4.6d R6.
1253:
1254: **Decisión:** Fuentes/Privacidad ofrece una acción distinta para borrar las claves locales de simulación, consentimiento y tema. No se usa `localStorage.clear()` ni `sessionStorage.clear()` para evitar afectar datos ajenos a la aplicación en el mismo origen.
```

```text
1256: ## ADR-110 — Nueva versión de términos por controles de conservación y eliminación
1257:
1258: **Estado:** Aceptada para validación UX.4.6d R6.
1259:
1260: **Decisión:** el texto de privacidad cambia a **2026-08-15.1** porque se amplía materialmente la información entregada al usuario sobre conservación, limpieza, reinicio y eliminación local. La nueva versión requiere aceptación nuevamente.
```

```text
1262: ## ADR-111 — Consulta posterior de términos no modifica el consentimiento
1263:
1264: **Estado:** Aceptada para validación UX.4.6d R7.
1265:
1266: **Decisión:** Términos/Privacidad utiliza un único documento y modal con dos modos. El consentimiento inicial exige lectura/aceptación antes de usar Simular; una consulta posterior desde Fuentes abre el mismo contenido en la ruta actual, oculta los controles de aceptación y no modifica la constancia vigente. El cierre `×` solo cierra en revisión; durante el consentimiento inicial equivale a no continuar.
```

```text
1720: ## ADR-164 — La renumeración vigente no reescribe la historia UX anterior
1721:
1722: **Estado:** Aceptada para UX.4.6e R6.
1723:
1724: **Decisión:** UX.4.6e queda reservado al bloque transversal de estandarización técnica, comentarios, coherencia de interfaz y preparación del repositorio. El trabajo funcional posterior se identifica como UX.4.6f — Paso 4, UX.4.6g — Paso 5 y UX.4.6h — Paso 6. Los documentos vigentes deben usar esta secuencia. Los releases, auditorías, snapshots y bitácoras que registraron la numeración prospectiva anterior conservan sus identificadores originales y, cuando sea necesario para evitar ambigüedad, reciben una nota posterior explícita en vez de reescribirse.
```

```text
1730: ## ADR-165 — La auditoría transversal es un gate antes de la validación funcional manual
1731:
1732: **Estado:** Aceptada para UX.4.6e R7.
1733:
1734: **Decisión:** antes de iniciar la prueba funcional manual/automática de cierre hasta el Paso 3, UX.4.6e ejecuta una auditoría transversal que comprueba coherencia entre código runtime, comentarios/docstrings, interfaz visible, documentación vigente, regresiones automatizadas y metadata manual de GitHub. Los snapshots históricos no se reinterpretan; cuando una referencia antigua pueda inducir a error, se añade una nota posterior explícita.
```

## docs/DEV2_CENTRO_DESARROLLO.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # DEV.2 R1/R2/R3/R4 — Centro de desarrollo
0002:
0003: **Estado:** DEV.2 cerrado documentalmente en R4.
0004:
0005: **Estado:** R1 integrado en `main` mediante PR #37.
0006:
0007: **Estado R1 documental:** integrado en `main` mediante PR #38.
0008:
0009: **Estado R2:** integrado en `main` mediante PR #39.
0010:
0011: **Estado R3:** integrado en `main` mediante PR #40.
0012:
0013: DEV.2 abre y cierra una superficie interna y local para revisar el estado técnico
0014: de Developer Diagnostics sin alterar los cálculos previsionales, sin leer datos
0015: de simulación y sin exponer información personal o financiera.
0016:
0017: DEV.2 no cambia cálculos, motores previsionales, normativa, resultados ni
0018: flujos públicos de simulación.
0019:
0020: ## Objetivo
0021:
0022: Crear una página de Centro de desarrollo que permita confirmar, durante el
0023: desarrollo local, si Developer Diagnostics está activo, qué esquema JSONL se usa,
0024: cuál es el archivo diagnóstico esperado, qué eventos recientes son visibles de
0025: forma segura, si existe material suficiente para una exportación ZIP sanitizada y
0026: qué componentes locales requieren atención.
0027:
0028: El cierre R4 consolida la documentación viva del bloque después de integrar R1,
0029: R2 y R3. No introduce comportamiento funcional nuevo.
0030:
0031: ## Activación
0032:
0033: Developer Diagnostics sigue desactivado por defecto. La activación local requiere:
0034:
0035: ```powershell
0036: $env:MRP_DEV_MODE = "1"
0037: ```
0038:
0039: Equivalente conceptual: `MRP_DEV_MODE=1`.
0040:
0041: El directorio diagnóstico puede mantenerse por defecto bajo `logs/diagnostico/` o
0042: configurarse con `MRP_DIAGNOSTIC_DIR` durante pruebas locales.
0043:
0044: ## Alcance de R1
0045:
0046: Incluye:
0047:
0048: - ruta interna `/dev/centro-desarrollo`;
0049: - estado de `MRP_DEV_MODE`;
0050: - versión de esquema de Developer Diagnostics;
0051: - resumen no sensible del log vigente y sus rotaciones conocidas;
0052: - indicación de disponibilidad de exportación ZIP sanitizada;
0053: - advertencias explícitas de privacidad.
0054:
0055: No incluye:
0056:
0057: - lectura de cuerpos HTTP;
0058: - lectura de PDFs, uploads, bases de datos o `sessionStorage`;
0059: - nombres, cédulas, NSS, salarios, cuotas o montos de pensión;
0060: - rutas absolutas locales del equipo;
0061: - telemetría remota;
0062: - cambios en los motores de cálculo;
0063: - cambios en cálculos previsionales o resultados;
0064: - cambio de VERSION al abrir el bloque.
0065:
0066: ## Alcance de R2
0067:
0068: DEV.2 R2 añade un visor diagnóstico seguro y un servicio interno de exportación
0069: ZIP controlada sobre los archivos JSONL ya conocidos por Developer Diagnostics.
0070:
0071: Incluye:
0072:
0073: - lectura acotada del archivo `mrp-diagnostics.jsonl` y sus rotaciones esperadas;
0074: - normalización de eventos recientes para la interfaz local;
0075: - conteo visible de eventos por nivel operacional;
0076: - exposición de `correlation_id` solo cuando existe y sin derivarlo de datos del usuario;
0077: - metadata limitada a operación, método HTTP, código de estado y tipo de excepción;
0078: - conteo de líneas JSONL inválidas sin mostrar su contenido;
0079: - servicio `exportar_zip_diagnostico_sanitizado()` para generar el ZIP permitido;
0080: - regresiones específicas para visor, privacidad y exportación.
0081:
0082: ## Alcance de R3
0083:
0084: DEV.2 R3 añade un autodiagnóstico técnico local sobre el Centro de desarrollo y
0085: Developer Diagnostics, sin introducir autenticación administrativa fuerte ni
0086: cambios de seguridad que correspondan a SEC.2.
0087:
0088: Incluye:
0089:
0090: - estado global del autodiagnóstico técnico;
```

### Coincidencias con contexto

```text
0113: - sincronización de `docs/ADR_179_VERSIONADO_REVISION_AWARE.md`;
0114: - regresión documental `tests/test_dev2_r4_cierre_final.py`;
0115: - conservación explícita de VER.2 como cierre transversal posterior.
0116:
0117: No incluye:
```

```text
0134:
0135: DEV.2 R1/R2/R3/R4 **no cambia VERSION** ni `APP_VERSION`. La versión visible
0136: permanece en `0.0.26-beta` durante este tramo.
0137:
0138: DEV.2 R4 no cambia VERSION. DEV.2 R4 no crea tag.
```

```text
0142:
0143: La promoción a una versión `0.GG.RR.EE-beta` queda reservada para el cierre
0144: posterior de VER.2, cuando el ledger y la documentación de versionado se alineen
0145: de forma sincrónica.
0146:
```

```text
0151: local y pruebas de seguridad sobre la capacidad existente.
0152:
0153: ## Relación con VER.2
0154:
0155: DEV.2 queda cerrado como bloque funcional independiente. VER.2 permanece como el
```

```text
0153: ## Relación con VER.2
0154:
0155: DEV.2 queda cerrado como bloque funcional independiente. VER.2 permanece como el
0156: cierre transversal pendiente de versionado revision-aware, ledger, documentación
0157: contable y promoción de versión cuando corresponda.
```

```text
0161: DEV.2 R1 fue integrado mediante PR #37 sobre `main` con el commit de squash
0162: `06e2821`. El cierre abre la ruta interna `/dev/centro-desarrollo`, mantiene
0163: `VERSION` y `APP_VERSION` en `0.0.26-beta`, no crea tag, no cambia motores
0164: previsionales y deja como siguiente trabajo DEV.2 R2.
0165:
```

```text
0178: DEV.2 R2 fue integrado mediante PR #39 sobre `main` con el commit de squash
0179: `5451d18`. El cierre agregó visor diagnóstico seguro y exportación ZIP
0180: sanitizada controlada, manteniendo `VERSION` y `APP_VERSION` en `0.0.26-beta`.
0181:
0182: La validación local de cierre quedó en:
```

```text
0194: DEV.2 R3 fue integrado mediante PR #40 sobre `main` con el commit de squash
0195: `9fb86af`. El cierre agregó autodiagnóstico técnico local, manteniendo `VERSION`
0196: y `APP_VERSION` en `0.0.26-beta`.
0197:
0198: La validación local de cierre quedó en:
```

## docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # Estándar de código y comentarios
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.24-beta`
0006: **Revisión documental:** UX.4.6e R4 — 2026-08-18
0007: **Revisión de mantenimiento:** MANT.1 R5E — estandarización de nombres de carpetas — 2026-08-23
0008: **Clasificación:** Técnica / Mantenibilidad
0009:
0010: Este documento define el patrón permanente para documentar código en Mi Retiro
0011: Proyectado. Su objetivo es permitir que otro desarrollador entienda intención,
0012: contratos, límites y dependencias sin convertir el código en una narración línea
0013: por línea.
0014:
0015: MANT.1 R1 registró la auditoría inicial de cobertura, MANT.1 R2 aplica la
0016: primera mejora documental sobre scripts, hooks y automatización local,
0017: MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento,
0018: MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica quede
0019: fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
0020: intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
0021: y plantillas grandes, y MANT.1 R5C cubre JavaScript complejo de interacción,
0022: almacenamiento, importación y resultados. MANT.1 R5D formaliza política y plantillas por extensión, uniforma encabezados de JavaScript/CSS operativo y MANT.1 R5E estandariza carpetas técnicas en inglés sin renombrar archivos. Las revisiones posteriores deben
0023: conservar esta misma trazabilidad incremental.
0024:
0025: ## 1. Principio general
0026:
0027: Un comentario debe explicar al menos una de estas cosas:
0028:
0029: - **intención**: qué responsabilidad cumple un bloque;
0030: - **contrato**: qué recibe, devuelve, modifica o invalida;
0031: - **motivo**: por qué se eligió una solución no obvia;
0032: - **límite**: qué deliberadamente no hace;
0033: - **riesgo**: qué podría romperse si se modifica sin contexto;
0034: - **procedencia**: cuándo una decisión depende de normativa, privacidad,
0035:   accesibilidad, compatibilidad o arquitectura.
0036:
0037: No se añaden comentarios que repitan literalmente una instrucción evidente.
0038:
0039: ## 2. Historia frente a documentación permanente
0040:
0041: Los identificadores `UX.*`, `GOV.*`, números de revisión y relatos cronológicos
0042: pertenecen a `CHANGELOG.md`, `RELEASES.md`, ADR, pruebas de regresión o archivos
0043: históricos. El código de runtime usa comentarios semánticos que sigan siendo
0044: útiles aunque cambie la numeración del roadmap.
0045:
0046: Las pruebas sí pueden conservar un identificador histórico cuando este explica
0047: el origen de una regresión.
0048:
0049: ### Encabezados operativos permanentes
0050:
0051: Los encabezados de archivos operativos deben describir el propósito permanente
0052: del archivo. No deben usar la primera línea para declarar `MANT.*`, `DEV.*`,
0053: `UX.*`, `VER.*`, números de PR ni el bloque que originó el cambio.
0054:
0055: En archivos YAML, hooks, scripts y README técnicos de carpetas operativas, el
0056: encabezado debe indicar:
0057:
0058: - **qué hace el archivo**;
0059: - **qué alcance conserva**;
0060: - **qué límites protege** cuando exista riesgo de modificar comportamiento.
0061:
0062: La trazabilidad de revisión se registra en `CHANGELOG.md`, `docs/ROADMAP.md`,
0063: `docs/VALIDACION.md` y documentación técnica equivalente, no en encabezados de
0064: archivos operativos.
0065:
0066: ### Nombres de carpetas técnicas
0067:
0068: Las carpetas técnicas se nombran en inglés para evitar mezclas entre paquetes,
0069: documentación, scripts, parámetros y pruebas. Los nombres vigentes de mayor
0070: impacto son `app/models/`, `app/engines/`, `app/services/`, `regulations/`,
0071: `tests/validation_cases/` y `docs/archive/`.
0072:
0073: Un cambio de carpeta no se considera completo hasta actualizar imports,
0074: hipervínculos, rutas de pruebas, documentación y configuración relacionada.
0075:
0076: ## 3. Python
0077:
0078: ### Comentarios internos en servicios de aplicación
0079:
0080: Los servicios propios de `app/services/` deben explicar decisiones de flujo cuando
0081: normalizan datos, separan totales, construyen matrices, agregan advertencias,
0082: leen documentos o transforman resultados en salidas para la interfaz. Estos
0083: comentarios deben describir intención y límites de negocio, no registrar el nombre
0084: de la revisión, el PR que los agregó ni la historia del bloque.
0085:
0086: En servicios de cálculo o integración no se comentan líneas evidentes. Se comenta
0087: la razón por la que una rama evita mutación, por qué se omite una fecha, por qué
0088: se conserva una advertencia o por qué una fuente se consulta en una capa concreta.
0089:
0090:
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.24-beta`
0006: **Revisión documental:** UX.4.6e R4 — 2026-08-18
```

```text
0005: **Versión base histórica:** `0.0.24-beta`
0006: **Revisión documental:** UX.4.6e R4 — 2026-08-18
0007: **Revisión de mantenimiento:** MANT.1 R5E — estandarización de nombres de carpetas — 2026-08-23
0008: **Clasificación:** Técnica / Mantenibilidad
0009:
```

```text
0013: por línea.
0014:
0015: MANT.1 R1 registró la auditoría inicial de cobertura, MANT.1 R2 aplica la
0016: primera mejora documental sobre scripts, hooks y automatización local,
0017: MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento,
```

```text
0015: MANT.1 R1 registró la auditoría inicial de cobertura, MANT.1 R2 aplica la
0016: primera mejora documental sobre scripts, hooks y automatización local,
0017: MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento,
0018: MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica quede
0019: fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
```

```text
0016: primera mejora documental sobre scripts, hooks y automatización local,
0017: MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento,
0018: MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica quede
0019: fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
0020: intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
```

```text
0017: MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento,
0018: MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica quede
0019: fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
0020: intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
0021: y plantillas grandes, y MANT.1 R5C cubre JavaScript complejo de interacción,
```

```text
0018: MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica quede
0019: fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
0020: intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
0021: y plantillas grandes, y MANT.1 R5C cubre JavaScript complejo de interacción,
0022: almacenamiento, importación y resultados. MANT.1 R5D formaliza política y plantillas por extensión, uniforma encabezados de JavaScript/CSS operativo y MANT.1 R5E estandariza carpetas técnicas en inglés sin renombrar archivos. Las revisiones posteriores deben
```

```text
0019: fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
0020: intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
0021: y plantillas grandes, y MANT.1 R5C cubre JavaScript complejo de interacción,
0022: almacenamiento, importación y resultados. MANT.1 R5D formaliza política y plantillas por extensión, uniforma encabezados de JavaScript/CSS operativo y MANT.1 R5E estandariza carpetas técnicas en inglés sin renombrar archivos. Las revisiones posteriores deben
0023: conservar esta misma trazabilidad incremental.
```

```text
0020: intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
0021: y plantillas grandes, y MANT.1 R5C cubre JavaScript complejo de interacción,
0022: almacenamiento, importación y resultados. MANT.1 R5D formaliza política y plantillas por extensión, uniforma encabezados de JavaScript/CSS operativo y MANT.1 R5E estandariza carpetas técnicas en inglés sin renombrar archivos. Las revisiones posteriores deben
0023: conservar esta misma trazabilidad incremental.
0024:
```

```text
0218: clave.
0219:
0220: MANT.1 R3 fija que los YAML versionados de GitHub pueden iniciar con un
0221: encabezado breve cuando ese encabezado documenta propósito, alcance y límites
0222: operativos. En workflows no debe alterar `on`, `permissions`, `concurrency`,
```

## docs/LEDGER_REVISIONES_PRE_1_0.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # Ledger de revisiones aceptadas pre-1.0
0002:
0003: **Proyecto:** Mi Retiro Proyectado
0004: **Base auditada:** `7037addd44253e528c77460b678d2b3ccd540dd5`
0005: **Contador aceptado en la base:** **G070**
0006: **Siguiente Global disponible si VER.2 supera su gate:** **G071**
0007:
0008: Este ledger registra los estados aceptados reconstruidos durante VER.2. La regla contable y las exclusiones se documentan en `MATRIZ_DECISION_REVISIONES_VER2.md` y `AUDITORIA_VERSIONADO_PRE_1_0.md`.
0009:
0010: Los identificadores revision-aware son una reconstrucción de auditoría. **No existieron históricamente y no autorizan mover, recrear ni renombrar los tags `v0.0.1-beta`–`v0.0.26-beta`.**
0011:
0012: ## Convención
0013:
0014: ```text
0015: 0.GG.RR.EE-beta
0016: ```
0017:
0018: - `G = GG × 100 + RR`;
0019: - `RR` usa dos dígitos (`00`–`99`);
0020: - `EE` es el ordinal del estado aceptado dentro del bloque, con dos dígitos;
0021: - un candidato fallido no consume `G`;
0022: - un PR/commit/tag no suma otra fila si solo materializa el mismo estado;
0023: - un mantenimiento técnico, de seguridad, gobierno, dependencias o documentación puede consumir `G` si crea un estado materialmente distinto, validado y aceptado.
0024:
0025: ## Ledger G001–G070
0026:
0027: | Global | ID revision-aware | Bloque / estado aceptado | Ancla histórica | Evidencia resumida |
0028: |---:|---|---|---|---|
0029: | G001 | `0.0.01.01-beta` | Estado retrospectivo 01 — base técnica | `0.0.1-beta` | GOV.1.1 / `RELEASES.md` |
0030: | G002 | `0.0.02.01-beta` | Estado retrospectivo 02 — historial/proyección | `0.0.2-beta` | GOV.1.1 / `RELEASES.md` |
0031: | G003 | `0.0.03.01-beta` | Estado retrospectivo 03 — retiro/precisión | `0.0.3-beta` | GOV.1.1 / `RELEASES.md` |
0032: | G004 | `0.0.04.01-beta` | Estado retrospectivo 04 — SEBD/modalidades | `0.0.4-beta` | GOV.1.1 / `RELEASES.md` |
0033: | G005 | `0.0.05.01-beta` | Estado retrospectivo 05 — Mixto/SUCGS | `0.0.5-beta` | GOV.1.1 / `RELEASES.md` |
0034: | G006 | `0.0.06.01-beta` | Estado retrospectivo 06 — organización/normativa | `0.0.6-beta` | GOV.1.1 / `RELEASES.md` |
0035: | G007 | `0.0.07.01-beta` | Estado retrospectivo 07 — comparador/trazabilidad | `0.0.7-beta` | GOV.1.1 / `RELEASES.md` |
0036: | G008 | `0.0.08.01-beta` | UX.3 — responsive/corte mensual | `0.0.8-beta` | cierre retrospectivo |
0037: | G009 | `0.0.09.01-beta` | Identidad/temas/accesibilidad, incluida UX.2.1 | `0.0.9-beta` | snapshot legado; UX.2.1 queda absorbida sin duplicación |
0038: | G010 | `0.0.10.01-beta` | Mantenimiento técnico estructural | `0.0.10-beta` | cierre retrospectivo |
0039: | G011 | `0.0.11.01-beta` | UX.4.1 — accesibilidad contextual | `0.0.11-beta` | cierre retrospectivo |
0040: | G012 | `0.0.12.01-beta` | UX.4.2 — estados/selección visual | `0.0.12-beta` | cierre retrospectivo |
0041: | G013 | `0.0.13.01-beta` | UX.4.3 — validación/teclado/estabilidad | `0.0.13-beta` | cierre retrospectivo |
0042: | G014 | `0.0.14.01-beta` | UX.4.4 — edad/detalle/importación | `0.0.14-beta` | cierre retrospectivo |
0043: | G015 | `0.0.15.01-beta` | UX.4.5 — acreditado vs. proyectado | `0.0.15-beta` | cierre retrospectivo |
0044: | G016 | `0.0.16.01-beta` | Hardening PDF/privacidad/E2E/CI | `0.0.16-beta` | cierre retrospectivo |
0045: | G017 | `0.0.17.01-beta` | Dependencias reproducibles | `0.0.17-beta` | cierre retrospectivo |
0046: | G018 | `0.0.18.01-beta` | UX.4.6a — cierre rediseño visual | `0.0.18-beta` | 198 pruebas / cierre PC-laptop |
0047: | G019 | `0.0.19.01-beta` | UX.4.6b — cierre Paso 1 | `0.0.19-beta` | R4 / 233 pruebas |
0048: | G020 | `0.0.20.01-beta` | UX.4.6c — cierre Paso 2 | `0.0.20-beta` | R3 / 253 pruebas |
0049: | G021 | `0.0.21.01-beta` | UX.4.6d — cierre Paso 3 | `0.0.21-beta` | R23 / 396 pruebas |
0050: | G022 | `0.0.22.01-beta` | GOV.1.2 — gobierno y versionado formal | `v0.0.22-beta` | 403 pruebas |
0051: | G023 | `0.0.23.01-beta` | GOV.1.3 R1 — estructura/histórico | base `0.0.22-beta` | 411 pruebas |
0052: | G024 | `0.0.24.02-beta` | GOV.1.3 R2 — documentación técnica | base `0.0.22-beta` | 423 pruebas |
0053: | G025 | `0.0.25.03-beta` | GOV.1.3 R3 — normativa/privacidad | base `0.0.22-beta` | 438 pruebas |
0054: | G026 | `0.0.26.04-beta` | GOV.1.3 R4 — auditoría documental | `v0.0.23-beta` | 458 pruebas |
0055: | G027 | `0.0.27.01-beta` | Integridad R1 — materialización criptográfica de tags | base `0.0.23-beta` | commit `685d056`; 23/23 firmas/objetos/targets |
0056: | G028 | `0.0.28.02-beta` | Integridad R2 — CI v7 y protecciones GitHub | base `0.0.23-beta` | PR #9 / 470 pruebas |
0057: | G029 | `0.0.29.03-beta` | Integridad R3 — corrección rutas PowerShell | base `0.0.23-beta` | PR #10 / 470 pruebas |
0058: | G030 | `0.0.30.04-beta` | Integridad R4 — actualización `pypdf 6.15.0` | base `0.0.23-beta` | PR #11 / 474 pruebas |
0059: | G031 | `0.0.31.05-beta` | Integridad R5 — cierre formal del prebloque | base `0.0.23-beta` | PR #12 / 474 pruebas / 0 PR pendientes |
0060: | G032 | `0.0.32.01-beta` | GOV.1.4 — Developer Diagnostics | base `0.0.23-beta` | 487 pruebas |
0061: | G033 | `0.0.33.01-beta` | GOV.1.5 R1 — modelo de amenazas | base `0.0.23-beta` | 7 regresiones / cierre original R1 |
0062: | G034 | `0.0.34.02-beta` | GOV.1.5 R2 — derechos e incidentes | base `0.0.23-beta` | +8 regresiones / 502 pruebas antes de R3 |
0063: | G035 | `0.0.35.03-beta` | GOV.1.5 R3 — cierre seguridad/privacidad/transparencia | base `0.0.23-beta` | PR #14 / 512 pruebas |
0064: | G036 | `0.0.36.01-beta` | GOV.1.6 — controles GitHub | base `0.0.23-beta` | 522 pruebas |
0065: | G037 | `0.0.37.01-beta` | GOV.1.7 — licencia/distribución | base `0.0.23-beta` | 530 pruebas |
0066: | G038 | `0.0.38.02-beta` | GOV.1.7 — hotfix de formato de licencia | base `0.0.23-beta` | PR #16 / 530 pruebas |
0067: | G039 | `0.0.39.01-beta` | GOV.1.8 — cierre integral GOV.1 | `v0.0.24-beta` | PR #17 / 540 pruebas |
0068: | G040 | `0.0.40.01-beta` | Saneamiento post-GOV.1 | base `0.0.24-beta` | PR #18 / 540 pruebas / auditoría de repositorio |
0069: | G041 | `0.0.41.01-beta` | UX.4.6e R1 — auditoría/patrón documental | base `0.0.24-beta` | R1 completada; avance explícito a R2 |
0070: | G042 | `0.0.42.02-beta` | UX.4.6e R2 — Python/proyección salarial | base `0.0.24-beta` | 550 pruebas |
0071: | G043 | `0.0.43.03-beta` | UX.4.6e R3 — JS/Web Storage | base `0.0.24-beta` | 558 pruebas |
0072: | G044 | `0.0.44.04-beta` | UX.4.6e R4 — runtime/Jinja/CSS | base `0.0.24-beta` | 566 pruebas |
0073: | G045 | `0.0.45.05-beta` | UX.4.6e R5 — coherencia visible/preparación pública | base `0.0.24-beta` | 576 pruebas |
0074: | G046 | `0.0.46.06-beta` | UX.4.6e R6 — renumeración/metadata | base `0.0.24-beta` | 586 pruebas |
0075: | G047 | `0.0.47.07-beta` | UX.4.6e R7 — auditoría transversal | base `0.0.24-beta` | 598 pruebas |
0076: | G048 | `0.0.48.08-beta` | UX.4.6e — identidad visual oficial y publicación | base `0.0.24-beta` | PR #20 / 624 pruebas |
0077: | G049 | `0.0.49.09-beta` | UX.4.6e R8 — validación funcional/procedencia | base `0.0.24-beta` | R8.2 644 / cierre documental 652 |
0078: | G050 | `0.0.50.10-beta` | UX.4.6e R9 — cierre formal | `v0.0.25-beta` | PR #21/#22 / 660 pruebas |
0079: | G051 | `0.0.51.01-beta` | PLAN.1 R1 — política/plan maestro | base `0.0.25-beta` | 665 pruebas |
0080: | G052 | `0.0.52.02-beta` | PLAN.1 R2A | base `0.0.25-beta` | 670 pruebas |
0081: | G053 | `0.0.53.03-beta` | PLAN.1 R2B1 | base `0.0.25-beta` | 676 pruebas |
0082: | G054 | `0.0.54.04-beta` | PLAN.1 R2B2 | base `0.0.25-beta` | 684 pruebas |
0083: | G055 | `0.0.55.05-beta` | PLAN.1 R2C | base `0.0.25-beta` | 689 pruebas |
0084: | G056 | `0.0.56.06-beta` | PLAN.1 R3A | base `0.0.25-beta` | 695 pruebas |
0085: | G057 | `0.0.57.07-beta` | PLAN.1 R3B1 | base `0.0.25-beta` | 702 pruebas |
0086: | G058 | `0.0.58.08-beta` | PLAN.1 R3B2 | base `0.0.25-beta` | 710 pruebas |
0087: | G059 | `0.0.59.09-beta` | PLAN.1 R4.1 — candidato local cerrado | base `0.0.25-beta` | PR #23 / 720 pruebas |
0088: | G060 | `0.0.60.10-beta` | PLAN.1 R4.2 — higiene y cierre formal | `v0.0.26-beta` | PR #24 / 720 sin `SyntaxWarning` |
0089: | G061 | `0.0.61.01-beta` | UX.4.6f R1/R1.1 — aceptación conjunta | base `0.0.26-beta` | PR #28 / 743 pruebas |
0090: | G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
```

### Coincidencias con contexto

```text
0004: **Base auditada:** `7037addd44253e528c77460b678d2b3ccd540dd5`
0005: **Contador aceptado en la base:** **G070**
0006: **Siguiente Global disponible si VER.2 supera su gate:** **G071**
0007:
0008: Este ledger registra los estados aceptados reconstruidos durante VER.2. La regla contable y las exclusiones se documentan en `MATRIZ_DECISION_REVISIONES_VER2.md` y `AUDITORIA_VERSIONADO_PRE_1_0.md`.
```

```text
0006: **Siguiente Global disponible si VER.2 supera su gate:** **G071**
0007:
0008: Este ledger registra los estados aceptados reconstruidos durante VER.2. La regla contable y las exclusiones se documentan en `MATRIZ_DECISION_REVISIONES_VER2.md` y `AUDITORIA_VERSIONADO_PRE_1_0.md`.
0009:
0010: Los identificadores revision-aware son una reconstrucción de auditoría. **No existieron históricamente y no autorizan mover, recrear ni renombrar los tags `v0.0.1-beta`–`v0.0.26-beta`.**
```

```text
0008: Este ledger registra los estados aceptados reconstruidos durante VER.2. La regla contable y las exclusiones se documentan en `MATRIZ_DECISION_REVISIONES_VER2.md` y `AUDITORIA_VERSIONADO_PRE_1_0.md`.
0009:
0010: Los identificadores revision-aware son una reconstrucción de auditoría. **No existieron históricamente y no autorizan mover, recrear ni renombrar los tags `v0.0.1-beta`–`v0.0.26-beta`.**
0011:
0012: ## Convención
```

```text
0072: | G044 | `0.0.44.04-beta` | UX.4.6e R4 — runtime/Jinja/CSS | base `0.0.24-beta` | 566 pruebas |
0073: | G045 | `0.0.45.05-beta` | UX.4.6e R5 — coherencia visible/preparación pública | base `0.0.24-beta` | 576 pruebas |
0074: | G046 | `0.0.46.06-beta` | UX.4.6e R6 — renumeración/metadata | base `0.0.24-beta` | 586 pruebas |
0075: | G047 | `0.0.47.07-beta` | UX.4.6e R7 — auditoría transversal | base `0.0.24-beta` | 598 pruebas |
0076: | G048 | `0.0.48.08-beta` | UX.4.6e — identidad visual oficial y publicación | base `0.0.24-beta` | PR #20 / 624 pruebas |
```

```text
0073: | G045 | `0.0.45.05-beta` | UX.4.6e R5 — coherencia visible/preparación pública | base `0.0.24-beta` | 576 pruebas |
0074: | G046 | `0.0.46.06-beta` | UX.4.6e R6 — renumeración/metadata | base `0.0.24-beta` | 586 pruebas |
0075: | G047 | `0.0.47.07-beta` | UX.4.6e R7 — auditoría transversal | base `0.0.24-beta` | 598 pruebas |
0076: | G048 | `0.0.48.08-beta` | UX.4.6e — identidad visual oficial y publicación | base `0.0.24-beta` | PR #20 / 624 pruebas |
0077: | G049 | `0.0.49.09-beta` | UX.4.6e R8 — validación funcional/procedencia | base `0.0.24-beta` | R8.2 644 / cierre documental 652 |
```

```text
0086: | G058 | `0.0.58.08-beta` | PLAN.1 R3B2 | base `0.0.25-beta` | 710 pruebas |
0087: | G059 | `0.0.59.09-beta` | PLAN.1 R4.1 — candidato local cerrado | base `0.0.25-beta` | PR #23 / 720 pruebas |
0088: | G060 | `0.0.60.10-beta` | PLAN.1 R4.2 — higiene y cierre formal | `v0.0.26-beta` | PR #24 / 720 sin `SyntaxWarning` |
0089: | G061 | `0.0.61.01-beta` | UX.4.6f R1/R1.1 — aceptación conjunta | base `0.0.26-beta` | PR #28 / 743 pruebas |
0090: | G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
```

```text
0087: | G059 | `0.0.59.09-beta` | PLAN.1 R4.1 — candidato local cerrado | base `0.0.25-beta` | PR #23 / 720 pruebas |
0088: | G060 | `0.0.60.10-beta` | PLAN.1 R4.2 — higiene y cierre formal | `v0.0.26-beta` | PR #24 / 720 sin `SyntaxWarning` |
0089: | G061 | `0.0.61.01-beta` | UX.4.6f R1/R1.1 — aceptación conjunta | base `0.0.26-beta` | PR #28 / 743 pruebas |
0090: | G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
0091: | G063 | `0.0.63.03-beta` | UX.4.6f R2 — auditoría lógica/matemática | base `0.0.26-beta` | PR #30 / 756 pruebas |
```

```text
0088: | G060 | `0.0.60.10-beta` | PLAN.1 R4.2 — higiene y cierre formal | `v0.0.26-beta` | PR #24 / 720 sin `SyntaxWarning` |
0089: | G061 | `0.0.61.01-beta` | UX.4.6f R1/R1.1 — aceptación conjunta | base `0.0.26-beta` | PR #28 / 743 pruebas |
0090: | G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
0091: | G063 | `0.0.63.03-beta` | UX.4.6f R2 — auditoría lógica/matemática | base `0.0.26-beta` | PR #30 / 756 pruebas |
0092: | G064 | `0.0.64.04-beta` | UX.4.6f — hardening `pre-commit` y cierre documental | base `0.0.26-beta` | PR #31 / 762 pruebas |
```

```text
0089: | G061 | `0.0.61.01-beta` | UX.4.6f R1/R1.1 — aceptación conjunta | base `0.0.26-beta` | PR #28 / 743 pruebas |
0090: | G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
0091: | G063 | `0.0.63.03-beta` | UX.4.6f R2 — auditoría lógica/matemática | base `0.0.26-beta` | PR #30 / 756 pruebas |
0092: | G064 | `0.0.64.04-beta` | UX.4.6f — hardening `pre-commit` y cierre documental | base `0.0.26-beta` | PR #31 / 762 pruebas |
0093: | G065 | `0.0.65.01-beta` | UX.4.6g R1 — cierre Paso 5 | base `0.0.26-beta` | PR #32 / 784 pruebas |
```

```text
0090: | G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
0091: | G063 | `0.0.63.03-beta` | UX.4.6f R2 — auditoría lógica/matemática | base `0.0.26-beta` | PR #30 / 756 pruebas |
0092: | G064 | `0.0.64.04-beta` | UX.4.6f — hardening `pre-commit` y cierre documental | base `0.0.26-beta` | PR #31 / 762 pruebas |
0093: | G065 | `0.0.65.01-beta` | UX.4.6g R1 — cierre Paso 5 | base `0.0.26-beta` | PR #32 / 784 pruebas |
0094: | G066 | `0.0.66.01-beta` | UX.4.6h R1.1 — corrección aceptada | base `0.0.26-beta` | supera candidato R1 fallido |
```

```text
0091: | G063 | `0.0.63.03-beta` | UX.4.6f R2 — auditoría lógica/matemática | base `0.0.26-beta` | PR #30 / 756 pruebas |
0092: | G064 | `0.0.64.04-beta` | UX.4.6f — hardening `pre-commit` y cierre documental | base `0.0.26-beta` | PR #31 / 762 pruebas |
0093: | G065 | `0.0.65.01-beta` | UX.4.6g R1 — cierre Paso 5 | base `0.0.26-beta` | PR #32 / 784 pruebas |
0094: | G066 | `0.0.66.01-beta` | UX.4.6h R1.1 — corrección aceptada | base `0.0.26-beta` | supera candidato R1 fallido |
0095: | G067 | `0.0.67.02-beta` | UX.4.6h R1.2 — claridad/jerarquía | base `0.0.26-beta` | revisión aceptada |
```

```text
0092: | G064 | `0.0.64.04-beta` | UX.4.6f — hardening `pre-commit` y cierre documental | base `0.0.26-beta` | PR #31 / 762 pruebas |
0093: | G065 | `0.0.65.01-beta` | UX.4.6g R1 — cierre Paso 5 | base `0.0.26-beta` | PR #32 / 784 pruebas |
0094: | G066 | `0.0.66.01-beta` | UX.4.6h R1.1 — corrección aceptada | base `0.0.26-beta` | supera candidato R1 fallido |
0095: | G067 | `0.0.67.02-beta` | UX.4.6h R1.2 — claridad/jerarquía | base `0.0.26-beta` | revisión aceptada |
0096: | G068 | `0.0.68.03-beta` | UX.4.6h R1.3 — informe A4 y cierre Paso 6 | base `0.0.26-beta` | PR #33 / 812 pruebas |
```

```text
0093: | G065 | `0.0.65.01-beta` | UX.4.6g R1 — cierre Paso 5 | base `0.0.26-beta` | PR #32 / 784 pruebas |
0094: | G066 | `0.0.66.01-beta` | UX.4.6h R1.1 — corrección aceptada | base `0.0.26-beta` | supera candidato R1 fallido |
0095: | G067 | `0.0.67.02-beta` | UX.4.6h R1.2 — claridad/jerarquía | base `0.0.26-beta` | revisión aceptada |
0096: | G068 | `0.0.68.03-beta` | UX.4.6h R1.3 — informe A4 y cierre Paso 6 | base `0.0.26-beta` | PR #33 / 812 pruebas |
0097: | G069 | `0.0.69.01-beta` | UX.4.6i R1 — guía pública de cálculo | base `0.0.26-beta` | gate aceptado 826 pruebas |
```

```text
0094: | G066 | `0.0.66.01-beta` | UX.4.6h R1.1 — corrección aceptada | base `0.0.26-beta` | supera candidato R1 fallido |
0095: | G067 | `0.0.67.02-beta` | UX.4.6h R1.2 — claridad/jerarquía | base `0.0.26-beta` | revisión aceptada |
0096: | G068 | `0.0.68.03-beta` | UX.4.6h R1.3 — informe A4 y cierre Paso 6 | base `0.0.26-beta` | PR #33 / 812 pruebas |
0097: | G069 | `0.0.69.01-beta` | UX.4.6i R1 — guía pública de cálculo | base `0.0.26-beta` | gate aceptado 826 pruebas |
0098: | G070 | `0.0.70.02-beta` | UX.4.6i R1.4 — cierre Cómo se calcula | base `0.0.26-beta` | PR #34 / 841 pruebas |
```

```text
0095: | G067 | `0.0.67.02-beta` | UX.4.6h R1.2 — claridad/jerarquía | base `0.0.26-beta` | revisión aceptada |
0096: | G068 | `0.0.68.03-beta` | UX.4.6h R1.3 — informe A4 y cierre Paso 6 | base `0.0.26-beta` | PR #33 / 812 pruebas |
0097: | G069 | `0.0.69.01-beta` | UX.4.6i R1 — guía pública de cálculo | base `0.0.26-beta` | gate aceptado 826 pruebas |
0098: | G070 | `0.0.70.02-beta` | UX.4.6i R1.4 — cierre Cómo se calcula | base `0.0.26-beta` | PR #34 / 841 pruebas |
0099:
```

```text
0096: | G068 | `0.0.68.03-beta` | UX.4.6h R1.3 — informe A4 y cierre Paso 6 | base `0.0.26-beta` | PR #33 / 812 pruebas |
0097: | G069 | `0.0.69.01-beta` | UX.4.6i R1 — guía pública de cálculo | base `0.0.26-beta` | gate aceptado 826 pruebas |
0098: | G070 | `0.0.70.02-beta` | UX.4.6i R1.4 — cierre Cómo se calcula | base `0.0.26-beta` | PR #34 / 841 pruebas |
0099:
0100: ## Estados preservados que no consumen Global
```

```text
0118: ## Próximo estado
0119:
0120: VER.2 no consume G071 por existir como rama o PR draft. Solo si su ledger, validador, documentación, pruebas y CI quedan aceptados se incorpora:
0121:
0122: | Global | ID revision-aware candidato | Bloque | Condición |
```

```text
0122: | Global | ID revision-aware candidato | Bloque | Condición |
0123: |---:|---|---|---|
0124: | G071 | `0.0.71.01-beta` | VER.2 R1 — reconciliación revision-aware | ledger + validador + gate completo + PR/CI verde + integración |
0125:
0126: Después de aceptar G071, DEV.2 puede volver a ser el bloque funcional activo.
```

## docs/MATRIZ_DECISION_REVISIONES_VER2.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # VER.2 — Matriz de decisión de revisiones aceptadas
0002:
0003: **Proyecto:** Mi Retiro Proyectado
0004: **Base auditada:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`
0005: **Rama:** `chore/ver2-revision-ledger`
0006: **Estado:** SEGUNDA PASADA RESUELTA EN LO CONTABLE; pendiente materialización del ledger y gates.
0007:
0008: ## 1. Regla de decisión
0009:
0010: Una revisión consume contador global cuando existe evidencia suficiente de un **estado materialmente distinto y aceptado**. La aceptación puede demostrarse mediante gate técnico satisfactorio, validación manual explícita, integración controlada o combinación de esas señales.
0011:
0012: No se cuenta otra vez el mismo estado por separar implementación, pruebas y documentación en varios commits. Tampoco se cuentan candidatos fallidos, cambios que seguían expresamente pendientes de validación o operaciones de tag/squash que no alteran materialmente el estado ya aceptado.
0013:
0014: Los mantenimientos técnicos, de seguridad, dependencias, gobierno o documentación **sí cuentan** cuando producen un estado independiente, validado y aceptado. No es requisito que tengan una etiqueta `R1/R2`; tampoco basta con que exista un PR o un commit.
0015:
0016: Un checkpoint que solo agrupa revisiones ya contabilizadas o deja explícitamente pendiente la revisión funcional siguiente no suma otra fila. Un hito transversal separado —por ejemplo, identidad oficial/publicación o un mantenimiento de dependencias integrado entre revisiones— sí puede hacerlo si cambia materialmente el estado auditable.
0017:
0018: ## 2. Estados históricos hasta `0.0.21-beta`
0019:
0020: | Estado | Cuenta | Motivo |
0021: |---|---|---|
0022: | Estados retrospectivos `0.0.1-beta`–`0.0.21-beta` | SÍ, 21 estados | GOV.1.1 reconstruyó 80 commits en 21 snapshots históricos; cada snapshot ya representa su unidad contable legado. |
0023: | UX.2.1 | NO adicional | Subfase real incluida en el rango histórico de `0.0.9-beta`; crear otra fila duplicaría el mismo snapshot. Debe aparecer como subfase de ese estado. |
0024: | UX.4.6a revisiones internas previas al cierre | NO adicional | La bitácora conserva iteraciones, pero el estado inequívocamente aceptado es el cierre con 198 pruebas. |
0025: | UX.4.6b R1–R3 | NO adicional | R4 es el cierre demostrado con 233 pruebas y validación PC/laptop/CI. No se demostró aceptación independiente previa equivalente. |
0026: | UX.4.6c R1–R2 | NO adicional | R3 es el cierre demostrado con 253 pruebas y validación visual; R1/R2 fueron refinamientos conducentes al mismo cierre. |
0027: | UX.4.6d R1–R22 | NO adicional | La bitácora repite que la validación integral seguía pendiente. R23 es el cierre inequívoco con 396 pruebas y recorrido Pasos 1–3 aceptado. |
0028:
0029: ## 3. GOV.1.2 y GOV.1.3
0030:
0031: | Estado | Cuenta | Evidencia |
0032: |---|---|---|
0033: | GOV.1.2 — gobierno/versionado formal | SÍ | `0.0.22-beta`, 403 pruebas y tag formal. Los commits de implementación/documentación son una misma revisión. |
0034: | GOV.1.3 R1 | SÍ | 411 pruebas / progreso explícito a R2. |
0035: | GOV.1.3 R2 | SÍ | 423 pruebas / cierre propio. |
0036: | GOV.1.3 R3 | SÍ | 438 pruebas / cierre propio. |
0037: | GOV.1.3 R4 | SÍ | 458 pruebas / cierre de GOV.1.3 y `0.0.23-beta`. |
0038:
0039: ## 4. Prebloque transversal de firma e integridad Git/GitHub
0040:
0041: La primera pasada comprimió todo el prebloque en una sola fila. La segunda pasada confirma cinco estados materiales e integrados consecutivamente.
0042:
0043: | Estado | Cuenta | Evidencia |
0044: |---|---|---|
0045: | Materialización criptográfica y cierre de 23/23 tags | SÍ | commit `685d056…`; 23/23 firmas/objetos/targets verificados y primer commit nuevo `Verified`. |
0046: | CI v7 + rulesets/protecciones GitHub | SÍ | PR #9 integrado; 470/470 pruebas; compilación, JS y `diff --check` limpios. |
0047: | Corrección de rutas PowerShell/caracteres de control | SÍ | PR #10 integrado después del estado #9; añade regresión específica y conserva 470/470. |
0048: | Actualización controlada `pypdf 6.15.0` | SÍ | PR #11 integrado; 474/474, `pip check`, importadores y contratos de terceros sincronizados. |
0049: | Cierre formal del prebloque | SÍ | PR #12 integrado; 474/474, revisión remota final y 0 PR pendientes. |
0050:
0051: **Decisión:** el prebloque aporta **cinco estados aceptados**, no uno.
0052:
0053: ## 5. GOV.1.4–GOV.1.8 y mantenimientos asociados
0054:
0055: | Estado | Cuenta | Evidencia |
0056: |---|---|---|
0057: | GOV.1.4 — Developer Diagnostics | SÍ | 487 pruebas, integración y cierre. |
0058: | GOV.1.5 R1 — modelo de amenazas | SÍ | documento declara cierre original R1; 7 regresiones específicas. |
0059: | GOV.1.5 R2 — derechos/incidentes | SÍ | documentos declaran cierre original R2; 8 regresiones adicionales; suite 502 antes de R3. |
0060: | GOV.1.5 R3 — cierre seguridad/privacidad/transparencia | SÍ | PR #14, 512 pruebas, bloque cerrado. |
0061: | GOV.1.6 — controles GitHub | SÍ | 522 pruebas antes de GOV.1.7; estado diferenciado aunque PR #15 integre más de un bloque. |
0062: | GOV.1.7 — licencia/distribución | SÍ | 530 pruebas; estado diferenciado. |
0063: | Hotfix de formato de licencia | SÍ | PR #16 fue integrado **después** del estado GOV.1.7; corrigió documentos y endureció la regresión con 530/530. |
0064: | GOV.1.8 — cierre integral GOV.1 | SÍ | PR #17; 540 pruebas; `v0.0.24-beta`. |
0065: | Saneamiento post-GOV.1 | SÍ | PR #18 integrado sobre el cierre GOV.1; 30 archivos, 540/540, auditoría del repositorio, soporte/código de conducta y configuración pública. |
0066:
0067: ## 6. UX.4.6e
0068:
0069: | Estado | Cuenta | Evidencia / decisión |
0070: |---|---|---|
0071: | R1 — auditoría integral y patrón documental | SÍ | conversación de desarrollo confirma R1 completada y avance a R2. |
0072: | R2 | SÍ | 550 pruebas, compilación/JS/diff limpios. |
0073: | R3 | SÍ | 558 pruebas. |
0074: | R4 | SÍ | 566 pruebas. |
0075: | R5 | SÍ | 576 pruebas. |
0076: | R6 | SÍ | 586 pruebas. |
0077: | R7 | SÍ | 598 pruebas. |
0078: | PR #19 — checkpoint técnico pre-R8 | NO adicional | Consolida trabajo ya representado por R2–R7 y deja expresamente R8 funcional pendiente. El gate 604 no crea una revisión nueva del producto. |
0079: | Identidad visual oficial + publicación del repositorio / PR #20 | SÍ | Hito transversal independiente: activos oficiales, `brand.css`, favicons/Social Preview, repositorio público y seguridad revalidada; 624 pruebas. No duplica R2–R7 ni R8. |
0080: | R8.1 | NO | Estado intermedio que todavía presentó defectos de `MutationObserver`/checkboxes. |
0081: | R8.2 / R8 funcional | SÍ | 644 pruebas y validación funcional satisfactoria; el posterior cierre documental a 652 materializa la misma R8. |
0082: | R9.1 / R9.2 | SÍ una sola vez | R9.1 alcanzó 660 y dejó el estado candidato; R9.2 materializó PR/CI/tag del mismo cierre. |
0083: | PR #22 — cierre documental final | NO adicional | Registra evidencia post-merge/release de R9 ya contabilizada; no introduce una revisión material nueva. |
0084:
0085: **Decisión:** UX.4.6e aporta **diez estados aceptados**: R1–R7, identidad/publicación, R8 y R9/cierre.
0086:
0087: ## 7. PLAN.1
0088:
0089: | Estado | Cuenta | Evidencia / decisión |
0090: |---|---|---|
```

### Coincidencias con contexto

```text
0001: # VER.2 — Matriz de decisión de revisiones aceptadas
0002:
0003: **Proyecto:** Mi Retiro Proyectado
```

```text
0074: | R4 | SÍ | 566 pruebas. |
0075: | R5 | SÍ | 576 pruebas. |
0076: | R6 | SÍ | 586 pruebas. |
0077: | R7 | SÍ | 598 pruebas. |
0078: | PR #19 — checkpoint técnico pre-R8 | NO adicional | Consolida trabajo ya representado por R2–R7 y deja expresamente R8 funcional pendiente. El gate 604 no crea una revisión nueva del producto. |
```

```text
0075: | R5 | SÍ | 576 pruebas. |
0076: | R6 | SÍ | 586 pruebas. |
0077: | R7 | SÍ | 598 pruebas. |
0078: | PR #19 — checkpoint técnico pre-R8 | NO adicional | Consolida trabajo ya representado por R2–R7 y deja expresamente R8 funcional pendiente. El gate 604 no crea una revisión nueva del producto. |
0079: | Identidad visual oficial + publicación del repositorio / PR #20 | SÍ | Hito transversal independiente: activos oficiales, `brand.css`, favicons/Social Preview, repositorio público y seguridad revalidada; 624 pruebas. No duplica R2–R7 ni R8. |
```

```text
0076: | R6 | SÍ | 586 pruebas. |
0077: | R7 | SÍ | 598 pruebas. |
0078: | PR #19 — checkpoint técnico pre-R8 | NO adicional | Consolida trabajo ya representado por R2–R7 y deja expresamente R8 funcional pendiente. El gate 604 no crea una revisión nueva del producto. |
0079: | Identidad visual oficial + publicación del repositorio / PR #20 | SÍ | Hito transversal independiente: activos oficiales, `brand.css`, favicons/Social Preview, repositorio público y seguridad revalidada; 624 pruebas. No duplica R2–R7 ni R8. |
0080: | R8.1 | NO | Estado intermedio que todavía presentó defectos de `MutationObserver`/checkboxes. |
```

```text
0077: | R7 | SÍ | 598 pruebas. |
0078: | PR #19 — checkpoint técnico pre-R8 | NO adicional | Consolida trabajo ya representado por R2–R7 y deja expresamente R8 funcional pendiente. El gate 604 no crea una revisión nueva del producto. |
0079: | Identidad visual oficial + publicación del repositorio / PR #20 | SÍ | Hito transversal independiente: activos oficiales, `brand.css`, favicons/Social Preview, repositorio público y seguridad revalidada; 624 pruebas. No duplica R2–R7 ni R8. |
0080: | R8.1 | NO | Estado intermedio que todavía presentó defectos de `MutationObserver`/checkboxes. |
0081: | R8.2 / R8 funcional | SÍ | 644 pruebas y validación funcional satisfactoria; el posterior cierre documental a 652 materializa la misma R8. |
```

```text
0083: | PR #22 — cierre documental final | NO adicional | Registra evidencia post-merge/release de R9 ya contabilizada; no introduce una revisión material nueva. |
0084:
0085: **Decisión:** UX.4.6e aporta **diez estados aceptados**: R1–R7, identidad/publicación, R8 y R9/cierre.
0086:
0087: ## 7. PLAN.1
```

```text
0139: | R1.2 | NO adicional | Changelog documenta el refinamiento y objetivo 832, pero la búsqueda cruzada no recupera aceptación independiente antes de R1.3. |
0140: | R1.3 | NO adicional | Changelog documenta el refinamiento y objetivo 840, pero la búsqueda cruzada no recupera aceptación independiente antes de R1.4. |
0141: | R1.4 | SÍ | cierre PR #34, 841/841, Python/JS/diff correctos y transición a DEV.2. |
0142:
0143: ## 12. Conteo resultante de la segunda pasada
```

```text
0162: | UX.4.6h | 3 |
0163: | UX.4.6i | 2 |
0164: | **Total aceptado antes de VER.2** | **70** |
0165:
0166: El último estado aceptado antes de VER.2 es, por tanto, **G070**.
```

```text
0164: | **Total aceptado antes de VER.2** | **70** |
0165:
0166: El último estado aceptado antes de VER.2 es, por tanto, **G070**.
0167:
0168: La secuencia desde G022 queda:
```

```text
0185: - G069–G070 UX.4.6i.
0186:
0187: ## 13. Consecuencia para VER.2
0188:
0189: Los conteos G057 y G060 quedan **formalmente superados** por esta segunda pasada.
```

```text
0189: Los conteos G057 y G060 quedan **formalmente superados** por esta segunda pasada.
0190:
0191: Si la materialización del ledger, las regresiones, el JSON estructurado y el gate de VER.2 no descubren otra inconsistencia histórica, el cierre aceptado de VER.2 consumirá **G071**. Hasta ese momento `VERSION` no debe tratarse como promovida definitivamente.
0192:
0193: ## 14. Próximo paso
```

## docs/OBSERVABILIDAD_LOGS.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # Observabilidad y Developer Diagnostics
0002:
0003: **Estado:** Vigente — GOV.1.4 cerrado
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Versión base histórica:** `0.0.23-beta`
0007: **Fecha de cierre original:** 2026-08-17
0008: **Última revisión documental:** PLAN.1 R2C — 2026-08-20
0009: **Clasificación:** Técnica / Desarrollo / Privacidad
0010:
0011: Mi Retiro Proyectado incorpora un mecanismo de diagnóstico **exclusivo de desarrollo**, desactivado por defecto. Su objetivo es depurar fallos, tiempos y dependencias técnicas sin convertir el log en una segunda base de datos de simulaciones.
0012:
0013: ## 1. Activación
0014:
0015: Developer Diagnostics solo se activa con:
0016:
0017: ```powershell
0018: $env:MRP_DEV_MODE = "1"
0019: ```
0020:
0021: Cualquier otro valor, incluida la variable ausente, mantiene el diagnóstico desactivado. No existe un control de interfaz para activarlo.
0022:
0023: El directorio puede sobrescribirse únicamente para desarrollo/pruebas:
0024:
0025: ```powershell
0026: $env:MRP_DIAGNOSTIC_DIR = "C:\ruta\temporal"
0027: ```
0028:
0029: Por defecto se usa:
0030:
0031: ```text
0032: logs/diagnostico/
0033: ```
0034:
0035: `logs/` está excluido por `.gitignore`.
0036:
0037: ## 2. Formato
0038:
0039: Cada línea de `mrp-diagnostics.jsonl` es un objeto JSON independiente con esquema lógico `1`:
0040:
0041: - `schema_version`;
0042: - `timestamp` UTC;
0043: - `level`;
0044: - `event`;
0045: - `component`;
0046: - `app_version`;
0047: - `correlation_id`;
0048: - `duration_ms`;
0049: - `outcome`;
0050: - `metadata`.
0051:
0052: La versión del esquema de diagnóstico es independiente de `VERSION`, de la normativa y de la política de privacidad.
0053:
0054: ## 3. Correlación
0055:
0056: Cada operación observada usa un `correlation_id` aleatorio UUID4 sin guiones.
0057:
0058: El identificador:
0059:
0060: - se genera aleatoriamente;
0061: - no deriva de cédula, NSS, nombre, fecha de nacimiento, salario, IP u otro dato del usuario;
0062: - permite relacionar eventos técnicos de una misma operación;
0063: - se devuelve como `X-Correlation-ID` únicamente cuando `MRP_DEV_MODE=1` y la ruta está instrumentada.
0064:
0065: ## 4. Middleware HTTP
0066:
0067: R2 integra Developer Diagnostics en FastAPI.
0068:
0069: El middleware:
0070:
0071: - se omite completamente cuando el modo está apagado;
0072: - llama a `call_next()` una sola vez;
0073: - no lee el cuerpo de la solicitud;
0074: - no serializa modelos Pydantic;
0075: - clasifica la operación mediante etiquetas fijas;
0076: - registra método, clase de operación, estado HTTP y duración;
0077: - registra errores no controlados sin almacenar el mensaje original de la excepción;
0078: - no registra literalmente rutas desconocidas: se agrupan como `http.other`;
0079: - omite recursos estáticos y favicon para reducir ruido.
0080:
0081: La observabilidad no ejecuta motores, servicios ni cálculos por segunda vez.
0082:
0083: ## 5. Operaciones observadas
0084:
0085: Las etiquetas técnicas incluyen, entre otras:
0086:
0087: ```text
0088: simulation.cuotas
0089: simulation.historial
0090: simulation.detalle_actual
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente — GOV.1.4 cerrado
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Versión base histórica:** `0.0.23-beta`
```

```text
0231: - coherencia de README, Arquitectura, Índice, Seguridad/Privacidad, Transparencia, Limitaciones, Validación, Roadmap y Guía interna.
0232:
0233: Históricamente, el siguiente bloque de gobierno fue GOV.1.5 — Seguridad, privacidad y transparencia.
0234:
0235: GOV.1.4 no modificó fórmulas previsionales ni `VERSION`; en su cierre original la aplicación permanecía en `0.0.23-beta`.
```

## docs/POLITICA_PRIVACIDAD.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # Política de privacidad y tratamiento de datos
0002:
0003: **Producto:** Mi Retiro Proyectado
0004: **Versión del texto:** `2026-08-16.1`
0005: **Estado:** Vigente en la aplicación
0006: **Versión de aplicación revisada:** `0.0.26-beta`
0007: **Versión base histórica:** `0.0.25-beta`
0008: **Versión base histórica:** `0.0.23-beta`
0009: **Base documental:** GOV.1.3 R3 — 2026-08-17
0010: **Revisión transversal histórica:** GOV.1.5 R3 — 2026-08-18
0011: **Última revisión documental:** PLAN.1 R3B1 — 2026-08-20
0012: **Revisión jurídica externa:** Pendiente antes de la primera versión oficial o de un despliegue remoto que cambie el tratamiento
0013:
0014: Esta política describe el tratamiento implementado actualmente. No constituye certificación jurídica.
0015:
0016: ## 1. Responsable
0017:
0018: **Rubén Enrique Cañizares Miranda**, Panamá.
0019:
0020: Contacto: `ruben.canizares@outlook.com`
0021:
0022: ## 2. Marco de referencia
0023:
0024: - Ley 81 de 26 de marzo de 2019 sobre Protección de Datos Personales;
0025: - Decreto Ejecutivo 285 de 28 de mayo de 2021;
0026: - orientaciones y preguntas frecuentes de ANTAI.
0027:
0028: Fuentes: `FUENTES_NORMATIVAS.md`.
0029:
0030: ## 3. Principios aplicados
0031:
0032: El diseño busca aplicar:
0033:
0034: - finalidad;
0035: - minimización;
0036: - transparencia;
0037: - seguridad;
0038: - confidencialidad;
0039: - control del titular.
0040:
0041: ## 4. Datos que puede tratar la simulación
0042:
0043: ### Identificación opcional
0044:
0045: - nombres/apellidos;
0046: - apellido de casada;
0047: - cédula;
0048: - número de Seguro Social.
0049:
0050: Estos datos no son necesarios para ejecutar las fórmulas principales.
0051:
0052: ### Datos previsionales
0053:
0054: - fecha de nacimiento;
0055: - sexo;
0056: - fecha de ingreso a CSS cuando se conozca;
0057: - sistema previsional;
0058: - cuotas;
0059: - salarios/historial;
0060: - detalle mensual/quincenal;
0061: - escenarios;
0062: - resultados.
0063:
0064: ## 5. Origen
0065:
0066: Los datos provienen:
0067:
0068: - de captura manual; o
0069: - de documentos seleccionados voluntariamente.
0070:
0071: Una importación se revisa antes de confirmar.
0072:
0073: ## 6. Finalidad
0074:
0075: Los datos se utilizan para:
0076:
0077: - construir la simulación;
0078: - comprobar coherencia;
0079: - proyectar;
0080: - comparar escenarios;
0081: - estimar prestaciones;
0082: - explicar resultados.
0083:
0084: No se autoriza su uso para publicidad, venta de información o perfilado comercial.
0085:
0086: ## 7. Consentimiento
0087:
0088: La versión material vigente es **2026-08-16.1**.
0089:
0090: Para utilizar Simular se requiere:
```

### Coincidencias con contexto

```text
0004: **Versión del texto:** `2026-08-16.1`
0005: **Estado:** Vigente en la aplicación
0006: **Versión de aplicación revisada:** `0.0.26-beta`
0007: **Versión base histórica:** `0.0.25-beta`
0008: **Versión base histórica:** `0.0.23-beta`
```

```text
0216: ## 19. Historia
0217:
0218: La evolución R6–R21 se conserva en:
0219:
0220: `docs/archive/regulatory-privacy/POLITICA_PRIVACIDAD_PRE_GOV1_3_R3.md`
```

## docs/TRANSPARENCIA.md

- Categoría DOC.1 R1: `REVISAR_MANUALMENTE`
- Existe: `True`

### Primeras líneas

```text
0001: # Transparencia del producto
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Versión base histórica preservada:** `0.0.23-beta`
0007: **Base documental preservada:** GOV.1.3 R4 — 2026-08-17
0008: **Revisión transversal vigente:** UX.4.6i — cierre de guía pública de cálculo — 2026-08-21
0009: **Clasificación:** Pública / Auditoría
0010:
0011: Mi Retiro Proyectado es una herramienta independiente de estimación previsional. Este documento delimita qué puede afirmarse sobre el producto y qué debe permanecer explícitamente como aproximación, limitación o pendiente.
0012:
0013: ## 1. Qué es
0014:
0015: La aplicación permite:
0016:
0017: - organizar datos previsionales;
0018: - diferenciar información acreditada de supuestos futuros;
0019: - ejecutar motores SEBD, Mixto y SUCGS dentro del alcance documentado;
0020: - comparar escenarios;
0021: - explicar resultados mediante una capa de trazabilidad;
0022: - vincular fuentes y decisiones de implementación;
0023: - disponer de diagnóstico técnico local de desarrollo mediante Developer Diagnostics.
0024:
0025: El repositorio de código es público bajo la licencia vigente del proyecto.
0026:
0027: ## 2. Qué no es
0028:
0029: La aplicación:
0030:
0031: - no es un sistema oficial de la Caja de Seguro Social;
0032: - no certifica cuotas, salarios, saldos o derechos;
0033: - no emite resoluciones;
0034: - no sustituye una determinación administrativa;
0035: - no constituye asesoría jurídica individual;
0036: - no garantiza que un resultado estimado coincida con una futura determinación oficial;
0037: - no se convierte en una versión oficial ni en un despliegue de producción únicamente porque su repositorio sea público.
0038:
0039: ## 3. Datos acreditados y proyectados
0040:
0041: El producto conserva como conceptos distintos:
0042:
0043: - datos históricos/acreditados;
0044: - información importada y confirmada;
0045: - supuestos manuales;
0046: - proyecciones futuras;
0047: - referencias personales externas.
0048:
0049: Una referencia de Mi Retiro Seguro no calibra ni corrige automáticamente los motores. Sirve para comparación contextual cuando los supuestos son compatibles.
0050:
0051: ## 4. Normativa
0052:
0053: Los parámetros legales se versionan en `regulations/*.json` y se relacionan con `NORMATIVA.md` y `FUENTES_NORMATIVAS.md`.
0054:
0055: Los JSON son configuración auditable de la implementación, no una reproducción con fuerza jurídica propia.
0056:
0057: Las discrepancias identificadas se documentan; no se armonizan silenciosamente.
0058:
0059: ## 5. Explicabilidad del cálculo
0060:
0061: `app/models/traceability.py` y `app/services/traceability.py` describen datos utilizados, origen, reglas, fórmulas mostrables, sustituciones, resultados intermedios, fuentes y advertencias.
0062:
0063: La capa de trazabilidad **no vuelve a calcular** la prestación. Developer Diagnostics tampoco recalcula: observa la operación ya ejecutada.
0064:
0065: La ruta pública `/como-se-calcula` explica el orden de operaciones de SEBD, Mixto y SUCGS con parámetros leídos desde `regulations/*.json`. La guía no ejecuta motores ni reconstruye el resultado personal: la sustitución con cifras del Asegurado(a) permanece en la trazabilidad del Paso 6. Los ejemplos son ilustrativos y cualquier parámetro hipotético se identifica como no oficial.
0066:
0067: ## 6. Privacidad
0068:
0069: La simulación actual está diseñada para ejecución local y no utiliza una base de datos permanente de casos.
0070:
0071: Las conexiones externas vigentes están documentadas:
0072:
0073: - jsDelivr para Bootstrap;
0074: - infraestructura oficial CSS para consulta mínima de fecha de referencia cuando corresponde.
0075:
0076: Developer Diagnostics:
0077:
0078: - está apagado por defecto;
0079: - es local;
0080: - no es analítica de producto;
0081: - no envía logs automáticamente a terceros;
0082: - prohíbe registrar PII, PDF y valores financieros.
0083:
0084: La visibilidad pública del código **no autoriza versionar documentos personales reales, credenciales, secretos ni evidencia sensible**.
0085:
0086: Consultar `POLITICA_PRIVACIDAD.md`, `SEGURIDAD_PRIVACIDAD.md` y `OBSERVABILIDAD_LOGS.md`.
0087:
0088: ## 7. Validación
0089:
0090: Las pruebas automatizadas demuestran contratos técnicos concretos. No demuestran por sí solas:
```

### Coincidencias con contexto

```text
0002:
0003: **Estado:** Vigente
0004: **Versión de aplicación revisada:** `0.0.26-beta`
0005: **Versión base histórica:** `0.0.25-beta`
0006: **Versión base histórica preservada:** `0.0.23-beta`
```

```text
0120: Como evidencia del checkpoint anterior se conserva la formulación: **no declara completada la primera beta publica de producto**. PLAN.1 sustituyó posteriormente esa meta por la transición directa desde la línea beta `0.0.N-beta` hacia `1.0.0.0`.
0121:
0122: Como evidencia histórica también se conserva la formulación **“cierre de UX.4.6e y del alcance funcional UX.4.6f–h”**, que en aquella revisión describía trabajo todavía pendiente. Esa frase se mantiene únicamente para preservar la trazabilidad documental y **ya no representa el estado vigente**.
0123:
0124: UX.4.6e cerró en `0.0.25-beta`; UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i están cerrados sobre `0.0.26-beta`. El bloque funcional activo es DEV.2 — Centro de desarrollo; después continúan SEC.2, DOC.2, PERSIST.1, REP.1, A11Y.2, REV.1, QA.1 y REL.1 conforme al plan maestro.
```

```text
0122: Como evidencia histórica también se conserva la formulación **“cierre de UX.4.6e y del alcance funcional UX.4.6f–h”**, que en aquella revisión describía trabajo todavía pendiente. Esa frase se mantiene únicamente para preservar la trazabilidad documental y **ya no representa el estado vigente**.
0123:
0124: UX.4.6e cerró en `0.0.25-beta`; UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i están cerrados sobre `0.0.26-beta`. El bloque funcional activo es DEV.2 — Centro de desarrollo; después continúan SEC.2, DOC.2, PERSIST.1, REP.1, A11Y.2, REV.1, QA.1 y REL.1 conforme al plan maestro.
0125:
0126: Continúan pendientes, según corresponda:
```
