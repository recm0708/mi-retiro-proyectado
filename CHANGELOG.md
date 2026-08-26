# Changelog

Este archivo registra **cambios notables por versión**. No sustituye el historial Git, `RELEASES.md` ni las bitácoras históricas conservadas en `docs/archive/`.

Las versiones `0.0.1-beta` a `0.0.21-beta` fueron reconstruidas retrospectivamente en GOV.1.1 a partir del historial real. `0.0.22-beta` es la primera versión formal adoptada bajo la política de GOV.1.2.

## [Unreleased]


### DOC.2 R1 — reconstrucción auditable del CHANGELOG legacy

- reconstruye `0.0.1-beta`–`0.0.21-beta` desde 80 commits reales y los rangos canónicos de `RELEASES.md`;
- preserva el carácter retrospectivo de esos estados y los tags materializados posteriormente;
- agrega evidencia machine-readable en `data/doc2-legacy-changelog-evidence.json` y auditoría en `docs/audits/documentation/changelog-reconstruction-doc2-r1.md`;
- sincroniza el cierre real de G110: `v0.1.10.01-beta` y su GitHub Release están publicados;
- registra el backfill administrativo histórico: 29 tags formales cuentan con 29 GitHub Releases, sin mover ni recrear tags;
- G111/E01 (`0.1.11.01-beta`) continúa reservado para DOC.2 y no se consume hasta gate, commit firmado, PR/CI y merge.
## [0.1.10.01-beta]
- G110/E01: REL.GOV.1 R1 aceptado mediante PR #85 y merge `5cd1cea`; normaliza el gobierno de GitHub Releases y corrige la interpretación viva de `v0.0.71.01-beta` como G087/E01 sin alterar su tag histórico.
- Releases: incorpora `.github/release.yml`, `scripts/release_contract.py` y validación de tag en GitHub Actions para estandarizar título, prerelease, cuerpo mínimo, firma y correspondencia VERSION/ledger/tag.
- Gate REL.GOV.1 R1: 1054 pruebas locales en `OK`, Markdown 142/142, CI Python 3.13/3.14, Markdown Audit y Repository Governance Audit en `success`; la promoción G110/E01 fue revalidada posteriormente con 1058 pruebas en `OK` antes del tag.
- Ledger: G110 queda aceptado; G111/E01 (`0.1.11.01-beta`) pasa a ser el siguiente candidato disponible para DOC.2.
- Tag/Release: `v0.1.10.01-beta` fue creado de forma firmada sobre `cef373a`, pasó Git Tag Signature Verification y cuenta con GitHub Release prerelease; los tags históricos permanecen inmutables.

## [0.1.09.01-beta]
- G109/E01: promoción post-merge de AUD.SEC2 R1 después de PR #83, 1040 pruebas locales y CI remota en Python 3.13/3.14 + auditorías de Markdown/gobernanza en `success`; la sincronización no consume G110.
- Ledger: G109 queda aceptado sobre `ec1842d`; G110/E01 (`0.1.10.01-beta`) queda disponible y posteriormente se reserva para REL.GOV.1 antes de DOC.2.
- Tag/Release: `v0.1.09.01-beta` fue creado de forma firmada y publicado como prerelease después de integrar/revalidar la promoción; `v0.0.71.01-beta` permanece inmutable.

- AUD.SEC2 R1: audita integralmente el snapshot post-SEC.2, corrige el kill switch administrativo, impide que una sesión web sustituya errores 403 de administración deshabilitada/no configurada, cambia el logout a POST y extiende `Cache-Control: no-store` a `/dev/`.
- AUD.SEC2 R1: reconcilia el ledger posterior a G070 hasta G108, preserva el snapshot histórico G070 por SHA-256 y documenta que `v0.0.71.01-beta` es un tag inmutable cuyo estado corresponde cronológicamente a G087.
- AUD.SEC2 R1: audita los 140 Markdown del snapshot `4bd7d8d`, actualiza únicamente documentación viva materialmente afectada y mueve la evidencia de cierre SEC.2 a `docs/audits/security/`.
- SEC.2 R2–R6: autenticación administrativa, protección centralizada, auditoría de accesos, sesión web temporal y endurecimiento configurable para despliegue interno HTTPS.
- SEC.2: cierre formal de R1–R6 integrado en `main`; no constituye por sí solo una nueva release ni autoriza retagging.
- SEC.2 R1: inicia el hardening integral, elimina dos sinks DOM dinámicos detectados por CodeQL en el informe imprimible y normaliza los nombres técnicos de workflows GitHub Actions.
- DOC.1 R2: completa la auditoría integral Markdown post-NOR.2, normaliza metadata y estados vigentes, retira cuatro stubs documentales residuales, preserva la verdad histórica e incorpora auditoría Markdown permanente en pre-commit y GitHub Actions.
- NOR.2 R8: ejecuta la auditoría integral de cierre, retira dos fragmentos transitorios de `docs/`, corrige estados vivos obsoletos, revalida estructura, artefactos locales, versión y ledger, y agrega regresión final de normalización.
- NOR.2 R7: migra la evidencia local heredada desde `_entregas/` hacia `_deliverables/`, conserva 20 artefactos únicos, retira 8 duplicados SHA-256 exactos y elimina un ZIP reproducible íntegramente desde Git.
- NOR.2 R6: normaliza el ledger estructurado a `data/pre-1-0-revision-ledger.json`, preserva íntegramente G001–G070 y actualiza consumidores vivos sin reescribir evidencia histórica.
- NOR.2 R5: archiva 36 documentos cerrados en `docs/archive/`, actualiza índices históricos y separa evidencia cerrada de documentación viva.
- NOR.2 R4: migra 41 documentos vivos a áreas canónicas, consolida 2 estándares heredados y sincroniza enlaces/referencias sin conservar stubs de compatibilidad.
- NOR.2 R3: migra 28 rutas técnicas de runtime, plantillas, pruebas y configuración; mantiene estables las URL públicas y preserva Ficha Digital como excepción de dominio.
- NOR.2 R2: clasifica la migración integral, corrige el estado público del `README.md` y define que el árbol vigente no conservará rutas/documentos obsoletos salvo evidencia histórica justificada.
- NOR.2 R1: inicia la auditoría integral de normalización contra los estándares cerrados por NOR.1, sin ejecutar todavía renombres ni movimientos.
- NOR.1 R7: cierra la fase de definición de estándares del repositorio y deja NOR.2 como siguiente fase de normalización previa a SEC.2.
- NOR.1 R1–R6: establece estructura, nomenclatura determinística, ciclo de vida, política de raíz/artefactos locales y auditorías de estructura, documentación y dependencias.
- DOC.1 R1: inicia la auditoría integral de todos los archivos Markdown post-MANT.1, con inventario, matriz de decisión, contexto de actualización y línea base documental.
- DOC.1 R1: cierra la auditoría documental Markdown post-MANT.1, documenta alcance, evidencia, límites respetados y agrega regresión documental.
- MANT.1 R7: cierra operativamente la auditoría post-renombres mediante PR #55, dejando `main` alineado con R5H/R6/R7 y sin cambios en archivos protegidos.
- MANT.1 R6: valida funcionalmente el repositorio después de los renombres técnicos, con pruebas focalizadas y documentación de cierre.
- MANT.1 R5H: se completa la auditoría de nombres técnicos restantes, con normalización de módulos, assets, plantillas, workflow y pruebas, sin cambios en cálculo, normativa ni versión.

### MANT.1 R5G

- Agrega auditoría documental R5G para revisar índice, enlaces internos y coherencia documental vigente.
- Actualiza `docs/INDICE.md` para incluir documentos raíz que existían en `docs/` pero no estaban listados.
- Conserva expresiones de dominio como normativa/privacidad, normativa/código y normativa/jurídica porque no son rutas obsoletas.
- Mantiene sin cambios la lógica de cálculo, valores normativos, `VERSION`, `APP_VERSION`, `SEC.2` y `_entregas/`.
## MANT.1 R5F

- Normaliza nombres de archivos técnicos en `scripts`, `data`, `regulations` y pruebas seleccionadas.
- Actualiza referencias documentales, hooks, rutas internas y pruebas relacionadas.
- Agrega `docs/archive/technical/AUDITORIA_ARCHIVOS_R5F.md` y `tests/test_mant1_r5f_nombres_archivos.py` para documentar y proteger el cambio.
- Mantiene sin renombrar archivos de dominio como `mixto.json`, `sebd.json` y `sucgs.json`, y preserva archivos históricos con trazabilidad `UX46`, `VER2` o `revision-aware`.

## MANT.1 R5E — estandarización de nombres de carpetas

- renombra carpetas técnicas en español a rutas en inglés: `app/models/`, `app/engines/`, `app/services/`, `regulations/`, `tests/validation_cases/` y `docs/archive/`;
- actualiza imports Python, rutas de pruebas, enlaces documentales, CODEOWNERS, `.gitignore` y referencias a parámetros JSON;
- documenta la auditoría de carpetas en `docs/archive/technical/AUDITORIA_CARPETAS_R5E.md`;
- agrega regresión para impedir que reaparezcan carpetas técnicas antiguas o referencias a rutas obsoletas;
- mantiene sin cambios `_entregas/`, carpetas convencionales con punto inicial, `VERSION`, `APP_VERSION`, motores previsionales, valores JSON, rutas públicas, selectores y SEC.2.

### MANT.1 R5D — política, plantillas y uniformidad por extensión

- documenta la política formal de estructura por extensión para archivos no Markdown;
- agrega auditoría de inventario por extensión y hallazgos de uniformidad;
- incorpora plantillas oficiales por extensión en `docs/templates/file-structure/`;
- uniforma encabezados de `app/static/js/*.js` y `app/static/css/*.css` con propósito y alcance permanente;
- agrega regresión para proteger política, plantillas y encabezados de presentación sin cambiar lógica, storage, selectores, rutas ni textos visibles;
- no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, ledger VER.2 ni SEC.2.

### MANT.1 R5C — comentarios internos en JavaScript complejo

- agrega comentarios internos de intención en JavaScript de alto impacto: comparador, simulación, resultados, orquestación del Paso 6, gestión de datos, privacidad, procesamiento de adjuntos e importación de documentos oficiales;
- documenta flujos de storage, invalidación descendente, borradores revisables, transición Mixto/SUCGS, comparación acreditado/proyectado y estado accesible de adjuntos;
- mantiene comentarios de `app/static/js/` libres de identificadores de revisión, PR o bloques históricos;
- agrega regresión para proteger comentarios funcionales en los ocho módulos revisados sin cambiar claves de storage, selectores, ids, clases, textos visibles ni lógica;
- no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.

### MANT.1 R5B — comentarios internos en CSS y plantilla Cómo se calcula

- agrega comentarios estructurales en `app/static/css/como-se-calcula.css` para delimitar hero, navegación, secciones, fórmulas, tablas, factores, accesibilidad y responsive;
- agrega comentarios Jinja en `app/templates/como_se_calcula.html` para ubicar recorrido general, bloques SEBD/Mixto/SUCGS, fuentes y cierre de la guía;
- mantiene los comentarios de `app/` libres de identificadores de revisión, PR o bloques históricos;
- agrega regresión para proteger comentarios funcionales en CSS y plantilla sin cambiar clases, ids, textos visibles ni lógica Jinja;
- no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.

### MANT.1 R5A — comentarios internos en servicios Python de aplicación

- agrega comentarios internos de intención en servicios Python de alto tamaño: trazabilidad, comparador, guía de cálculo, fuentes normativas, detalle del año actual y Ficha Digital;
- mantiene los comentarios dentro de `app/services/` libres de identificadores de revisión, PR o bloques históricos;
- agrega regresión para exigir comentarios internos útiles en los servicios revisados sin cambiar lógica funcional;
- no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, contratos JSON, rutas públicas ni SEC.2.

### MANT.1 R4 — limpieza de trazabilidad en encabezados operativos

- limpia encabezados de YAML GitHub para que describan propósito y alcance permanente, sin declarar MANT.1 dentro de archivos operativos;
- elimina metadatos de bloque/origen de los README operativos de `.githooks/` y `scripts/`;
- ajusta la regresión de MANT.1 R3 para exigir encabezados funcionales en YAML, no encabezados con nombre de revisión;
- agrega regresión MANT.1 R4 para impedir trazabilidad de revisión en encabezados operativos;
- no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa, workflows, formularios, Dependabot ni SEC.2.

### MANT.1 R3 — encabezados YAML de GitHub

- documenta los YAML de GitHub antes de SEC.2 sin modificar triggers, jobs, permisos, formularios, labels ni cadencias;
- no cambia `VERSION`, `APP_VERSION`, motores previsionales, normativa ni ledger VER.2;
- agrega encabezados semánticos a Dependabot, workflows e Issue Forms para explicar propósito, límites y privacidad operacional;
- sincroniza `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`, `docs/VALIDACION.md`, `docs/ARQUITECTURA.md` y `docs/ROADMAP.md`;
- agrega regresión documental para proteger encabezados funcionales en `.github/` y que MANT.1 R1/R2/R3 queden visibles en la documentación transversal.

### MANT.1 R2 — documentación de scripts y hooks

- materializa los primeros cambios de mantenimiento técnico derivados de MANT.1 R1, sin cambiar `VERSION`, `APP_VERSION`, motores previsionales ni normativa;
- documenta `.githooks/pre-commit`, `scripts/configure_git_hooks.ps1` y `scripts/validate_precommit.py`;
- agrega `scripts/README.md` y `.githooks/README.md` para explicar propósito, alcance, límites y relación con CI;
- sincroniza `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`, `docs/VALIDACION.md`, `docs/ARQUITECTURA.md` y `docs/ROADMAP.md`;
- agrega regresión documental para proteger el contrato de scripts y hooks;
- absorbe la corrección de higiene textual detectada durante la validación local previa al commit.

### MANT.1 R1 — auditoría inicial y plan de mantenimiento

- inicia MANT.1 como mantenimiento técnico previo a SEC.2;
- clasifica el inventario rastreado de código, configuración, hooks y pruebas en `.githooks`, `.github`, `app`, `scripts` y `tests`;
- identifica archivos sin encabezado inicial en YAML, JavaScript, plantillas principales, CSS específico y PowerShell;
- define una ejecución incremental por revisiones para evitar cambios masivos y preservar la sincronización entre código, pruebas y documentación.

### DEV.2 — cierre del Centro de desarrollo

- cierra documentalmente DEV.2 después de integrar PR #37, PR #38, PR #39 y PR #40;
- deja el Centro de desarrollo con estado interno, visor diagnóstico seguro, exportación ZIP sanitizada y autodiagnóstico técnico local;
- sincroniza README, CHANGELOG, ARQUITECTURA, ADR-179 y `docs/DEV2_CENTRO_DESARROLLO.md` para eliminar referencias a DEV.2 como bloque no iniciado;
- conserva `VERSION` y `APP_VERSION` en `0.0.26-beta`, no crea tag y no modifica motores previsionales ni flujos públicos de cálculo;
- deja VER.2 como siguiente cierre transversal de versionado y documentación revision-aware.

### VER.2 — reconciliación revision-aware pre-1.0

- reaudita por segunda vez el historial completo hasta el cierre UX.4.6i y separa estados aceptados, candidatos fallidos, refinamientos internos, commits lógicos, checkpoints y mantenimiento independiente;
- sustituye los conteos provisionales anteriores y fija la base `7037addd44253e528c77460b678d2b3ccd540dd5` en **70 estados aceptados (G001–G070)**;
- adopta para estados beta nuevos el identificador `0.GG.RR.EE-beta`, manteniendo `0.0.N-beta` como familia legacy histórica;
- reserva `0.0.71.01-beta` para VER.2 G071/E01; G071 solo se consume después de ledger/validador, gate completo, PR/CI e integración;
- preserva sin mover ni recrear los tags `v0.0.1-beta`–`v0.0.26-beta` y prohíbe tags revision-aware retrospectivos para G001–G070;
- documenta UX.2.1 y las revisiones internas UX.4.6a–d sin volver a contarlas cuando ya están absorbidas por los 21 estados retrospectivos;
- reconoce como estados independientes cuando la evidencia lo sustenta los hitos de firma/integridad, seguridad/gobierno, mantenimiento, identidad/publicación, PLAN.1 y los cierres posteriores;
- corrige la secuencia canónica de UX.4.6i a **R1 → R1.2 → R1.3 → R1.4**; no existe evidencia independiente de una revisión intermedia no demostrada entre UX.4.6i R1 y R1.2;
- separa la versión vigente de aplicación de la metadata histórica que indica en qué versión fue revisado un documento de dominio;
- incorpora ledger estructurado en `data/pre-1-0-revision-ledger.json`, validador `app/core/version_ledger.py`, matriz de decisión, auditoría y regresiones de coherencia;
- DEV.2 queda cerrado como bloque funcional independiente antes del cierre final de VER.2, sin consumir promoción revision-aware ni cambiar VERSION, APP_VERSION o tags.

### UX.4.6i — cierre de Cómo se calcula

- R1.4 simplifica la etiqueta visible de sustitución numérica de **Ejemplo con números** a **Ejemplo** sin alterar fórmulas ni valores;
- consolida R1/R1.2/R1.3/R1.4 como cierre de la guía pública de cálculo;
- la validación manual confirmó navegación, recorrido Pasos 1–6, SEBD, Mixto, SUCGS, tablas compactas, terminología contextual, ejemplos sustituidos y jerarquía visual;
- el gate de cierre quedó fijado en **841 pruebas** y DEV.2 quedó documentado en ese momento como bloque funcional posterior a cualquier reconciliación transversal necesaria.

### UX.4.6i R1.3 — ejemplos sustituidos, términos y respiración visual

- añade ejemplos numéricos inmediatamente después de las fórmulas descriptivas de los Pasos 1–6 y de SEBD, Mixto y SUCGS, sin sustituir la fórmula general ni ejecutar un segundo motor;
- incorpora definiciones contextuales de cuotas, salario cotizado, modalidad, salario base, tasa de reemplazo, BD, CAP, saldo CAP, pensión programada CAP, factor actuarial, PGS y demás términos necesarios para leer la guía;
- documenta también la tasa anual equivalente de un salario futuro conocido y la estimación de cuotas de una fracción de año;
- aumenta el espacio entre títulos/tablas, fórmulas/notas y la franja de fuentes de cada sistema;
- mantiene los refinamientos mediante tokens semánticos para Claro, Oscuro y Alto contraste;
- añade ocho regresiones específicas; gate objetivo **840 pruebas**.

### UX.4.6i R1.2 — recorrido de datos y densidad visual

- añade **Cómo se calcula** como destino directo de la navegación principal y lo marca como página activa independiente de Fuentes;
- amplía el recorrido general para explicar cómo los datos de los Pasos 1–5 se transforman en edad, cuotas, historial, salario normalizado, proyección, línea temporal y escenario de retiro antes del cálculo del Paso 6;
- incorpora las fórmulas descriptivas ya implementadas para normalización salarial, cuotas restantes, crecimiento compuesto, prorrateo por cuotas y estimación de cuotas a la fecha de retiro, sin crear un motor alternativo;
- presenta importes de la guía con separador de miles y dos decimales;
- compacta la tabla mensual SEBD a 8 columnas en escritorio y los factores actuariales SUCGS a 10 columnas, con degradación responsive;
- reduce lenguaje de implementación visible y refuerza foco, temas y jerarquía visual;
- añade seis regresiones específicas; gate objetivo **832 pruebas**.

### UX.4.6i R1 — guía pública Cómo se calcula

- incorpora `/como-se-calcula` como sección pública de transparencia para SEBD, Subsistema Mixto y SUCGS;
- explica datos, clasificación, orden de operaciones, fórmulas descriptivas, factores, límites, redondeos, ejemplos y limitaciones sin ejecutar un segundo cálculo;
- `como_se_calcula.py` expone parámetros canónicos desde `regulations/` y no importa motores previsionales;
- Paso 6 añade **Ver cómo se obtuvo este cálculo** y dirige al sistema correspondiente sin transportar datos personales en la URL;
- Metodología y fuentes enlaza a la guía y la nueva página reutiliza el catálogo oficial versionado;
- ADR-178, RF-383 a RF-389 y TR-026 formalizan el contrato; se añaden 14 regresiones específicas y el gate objetivo asciende a **826 pruebas**.

### UX.4.6h — cierre del Paso 6 · Resultados y exportación

- consolida R1/R1.1/R1.2/R1.3 como cierre funcional del Paso 6 sin modificar las fórmulas previsionales de SEBD, Mixto o SUCGS;
- la validación manual del caso SEBD confirmó contexto de retiro, escenario salarial, comparación acreditada/proyectada, modalidad, salario base, tasa, cuotas, trazabilidad y referencia personal de Mi Retiro Seguro;
- la salida imprimible deja de ser una copia de la página web y pasa a un informe A4 independiente, compacto y orientado a lectura;
- la acción provisional continúa dependiendo de la impresión nativa del navegador; la generación y descarga directa de PDF por la aplicación, sus metadatos y formatos finales permanecen en REP.1;
- la suite de cierre queda fijada en **812 pruebas** y el bloque siguiente pasa a UX.4.6i — Cómo se calcula.

### UX.4.6h R1.3 — informe imprimible compacto

- sustituye la impresión directa del Paso 6 por un documento A4 independiente de la interfaz web;
- elimina controles, navegación, skip-link y tarjetas sobredimensionadas de la salida impresa;
- organiza identificación, resumen, comparación acreditado/proyectado, referencia personal, resultado del sistema y trazabilidad en una estructura compacta;
- conserva la impresión nativa del navegador como mecanismo provisional y reserva la generación PDF formal para REP.1;
- añade seis regresiones específicas; gate objetivo **812 pruebas**.

### UX.4.6h R1.2 — claridad y jerarquía visual del resultado

- simplifica la explicación de información acreditada vs. proyección para centrarla en el efecto de las cotizaciones futuras;
- corrige la comparación no compatible con Mi Retiro Seguro para explicar de forma gramatical y específica la diferencia de edad u otros motivos;
- sustituye la alerta SEBD redundante por un estado de cálculo útil y deja la modalidad exacta en su tarjeta dedicada;
- oculta Factores de la modalidad cuando la pensión es Normal y esos factores no intervienen;
- distingue años con información acreditada y proyección futura como **Histórico + proyectado**;
- elimina el scrollbar vertical de la comparación corta, la ayuda salarial duplicada y el botón Anterior local redundante;
- muestra la fecha de retiro de la trazabilidad en formato visible `DD/MM/YYYY` y reduce la jerarquía tipográfica de estados textuales frente al monto principal;
- añade 6 regresiones específicas; gate candidato: **806 pruebas**.

### UX.4.6h R1.1 — corrección del gate y sincronización documental

- elimina del comentario runtime de carga del Paso 6 el identificador cronológico `UX.4.6h`, respetando el contrato permanente de ADR-162;
- desacopla la regresión histórica de UX.4.6f del bloque funcional que esté activo en el futuro;
- alinea `ROADMAP.md` y `PLAN_MAESTRO_HACIA_1_0.md` con el cierre de UX.4.6g mediante PR #32 y el inicio de UX.4.6h;
- mantiene el gate objetivo de UX.4.6h R1 en **800 pruebas**, sin modificar motores previsionales ni fórmulas.

### UX.4.6h R1 — resultados explícitos y copia imprimible

- UX.4.6g queda cerrado tras la integración del PR #32, con 784 pruebas en `OK` y los checks de Python 3.13, Python 3.14 y Auditoría de gobernanza en verde;
- cuando el Paso 4 contiene varios escenarios salariales, el Paso 6 deja de escoger silenciosamente el primero y exige una elección explícita; si existe uno solo, se identifica como única alternativa disponible;
- cualquier cambio en la configuración del Paso 6 invalida también el resumen unificado, las comparaciones, la trazabilidad y la acción de impresión para impedir que permanezcan resultados obsoletos visibles;
- la transición del Subsistema Mixto al SUCGS ofrece una ruta explícita para preparar el cálculo SUCGS del mismo escenario sin reescribir silenciosamente el sistema informado en el Paso 1;
- los valores B/.144.00 y B/.265.00 del SUCGS se presentan como referencias legales versionadas al 22/05/2025 y solo se tratan como valores oficiales aplicables cuando el usuario lo confirma;
- B/.0.00 en el bono de reconocimiento del Mixto se explica como ausencia de bono incorporado al cálculo, evitando que parezca un dato oficial inferido;
- el resumen unificado sustituye lenguaje interno por una explicación orientada al Asegurado(a);
- se prepara una copia imprimible mediante la función nativa del navegador (**Imprimir / Guardar como PDF**) con identificación de versión, sistema, escenario y fecha de generación, dejando explícito que no es un documento oficial de la CSS; el informe formal y los formatos finales continúan reservados para REP.1;
- la orquestación se encapsula en `results_orchestration.js` para no duplicar fórmulas de los motores existentes y se añaden 16 regresiones específicas; gate candidato: **800 pruebas**.

### UX.4.6g R1.4.3 — alineación visual final

- alinea Año inicial/Período del historial y Año inicial/Proyectar hasta el año;
- redistribuye el resumen del Paso 5 para evitar el salto de línea de Cierre esperado este año en escritorio;
- añade regresiones y trazabilidad ADR-177 / RF-380–RF-382 / TR-025.

### UX.4.6g R1 — escenarios de retiro derivados y anticipados explícitos

- eliminada la selección fija de `-2`, `-1`, `+1`, `+2`, `+3` y `+5` del HTML; la edad de referencia queda como único escenario seguro por defecto también en la API;
- los años posteriores se sugieren desde el horizonte realmente cubierto por Paso 4 y la selección conserva procedencia `SUGERIDO_PASO4` o `EDITADO_USUARIO`, evitando pisar decisiones manuales;
- añadido `+4 años`, completando la secuencia `+1` a `+5`;
- los escenarios anticipados permanecen sin marcar hasta una decisión explícita, muestran su fecha exacta y se deshabilitan cuando esa fecha ya transcurrió;
- cuando la fecha de evaluación está dentro de la banda anticipada estándar se ofrece explícitamente **Retirarme en la fecha de evaluación**, sin afirmar por sí sola elegibilidad legal;
- el backend admite ese escenario de evaluación únicamente dentro de la banda anticipada versionada y conserva la clasificación legal para el Paso 6;
- la tabla del Paso 5 elimina el scroll vertical interno en tablas cortas y conserva desplazamiento horizontal cuando el viewport lo requiere;
- ADR-174/ADR-175, RF-366 a RF-374 y TR-022/TR-023 formalizan el contrato; se añaden 13 regresiones específicas y `VERSION` permanece en `0.0.26-beta`.
- R1.2/R1.3 recuperan la cuadrícula compacta del Paso 5, conservan `+4 años` y corrigen la visibilidad de **Ajustar horizonte en el Paso 4** en Claro, Oscuro y Alto contraste sin alterar la lógica previsional.
- R1.4 normaliza abreviaturas de sexo (`F`/`M`) para calcular la referencia en frontend, hace visible **Retirarme en la fecha de evaluación** cuando corresponde, informa si una fecha personalizada está cubierta por el horizonte salarial y adopta un contrato transversal para todos los `input[type=date]`: año de cuatro dígitos, rango 1900–2200, validación calendárica y ancho compacto adaptable. ADR-176, RF-375 a RF-379 y TR-024 amplían la trazabilidad; el gate candidato asciende a 780 pruebas.
- R1.4.2 endurece la inicialización dinámica de accesibilidad para impedir ciclos de `MutationObserver` durante recargas completas; la preparación de controles de fecha pasa a ser idempotente y el observador se suspende mientras aplica sus propias mutaciones. El gate candidato asciende a 781 pruebas.

### UX.4.6f R2 — auditoría lógica, matemática y trazabilidad del Paso 4

- reforzada `construir_linea_tiempo()` para rechazar historial incompleto, totales de cuotas desincronizados entre Pasos 2–3 y discrepancias en las cuotas del año actual antes de combinar realidad y proyección;
- `RegistroLineaTiempo` transporta `salario_mensual_proyectado` directamente desde el motor salarial y la interfaz deja de reconstruirlo a partir de un importe cotizado prorrateado;
- los años futuros con decisión explícita de no continuar cotizando se distinguen como **Sin cotización proyectada**, manteniendo separada la trayectoria salarial hipotética de las cuotas/salario cotizado;
- `PORCENTAJE` y `ESCENARIOS` explican su composición anual; `ESCENARIOS` deja de precargar `0, 1, 2, 3` y exige porcentajes elegidos explícitamente por el Asegurado(a); `FUTURO_CONOCIDO` deriva CAGR hasta el año objetivo, materializa exactamente ese salario y lo mantiene constante después del objetivo para evitar extrapolación silenciosa;
- cuando Paso 5 amplía el horizonte para cubrir un retiro más lejano, Paso 4 conserva el nuevo año como borrador y registra procedencia `AJUSTADO_DESDE_RETIRO`; una edición posterior pasa a `EDITADO_USUARIO`;
- el caso visible del año actual con 5 cuotas, B/.7,321.13 históricos y B/.1,500.00 mensuales queda protegido para cerrar en 12 cuotas y B/.17,821.13, con B/.18,000.00 por año futuro en modalidad constante;
- ADR-172/ADR-173, RF-358 a RF-365 y TR-020/TR-021 formalizan el contrato auditado; se añaden 13 regresiones específicas y `VERSION` permanece en `0.0.26-beta`;
- R2 fue validada funcionalmente con el caso femenino y las cuatro modalidades salariales; PR #30 se integró por squash en `9634ae4b1a0a07cc14682d315b6cdb9c1b37eb4d` después de **756/756 pruebas en `OK`** en CI para Python 3.13/3.14 y Auditoría de gobernanza en verde; UX.4.6f queda cerrado y el bloque funcional activo pasa a UX.4.6g — Paso 5 · Escenarios de retiro.
- el primer intento de cierre documental expuso cuatro regresiones históricas que todavía fijaban UX.4.6f como bloque activo; se desacoplan esas pruebas del estado futuro y se incorpora un gate `pre-commit` versionado que bloquea commits locales ante árbol no reproducible, whitespace preparado, dependencias rotas, errores Python/JavaScript o cualquier prueba fallida; cinco regresiones nuevas protegen el mecanismo y elevan la suite de cierre a **762 pruebas** sin modificar `VERSION`.

### Mantenimiento de dependencias post-UX.4.6f R1

- actualizadas las dependencias directas `pypdf` de `6.15.0` a `6.16.1` y `uvicorn` de `0.52.1` a `0.52.3`, manteniendo `VERSION = 0.0.26-beta`;
- `pypdf 6.16.1` incorpora correcciones upstream de seguridad/robustez y se conserva el contrato de compatibilidad de ambos importadores con PDFs sintéticos;
- `Uvicorn 0.52.3` incorpora mantenimiento upstream de la ruta HTTP/1.1 sin cambiar la configuración ASGI del proyecto;
- sincronizados `requirements.txt`, inventario de terceros, avisos de licencia y guards de versiones actuales; las referencias históricas a `pypdf 6.15.0` en hitos ya cerrados permanecen intactas;
- los PR Dependabot #26 y #27 originaron la revisión y fueron cerrados como sustituidos; la actualización coordinada se integró mediante PR #29 tras superar Python 3.13, Python 3.14 y Auditoría de gobernanza, sin cambios funcionales de UX.4.6f.

### UX.4.6f R1.1 — bloqueo documental y restauración visual

- restaurado el bloqueo de solo lectura en la vista principal para datos detectados por Mi Retiro Seguro y Ficha Digital; las correcciones vuelven a concentrarse en **Revisar importación** → **Editar campos**;
- los campos originalmente no detectados permanecen editables para captura manual, diferenciando ausencia documental de un dato confirmado;
- restaurada la franja primaria de campos no editables en temas Claro, Oscuro y Alto contraste mediante el contrato transversal existente;
- `Completado manualmente` vuelve a usar el icono de lápiz y `Excluido por ti` recupera el símbolo `⊘`, manteniendo alineación común y sin adornos circulares adicionales;
- `Disponibilidad del historial` deja de ser respondida automáticamente por una importación de Mi Retiro Seguro y permanece en `Seleccione una opción` hasta una elección explícita;
- aclarado que las bases salariales automáticas del Paso 3 solo se habilitan después de analizar y validar un detalle del año actual que aporte las métricas necesarias;
- ADR-171, RF-351 a RF-357 y TR-019 formalizan el contrato corregido tras la validación visual de R1;
- confirmado durante la revisión manual que el estado global **Analizando documento…** funciona correctamente para Mi Retiro Seguro y Ficha Digital; `VERSION` permanece en `0.0.26-beta`.
- R1 + R1.1 fueron validados con **743/743 pruebas en `OK`**, compilación Python, sintaxis JavaScript, `git diff --check` y revisión visual manual; PR #28 integrado por squash en `5e93dfc3d4c33b264c61e50f72c1eb0b84b3bc29`, con Python 3.13, Python 3.14 y Auditoría de gobernanza en verde.

### UX.4.6f R1 — consistencia de procedencia, decisiones y adjuntos

- unificados los estados de procedencia `Detectado`, `Editado por ti`, `Completado manualmente`, `Excluido por ti`, `No detectado` y `Calculado automáticamente`, eliminando círculos decorativos inconsistentes y corrigiendo la alineación de sus iconos;
- convertidos los avisos amarillos de ajustes documentales en mensajes contextuales que mencionan únicamente ediciones, complementos y/o exclusiones realmente activas;
- mantenida la sugerencia editable de 12 cuotas cuando el Asegurado(a) confirma que continuará cotizando, ahora con explicación visible y accesible;
- los cuatro selectores decisionales señalados del Paso 3 comienzan en `Seleccione una opción` y dejan de persistir elecciones silenciosas antes de una decisión real;
- el año inicial del historial y el horizonte inicial de cinco años del Paso 4 exponen procedencia automática y cambian a `Editado por ti` cuando el usuario los modifica;
- incorporada `attachment_processing.js` como contrato global para comunicar `Analizando documento… Esto puede tardar unos segundos.`, bloquear dobles ejecuciones y exponer estado accesible durante los tres análisis de archivo existentes;
- corregido el registro defectuoso del listener de **Revisar importación** del detalle anual que podía interrumpir la inicialización de controles posteriores del Paso 3;
- ADR-169 y ADR-170 formalizan los contratos de decisiones/procedencia y procesamiento de adjuntos; RF-337 a RF-350 y TR-017/TR-018 incorporan su trazabilidad;
- `VERSION` permanece en `0.0.26-beta`; R1 no modifica motores previsionales, normativa, parsers ni dependencias.

### Documentación post-release

- reconciliado el estado documental después de publicar el tag firmado `v0.0.26-beta`;
- objeto tag remoto `bfbb746b177ebcc577f7241fef4d6914f713739a` → target `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`;
- PLAN.1 queda cerrado y UX.4.6f vuelve a ser el bloque funcional activo;
- no se modifica `VERSION`, runtime, motores, normativa, fórmulas ni el tag publicado.

## [0.0.71.01-beta] — 2026-08-24

- promueve `VERSION`/`APP_VERSION` a `0.0.71.01-beta` como VER.2 G071/E01 después de cerrar R1, R2 y R3;
- mantiene `v0.0.26-beta` como último tag formal legacy hasta crear el tag firmado `v0.0.71.01-beta` después de merge y revalidación post-merge;
- no crea tags revision-aware retrospectivos para G001–G070;
- no modifica motores previsionales, normativa, datos protegidos ni `_entregas/`.

## [0.0.26-beta] — 2026-08-20

### PLAN.1 — alineación hacia la primera versión oficial

- mantenida `0.0.N-beta` como línea de desarrollo beta y sustituido `0.1.0-beta.1` como objetivo futuro vigente;
- definida `1.0.0.0` como primera versión oficial objetivo, condicionada al cierre de todos los gates del plan maestro;
- adoptada la convención oficial `MAYOR.MENOR.PARCHE.REVISIÓN`, propia del producto y distinta de SemVer estricto;
- definido Build independiente de seis dígitos para artefactos oficiales reproducibles, sin incorporarlo a `VERSION`, tags ni commits individuales;
- preparado `app/core/version.py` para validar tanto la familia beta vigente como la futura familia oficial de cuatro componentes sin modificar `VERSION`;
- creado `docs/PLAN_MAESTRO_HACIA_1_0.md` con la secuencia de 14 bloques hasta REL.1;
- alineados README, RELEASES, ROADMAP, cierre GOV.1, índice, transparencia y proceso de release, preservando las formulaciones históricas que describen planes anteriores;
- ADR-168 registra la transición directa desde la etapa beta a la versión oficial y difiere la fuente canónica del Build hasta REL.1;
- R1 fue validada localmente con **665 pruebas en `OK`**; R2A con **670 pruebas en `OK`**; R2B1 con **676 pruebas en `OK`**; R2B2 cerró con **684 pruebas en `OK`**;
- R2C saneó metadata viva de Observabilidad, Limitaciones y Preparación pública, distinguió versión base histórica de versión revisada y cerró con **689 pruebas en `OK`**;
- R3A alineó seguridad, soporte y despliegue con la etapa beta vigente, preservó las bases históricas GOV.1.5 y cerró con **695 pruebas en `OK`**;
- R3B1 alineó licencia, dependencias, política de privacidad, términos y matriz Ley 81, preservó `2026-08-16.1` y cerró con **702 pruebas en `OK`**;
- R3B2 actualizó threat model y procedimientos GOV.1.5, incorporó el guard automático de referencias históricas y cerró con **710 pruebas en `OK`**;
- R4.1 promovió `VERSION` a `0.0.26-beta`, actualizó la documentación viva y cerró localmente con **720 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpio;
- R4.2 integró el PR #23 por squash en `497097f720c98f6e5a7ed689cf91368011a96be1`, después de que el head firmado `7c50d989f5c6d266db26c9625367dd82e9895aba` superara `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`;
- la revalidación post-merge repitió **720 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios, pero detectó un `SyntaxWarning` por una secuencia de escape inválida en `test_plan1_documentacion_transversal.py`; la higiene pre-tag convierte ese literal en cadena raw sin alterar el contrato ni el número de pruebas;
- la higiene pre-tag fue integrada posteriormente mediante PR #24; el gate final post-merge repitió **720 pruebas en `OK`** sin `SyntaxWarning`;
- tag formal asociado: `v0.0.26-beta`; objeto tag `bfbb746b177ebcc577f7241fef4d6914f713739a`; target `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`;
- `v0.0.25-beta` permanece inmutable.

## [0.0.25-beta] — 2026-08-19

### UX.4.6e R9.1 — candidato local de cierre

- promovida la fuente canónica de versión a `0.0.25-beta` como candidato del cierre de UX.4.6e;
- R8 queda cerrada funcionalmente con 652 pruebas después del cierre documental;
- desacopladas regresiones históricas de `0.0.24-beta` para permitir que la versión canónica avance sin reescribir la evidencia de GOV.1, R4, identidad pre-R8 o R8;
- actualizado README y soporte de seguridad para la nueva línea pre-beta;
- R9.1 cerró localmente con **660 pruebas en `OK`**, compilación/sintaxis y `git diff --check` limpios;
- R9.2 integró el PR #21 por squash en `18e81e4ff58a1ad9622d366f7add10b7674f6e44`, con commit verificado y los checks `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` en verde;
- el árbol Git integrado `e0c4f314c5365a89178bd0fadb8a950286abb6ff` coincide exactamente con el árbol del head validado `a064bf745f4fb5e55e70f6ae3fd9b2bb80af8148`;
- cerrado UX.4.6e y asociado el hito al tag formal `v0.0.25-beta`; UX.4.6f — Paso 4 quedó documentado en ese momento como bloque funcional posterior;
- la primera beta pública continuaba siendo futura y UX.4.6f — Paso 4 quedó documentado en ese momento como bloque funcional posterior.

### Checkpoint pre-R8 — identidad visual y repositorio público

- adoptado como logo oficial el símbolo circular propio de Mi Retiro Proyectado y versionada su fuente canónica, familia de iconos, derivados de runtime y Social Preview;
- sustituido el marcador textual `MR` de la barra superior por el logo oficial, con favicons reales y Apple Touch icon;
- añadida una capa `brand.css` dedicada para conservar separación entre identidad gráfica y sistema visual transversal;
- configurado y versionado el Social Preview de GitHub en `assets/social/github-social-preview.png`;
- cambiado el repositorio a visibilidad **pública** sin promover la aplicación a primera beta pública ni alterar `VERSION`;
- revalidada la seguridad del repositorio público con Dependency graph, Dependabot, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting habilitados;
- revisión manual de Code scanning, Secret scanning y Dependabot con **0 alertas abiertas** al 2026-08-19;
- documentada la identidad oficial en `docs/IDENTIDAD_VISUAL.md` y actualizados README, seguridad, soporte, versionado, transparencia, auditoría GitHub y preparación pública;
- añadidas 20 regresiones de identidad/publicación sobre la línea base de 604 pruebas;
- validación integrada del checkpoint: **624 pruebas en `OK`** y `git diff --check` limpio;
- `VERSION` permanece en `0.0.24-beta`; R8 funcional hasta Paso 3 continúa pendiente.

### UX.4.6e R8 — validación funcional hasta Paso 3

- cerrada R7 con **598 pruebas en `OK`** y auditoría transversal limpia;
- detectada y corregida una regresión de reconsentimiento después de **Borrar datos de esta aplicación en este navegador**;
- reforzado el borrado integral para purgar namespace vigente y residuos pre-beta exclusivamente con finalidad destructiva, sin restauración/migración;
- validado el caso femenino mediante Mi Retiro Seguro + Ficha Digital hasta junio, con reconciliación 282/6 y exclusión explícita 281/5;
- sustituido el bloqueo obligatorio de datos importados por un contrato editable que preserva fotografía original y copia de trabajo;
- añadidos estados dinámicos `Detectado`, `Editado por ti`, `Completado manualmente`, `Excluido por ti` y `No detectado`;
- la exclusión de junio conserva B/.1,562.37 como referencia documental, pero lo retira de cuota/salario utilizado; enero–mayo reales suman B/.7,321.13;
- la reinclusión restaura 282 cuotas, 6 cuotas 2026 y B/.8,883.50;
- sincronizada la edición posterior de campos personales con **Revisar importación**, conservando por separado el valor original del PDF;
- corregidos dos defectos de la nueva capa: bucle de `MutationObserver` al importar y gancho invisible de checkboxes documentales editables;
- normalizada la iconografía de procedencia y hechos reactivos los avisos de ajustes;
- R8.2 cerró funcionalmente con **644 pruebas en `OK`**, compilación/sintaxis y validación manual satisfactoria;
- ADR-167 formaliza el nuevo contrato; `VERSION` permanece en `0.0.24-beta` hasta R9.

### UX.4.6e R7 — auditoría transversal de coherencia

- validada R6 con **586 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios;
- auditada la coherencia entre código runtime, interfaz visible, documentación vigente, pruebas y metadata manual de GitHub;
- confirmada cobertura de docstrings en `app/`, ausencia de identificadores cronológicos en comentarios de producción y ausencia de claves Web Storage pre-beta en runtime;
- confirmados enlaces Markdown relativos vigentes, JSON válido, ausencia de BOM/whitespace final en archivos versionables y política canónica LF mediante `.gitattributes`, sin depender del EOL físico del checkout de Windows;
- preservada la conclusión histórica de la auditoría post-GOV.1 con una nota posterior que remite a la secuencia UX.4.6e–h vigente;
- añadida auditoría R7 y 12 regresiones transversales;
- `VERSION` permanece en `0.0.24-beta` hasta el cierre integral de UX.4.6e.

### UX.4.6e R6 — renumeración documental y metadata GitHub en español

- validada R5 con 576 pruebas en `OK`, YAML/Python/JavaScript correctos y `git diff --check` limpio;
- normalizada la secuencia vigente para reservar UX.4.6e a la estandarización transversal y desplazar Paso 4/5/6 a UX.4.6f/UX.4.6g/UX.4.6h;
- preservadas sin reescritura las referencias históricas que documentan la numeración prospectiva vigente antes de R6;
- adoptada una política de topics prioritariamente en español, manteniendo nombres tecnológicos canónicos como `python` y `fastapi`;
- ampliada la taxonomía a 21 labels, conservando en inglés las convenciones GitHub `duplicate`, `good first issue`, `help wanted`, `invalid` y `wontfix`;
- documentado `sebd` como topic preferido y `sebd-panama` como alternativa únicamente si la interfaz de GitHub impide crear el identificador exacto;
- `VERSION` permanece en `0.0.24-beta` hasta el cierre integral de UX.4.6e.

### UX.4.6e R5 — coherencia visible y preparación pública de GitHub

- incorporada una sección visible de ayuda, contacto y proyecto dentro de Metodología y fuentes;
- añadido acceso a Ayuda y contacto desde el footer sin exponer controles internos de gobierno al Asegurado(a);
- unificada la acción de recursos individuales bajo la etiqueta `Abrir fuente oficial`;
- preparado el README con badges de CI, auditoría, versión, Python y licencia;
- documentados topics, labels, social preview y checklist de publicación en `docs/PREPARACION_PUBLICA_GITHUB.md`;
- preparados los Issue Forms para aplicar labels iniciales cuando la taxonomía exista en GitHub;
- documentado Shields.io como tercero exclusivo de presentación del README, fuera del runtime;
- la visibilidad continúa privada y `VERSION` permanece en `0.0.24-beta` hasta el cierre formal de UX.4.6e.

### UX.4.6e — Estandarización técnica, comentarios y coherencia de interfaz post-GOV.1

- iniciada R2 de normalización técnica; durante la auditoría del backend se corrigió una deriva de precisión preexistente en la proyección de salario futuro conocido, sin adelantar el trabajo visual del Paso 4 reservado a UX.4.6f;
- la modalidad de salario futuro conocido deriva su tasa compuesta equivalente íntegramente con `Decimal`;
- se conserva la separación entre año actual acreditado/proyectado y años futuros completamente proyectados;
- añadidas 10 regresiones específicas para las cuatro modalidades salariales, validaciones de horizonte y línea temporal;
- desacoplada la regresión histórica de ADR-159 del límite total de ADR, preservando íntegra la evidencia ADR-001..ADR-159 y exigiendo numeración consecutiva para decisiones posteriores;
- R2 cerró localmente con **550 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios;
- iniciada R3 con un estándar canónico de comentarios/docstrings por tecnología;
- normalizadas las claves de Web Storage a `miRetiroProyectado.*`, incluida la preferencia de tema, sin compatibilidad con identificadores pre-beta por decisión expresa del mantenedor;
- retiradas referencias cronológicas `UX.*`/`GOV.*` de comentarios JavaScript de runtime y sustituidas por explicaciones funcionales permanentes;
- iniciada R4 de normalización permanente del runtime: Python, Jinja/HTML y CSS dejan de incrustar identificadores cronológicos de fase en comentarios/docstrings;
- completada la cobertura de docstrings en funciones y clases de `app/`, con énfasis en observabilidad, fecha externa, parsers y trazabilidad;
- todos los módulos de pruebas cuentan con docstring de módulo y los comentarios CSS se normalizan sin reordenar reglas ni alterar la cascada;
- reforzada documentación de módulos JavaScript que coordinan almacenamiento, privacidad, importaciones, comparación, gestión destructiva y accesibilidad;
- `VERSION` permanece en `0.0.24-beta` hasta el cierre integral de UX.4.6e.

### Mantenimiento de repositorio post-GOV.1

- auditado el repositorio local y remoto después del cierre GOV.1;
- preparado el cambio de nombre del repositorio a `mi-retiro-proyectado`;
- normalizada documentación que conservaba estados transitorios de GOV.1.5–GOV.1.8;
- añadidos `CODE_OF_CONDUCT.md`, `SUPPORT.md` y formulario estructurado de consulta/soporte;
- documentada la política de conservar los commits históricos no firmados sin reescribir la historia;
- confirmados 24/24 tags con firma SSH válida, incluido `v0.0.24-beta`;
- reforzada la exclusión de carpetas temporales de auditoría local;
- `VERSION` permanece en `0.0.24-beta` y el tag publicado `v0.0.24-beta` no se mueve.

## [0.0.24-beta] — 2026-08-18

### GOV.1.8 — Auditoría final y cierre pre-beta de gobierno

- ejecutada auditoría transversal de gobierno, seguridad, privacidad, licencia, CI, Git/GitHub y documentación;
- cerrados formalmente GOV.1.1 a GOV.1.8;
- promovido `0.0.24-beta` como versión formal de cierre de GOV.1;
- reanudado UX.4.6e como siguiente bloque activo;
- añadidas 10 regresiones específicas de cierre GOV.1;
- desacopladas las regresiones históricas GOV.1.3/GOV.1.5/GOV.1.7 de la versión canónica futura, preservando `0.0.23-beta` como versión base de aquellas revisiones;
- creado y publicado el tag anotado y firmado `v0.0.24-beta` después de merge, validación post-merge y CI remota verde;
- se mantiene `0.1.0-beta.1` como futura primera beta pública, no como consecuencia automática del cierre de GOV.1;
- permanecen como gates pre-publicación la revisión jurídica externa, cualquier hardening de despliegue remoto aplicable, la decisión final sobre Bootstrap local/tercero, la auditoría ampliada de accesibilidad y el alcance funcional de UX.4.6e–g.

### GOV.1.7 — Licencia y derechos de distribución

- evaluadas alternativas permisivas, copyleft y propietaria para la etapa pre-beta;
- seleccionada una licencia propietaria pre-beta / todos los derechos reservados para materiales originales;
- añadido `LICENSE` sin relicenciar componentes de terceros;
- añadido `THIRD_PARTY_NOTICES.md` con dependencias directas y Bootstrap;
- añadido `docs/LICENCIA_Y_DISTRIBUCION.md` con alcance, compatibilidad y gates de distribución;
- actualizado el proceso de release para exigir inventario real y avisos upstream cuando un artefacto incorpore dependencias;
- añadidas 8 regresiones específicas de licencia/distribución;
- corregido posteriormente el formato de `LICENSE`, `THIRD_PARTY_NOTICES.md` y `docs/LICENCIA_Y_DISTRIBUCION.md` para usar saltos de línea reales, con regresión reforzada;
- durante GOV.1.7 `VERSION` permaneció en `0.0.23-beta`.

### GOV.1.6 — Controles GitHub y auditoría automática

- añadidas plantillas estructuradas para reportes de errores y solicitudes de mejora;
- añadido template común de Pull Request con checklist de pruebas, documentación, privacidad y alcance;
- añadido `SECURITY.md` con canal privado de reporte y divulgación coordinada;
- añadido `docs/archive/governance/AUDITORIA_GITHUB.md` con inventario de controles y revisión periódica;
- añadido workflow `Auditoría de gobernanza` con permisos de solo lectura y acciones oficiales `@v7`;
- añadidas 10 regresiones específicas de gobierno/repositorio;
- promovido `Auditoría de gobernanza` al conjunto de checks requeridos de `main` después de su primera ejecución exitosa;
- `VERSION` permanece en `0.0.23-beta`.

### GOV.1.5 — Seguridad, privacidad y transparencia

- añadido modelo de amenazas con activos, fronteras de confianza, matriz de riesgos y disparadores de revisión;
- formalizado procedimiento de derechos del titular con plazos publicados por ANTAI y registro mínimo fuera de Git;
- formalizado procedimiento de respuesta a incidentes con severidad, contención, evidencia, notificación, recuperación y post-mortem;
- documentada la revisión de terceros y conexiones externas, incluidos jsDelivr, infraestructura CSS y GitHub;
- definidos gates de TLS, proxy, forwarded headers, CORS/CSRF, secretos y despliegue remoto;
- revisado Developer Diagnostics como superficie de seguridad sin ampliar su tratamiento de datos;
- definida la frontera de revisión jurídica externa previa a beta pública;
- mantenida la versión material de privacidad `2026-08-16.1` al no identificarse internamente un cambio material de finalidad, categorías, destinatarios o conservación;
- GOV.1.5 cerrado internamente; revisión jurídica externa y despliegue remoto permanecen como gates pre-publicación;
- `VERSION` permanece en `0.0.23-beta`.

### GOV.1.4 — Observabilidad y Developer Diagnostics

- incorporado modo exclusivo de desarrollo mediante `MRP_DEV_MODE=1`, desactivado por defecto;
- añadido logging estructurado JSONL con esquema propio, timestamps UTC, niveles, categorías, duración, resultado y correlation IDs aleatorios;
- añadida redacción defensiva y prohibición explícita de registrar cuerpos HTTP, PDF, identificadores, salarios, montos, cookies, tokens o mensajes de excepción potencialmente sensibles;
- añadidas rotación local, retención acotada y exportación diagnóstica controlada sin telemetría remota;
- integrado middleware FastAPI sin doble ejecución de cálculos y con `X-Correlation-ID` solo en modo de desarrollo;
- instrumentada la consulta externa de fecha con metadata agregada de cache/resultado, sin URLs, fechas recibidas ni datos de simulación;
- añadidas 13 regresiones específicas de observabilidad; la suite completa alcanza **487 pruebas en `OK`**;
- sincronizada la documentación transversal y cerrado formalmente GOV.1.4;
- `VERSION` permanece en `0.0.23-beta`.

### Gobierno e integridad Git

- adoptada firma SSH Ed25519 para commits y tags nuevos;
- añadido registro público de firmantes autorizados;
- materializados y auditados 23/23 tags firmados de `v0.0.1-beta` a `v0.0.23-beta`;
- ejecutada la reemisión única de `v0.0.22-beta` y `v0.0.23-beta`, preservando `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5` y `07278f7a193ce964612d9697da57350691bf62c0`;
- añadido workflow de verificación de firmas de tags;
- añadidas regresiones de política de firma y trazabilidad histórica;
- primer commit nuevo firmado confirmado por GitHub como `Verified` y CI #23 en `success`;
- verificados 23/23 objetos y targets remotos sin reescritura de commits históricos;
- activado ruleset inmutable para tags `v*`: permite nuevas versiones y bloquea actualización, eliminación y force push de tags publicados;
- activado ruleset de la rama predeterminada con Pull Request obligatorio, firmas verificadas, historial lineal, resolución de conversaciones y checks Python 3.13/3.14;
- configurada la integración mediante `Squash and merge` y la eliminación automática de ramas remotas integradas;
- endurecidos los permisos de GitHub Actions y restringido el uso a acciones propias y oficiales de GitHub;
- activados Dependency graph, Dependabot alerts y Dependabot security updates;
- Dependabot revisado con 0 vulnerabilidades abiertas al habilitar las alertas;
- migradas las GitHub Actions vigentes de `@v6` a `@v7` en todos los workflows actuales.
- corregidas rutas PowerShell documentales afectadas por un carácter de control y añadida regresión preventiva;
- cerrado formalmente el prebloque transversal de firma e integridad Git/GitHub tras completar rulesets, configuración de Actions, Dependabot y auditoría de PR;
- verificado el cierre remoto con 0 Pull Requests abiertos y flujo protegido por rama, firma, PR, CI requerida y squash.

### Dependencias y seguridad

- preparado el salto controlado de `pypdf` `5.9.0` a `6.15.0`;
- añadidas cuatro regresiones específicas sobre versión instalada, `PdfReader`/`PdfWriter`, rechazo controlado de PDFs sin texto y límites de páginas de ambos importadores;
- la aceptación exige instalación reproducible desde `requirements.txt`, `pip check`, suite completa, compilación Python, sintaxis JavaScript y `git diff --check`;
- `VERSION` permanece en `0.0.23-beta`;
- PR de Dependabot `#7` cerrado como sustituido por la actualización controlada; `#6`, `#5` y `#4` cerrados para preservar compatibilidad y el snapshot transitivo reproducible.

## [0.0.23-beta] — 2026-08-17

### GOV.1.3 — Auditoría y reorganización documental

- GOV.1.3 R1 completada y validada con reorganización de documentos de entrada y preservación histórica.
- Separación entre documentación vigente y documentación histórica.
- Reorganización del índice documental.
- Simplificación de README y CONTRIBUTING.
- Conversión del roadmap en un documento de presente/futuro.
- Conservación de bitácoras UX bajo `docs/archive/ux/`.
- Incorporación de regresiones para proteger la estructura documental.
- Validación R1: compilación Python, sintaxis JavaScript, git diff --check, 411 pruebas automatizadas en OK y 8/8 regresiones específicas de documentación.
- GOV.1.3 R2 completada: consolidación de Arquitectura, Modelo de datos, Gestión de datos, Motor, Especificación funcional, Guía interna y Validación.
- Validación R2: compilación Python, sintaxis JavaScript y `git diff --check` sin errores; 423 pruebas automatizadas en `OK`, incluidas 12/12 regresiones específicas de R2 y 8/8 regresiones documentales de R1.
- GOV.1.3 R3 completada: consolidación normativa, seguridad y privacidad documental;
- mantenida la versión material de privacidad `2026-08-16.1`.
- Validación R3: compilación Python, sintaxis JavaScript y `git diff --check` sin errores; 438 pruebas automatizadas en `OK`, incluidas 15/15 regresiones específicas de R3, 12/12 de R2 y 8/8 de R1.
- La regresión documental de R2 se endureció para preservar su evidencia de cierre en `CHANGELOG.md` sin depender del estado evolutivo de `VALIDACION.md`.
- GOV.1.3 R4 completada: transparencia, matriz de trazabilidad, auditoría de cálculos, limitaciones conocidas, dependencias/terceros, proceso de release e índice auditable de 158 ADR.
- ADR-086 se conserva como anomalía histórica de metadata sin inventar un estado retroactivo.
- Validación R4 y cierre GOV.1.3: 458 pruebas automatizadas en `OK`, compilación Python, sintaxis JavaScript y `git diff --check` sin errores.

## [0.0.22-beta] — 2026-08-17

Primera versión formal gobernada por `VERSIONING.md`.

### Añadido

- archivo canónico `VERSION`;
- `app/core/version.py`;
- `GOVERNANCE.md`;
- `VERSIONING.md`;
- `RELEASES.md`;
- `.github/CODEOWNERS`;
- regresiones específicas de gobierno/versionado.

### Verificado

- versión canónica, FastAPI y footer sincronizados;
- compilación Python;
- sintaxis JavaScript;
- `git diff --check`;
- 403 pruebas automatizadas en `OK`;
- tag formal `v0.0.22-beta`.

## Estados retrospectivos 0.0.1-beta a 0.0.21-beta

> Estos estados fueron reconstruidos retrospectivamente. DOC.2 R1 detalla cada rango con los commits reales preservados en Git.

### [0.0.21-beta] — 2026-08-17

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.21-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `05232df` → `7941f58` · **3 commits**.

**Hito reconstruido:** UX.4.6d: Paso 3, Ficha Digital, sincronización de Pasos 1–3 y cierre integral.

#### Funcionalidad

- `05232df` — feat(ux): completar UX.4.6d en los pasos 1 a 3

#### Documentación

- `f0fa70d` — docs(ux): cerrar documentacion de UX.4.6d
- `7941f58` — docs(ux): consolidar cierre final de UX.4.6d

### [0.0.20-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.20-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `e80d15e` → `2a69fb8` · **3 commits**.

**Hito reconstruido:** UX.4.6c: Paso 2, cuotas e importación contextual.

#### Funcionalidad

- `e80d15e` — feat(ux): redisenar cuotas e importacion contextual en UX.4.6c

#### Pruebas

- `8fbe806` — test(ux): cubrir cuotas e importacion contextual de UX.4.6c

#### Documentación

- `2a69fb8` — docs(ux): cerrar documentacion de UX.4.6c

### [0.0.19-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.19-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `e6c2310` → `83a67ed` · **3 commits**.

**Hito reconstruido:** UX.4.6b: Paso 1, datos personales, privacidad e importación.

#### Funcionalidad

- `e6c2310` — feat(ux): redisenar datos personales e importacion en UX.4.6b

#### Pruebas

- `298c1e2` — test(ux): cubrir privacidad e importacion de UX.4.6b

#### Documentación

- `83a67ed` — docs(ux): cerrar documentacion de UX.4.6b

### [0.0.18-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.18-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `429201a` → `11aefca` · **3 commits**.

**Hito reconstruido:** UX.4.6a: rediseño visual integral.

#### Funcionalidad

- `429201a` — feat(ux): completar rediseño visual integral UX.4.6a

#### Pruebas

- `bd2d52e` — test(ux): cubrir regresiones del rediseño UX.4.6a

#### Documentación

- `11aefca` — docs(ux): cerrar documentacion de UX.4.6a

### [0.0.17-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.17-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `488aff5` → `e55190b` · **3 commits**.

**Hito reconstruido:** Estrategia reproducible de dependencias pre-beta.

#### Pruebas

- `b6a02e8` — test: desacoplar validaciones de versiones fijas

#### Documentación

- `e55190b` — docs: documentar estrategia de dependencias pre-beta

#### Mantenimiento técnico

- `488aff5` — chore: ajustar estrategia de dependencias pre-beta

### [0.0.16-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.16-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `338db37` → `6f138da` · **4 commits**.

**Hito reconstruido:** Hardening PDF, privacidad, regresión E2E, CI y Dependabot.

#### Funcionalidad

- `338db37` — feat: endurecer importacion PDF y privacidad pre-beta

#### Pruebas

- `7443a81` — test: agregar regresion E2E y hardening pre-beta

#### Documentación

- `6f138da` — docs: documentar hardening y preparacion pre-beta

#### Mantenimiento técnico

- `0bd26d3` — ci: agregar validacion automatica y dependabot

### [0.0.15-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.15-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `88a1d14` → `3430f2e` · **3 commits**.

**Hito reconstruido:** UX.4.5: información acreditada frente a proyectada y cierre accesible.

#### Funcionalidad

- `88a1d14` — feat: cerrar resultados acreditados y proyectados de UX.4.5

#### Pruebas

- `b40dc44` — test: validar cierre de resultados y accesibilidad de UX.4.5

#### Documentación

- `3430f2e` — docs: documentar cierre funcional de UX.4.5

### [0.0.14-beta] — 2026-08-13

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.14-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `5ca39ac` → `f4a0d45` · **6 commits**.

**Hito reconstruido:** UX.4.4: edad anual, detalle salarial e importación documental.

#### Funcionalidad

- `abb4fad` — feat: mostrar edad anual en linea temporal de UX.4.4
- `10c4e48` — feat: completar detalle salarial e importacion oficial de UX.4.4

#### Pruebas

- `5ca39ac` — test: validar edad anual en linea temporal de UX.4.4
- `be7f711` — test: validar detalle salarial e importacion oficial de UX.4.4

#### Documentación

- `5be85f8` — docs: documentar cierre UX.4.3 e inicio UX.4.4
- `f4a0d45` — docs: documentar cierre funcional de UX.4.4

### [0.0.13-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.13-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `b671c9a` → `9f849d0` · **2 commits**.

**Hito reconstruido:** UX.4.3: validación accesible, teclado, errores y estabilidad.

#### Correcciones

- `b671c9a` — fix: cerrar validacion accesible y estabilidad de UX.4.3

#### Pruebas

- `9f849d0` — test: validar formularios teclado y errores de UX.4.3

### [0.0.12-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.12-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `5607cc1` → `6e6b33b` · **3 commits**.

**Hito reconstruido:** UX.4.2: estados activos y selección perceptible.

#### Funcionalidad

- `5607cc1` — feat: reforzar estados activos y seleccion visual de UX.4.2

#### Pruebas

- `5a01293` — test: validar estados activos y seleccion de UX.4.2

#### Documentación

- `6e6b33b` — docs: documentar estados visuales de UX.4.2

### [0.0.11-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.11-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `c2da494` → `1f350f6` · **3 commits**.

**Hito reconstruido:** UX.4.1: accesibilidad y ayudas contextuales.

#### Funcionalidad

- `c2da494` — feat: mejorar accesibilidad y refinamientos de UX.4.1

#### Pruebas

- `4e3434d` — test: validar accesibilidad y remate visual de UX.4.1

#### Documentación

- `1f350f6` — docs: documentar UX.4.1 y herramientas de validacion

### [0.0.10-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.10-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `3f2f5d7` → `8feb682` · **6 commits**.

**Hito reconstruido:** Mantenimiento técnico: LF, favicon temporal, estructura y respaldos.

#### Correcciones

- `a5f4b7b` — fix: evitar 404 temporal del favicon

#### Pruebas

- `263a0a8` — test: validar normalizacion LF y favicon temporal

#### Documentación

- `6ccda5c` — docs: documentar mantenimiento tecnico previo a UX.4
- `8feb682` — docs: documentar estructura y respaldos externos

#### Mantenimiento técnico

- `3f2f5d7` — chore: normalizar finales de linea del repositorio
- `a9d8e5c` — chore: limpiar marcadores obsoletos de estructura

### [0.0.9-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.9-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `376a967` → `e6b02dc` · **4 commits**.

**Hito reconstruido:** Identidad, temas, accesibilidad y terminología pública.

#### Funcionalidad

- `376a967` — feat: consolidar identidad temas y accesibilidad de interfaz

#### Pruebas

- `7ed97ff` — test: validar identidad temas accesibilidad y fuentes

#### Documentación

- `e6b02dc` — docs: actualizar identidad metodologia y fuentes normativas

#### Refactorización

- `74fbd29` — refactor: alinear terminologia publica y trazabilidad previsional

### [0.0.8-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.8-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `6d4c2d8` → `d599ee2` · **3 commits**.

**Hito reconstruido:** UX.3: responsive y precisión del corte mensual de cuotas.

#### Funcionalidad

- `6d4c2d8` — feat: mejorar UX responsive y precision del corte de cuotas

#### Pruebas

- `54c9762` — test: validar UX responsive y corte mensual de cuotas

#### Documentación

- `d599ee2` — docs: documentar UX.3 y corte mensual de cuotas

### [0.0.7-beta] — 2026-08-12

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.7-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `c442ec2` → `e956ea9` · **4 commits**.

**Hito reconstruido:** Comparador, trazabilidad, resultado unificado y cierre funcional de Fase 6.

#### Funcionalidad

- `c442ec2` — feat: completar comparador trazabilidad y cierre funcional

#### Pruebas

- `68be9a9` — test: validar comparador trazabilidad y resultado unificado

#### Documentación

- `e956ea9` — docs: cerrar fase 6 y documentar metodologia y resultados

#### Mantenimiento técnico

- `35fbd9f` — chore: agregar dependencia para pruebas HTTP

### [0.0.6-beta] — 2026-08-11

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.6-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `fa5348f` → `e087d6e` · **4 commits**.

**Hito reconstruido:** Organización del repositorio, centralización normativa y casos de validación.

#### Documentación

- `1ee2b0c` — docs: reorganizar documentacion y fuentes normativas
- `e087d6e` — docs: actualizar guia de casos de validacion

#### Mantenimiento técnico

- `fa5348f` — chore: ordenar configuracion y reglas del repositorio
- `7051916` — chore: centralizar fuentes y metadatos normativos

### [0.0.5-beta] — 2026-08-11

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.5-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `d41682c` → `8a7e381` · **3 commits**.

**Hito reconstruido:** Motores Mixto y SUCGS.

#### Funcionalidad

- `d41682c` — feat: completar motores Mixto y SUCGS

#### Pruebas

- `292e10f` — test: validar motores Mixto y SUCGS

#### Documentación

- `8a7e381` — docs: documentar motores Mixto y SUCGS

### [0.0.4-beta] — 2026-08-11

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.4-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `563d6c4` → `2d4dfd0` · **7 commits**.

**Hito reconstruido:** Motor SEBD, modalidades e Indemnización por Vejez.

#### Funcionalidad

- `563d6c4` — feat: implementar modalidades SEBD y resultados integrados
- `d7d8c71` — feat: completar indemnizacion por vejez SEBD

#### Correcciones

- `2d4dfd0` — fix: incluir parametros normativos de indemnizacion por vejez

#### Pruebas

- `3e7c8ab` — test: validar modalidades y escenarios SEBD
- `266cc97` — test: validar indemnizacion por vejez SEBD

#### Documentación

- `2567191` — docs: documentar modalidades y motor SEBD
- `fb5857d` — docs: documentar indemnizacion por vejez SEBD

### [0.0.3-beta] — 2026-08-11

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.3-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `a7e1ed4` → `78e5188` · **4 commits**.

**Hito reconstruido:** Retiro, precisión monetaria, pruebas y protección de datos de validación.

#### Funcionalidad

- `a7e1ed4` — feat: completar retiro y precision monetaria

#### Pruebas

- `8a0c8fc` — test: agregar validaciones de precision y retiro

#### Documentación

- `78e5188` — docs: documentar precision retiro y validacion

#### Mantenimiento técnico

- `204c479` — chore: normalizar archivos y proteger datos de validacion

### [0.0.2-beta] — 2026-08-11

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.2-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `ae45943` → `eafe54d` · **3 commits**.

**Hito reconstruido:** Historial salarial, proyección y línea temporal.

#### Funcionalidad

- `ae45943` — feat: integrar historial salarial y linea temporal de proyeccion

#### Documentación

- `1718194` — docs: actualizar historial y proyeccion salarial
- `eafe54d` — docs: actualizar guia de contribucion

### [0.0.1-beta] — 2026-08-10

> Estado retrospectivo asignado por GOV.1.1 a un rango real del historial. El tag `v0.0.1-beta` fue materializado posteriormente sin alterar esos commits.

**Evidencia Git:** `a0a9e09` → `13ce028` · **6 commits**.

**Hito reconstruido:** Base técnica, FastAPI, primera interfaz, asistente, cuotas, salario y documentación inicial.

#### Funcionalidad

- `422bbab` — feat: agregar interfaz inicial y asistente de simulacion
- `47635ee` — feat: agregar analisis de cuotas y persistencia temporal
- `fa67022` — feat: agregar cuotas y salario al asistente de simulacion

#### Documentación

- `13ce028` — docs: normalizar comentarios y documentacion del codigo

#### Mantenimiento técnico

- `f329826` — chore: inicializar estructura del proyecto

#### Otros cambios

- `a0a9e09` — tipo: descripción del cambio

**Nota histórica:** el commit raíz `a0a9e09` conserva el mensaje `tipo: descripción del cambio`; DOC.2 lo registra como anomalía histórica y no lo reescribe.

## Evidencia histórica

Para una auditoría completa consultar, en este orden:

1. `RELEASES.md` — rangos Git y clasificación de versiones;
2. `docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md` — mapa cronológico;
3. `docs/archive/` — bitácoras y snapshots anteriores;
4. `docs/DECISIONES.md` y ADR independientes posteriores — decisiones;
5. historial Git — evidencia primaria e inmutable de cada cambio versionado.
