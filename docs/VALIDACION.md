# Validación

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.24-beta`
**Base documental histórica:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** identidad visual y repositorio público pre-R8 — 2026-08-19
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

La revalidación manual del repositorio público del 2026-08-19 confirmó Dependency graph, Dependabot alerts/security updates, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting habilitados, con **0 alertas abiertas** en Code scanning, Secret scanning y Dependabot en ese momento. Esta evidencia no sustituye revisión periódica ni auditoría externa.

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

Para cambios de dependencias también se exige:

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

## 3. Inventario actual de pruebas

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
- `tests/test_gov_firma_git.py`
- `tests/test_gov14_observabilidad.py`
- `tests/test_gov14_observabilidad_integracion.py`
- `tests/test_gov15_modelo_amenazas.py`
- `tests/test_gov15_procedimientos_privacidad.py`
- `tests/test_gov15_cierre_seguridad_privacidad.py`
- `tests/test_gov16_controles_github.py`
- `tests/test_gov17_licencia.py`
- `tests/test_gov18_cierre_gobierno.py`
- `tests/test_identidad_interfaz.py`
- `tests/test_identidad_visual_pre_r8.py`
- `tests/test_identidad_publica_github_pre_r8.py`
- `tests/test_indemnizacion_vejez.py`
- `tests/test_linea_tiempo.py`
- `tests/test_mantenimiento_tecnico.py`
- `tests/test_mixto.py`
- `tests/test_mixto_prestaciones_cap.py`
- `tests/test_prebeta_e2e_hardening.py`
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
- `tests/test_ux46e_proyeccion_salarial.py`
- `tests/test_ux46e_almacenamiento_comentarios_js.py`
- `tests/test_ux46e_auditoria_coherencia.py`
- `tests/test_ux46e_estandar_runtime.py`
- `tests/test_ux46e_preparacion_publica.py`
- `tests/test_ux46e_r8_reconsentimiento_borrado.py`
- `tests/test_ux46e_renumeracion_documental.py`
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
