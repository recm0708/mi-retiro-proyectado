# Validación

**Estado:** Vigente
**Versión candidata revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.25-beta`
**Base documental histórica:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal histórica preservada:** UX.4.6e R8 — validación funcional y procedencia editable — 2026-08-19
**Última revisión transversal:** UX.4.6f R2 integrada y cierre del Paso 4 — 2026-08-20
**Revisión de mantenimiento:** MANT.1 R3 — encabezados YAML de GitHub — 2026-08-23
**Clasificación:** Técnica / Calidad

La estrategia combina pruebas automatizadas, CI, casos sintéticos/anonimizados y validación manual cuando una propiedad no puede demostrarse suficientemente con código.

## 1. Línea base

Cierre validado de GOV.1.3 R2:

```text
Ran 423 tests
OK
```

GOV.1.3 R3 agregó **15 regresiones documentales**. El cierre de R3 fue validado con una suite completa de **438 pruebas en `OK`**, incluidas **15/15 regresiones específicas de R3**, **12/12 regresiones de R2** y **8/8 regresiones documentales de R1**.

Durante R3 también se endureció la regresión de cierre de R2: su evidencia histórica se valida contra `CHANGELOG.md` en lugar de exigir que el documento vigente `VALIDACION.md` conserve indefinidamente la línea base de una revisión anterior.
GOV.1.3 R4 agregó **20 regresiones de auditoría documental y consistencia**. El cierre de R4 y de GOV.1.3 fue validado con una suite completa de **458 pruebas en `OK`**, además de compilación Python, validación de sintaxis JavaScript y `git diff --check` sin errores.

El prebloque de firma Git agregó **12 regresiones** sobre una línea base previa de **458 pruebas**. La suite completa fue ejecutada con **470 pruebas en `OK`**, además de compilación Python, validación de sintaxis JavaScript y `git diff --check` limpio.

La materialización criptográfica posterior no modifica lógica de aplicación: se verificaron **23/23 tags firmados**, **23/23 objetos remotos** y **23/23 targets remotos**, conservando intactos los commits históricos.

Posteriormente se activaron rulesets para tags `v*` y para la rama predeterminada, con Pull Request obligatorio, firmas verificadas y CI `Python 3.13`/`Python 3.14`.

También se habilitaron Dependency graph, Dependabot alerts y Dependabot security updates; la primera revisión mostró **0 vulnerabilidades abiertas**.

Los workflows vigentes fueron migrados de GitHub Actions `@v6` a `@v7`. La validación local de este mantenimiento conserva la línea base de **470 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpio.

La actualización controlada de `pypdf` a `6.15.0` añadió **4 regresiones específicas** y fue aceptada con **474 pruebas en `OK`**, `pip check` limpio, compilación Python, sintaxis JavaScript y `git diff --check` sin errores. Se conservaron el comportamiento de `PdfReader`/`PdfWriter`, el rechazo controlado de PDFs digitales sin texto y los límites de páginas de ambos importadores.

El prebloque transversal de firma e integridad Git/GitHub quedó cerrado después de completar la auditoría de 23/23 tags, los rulesets de tags y `main`, la configuración de GitHub Actions, Dependency graph, Dependabot alerts/security updates y la revisión de los PR pendientes. La comprobación remota final registró **0 Pull Requests abiertos**. Los PR `#8` y `#7` quedaron sustituidos por cambios controlados del mantenedor; `#6`, `#5` y `#4` se cerraron sin merge para preservar las combinaciones compatibles y el snapshot transitivo reproducible.

GOV.1.4 añadió **13 regresiones específicas**: 7 para el núcleo de Developer Diagnostics y 6 para integración HTTP/fecha externa. El cierre fue validado con **487 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpio. Las regresiones comprueban modo apagado/activo, JSONL, correlación, redacción, excepciones, rotación, exportación, middleware, ausencia de doble cálculo, consulta externa y coherencia documental.

GOV.1.5 R1 añadió **7 regresiones** del modelo de amenazas y R2 añadió **8 regresiones** de derechos/incidentes, elevando la suite validada a **502 pruebas en `OK`** antes de R3.

GOV.1.5 R3 añadió **10 regresiones de cierre** sobre terceros, despliegue, privacidad, seguridad, documentación y gates pre-publicación. El cierre fue validado con **512 pruebas en `OK`**, además de compilación Python, sintaxis JavaScript y `git diff --check` limpio.

GOV.1.6 añadió **10 regresiones específicas** sobre `SECURITY.md`, issue forms, template de Pull Request, workflow de auditoría, permisos mínimos, documentación y continuidad de controles. Su cierre local se valida con **522 pruebas en `OK`** antes de aplicar GOV.1.7.

GOV.1.7 añadió **8 regresiones específicas** sobre `LICENSE`, avisos de terceros, decisión de distribución, proceso de release y transición del roadmap a GOV.1.8. Después del hotfix de saltos de línea, la suite integrada quedó en **530 pruebas en `OK`** y la regresión de licencia rechaza secuencias `\n` literales.

GOV.1.8 añadió **10 regresiones específicas de cierre**. La suite integrada alcanzó **540 pruebas en `OK`**. Estas regresiones verifican `0.0.24-beta`, cierre completo GOV.1, reanudación UX.4.6e, release/tag firmado, tres checks de GitHub, soporte de seguridad, gates restantes y separación entre versión canónica actual y versiones base de auditorías históricas.

A partir de GOV.1.8, las regresiones históricas de GOV.1.3, GOV.1.5 y GOV.1.7 **no obligan a reescribir sus documentos cada vez que cambia `VERSION`**. Conservan `0.0.23-beta` como versión base de la revisión que originó esos contratos; la coherencia de la versión canónica actual se valida en GOV.1.2/GOV.1.8.

La auditoría post-GOV.1 del 2026-08-18 confirmó 24/24 tags con firma SSH válida, integridad Git sin corrupción, archivos textuales vigentes sin BOM/CRLF/caracteres de control/whitespace final, JSON/YAML válidos y enlaces Markdown internos vigentes sin roturas detectadas. El detalle se conserva en `AUDITORIA_REPOSITORIO_2026-08-18.md`.

UX.4.6e R3 añadió **8 regresiones** de namespace Web Storage y estándar documental, llevando la suite a **558 pruebas en `OK`**. R4 añade **8 regresiones** de documentación permanente del runtime: cobertura de docstrings en `app/`, módulos de pruebas documentados y ausencia de identificadores cronológicos `UX.*`/`GOV.*` en Python, Jinja/HTML y CSS vigentes.

UX.4.6e R2 incorporó **10 regresiones específicas** surgidas de la auditoría técnica del contrato salarial existente: cuatro modalidades de proyección, crecimiento/descenso compuesto, salario futuro conocido, límites temporales, deduplicación de escenarios y separación del año actual frente al futuro por densidad de cuotas. La revisión cerró con **550 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios. La corrección protege una pieza ya implementada y **no adelanta UX.4.6f**, reservado al Paso 4 · Proyección salarial/laboral. La regresión histórica de firma Git conserva ADR-001..ADR-159 como evidencia y permite ADR posteriores únicamente si toda la numeración permanece consecutiva.

UX.4.6e R3 añade **8 regresiones específicas** de mantenibilidad y almacenamiento: namespace `miRetiroProyectado.*`, ausencia de claves pre-beta en runtime vigente, coherencia entre módulos de borrado/privacidad/tema, ausencia de identificadores cronológicos en comentarios JavaScript de producción y presencia del estándar documental canónico. Sobre la línea base de 550 pruebas, el objetivo de R3 es **558 pruebas en `OK`**.

UX.4.6e R4 cerró con **566 pruebas en `OK`** después de añadir 8 regresiones de documentación permanente del runtime. R5 añade **10 regresiones** sobre ayuda/contacto visible, repositorio, footer, botones de fuentes, badges, topics/labels documentados, Issue Forms y terceros de presentación. El objetivo de R5 es **576 pruebas en `OK`**, sin cambio de `VERSION`.

UX.4.6e R5 cerró con **576 pruebas en `OK`**, YAML/Python/JavaScript válidos y `git diff --check` limpio. R6 añade **10 regresiones** de renumeración y metadata: secuencia vigente UX.4.6e–h, preservación de evidencia histórica, topics prioritariamente en español, alternativa controlada para SEBD y taxonomía de 21 labels. El objetivo de R6 es **586 pruebas en `OK`**, sin cambio de `VERSION`.

UX.4.6e R6 cerró con **586 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios. R7 añade **12 regresiones de auditoría transversal** sobre secuencia documental vigente, docstrings, comentarios de runtime, namespace Web Storage, superficie visible post-GOV, enlaces Markdown, higiene textual/JSON y continuidad ADR. El objetivo de R7 es **598 pruebas en `OK`**, sin cambio de `VERSION`.

UX.4.6e R7 cerró con **598 pruebas en `OK`**. Durante R8, la primera prueba manual detectó que el borrado integral podía dejar al navegador sin volver a presentar los términos al regresar a Simular. La corrección de R8 purga claves vigentes y residuos pre-beta exclusivamente durante el borrado, fuerza una nueva presentación de condiciones desde Inicio y añade **6 regresiones** ejecutables de reconsentimiento. El objetivo intermedio pasó a **604 pruebas en `OK`**, sin cambio de `VERSION`.

El checkpoint de identidad visual y publicación del repositorio previo a continuar R8 añadió **20 regresiones**: 10 para estructura/dimensiones de activos, favicon, navbar, temas y Social Preview; y 10 para coherencia pública de README, seguridad, soporte, versionado, identidad, auditoría y transparencia. La suite integrada fue ejecutada con **624 pruebas en `OK`**. `git diff --check` permaneció limpio y la validación visual confirmó el logo oficial en la navbar y el Social Preview. `VERSION` continúa en `0.0.24-beta`.


UX.4.6e R8.1/R8.2 sustituyó el bloqueo obligatorio de datos importados por una procedencia editable con fotografía original preservada. La capa añadió y refinó **20 regresiones** sobre edición, exclusión, sincronización, avisos reactivos, iconografía, checkboxes y referencias documentales. Después de los hotfixes de `MutationObserver` y representación del gancho, la suite integrada alcanzó **644 pruebas en `OK`**.

La validación manual del caso femenino comprobó:

- Mi Retiro Seguro confirmado con 281 cuotas al corte previo;
- Ficha Digital hasta junio con 282 cuotas totales, 6 cuotas en 2026 y B/.8,883.50;
- exclusión explícita de junio con 281 cuotas totales, 5 cuotas en 2026 y B/.7,321.13 correspondientes a la suma real enero–mayo de la Ficha;
- permanencia visible de B/.1,562.37 como referencia documental del mes excluido;
- reinclusión de junio con retorno a 282/6 y B/.8,883.50;
- actualización inmediata de `No detectado` a `Completado manualmente` al ingresar el apellido de casada;
- sincronización del valor manual con la vista **Revisar importación**;
- aviso de ajustes visible solo mientras existe un cambio activo en el bloque correspondiente;
- iconografía `●`, `✎`, `⊘` y `!` coherente con la procedencia.

El cierre documental de R8 añade **8 regresiones adicionales** sobre ADR-167 y coherencia funcional/documental. Partiendo de 644, el gate esperado para declarar R8 completamente cerrado es **652 pruebas en `OK`**. `VERSION` permanece en `0.0.24-beta`; la promoción de versión pertenece a R9.

La revalidación manual del repositorio público del 2026-08-19 confirmó Dependency graph, Dependabot alerts/security updates, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting habilitados, con **0 alertas abiertas** en Code scanning, Secret scanning y Dependabot en ese momento. Esta evidencia no sustituye revisión periódica ni auditoría externa.


## Gate R9.1 — candidato `0.0.25-beta`

R8 cerró documentalmente con **652 pruebas en `OK`**.

R9.1 modifica regresiones históricas que fijaban `0.0.24-beta` como si fuera la versión canónica permanente. La evidencia histórica se mantiene en sus documentos de cierre, mientras `VERSION` y `APP_VERSION` avanzan juntos a `0.0.25-beta`.

R9.1 añade **8 regresiones específicas** para proteger:

- versión canónica `0.0.25-beta`;
- sincronización de `VERSION` y `APP_VERSION`;
- README y soporte de seguridad;
- promoción del CHANGELOG;
- estado R8 cerrado / R9.2 pendiente;
- preservación histórica de `v0.0.24-beta`;
- ausencia de regresiones históricas que vuelvan a bloquear el incremento;
- separación entre este hito y la futura beta pública.

Partiendo de 652 pruebas, R9.1 alcanzó **660 pruebas en `OK`** el 2026-08-19. La compilación Python, la sintaxis JavaScript y `git diff --check` quedaron limpios.

Con este gate local cumplido, R9.2 puede comenzar: commits firmados, PR, CI requerida, squash, validación post-merge y tag firmado.


## Gate R9.2 — cierre formal UX.4.6e

Evidencia remota del cierre principal:

- PR #21 integrado por `Squash and merge`;
- head validado: `a064bf745f4fb5e55e70f6ae3fd9b2bb80af8148`;
- checks requeridos previos al merge:
  - `Python 3.13` — `success`;
  - `Python 3.14` — `success`;
  - `Auditoría de gobernanza` — `success`;
- commit integrado en `main`: `18e81e4ff58a1ad9622d366f7add10b7674f6e44`;
- verificación criptográfica del commit de squash: válida;
- árbol Git del head y del squash: `e0c4f314c5365a89178bd0fadb8a950286abb6ff`.

La igualdad del árbol demuestra que el contenido integrado en `main` es exactamente el contenido que pasó el gate local de **660 pruebas en `OK`** y los checks del PR.

Este cierre documental no modifica motores, cálculos, normativa ni contratos de runtime. El gate final antes de crear `v0.0.25-beta` continúa siendo:

- suite completa: **660 pruebas en `OK`**;
- compilación Python correcta;
- sintaxis JavaScript correcta;
- `git diff --check` limpio;
- commit de cierre documental firmado;
- CI requerida verde después de integrar el cierre;
- tag `v0.0.25-beta` anotado y firmado, creado después del merge final y validado antes de iniciar UX.4.6f.


## PLAN.1 — alineación hacia la primera versión oficial

PLAN.1 se ejecuta sobre `0.0.25-beta` sin mover ni recrear `v0.0.25-beta`.

Evidencia local ya ejecutada:

- R1 — política de versionado, soporte técnico futuro y plan maestro: **665 pruebas en `OK`**;
- R2A — documentación primaria y preservación histórica: **670 pruebas en `OK`**;
- R2B1 — índice, transparencia y proceso de release: **676 pruebas en `OK`**;
- en los tres gates anteriores `git diff --check` permaneció limpio y `VERSION` continuó en `0.0.25-beta`.

R2B2 añadió **8 regresiones específicas** para ADR-168, gobierno, CHANGELOG, evidencia de validación, continuidad histórica y permanencia de la versión canónica. La revisión fue ejecutada y cerró con **684 pruebas en `OK`**, `git diff --check` limpio y `VERSION` todavía en `0.0.25-beta`.

R2C añadió **5 regresiones específicas** para saneamiento de metadata viva, preservación de versiones base históricas, terminología beta/oficial y eliminación de duplicaciones documentales. La revisión fue ejecutada y cerró con **689 pruebas en `OK`**, `git diff --check` limpio y `VERSION` todavía en `0.0.25-beta`.

R3A añadió **6 regresiones específicas** para terminología vigente de seguridad, soporte y despliegue. La revisión fue ejecutada y cerró con **695 pruebas en `OK`**, `git diff --check` limpio y `VERSION` todavía en `0.0.25-beta`.

R3B1 añadió **7 regresiones específicas** para licencia, dependencias, privacidad, términos, matriz Ley 81 y preservación de bases históricas. La revisión fue ejecutada y cerró con **702 pruebas en `OK`**, `git diff --check` limpio y `VERSION` todavía en `0.0.25-beta`.

R3B2 añadió **8 regresiones específicas** para threat model, procedimientos GOV.1.5, política del guard histórico, documentos operativos y continuidad de evidencias. La revisión fue ejecutada y cerró con **710 pruebas en `OK`**, `git diff --check` limpio y `VERSION` todavía en `0.0.25-beta`.

R4.1 promovió `VERSION` a `0.0.26-beta`, actualizó metadata de documentación viva, incorporó la auditoría integral de PLAN.1 y añadió **10 regresiones específicas** de cierre. La revisión fue ejecutada y cerró localmente con **720 pruebas en `OK`**, compilación Python correcta, validación de sintaxis JavaScript correcta y `git diff --check` limpio.

R4.2 materializó el commit de rama firmado `7c50d989f5c6d266db26c9625367dd82e9895aba`, abrió el PR #23 y obtuvo `success` en `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`. El PR fue integrado por squash y `main` quedó en `497097f720c98f6e5a7ed689cf91368011a96be1`, verificado por GitHub.

La primera revalidación post-merge repitió **720 pruebas en `OK`** y detectó un `SyntaxWarning` documental. El PR #24 integró la corrección sin cambiar runtime, VERSION ni el inventario de pruebas. Después de sincronizar `main` en `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`, el gate final volvió a ejecutar **720 pruebas en `OK`** sin `SyntaxWarning`, con compilación Python, sintaxis JavaScript, `git diff --check` y working tree limpios.

Se creó y publicó el tag anotado y firmado `v0.0.26-beta`. Objeto tag: `bfbb746b177ebcc577f7241fef4d6914f713739a`. Target: `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`. La firma SSH fue verificada con la clave autorizada del mantenedor. PLAN.1 queda cerrado; esta reconciliación documental posterior no mueve el tag ni cambia `VERSION`.

La política vigente conserva las referencias históricas a `0.1.0-beta.1` cuando documentan decisiones o planes anteriores, pero exige que los documentos de planificación actual identifiquen `1.0.0.0` como primera versión oficial objetivo y mantengan Build separado de `VERSION`.

## UX.4.6f R1 — consistencia de procedencia, decisiones y adjuntos

R1 se ejecuta sobre `0.0.26-beta` y no modifica `VERSION`, motores de pensión, normativa ni dependencias. El alcance corrige inconsistencias transversales observadas durante la revisión de los Pasos 1–4 antes de profundizar el cierre funcional del Paso 4.

La revisión añade **14 regresiones específicas** para proteger:

- seis estados de procedencia coherentes, incluido `Calculado automáticamente`;
- iconografía sin círculos decorativos y alineación uniforme de estados;
- avisos contextuales que describen únicamente las acciones realmente realizadas por el usuario;
- sugerencia editable de 12 cuotas cuando se confirma continuidad de cotización;
- cuatro decisiones del Paso 3 con estado inicial real `Seleccione una opción`, sin persistir una respuesta silenciosa;
- procedencia automática/editada del año inicial del historial;
- procedencia automática/editada del horizonte inicial de cinco años del Paso 4;
- contrato global de procesamiento para los tres campos de adjuntos vigentes, con indicador visible, `aria-live`, `aria-busy`, bloqueo de doble ejecución y restauración del estado previo;
- corrección del listener de **Revisar importación** del detalle salarial del año actual;
- trazabilidad ADR-169/ADR-170, RF-337..RF-350, matriz, CHANGELOG y roadmap.

Partiendo de la línea base de **720 pruebas**, R1 eleva el inventario esperado a **734 pruebas**. En el entorno aislado de preparación se ejecutaron **733/734 pruebas correctamente**; la única prueba no satisfactoria fue el guard de compatibilidad de `pypdf`, porque ese entorno contiene `pypdf 5.9.0` mientras el proyecto fija correctamente `pypdf==6.15.0` en `requirements.txt`. No fue posible instalar la versión fijada allí por ausencia de acceso a PyPI. Este resultado se clasifica como **limitación del entorno de preparación, no como fallo funcional del cambio**.

En ese mismo entorno quedaron correctos:

- `python -m compileall -q app`;
- validación `node --check` de todos los archivos `app/static/js/*.js`;
- `git diff --check`;
- las **14/14 regresiones específicas de R1**;
- las regresiones históricas reconciliadas que protegen procedencia, historial y continuidad documental.

El gate canónico de R1 fue ejecutado posteriormente en el `.venv` del proyecto con `pypdf==6.15.0` y obtuvo **734/734 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios. La validación manual posterior confirmó el estado global de procesamiento de adjuntos, pero detectó que los datos documentales se habían vuelto editables en las vistas principales, que la señal visual de solo lectura había desaparecido y que la iconografía de complemento/exclusión no coincidía con el patrón esperado. Esos hallazgos originan R1.1 antes de cerrar R1.

### UX.4.6f R1.1 — bloqueo documental y restauración visual

R1.1 añade **9 regresiones** y formaliza ADR-171, RF-351..RF-357 y TR-019. El alcance protege que los datos originalmente detectados se bloqueen en la vista principal, que los no detectados sigan completables, que la edición documental ocurra en la revisión modal, que la franja visual de solo lectura funcione en los tres temas y que `Disponibilidad del historial` no se responda automáticamente al importar registros.

También se documenta que las bases salariales automáticas del Paso 3 son condicionales: permanecen deshabilitadas hasta que el detalle salarial del año actual haya sido analizado y validado y exista la métrica positiva correspondiente. La opción manual continúa disponible.

La suite pasa de **734 a 743 pruebas**. En el entorno aislado de preparación se ejecutaron **742/743 correctamente**; la única no satisfactoria continúa siendo el guard de `pypdf`, porque ese entorno mantiene `5.9.0` mientras `requirements.txt` fija `6.15.0`. Compilación Python, sintaxis de todos los JavaScript y `git diff --check` permanecen limpios.

El gate canónico de R1.1 se completó en el `.venv` del proyecto con `pypdf==6.15.0`: **743/743 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpios. La validación manual de Pasos 1–4 confirmó el bloqueo de los campos detectados, la franja primaria, los iconos `✎`/`⊘`, el selector de disponibilidad del historial sin respuesta silenciosa y el estado de análisis de Mi Retiro Seguro/Ficha Digital.

El PR #28 integró R1 + R1.1 por squash en `5e93dfc3d4c33b264c61e50f72c1eb0b84b3bc29`. Los checks `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` finalizaron en verde. R1 queda cerrado y UX.4.6f continúa con la auditoría lógica/matemática del Paso 4.

### Mantenimiento de dependencias post-R1

Dependabot propuso `uvicorn 0.52.1 → 0.52.3` (#26) y `pypdf 6.15.0 → 6.16.1` (#27). Los PR aislados no podían superar la suite porque los guards de inventario y compatibilidad fijaban correctamente las versiones vigentes anteriores. La actualización coordinada sincronizó `requirements.txt`, `docs/DEPENDENCIAS_TERCEROS.md`, `THIRD_PARTY_NOTICES.md` y las regresiones de versión.

El gate local completó `pip check`, `compileall`, sintaxis JavaScript, **743/743 pruebas en `OK`** y `git diff --check`; `pypdf 6.16.1` superó el roundtrip sintético, rechazo controlado de PDF sin texto y límites de páginas de ambos importadores. PR #29 fue integrado por squash en `2b4aa0401fe9cc2eef545d335492863bca675e5c` después de Python 3.13, Python 3.14 y Auditoría de gobernanza en verde. #26 y #27 quedaron cerrados como sustituidos. `VERSION` permanece en `0.0.26-beta`.

### UX.4.6f R2 — cierre de auditoría del Paso 4

R2 añade **13 regresiones** sobre la base de 743 para proteger: cierre del caso visible de 2026; proyección constante futura; rechazo de totales/cuotas del año actual desincronizados; rechazo de historial incompleto; transporte explícito del salario mensual proyectado; estado sin cotización futura; comportamiento conservador de `FUTURO_CONOCIDO`; copy de composición anual; ausencia de porcentajes predeterminados en `ESCENARIOS`; rechazo de esa modalidad sin tasas explícitas; procedencia del horizonte ampliado desde retiro; y trazabilidad ADR/RF/TR.

El inventario objetivo del candidato es **756 pruebas**. En el entorno aislado de preparación se ejecutaron **755/756**; la única prueba no satisfactoria fue el guard de versión instalada porque ese entorno conserva `pypdf 5.9.0` mientras el proyecto fija `pypdf==6.16.1`. Las 13 regresiones específicas de R2 y el frente de proyección/línea temporal pasaron correctamente.

El gate remoto de PR #30 instaló `pypdf 6.16.1`, completó `pip check`, `compileall`, sintaxis JavaScript y ejecutó **756/756 pruebas en `OK`** tanto en Python 3.13 como en Python 3.14; Auditoría de gobernanza también finalizó en verde. La validación manual confirmó el caso femenino, salario constante, crecimiento porcentual compuesto, salario futuro conocido con mantenimiento constante posterior al objetivo y comparación de escenarios sin valores predeterminados. PR #30 fue integrado por squash en `9634ae4b1a0a07cc14682d315b6cdb9c1b37eb4d`.

El cierre documental inicial añadió una regresión para impedir que README, ROADMAP y el plan maestro volvieran a presentar Paso 4 como pendiente. Su primera ejecución completa alcanzó 757 pruebas pero detectó **cuatro fallos históricos**: tres módulos de UX.4.6e todavía exigían que UX.4.6f permaneciera activo o pendiente. Esas regresiones se corrigen para preservar la evidencia de UX.4.6e sin congelar el estado futuro del roadmap.

Como endurecimiento permanente, el repositorio incorpora `.githooks/pre-commit`, `scripts/validar_precommit.py` y `scripts/configurar_hooks_git.ps1`. Una vez activado por clon, Git rechaza el commit si se intenta confirmar directamente en `main`, existe un árbol de trabajo que no corresponde al staging, falla `git diff --cached --check`, `pip check`, `compileall`, `node --check` o la suite completa. Cinco regresiones adicionales protegen el contrato; el inventario de cierre pasa a **762 pruebas** sin modificar `VERSION`. Los checks remotos del Pull Request siguen siendo obligatorios y no son sustituidos por el hook local.


### MANT.1 R2 — documentación de scripts y hooks


MANT.1 R1 queda como auditoría inicial: inventario de archivos de código/configuración,
clasificación de superficies por carpeta y decisión de ejecutar el mantenimiento por
revisiones pequeñas antes de SEC.2. No modificó runtime, versión, motores ni normativa.

MANT.1 R2 documenta la infraestructura local del gate pre-commit sin cambiar su
comportamiento funcional. La revisión cubre:

- `.githooks/pre-commit`;
- `scripts/configurar_hooks_git.ps1`;
- `scripts/validar_precommit.py`;
- `scripts/README.md`;
- `.githooks/README.md`;
- regresión `tests/test_mant1_scripts_hooks_documentados.py`.

El alcance de validación de MANT.1 R2 exige que los scripts y hooks expliquen su
propósito, límites, dependencias y relación con la CI. El gate local sigue
ejecutando `pip check`, compilación Python, `node --check`, suite completa y
verificación de whitespace preparada antes de permitir commits.

### MANT.1 R3 — encabezados YAML de GitHub

MANT.1 R3 documenta los archivos YAML de `.github/` detectados en la auditoría
inicial de MANT.1 R1. La revisión agrega comentarios superiores a Dependabot,
Issue Forms y workflows sin cambiar triggers, jobs, permisos, labels, campos,
cadencias ni comandos operativos.

La regresión `tests/test_mant1_r3_yaml_github_documentados.py` protege que:

- los ocho YAML de GitHub comiencen con encabezado `MANT.1 R3`;
- los encabezados declaren propósito y límites;
- las superficies transversales mantengan visibles MANT.1 R1, MANT.1 R2 y MANT.1 R3;
- los workflows e Issue Forms conserven sus claves funcionales principales.

## 2. Comandos obligatorios

```powershell
python -m compileall app

Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

python -m unittest discover -s tests -q
git diff --check
```

El mismo conjunto se ejecuta automáticamente antes de cada commit cuando el clon tiene configurado `core.hooksPath=.githooks`. El hook devuelve código no cero ante cualquier fallo, por lo que Git no debe materializar el commit. `--no-verify` no se considera una forma válida de resolver un gate fallido.

Para cambios de dependencias también se exige:

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

## 3. Inventario actual de pruebas

Inventario vigente: **99 módulos**.

- `tests/test_accesibilidad_temas.py`
- `tests/test_accesibilidad_ux4.py`
- `tests/test_comparador.py`
- `tests/test_dinero.py`
- `tests/test_estabilizacion_visual.py`
- `tests/test_fuentes_normativas.py`
- `tests/test_gov12_versionado.py`
- `tests/test_gov13_documentacion.py`
- `tests/test_gov13_documentacion_r2.py`
- `tests/test_gov13_documentacion_r3.py`
- `tests/test_gov13_documentacion_r4.py`
- `tests/test_gov14_observabilidad.py`
- `tests/test_gov14_observabilidad_integracion.py`
- `tests/test_gov15_cierre_seguridad_privacidad.py`
- `tests/test_gov15_modelo_amenazas.py`
- `tests/test_gov15_procedimientos_privacidad.py`
- `tests/test_gov16_controles_github.py`
- `tests/test_gov17_licencia.py`
- `tests/test_gov18_cierre_gobierno.py`
- `tests/test_gov_firma_git.py`
- `tests/test_identidad_interfaz.py`
- `tests/test_identidad_publica_github_pre_r8.py`
- `tests/test_identidad_visual_pre_r8.py`
- `tests/test_indemnizacion_vejez.py`
- `tests/test_linea_tiempo.py`
- `tests/test_mantenimiento_tecnico.py`
- `tests/test_mixto.py`
- `tests/test_mixto_prestaciones_cap.py`
- `tests/test_plan1_documentacion_primaria.py`
- `tests/test_plan1_documentacion_transversal.py`
- `tests/test_plan1_gobierno_versionado_oficial.py`
- `tests/test_plan1_guard_referencias_historicas.py`
- `tests/test_plan1_licencia_privacidad_viva.py`
- `tests/test_plan1_r4_candidato_cierre.py`
- `tests/test_plan1_saneamiento_metadata.py`
- `tests/test_plan1_terminologia_seguridad.py`
- `tests/test_plan1_versionado_oficial.py`
- `tests/test_prebeta_e2e_hardening.py`
- `tests/test_precommit_guard.py`
- `tests/test_proyeccion_salarios.py`
- `tests/test_pypdf_compatibilidad.py`
- `tests/test_responsive_ux3.py`
- `tests/test_resultado_unificado.py`
- `tests/test_resultados.py`
- `tests/test_resultados_mixto.py`
- `tests/test_resultados_modalidades.py`
- `tests/test_resultados_sucgs.py`
- `tests/test_retiro.py`
- `tests/test_sebd.py`
- `tests/test_sebd_modalidades.py`
- `tests/test_sucgs.py`
- `tests/test_sucgs_capa_solidaria.py`
- `tests/test_sucgs_reemplazo.py`
- `tests/test_trazabilidad.py`
- `tests/test_ux42_estados_visuales.py`
- `tests/test_ux43_formularios_teclado.py`
- `tests/test_ux44_detalle_anio_actual.py`
- `tests/test_ux44_edad_linea_tiempo.py`
- `tests/test_ux44_importacion_oficial.py`
- `tests/test_ux44_referencia_pdf.py`
- `tests/test_ux45_cierre_resultados_accesibilidad.py`
- `tests/test_ux46a_redisenio_integral.py`
- `tests/test_ux46b_paso1_datos_personales.py`
- `tests/test_ux46b_revision2_privacidad.py`
- `tests/test_ux46b_revision3_terminos_navegacion.py`
- `tests/test_ux46c_cuotas.py`
- `tests/test_ux46d_gestion_datos.py`
- `tests/test_ux46d_historial.py`
- `tests/test_ux46d_revision10_tablas_transversales.py`
- `tests/test_ux46d_revision11_scrollbars_y_carga.py`
- `tests/test_ux46d_revision12_scroll_global_y_vacio.py`
- `tests/test_ux46d_revision13_selector_archivo.py`
- `tests/test_ux46d_revision14_paso1_informacion_personal.py`
- `tests/test_ux46d_revision15_campos_importacion_y_limpieza.py`
- `tests/test_ux46d_revision16_flujo_paso3.py`
- `tests/test_ux46d_revision17_auditoria_datos.py`
- `tests/test_ux46d_revision18_procedencia_persistencia.py`
- `tests/test_ux46d_revision19_sincronizacion_actual.py`
- `tests/test_ux46d_revision20_vigencia_resumen.py`
- `tests/test_ux46d_revision21_fecha_confiable.py`
- `tests/test_ux46d_revision22_cierre_paso3.py`
- `tests/test_ux46d_revision23_ficha_actualiza_cuotas.py`
- `tests/test_ux46d_revision7_privacidad_consulta.py`
- `tests/test_ux46d_revision8_tablas.py`
- `tests/test_ux46d_revision9_reactividad_privacidad.py`
- `tests/test_ux46e_almacenamiento_comentarios_js.py`
- `tests/test_ux46e_auditoria_coherencia.py`
- `tests/test_ux46e_estandar_runtime.py`
- `tests/test_ux46e_preparacion_publica.py`
- `tests/test_ux46e_proyeccion_salarial.py`
- `tests/test_ux46e_r81_procedencia_editable.py`
- `tests/test_ux46e_r8_cierre_funcional.py`
- `tests/test_ux46e_r8_reconsentimiento_borrado.py`
- `tests/test_ux46e_r91_candidato_cierre.py`
- `tests/test_ux46e_renumeracion_documental.py`
- `tests/test_ux46f_r11_bloqueo_documental_vista_principal.py`
- `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py`
- `tests/test_ux46g_r1_escenarios_retiro.py`
- `tests/test_ux4_remate_visual.py`

## 4. Categorías

- núcleo/servicios;
- motores;
- integración;
- UX/accesibilidad;
- importadores;
- gobierno/documentación.

## 5. Casos personales

Los originales reales no se versionan.

Una regresión derivada de un caso personal debe transformarse en datos sintéticos o anonimizados suficientes para preservar la propiedad técnica.

## 6. Importadores

Deben cubrir formato, límites, cifrado, texto, clasificación, año de Ficha, fecha externa, procedencia, confirmación, no persistencia y reconciliación.

La compatibilidad de la biblioteca PDF se valida sin documentos personales reales: se generan PDFs sintéticos en memoria con `PdfWriter` y se procesan con `PdfReader` a través de los servicios reales.

La suite no depende de disponibilidad real de CSS: las consultas externas se sustituyen/mokean en pruebas.

## 7. Privacidad

Las regresiones deben comprobar:

- versión de consentimiento sincronizada con el frontend;
- ausencia de versiones intermedias en documentos vigentes;
- almacenamiento local/sesión correctamente descrito;
- conexiones externas documentadas;
- separación entre control interno y certificación jurídica.

## 8. Normativa

Las regresiones documentales comprueban metadata/fuentes/versionado; **no sustituyen una revisión jurídica del contenido legal**.

## 9. Validación manual

Sigue siendo necesaria para:

- visual;
- teclado/foco;
- modales;
- temas;
- lectura/consentimiento;
- selectores de archivos;
- comportamiento multidispositivo.

## 10. CI

La CI debe permanecer verde antes de considerar cerrado un hito formal.

### UX.4.6g R1 — gate candidato

La revisión acumula 18 regresiones en `tests/test_ux46g_r1_escenarios_retiro.py`. Partiendo del cierre de UX.4.6f con 762 pruebas, el gate objetivo del candidato es **780 pruebas en `OK`**, además de `pip check`, `compileall`, sintaxis JavaScript y `git diff --check`. La validación manual debe cubrir: sugerencia `+1…+N` desde Paso 4, preservación de una edición manual, ausencia de selección anticipada automática, fechas anticipadas transcurridas deshabilitadas, disponibilidad de la fecha de evaluación dentro de banda para sexo `F`/`M`, presencia de `+4`, tabla corta sin scroll vertical interno, mensaje explícito de cobertura de fecha personalizada y controles de fecha compactos/validados en Claro, Oscuro y Alto contraste.

### UX.4.6g R1.4.2 — robustez de inicialización

Se añade una regresión para impedir que la normalización global de accesibilidad observe recursivamente sus propias mutaciones de clase. El gate objetivo pasa a **781 pruebas**. La validación manual debe incluir recarga normal y recarga completa (`Ctrl+F5`) sin bloqueo del navegador ni pérdida aparente del estado de la simulación.

### UX.4.6g R1.4.3 — alineación visual final

Se añaden tres regresiones para la alineación del período del historial, la alineación de los dos años del Paso 4 y la distribución responsive del resumen de retiro. El gate objetivo pasa a **784 pruebas en `OK`**. La validación manual debe confirmar estas tres geometrías en escritorio y que el apilado móvil no se degrade.

### UX.4.6i R1 — guía pública Cómo se calcula

La revisión añade **14 regresiones específicas** en `tests/test_ux46i_r1_como_se_calcula.py`. Partiendo del cierre de UX.4.6h con 812 pruebas, el gate objetivo del candidato es **826 pruebas en `OK`**, además de `pip check`, compilación Python, sintaxis JavaScript y `git diff --check`.

La validación automática cubre ruta pública, lectura de parámetros normativos, ausencia de motores en la capa explicativa, contenido SEBD/Mixto/SUCGS, enlaces desde resultados y Metodología, estructura accesible/responsive, ADR/RF/TR y documentación. La validación manual debe comprobar temas Claro, Oscuro y Alto contraste, navegación por anclas, tablas desplegables y legibilidad en escritorio/móvil.

### UX.4.6i R1.2 — recorrido completo y refinamiento visual

La primera validación visual de R1 confirmó la estructura general y detectó cuatro mejoras necesarias: acceso directo desde la navbar, explicación más profunda de la transformación de datos entre Pasos 1–6, separador de miles en importes de la guía y menor altura de las tablas de factores.

R1.2 añade **6 regresiones** sobre la línea de 826 pruebas: navegación activa, recorrido de transformación de datos, ausencia de lenguaje interno en la copia principal, formato monetario, densidad de factores SEBD/SUCGS y uso de tokens/tema. El gate objetivo pasa a **832 pruebas en `OK`**.

La validación manual debe confirmar Claro, Oscuro y Alto contraste; navbar activa; tablas SEBD en 3 filas y SUCGS en aproximadamente 5 filas en escritorio amplio; legibilidad responsive; y correspondencia de las explicaciones de Pasos 1–6 con la simulación real.
### UX.4.6i R1.3 — sustituciones numéricas y terminología contextual

R1.3 añade **8 regresiones** sobre la línea de 832 pruebas. Protegen la presencia simultánea de fórmula general y ejemplo sustituido, la terminología contextual de SEBD/Mixto/SUCGS, las fórmulas adicionales de tasa equivalente y fracción de año, el espaciado de tabla/nota/fuentes y el uso exclusivo de tokens semánticos en la nueva capa visual. El gate objetivo pasa a **840 pruebas en `OK`**.
### UX.4.6i R1.4 — cierre de guía pública

R1.4 simplifica la etiqueta visible de cada sustitución numérica a **Ejemplo** y añade una regresión para impedir que reaparezca la coletilla anterior. La validación manual acumulada confirmó estructura, navegación, recorrido de datos Pasos 1–6, fórmulas con sustitución, definiciones contextuales, tablas SEBD/SUCGS compactas, espaciado y presentación de los tres sistemas. El gate de cierre queda en **841 pruebas en `OK`**.
