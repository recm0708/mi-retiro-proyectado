# Validación

**Estado:** Vigente
**Versión candidata revisada:** `0.0.71.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Base documental histórica:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal histórica preservada:** UX.4.6e R8 — validación funcional y procedencia editable — 2026-08-19
**Última revisión transversal:** UX.4.6f R2 integrada y cierre del Paso 4 — 2026-08-20
**Revisión de normalización:** NOR.1 R7 — cierre de estándares y preparación de NOR.2 — 2026-08-24
**Clasificación:** Técnica / Calidad


<!-- NOR1-R7-VALIDATION:START -->
## Validación NOR.1

NOR.1 R7 cierra la fase de definición de estándares y prepara la transición a
NOR.2.

Línea base observada antes de R7:

- NOR.1 R6: `5 passed` en las pruebas específicas de estándares;
- NOR.1 + MANT.1 R5E: `9 passed, 19 subtests passed`;
- gate `pre-commit` de R6: `933 tests OK`;
- workflows de **Validación continua** y **Auditoría de gobernanza** en verde;
- PR #65 integrado por squash.

El cierre formal de R7 exige repetir pruebas focales, gate completo, CI y merge.
NOR.2 no debe iniciarse desde una rama que no haya cumplido estos gates.
<!-- NOR1-R7-VALIDATION:END -->


<!-- NOR2-R1-VALIDATION:START -->
## Validación NOR.2 R1

R1 es una auditoría de línea base. La evidencia se genera desde `git ls-files` y
los conteos de referencias críticas se obtienen con `git grep`.

R1 no modifica código funcional, motores previsionales, normativa, `VERSION` ni
rutas públicas. El gate debe demostrar además que la documentación transversal
registra NOR.2 R1 y que la evidencia de auditoría permanece bajo `docs/audits/`.
<!-- NOR2-R1-VALIDATION:END -->


<!-- NOR2-R2-VALIDATION:START -->
## Validación NOR.2 R2

R2 protegió la matriz de migración y el estado público del repositorio. En ese
cierre, la validación exigió que `README.md` no marcara DOC.1 como activo,
reconociera NOR.1 como cerrado, declarara NOR.2 R2 como activo en ese momento y
representara las carpetas reales `engines/`, `models/` y `services/`.

La versión de aplicación no cambia.
<!-- NOR2-R2-VALIDATION:END -->


<!-- NOR2-R3-VALIDATION:START -->
## Validación NOR.2 R3

R3 valida los 28 movimientos técnicos, ausencia de las rutas antiguas,
existencia de las rutas nuevas, imports de servicios, estabilidad de URL
públicas, excepción Ficha Digital y versión canónica sin cambios.

Evidencia local observada en R3:

- gate focal NOR.2: `28 passed, 32 subtests passed`;
- regresiones corregidas: `56 passed, 37 subtests passed`;
- suite completa: `956 tests` en `OK`;
- compilación Python sin errores;
- validación sintáctica de todos los JavaScript sin errores;
- `git diff --check` limpio;
- gate `pre-commit` completo superado.
<!-- NOR2-R3-VALIDATION:END -->

<!-- DOC1-R1-POST-MANT1:START -->
## Estado de validación post-MANT.1

La validación documental vigente queda alineada con el cierre operativo de MANT.1 R7.

Evidencia observada:

- Suite completa local post-R7: `939 passed`.
- Gate `pre-commit` observado durante R7: `928 tests OK`.
- Pruebas focalizadas R5H/R6/R7 ejecutadas correctamente antes del cierre.
- `git diff --check` no reportó errores antes del commit R7.
- Archivos protegidos verificados sin cambios: `VERSION`, `app/core/version.py`, `app/core/config.py`, `regulations/`, `data/` y `_entregas/`.

DOC.1 R1 no cambia el contrato funcional ni los motores previsionales. Su validación se limita a coherencia documental, referencias Markdown y preservación del estado canónico post-MANT.1.
<!-- DOC1-R1-POST-MANT1:END -->

La estrategia combina pruebas automatizadas, CI, casos sintéticos/anonimizados y validación manual cuando una propiedad no puede demostrarse suficientemente con código.

## Validación MANT.1 R5H — nombres técnicos restantes

MANT.1 R5H completa una segunda pasada sobre nombres técnicos restantes,
sincronizando imports, rutas de assets, referencias de plantillas,
documentación viva y pruebas automatizadas.

Comandos ejecutados para el cierre local:

```powershell
python -m compileall app tests -q
python -m pytest -q --tb=short
python -m unittest discover -s tests -q
git diff --check
```

Resultado observado:

```text
924 passed, 4749 subtests passed
Ran 924 tests
OK
git diff --check: OK
```

La revisión no cambia `VERSION`, `APP_VERSION`, motores previsionales,
parámetros normativos, contratos JSON regulatorios, rutas públicas
funcionales, claves de almacenamiento, ids, clases ni `_entregas/`.

## Validación MANT.1 R5E — nombres de carpetas técnicas

MANT.1 R5E valida que las carpetas técnicas en español hayan sido renombradas a
inglés y que las referencias internas queden sincronizadas.

Comandos mínimos para el cierre local:

```powershell
python -m pytest tests\test_mant1_r5e_nombres_carpetas.py -q
python -m pytest tests\test_mant1_r5d_politica_extensiones.py tests\test_mant1_r5e_nombres_carpetas.py -q
git diff --check
python -m pytest -q
python -m unittest discover -s tests -q
```

La revisión no cambia `VERSION`, `APP_VERSION`, fórmulas previsionales, valores
JSON, rutas públicas, ids, clases, selectores ni `_entregas/`.

## Validación MANT.1 R5D — política, plantillas y uniformidad por extensión

MANT.1 R5D valida que exista una política formal por extensión, que las
plantillas oficiales estén presentes con su extensión correspondiente y que los
encabezados de JavaScript/CSS operativo sigan un patrón uniforme de propósito y
alcance permanente.

Comandos previstos:

```powershell
python -m pytest tests\test_mant1_r5d_politica_extensiones.py -q
python -m pytest tests\test_mant1_r5c_comentarios_js_app.py tests\test_mant1_r5d_politica_extensiones.py -q
git diff --check
python -m pytest -q
```

La revisión no cambia `VERSION`, `APP_VERSION`, motores previsionales,
normativa, rutas públicas, contratos JSON, claves de almacenamiento, selectores,
ids, clases, textos visibles ni SEC.2.

## Validación MANT.1 R5C — comentarios internos en JavaScript complejo

MANT.1 R5C valida que los módulos JavaScript revisados tengan comentarios
internos de intención para almacenamiento, invalidación, borradores revisables,
privacidad, adjuntos, comparación y resultados, sin cambiar claves, selectores,
ids, clases, textos visibles ni lógica funcional.

Comandos usados:

```powershell
python -m pytest tests\test_mant1_r5c_comentarios_js_app.py -q
python -m pytest tests\test_mant1_r5a_comentarios_servicios_app.py tests\test_mant1_r5b_comentarios_presentacion_app.py tests\test_mant1_r5c_comentarios_js_app.py -q
python -m pytest tests\test_ux46e_almacenamiento_comentarios_js.py tests\test_ux46e_auditoria_coherencia.py -q
git diff --check
python -m pytest -q
```

La revisión no cambia `VERSION`, `APP_VERSION`, motores previsionales,
normativa, rutas públicas, contratos JSON, claves de almacenamiento ni SEC.2.

## Validación MANT.1 R5B — comentarios internos en CSS y plantilla Cómo se calcula

MANT.1 R5B valida que la hoja de estilos y la plantilla principal de la guía
pública tengan comentarios estructurales útiles, sin cambiar clases, ids, textos
visibles, rutas ni lógica Jinja.

Comandos usados:

```powershell
python -m pytest tests\test_mant1_r5b_comentarios_presentacion_app.py -q
python -m pytest tests\test_mant1_r5a_comentarios_servicios_app.py tests\test_mant1_r5b_comentarios_presentacion_app.py -q
python -m pytest tests\test_ux46e_almacenamiento_comentarios_js.py tests\test_ux46e_auditoria_coherencia.py -q
git diff --check
python -m pytest -q
```

La revisión no cambia `VERSION`, `APP_VERSION`, motores previsionales,
normativa, rutas públicas, contratos JSON ni SEC.2.

## Validación MANT.1 R5A — comentarios internos en servicios Python

MANT.1 R5A valida que los servicios Python de aplicación revisados contengan
comentarios internos de intención para flujos complejos, sin introducir
identificadores de revisión dentro del código operativo.

Comandos mínimos para el cierre local:

```text
python -m pytest tests\test_mant1_r5a_comentarios_servicios_app.py -q
python -m pytest tests\test_mant1_r4_encabezados_operativos_limpios.py tests\test_mant1_r5a_comentarios_servicios_app.py -q
python -m pytest tests\test_ux46e_almacenamiento_comentarios_js.py tests\test_ux46e_auditoria_coherencia.py -q
git diff --check
python -m pytest -q
```

Esta revisión no cambia motores, normativa, contratos JSON, rutas públicas,
`VERSION`, `APP_VERSION` ni SEC.2.

## Validación MANT.1 R4 — encabezados operativos limpios

MANT.1 R4 corrige la ubicación de trazabilidad histórica en archivos operativos.
La validación esperada debe confirmar que YAML, hooks y README técnicos conserven
encabezados funcionales, sin declarar MANT.1 en sus primeras líneas.

Comandos mínimos para el cierre local:

```text
python -m pytest tests\test_mant1_r4_encabezados_operativos_limpios.py -q
python -m pytest tests\test_mant1_r3_yaml_github_documentados.py tests\test_mant1_r4_encabezados_operativos_limpios.py -q
python -m pytest tests\test_mant1_scripts_hooks_documentados.py tests\test_mant1_r3_yaml_github_documentados.py tests\test_mant1_r4_encabezados_operativos_limpios.py -q
git diff --check
python -m pytest -q
```

Esta revisión no cambia workflows, formularios, Dependabot, motores, normativa,
`VERSION`, `APP_VERSION` ni SEC.2.


## 1. Línea base

Cierre validado de GOV.1.3 R2:

```text
Ran 423 tests
OK
```

GOV.1.3 R3 agregó **15 regresiones documentales**. El cierre de R3 fue validado con una suite completa de **438 pruebas en `OK`**, incluidas **15/15 regresiones específicas de R3**, **12/12 regresiones de R2** y **8/8 regresiones documentales de R1**.

Durante R3 también se endureció la regresión de cierre de R2: su evidencia histórica se valida contra `CHANGELOG.md` en lugar de exigir que el documento vigente `validation.md` conserve indefinidamente la línea base de una revisión anterior.
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

Dependabot propuso `uvicorn 0.52.1 → 0.52.3` (#26) y `pypdf 6.15.0 → 6.16.1` (#27). Los PR aislados no podían superar la suite porque los guards de inventario y compatibilidad fijaban correctamente las versiones vigentes anteriores. La actualización coordinada sincronizó `requirements.txt`, `docs/operations/third-party-dependencies.md`, `THIRD_PARTY_NOTICES.md` y las regresiones de versión.

El gate local completó `pip check`, `compileall`, sintaxis JavaScript, **743/743 pruebas en `OK`** y `git diff --check`; `pypdf 6.16.1` superó el roundtrip sintético, rechazo controlado de PDF sin texto y límites de páginas de ambos importadores. PR #29 fue integrado por squash en `2b4aa0401fe9cc2eef545d335492863bca675e5c` después de Python 3.13, Python 3.14 y Auditoría de gobernanza en verde. #26 y #27 quedaron cerrados como sustituidos. `VERSION` permanece en `0.0.26-beta`.

### UX.4.6f R2 — cierre de auditoría del Paso 4

R2 añade **13 regresiones** sobre la base de 743 para proteger: cierre del caso visible de 2026; proyección constante futura; rechazo de totales/cuotas del año actual desincronizados; rechazo de historial incompleto; transporte explícito del salario mensual proyectado; estado sin cotización futura; comportamiento conservador de `FUTURO_CONOCIDO`; copy de composición anual; ausencia de porcentajes predeterminados en `ESCENARIOS`; rechazo de esa modalidad sin tasas explícitas; procedencia del horizonte ampliado desde retiro; y trazabilidad ADR/RF/TR.

El inventario objetivo del candidato es **756 pruebas**. En el entorno aislado de preparación se ejecutaron **755/756**; la única prueba no satisfactoria fue el guard de versión instalada porque ese entorno conserva `pypdf 5.9.0` mientras el proyecto fija `pypdf==6.16.1`. Las 13 regresiones específicas de R2 y el frente de proyección/línea temporal pasaron correctamente.

El gate remoto de PR #30 instaló `pypdf 6.16.1`, completó `pip check`, `compileall`, sintaxis JavaScript y ejecutó **756/756 pruebas en `OK`** tanto en Python 3.13 como en Python 3.14; Auditoría de gobernanza también finalizó en verde. La validación manual confirmó el caso femenino, salario constante, crecimiento porcentual compuesto, salario futuro conocido con mantenimiento constante posterior al objetivo y comparación de escenarios sin valores predeterminados. PR #30 fue integrado por squash en `9634ae4b1a0a07cc14682d315b6cdb9c1b37eb4d`.

El cierre documental inicial añadió una regresión para impedir que README, ROADMAP y el plan maestro volvieran a presentar Paso 4 como pendiente. Su primera ejecución completa alcanzó 757 pruebas pero detectó **cuatro fallos históricos**: tres módulos de UX.4.6e todavía exigían que UX.4.6f permaneciera activo o pendiente. Esas regresiones se corrigen para preservar la evidencia de UX.4.6e sin congelar el estado futuro del roadmap.

Como endurecimiento permanente, el repositorio incorpora `.githooks/pre-commit`, `scripts/validate_precommit.py` y `scripts/configure_git_hooks.ps1`. Una vez activado por clon, Git rechaza el commit si se intenta confirmar directamente en `main`, existe un árbol de trabajo que no corresponde al staging, falla `git diff --cached --check`, `pip check`, `compileall`, `node --check` o la suite completa. Cinco regresiones adicionales protegen el contrato; el inventario de cierre pasa a **762 pruebas** sin modificar `VERSION`. Los checks remotos del Pull Request siguen siendo obligatorios y no son sustituidos por el hook local.


### MANT.1 R2 — documentación de scripts y hooks


MANT.1 R1 queda como auditoría inicial: inventario de archivos de código/configuración,
clasificación de superficies por carpeta y decisión de ejecutar el mantenimiento por
revisiones pequeñas antes de SEC.2. No modificó runtime, versión, motores ni normativa.

MANT.1 R2 documenta la infraestructura local del gate pre-commit sin cambiar su
comportamiento funcional. La revisión cubre:

- `.githooks/pre-commit`;
- `scripts/configure_git_hooks.ps1`;
- `scripts/validate_precommit.py`;
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

- los ocho YAML de GitHub conserven encabezados funcionales permanentes;
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

Inventario vigente: **133 módulos**.

- `tests/test_accessibility_themes.py`
- `tests/test_accessibility_ux4.py`
- `tests/test_comparator.py`
- `tests/test_dev2_development_center.py`
- `tests/test_dev2_r1_cierre_documental.py`
- `tests/test_dev2_r2_visor_diagnostico.py`
- `tests/test_dev2_r3_autodiagnostico.py`
- `tests/test_dev2_r4_cierre_final.py`
- `tests/test_doc1_r1_auditoria_markdown_post_mant1.py`
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
- `tests/test_indemnizacion_vejez.py`
- `tests/test_mant1_r3_yaml_github_documentados.py`
- `tests/test_mant1_r4_encabezados_operativos_limpios.py`
- `tests/test_mant1_r5a_comentarios_servicios_app.py`
- `tests/test_mant1_r5b_comentarios_presentacion_app.py`
- `tests/test_mant1_r5c_comentarios_js_app.py`
- `tests/test_mant1_r5d_politica_extensiones.py`
- `tests/test_mant1_r5e_nombres_carpetas.py`
- `tests/test_mant1_r5f_nombres_archivos.py`
- `tests/test_mant1_r5g_documentacion.py`
- `tests/test_mant1_r5h_auditoria_nombres_restantes.py`
- `tests/test_mant1_r6_auditoria_funcional_post_renombres.py`
- `tests/test_mant1_r7_cierre_operativo_post_auditoria.py`
- `tests/test_mant1_scripts_hooks_documentados.py`
- `tests/test_mantenimiento_tecnico.py`
- `tests/test_mixto.py`
- `tests/test_mixto_prestaciones_cap.py`
- `tests/test_mixto_results.py`
- `tests/test_modality_results.py`
- `tests/test_money.py`
- `tests/test_nor1_repository_standards.py`
- `tests/test_nor2_r2_migration_matrix.py`
- `tests/test_nor2_r3_runtime_migration.py`
- `tests/test_nor2_repository_normalization.py`
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
- `tests/test_pypdf_compatibilidad.py`
- `tests/test_regulatory_sources.py`
- `tests/test_responsive_ux3.py`
- `tests/test_results.py`
- `tests/test_retirement.py`
- `tests/test_salary_projection.py`
- `tests/test_sebd.py`
- `tests/test_sebd_modalidades.py`
- `tests/test_sucgs.py`
- `tests/test_sucgs_capa_solidaria.py`
- `tests/test_sucgs_reemplazo.py`
- `tests/test_sucgs_results.py`
- `tests/test_timeline.py`
- `tests/test_traceability.py`
- `tests/test_unified_result.py`
- `tests/test_ux42_estados_visuales.py`
- `tests/test_ux43_formularios_teclado.py`
- `tests/test_ux44_current_year_detail.py`
- `tests/test_ux44_edad_linea_tiempo.py`
- `tests/test_ux44_importacion_oficial.py`
- `tests/test_ux44_pdf_reference.py`
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
- `tests/test_ux46d_revision18_provenance_persistence.py`
- `tests/test_ux46d_revision19_current_sync.py`
- `tests/test_ux46d_revision20_vigencia_resumen.py`
- `tests/test_ux46d_revision21_fecha_confiable.py`
- `tests/test_ux46d_revision22_cierre_paso3.py`
- `tests/test_ux46d_revision23_ficha_updates_contributions.py`
- `tests/test_ux46d_revision7_privacidad_consulta.py`
- `tests/test_ux46d_revision8_tablas.py`
- `tests/test_ux46d_revision9_reactividad_privacidad.py`
- `tests/test_ux46e_almacenamiento_comentarios_js.py`
- `tests/test_ux46e_auditoria_coherencia.py`
- `tests/test_ux46e_estandar_runtime.py`
- `tests/test_ux46e_preparacion_publica.py`
- `tests/test_ux46e_proyeccion_salarial.py`
- `tests/test_ux46e_r81_editable_provenance.py`
- `tests/test_ux46e_r8_cierre_funcional.py`
- `tests/test_ux46e_r8_reconsentimiento_borrado.py`
- `tests/test_ux46e_r91_candidato_cierre.py`
- `tests/test_ux46e_renumeracion_documental.py`
- `tests/test_ux46f_r11_bloqueo_documental_vista_principal.py`
- `tests/test_ux46f_r1_attachment_provenance_consistency.py`
- `tests/test_ux46f_r2_auditoria_paso4.py`
- `tests/test_ux46g_r1_retirement_scenarios.py`
- `tests/test_ux46h_r1_resultados_exportacion.py`
- `tests/test_ux46i_r1_calculation_guide.py`
- `tests/test_ux4_remate_visual.py`
- `tests/test_ver2_documentacion_vigente.py`
- `tests/test_ver2_ledger_estructurado.py`
- `tests/test_ver2_r1_reconciliacion_post_doc1.py`
- `tests/test_ver2_r2_documentacion_viva_post_r1.py`
- `tests/test_ver2_r3_decision_version_candidata_post_r2.py`
- `tests/test_ver2_r4_promocion_g071_e01.py`
- `tests/test_ver2_r5_estabilizacion_post_release.py`
- `tests/test_ver2_version_revision_aware.py`
- `tests/test_visual_identity_pre_r8.py`
- `tests/test_visual_stabilization.py`

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

La revisión acumula 18 regresiones en `tests/test_ux46g_r1_retirement_scenarios.py`. Partiendo del cierre de UX.4.6f con 762 pruebas, el gate objetivo del candidato es **780 pruebas en `OK`**, además de `pip check`, `compileall`, sintaxis JavaScript y `git diff --check`. La validación manual debe cubrir: sugerencia `+1…+N` desde Paso 4, preservación de una edición manual, ausencia de selección anticipada automática, fechas anticipadas transcurridas deshabilitadas, disponibilidad de la fecha de evaluación dentro de banda para sexo `F`/`M`, presencia de `+4`, tabla corta sin scroll vertical interno, mensaje explícito de cobertura de fecha personalizada y controles de fecha compactos/validados en Claro, Oscuro y Alto contraste.

### UX.4.6g R1.4.2 — robustez de inicialización

Se añade una regresión para impedir que la normalización global de accesibilidad observe recursivamente sus propias mutaciones de clase. El gate objetivo pasa a **781 pruebas**. La validación manual debe incluir recarga normal y recarga completa (`Ctrl+F5`) sin bloqueo del navegador ni pérdida aparente del estado de la simulación.

### UX.4.6g R1.4.3 — alineación visual final

Se añaden tres regresiones para la alineación del período del historial, la alineación de los dos años del Paso 4 y la distribución responsive del resumen de retiro. El gate objetivo pasa a **784 pruebas en `OK`**. La validación manual debe confirmar estas tres geometrías en escritorio y que el apilado móvil no se degrade.

### UX.4.6i R1 — guía pública Cómo se calcula

La revisión añade **14 regresiones específicas** en `tests/test_ux46i_r1_calculation_guide.py`. Partiendo del cierre de UX.4.6h con 812 pruebas, el gate objetivo del candidato es **826 pruebas en `OK`**, además de `pip check`, compilación Python, sintaxis JavaScript y `git diff --check`.

La validación automática cubre ruta pública, lectura de parámetros normativos, ausencia de motores en la capa explicativa, contenido SEBD/Mixto/SUCGS, enlaces desde resultados y Metodología, estructura accesible/responsive, ADR/RF/TR y documentación. La validación manual debe comprobar temas Claro, Oscuro y Alto contraste, navegación por anclas, tablas desplegables y legibilidad en escritorio/móvil.

### UX.4.6i R1.2 — recorrido completo y refinamiento visual

La primera validación visual de R1 confirmó la estructura general y detectó cuatro mejoras necesarias: acceso directo desde la navbar, explicación más profunda de la transformación de datos entre Pasos 1–6, separador de miles en importes de la guía y menor altura de las tablas de factores.

R1.2 añade **6 regresiones** sobre la línea de 826 pruebas: navegación activa, recorrido de transformación de datos, ausencia de lenguaje interno en la copia principal, formato monetario, densidad de factores SEBD/SUCGS y uso de tokens/tema. El gate objetivo pasa a **832 pruebas en `OK`**.

La validación manual debe confirmar Claro, Oscuro y Alto contraste; navbar activa; tablas SEBD en 3 filas y SUCGS en aproximadamente 5 filas en escritorio amplio; legibilidad responsive; y correspondencia de las explicaciones de Pasos 1–6 con la simulación real.
### UX.4.6i R1.3 — sustituciones numéricas y terminología contextual

R1.3 añade **8 regresiones** sobre la línea de 832 pruebas. Protegen la presencia simultánea de fórmula general y ejemplo sustituido, la terminología contextual de SEBD/Mixto/SUCGS, las fórmulas adicionales de tasa equivalente y fracción de año, el espaciado de tabla/nota/fuentes y el uso exclusivo de tokens semánticos en la nueva capa visual. El gate objetivo pasa a **840 pruebas en `OK`**.
### UX.4.6i R1.4 — cierre de guía pública

R1.4 simplifica la etiqueta visible de cada sustitución numérica a **Ejemplo** y añade una regresión para impedir que reaparezca la coletilla anterior. La validación manual acumulada confirmó estructura, navegación, recorrido de datos Pasos 1–6, fórmulas con sustitución, definiciones contextuales, tablas SEBD/SUCGS compactas, espaciado y presentación de los tres sistemas. El gate de cierre queda en **841 pruebas en `OK`**.

### Validación MANT.1 R5G

La revisión documental R5G se valida con:

- `python -m pytest tests\test_mant1_r5g_documentacion.py -q`
- `python -m pytest tests\test_ver2_documentacion_vigente.py -q`
- `python -m pytest tests\test_ux46e_estandar_runtime.py -q`

Antes del cierre del Pull Request debe ejecutarse además la suite completa:

- `python -m pytest -q`
- `python -m unittest discover -s tests -q`
### Validación MANT.1 R5F

La revisión de nombres de archivos técnicos se valida con:

- `python -m pytest tests\test_mant1_r5f_nombres_archivos.py -q`
- `python -m pytest tests\test_mant1_scripts_hooks_documentados.py tests\test_precommit_guard.py -q`
- `python -m pytest tests\test_mant1_r5e_nombres_carpetas.py -q`
- `python -m compileall app tests -q`

Antes del cierre del Pull Request debe ejecutarse además la suite completa:

- `python -m pytest -q`
- `python -m unittest discover -s tests -q`


## Validación NOR.2 R4

R4 protege la existencia de las 43 rutas canónicas resultantes, la ausencia de las 43 rutas heredadas, la resolución de enlaces Markdown locales en documentación viva, la indexación de estándares especializados y la continuidad de `VERSION`.

### Gate local previo al commit — 2026-08-24

Resultados observados después de completar la migración y sanear las regresiones documentales:

- suite completa: **963 pruebas ejecutadas — OK**;
- gate amplio documental R4: **113 pruebas + 229 subtests — OK**;
- regresiones finales saneadas: **71 pruebas + 83 subtests — OK**;
- contrato específico NOR.2 R4: **7 pruebas + 54 subtests — OK**;
- `python -m compileall -q app`: **OK**;
- validación sintáctica de JavaScript mediante `node --check`: **OK**;
- `git diff --check`: **OK**;
- `VERSION` permanece en `0.0.71.01-beta`.

Este resultado valida localmente la rama R4 antes del commit y del gate remoto. R4
permanece activo hasta su integración en `main`; R5 es la siguiente revisión.

## NOR.2 R5 — validación de archivo histórico

El gate de R5 verificó que las 36 rutas raíz clasificadas como `ARCHIVAR`
desaparecieron, sus destinos históricos existen y `docs/` conserva únicamente
su `README.md` como Markdown de primer nivel.

Resultados observados antes del commit:

- **971 pruebas ejecutadas — OK**;
- **8 pruebas + 40 subtests** del contrato específico NOR.2 R5 — OK;
- `python -m compileall -q app` — OK;
- validación sintáctica de JavaScript mediante `node --check` — OK;
- `git diff --check` — OK;
- **36 rutas antiguas inspeccionadas** y **0 referencias vivas obsoletas**;
- **124 Markdown inspeccionados** y **0 grupos con contenido idéntico**.

`VERSION` permanece en `0.0.71.01-beta`.

<!-- NOR2-R6-VALIDATION:START -->
## Validación NOR.2 R6

R6 normaliza el ledger estructurado en
`data/pre-1-0-revision-ledger.json`, preservando sin cambios el contenido
del archivo de origen identificado durante NOR.2 R2.

El contenido del JSON permanece inalterado. El preflight verificó:

- SHA-256:
  `f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e`;
- **70 entradas** continuas G001–G070;
- `schema_version = 1`;
- siguiente Global **71**;
- siguiente candidato `0.0.71.01-beta`;
- **22 archivos** con referencias al nombre anterior, clasificados entre
  referencias vivas y evidencia histórica.

El gate local final de R6 verificó:

- **46 pruebas + 3890 subtests** en el gate focal;
- **977 pruebas** en la suite completa — `OK`;
- `python -m pip check` — `OK`;
- `python -m compileall -q app tests` — `OK`;
- sintaxis de JavaScript mediante `node --check` — `OK`;
- `git diff --check` — `OK`;
- **0 referencias obsoletas no justificadas**;
- SHA-256 del ledger preservado:
  `f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e`;
- **70 entradas G001–G070** preservadas;
- `VERSION` permanece en `0.0.71.01-beta`.

R6 quedó integrado en `main` mediante PR #72 y commit squash `365ba5b`.
<!-- NOR2-R6-VALIDATION:END -->


<!-- NOR2-R7-VALIDATION:START -->
## Validación NOR.2 R7

R7 audita y normaliza los artefactos locales heredados sin incorporarlos al
árbol Git canónico.

La línea base verificada fue:

- **29 archivos**;
- **9,874,828 bytes**;
- **20 `.txt`**;
- **8 `.patch`**;
- **1 `.zip`**;
- `_deliverables/` inicialmente vacío.

La migración local verificó:

- **20 evidencias únicas preservadas**;
- **2 archivos** en `_deliverables/dev2/`;
- **18 archivos** en `_deliverables/ver2-r2/`;
- **8 duplicados SHA-256 exactos retirados**;
- **1 ZIP reproducible retirado**;
- `_entregas/` retirado;
- `_deliverables/` permanece ignorado por Git.

El ZIP `VER2_PR35_NETO_929628d.zip`, de **8,412,675 bytes**, fue comparado
directamente contra el commit
`929628df38d4750fb103ffc79bdb81f8405535bb`.

Resultado de reproducibilidad:

- archivos Git: **329**;
- archivos ZIP: **329**;
- comunes: **329**;
- solo Git: **0**;
- solo ZIP: **0**;
- contenido diferente: **0**.

Después de la migración, `git status` permaneció limpio porque los artefactos
locales están excluidos mediante `.gitignore`.

El gate local final de R7 quedó completado satisfactoriamente.

Resultados observados:

- regresión específica `tests/test_nor2_r7_local_artifacts.py`: **7 pruebas — OK**;
- gate focal NOR.2/documental inicial: **71 pruebas + 77 subtests — OK**;
- regresiones heredadas corregidas y revalidadas: **37 pruebas + 19 subtests — OK**;
- `python -m pytest -q`: **1024 pruebas + 4902 subtests — OK**;
- `python -m unittest discover -s tests -q`: **984 tests — OK**;
- `python -m pip check`: **OK**;
- `python -m compileall -q app tests`: **OK**;
- Node.js: **v24.19.0**;
- `node --check`: **18 archivos JavaScript — OK**;
- `git diff --check`: **OK**;
- estados vivos potencialmente obsoletos auditados: **0 hallazgos**;
- fecha `2026-08-25` en documentación viva: **0 hallazgos**;
- `_entregas/`: **inexistente**;
- `_deliverables/`: **20 archivos locales**, **0 trackeados por Git**;
- `VERSION`: **`0.0.71.01-beta`**;
- `APP_VERSION`: **`0.0.71.01-beta`**.

En ese checkpoint, R7 permanecía activo únicamente hasta completar commit, Pull Request, CI,
integración en `main` y verificación post-merge.

Después de R7 continuaba **NOR.2 R8 — auditoría integral y cierre formal** y SEC.2 permanecía pausado hasta completar R8. Ambos estados son históricos; NOR.2 y SEC.2 están cerrados en el estado vigente.
<!-- NOR2-R7-VALIDATION:END -->


<!-- NOR2-R8-VALIDATION:START -->
## Validación NOR.2 R8

R8 ejecuta la segunda auditoría integral del repositorio después de las
migraciones R3–R7.

Hallazgos y correcciones locales:

- `docs/CHANGELOG_ADD_R5.txt` retirado como fragmento transitorio;
- `docs/INDICE_ADD_R5.txt` retirado como fragmento transitorio;
- `docs/` raíz queda únicamente con `README.md`;
- 115 decisiones de la matriz R2 re-auditadas;
- 3 alertas mecánicas clasificadas como falsos positivos semánticos;
- consumidores operativos vivos de rutas heredadas: **0**;
- estados vivos obsoletos antes de la corrección: **11**;
- estados vivos obsoletos después de la corrección: **0**.

Gate estructural:

- estructura raíz canónica: **OK**;
- `_entregas/`: inexistente;
- `_deliverables/`: **20 archivos locales**;
- artefactos locales trackeados: **0**;
- `VERSION`: **`0.0.71.01-beta`**;
- `APP_VERSION`: **`0.0.71.01-beta`**;
- ledger canónico: **70 entradas G001–G070 continuas**;
- ruta antigua del ledger: inexistente.

Regresiones ejecutadas hasta este checkpoint:

- `tests/test_nor2_r8_final_audit.py`:
  **10 pruebas + 17 subtests — OK**;
- suite completa `test_nor2_*.py`:
  **59 pruebas + 143 subtests — OK**;
- regresiones transversales DEV.2/GOV.1/UX.4.6i:
  **43 pruebas + 37 subtests — OK**;
- `git diff --check`: **OK**.

El gate integral local quedó completo: **1034 pruebas + 4905 subtests** en
`pytest`, **994 tests** en `unittest`, `pip check`, `compileall`, los **18 archivos JavaScript** y `git diff --check` quedaron en **OK**. Permanecen pendientes pre-commit, PR, CI, integración y verificación post-merge.

En ese checkpoint, R8 permanecía activo hasta completar dichos gates e integrarse en `main`, y SEC.2 permanecía pausado hasta el cierre formal de NOR.2. El estado vigente posterior registra ambos bloques como cerrados.
<!-- NOR2-R8-VALIDATION:END -->

## Validación DOC.1 R2

DOC.1 R2 ejecuta la auditoría integral de la documentación Markdown posterior al
cierre de NOR.2. La revisión no modifica motores previsionales, normativa,
contratos funcionales ni la versión de la aplicación.

Resultados documentales confirmados durante la revisión:

- inventario inicial auditado: **141 archivos Markdown**;
- inventario posterior al retiro de cuatro stubs: **137 archivos Markdown
  versionados antes de incorporar la evidencia final de R2**;
- stubs documentales de compatibilidad restantes: **0**;
- problemas Markdown bloqueantes después de las correcciones: **0**;
- `VERSION`: **`0.0.71.01-beta`**;
- SEC.2 permanece sin inicio formal durante esta revisión.

Controles permanentes incorporados:

- `scripts/audit_markdown.py`;
- integración del auditor en `scripts/validate_precommit.py`;
- regresiones específicas en `tests/test_markdown_audit.py`;
- documentación operativa en `scripts/README.md`;
- reglas canónicas en `docs/standards/documentation-standards.md`;
- workflow `.github/workflows/markdown-audit.yml`.

Validaciones focales ya confirmadas:

- `tests/test_markdown_audit.py`:
  **7 pruebas + 12 subtests — OK**;
- `tests/test_mant1_scripts_hooks_documentados.py`:
  **4 pruebas — OK**;
- gate focal conjunto de auditor, pre-commit y documentación de scripts:
  **15 pruebas + 8 subtests — OK** en el checkpoint previo a la incorporación
  del workflow;
- `python scripts/audit_markdown.py`: **OK**;
- `git diff --check`: **OK**.

Gate integral local confirmado hasta este checkpoint:

- suite completa `pytest`: **1041 pruebas + 4876 subtests — OK**;
- `python scripts/audit_markdown.py`: **OK**;
- `git diff --check`: **OK**.

El pre-commit integral quedó superado después de validar dependencias, auditoría
Markdown, compilación Python, sintaxis de los 18 archivos JavaScript y la suite
`unittest`, con **1001 tests — OK**.

Permanecen como gates remotos el PR, CI, integración y verificación post-merge
antes de iniciar formalmente SEC.2.
<!-- DOC1-R2-VALIDATION:END -->

## Validación SEC.2 R1

SEC.2 R1 inicia el hardening de seguridad con la corrección de dos hallazgos
CodeQL `DOM text reinterpreted as HTML` del informe imprimible.

Checkpoint local confirmado:

- dos sinks dinámicos `innerHTML` retirados;
- DOM dinámico reconstruido con `createElement`, `textContent` y
  `createTextNode`;
- tres usos restantes de `innerHTML` revisados como contenido estático;
- workflows normalizados a nombres técnicos en inglés;
- regresión específica SEC.2 R1 incorporada;
- pruebas focales: **30 pruebas + 4 subtests — OK**;
- regresión transversal: **37 pruebas + 62 subtests — OK**;
- `node --check`: **OK**;
- auditor Markdown: **OK**;
- `git diff --check`: **OK**;
- suite completa `pytest`: **1043 pruebas + 4922 subtests — OK**;
- pre-commit integral: **1003 tests — OK**;
- `VERSION`: **`0.0.71.01-beta`**, sin promoción.

SEC.2 R1 completó PR, CI, CodeQL, integración y verificación post-merge.
<!-- SEC2-R1-VALIDATION:END -->

## AUD.SEC2 R1 — validación post-cierre

La auditoría del snapshot `4bd7d8d` añadió regresiones para:

- exigir que `MRP_ADMIN_ENABLED` bloquee GET/POST del login y no pueda ser
  sustituido por una sesión previa;
- permitir fallback de cookie únicamente ante ausencia de Bearer (`401`), nunca
  ante un `403` de política;
- usar POST para logout;
- aplicar `Cache-Control: no-store` a `/dev/`;
- proteger la reconciliación G001–G108, el snapshot G070 y el candidato G109;
- verificar el inventario de 140 Markdown auditados individualmente.

La suite focal SEC.2 del paquete fue ejecutada con **33 pruebas en OK**. La suite
integral del entorno de auditoría quedó limitada por una discrepancia externa de
`pypdf` (entorno 5.9.0 frente al pin del proyecto 6.16.1); por ello el gate final
debe ejecutarse en el `.venv` del repositorio antes del commit firmado.
