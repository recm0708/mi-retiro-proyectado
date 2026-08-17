# Validación

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.22-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Clasificación:** Técnica / Calidad

La estrategia combina pruebas automatizadas, CI, casos sintéticos/anonimizados y validación manual cuando la propiedad no puede demostrarse de forma suficiente mediante código.

## 1. Línea base

Cierre validado de GOV.1.3 R1:

```text
Ran 411 tests
OK
```

GOV.1.3 R2 agregó **12 regresiones documentales/técnicas**. El cierre de R2 fue validado con una suite completa de **423 pruebas en `OK`**, incluidas **12/12 regresiones específicas de R2** y la confirmación adicional de **8/8 regresiones documentales de R1**.

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

Cuando se modifica únicamente documentación, la suite completa continúa ejecutándose porque las regresiones documentales pueden depender de contratos del código.

## 3. Inventario actual de pruebas

La lista se deriva de los archivos `tests/test_*.py` existentes al aplicar R2.

- `tests/test_accesibilidad_temas.py`
- `tests/test_accesibilidad_ux4.py`
- `tests/test_comparador.py`
- `tests/test_dinero.py`
- `tests/test_estabilizacion_visual.py`
- `tests/test_fuentes_normativas.py`
- `tests/test_gov12_versionado.py`
- `tests/test_gov13_documentacion.py`
- `tests/test_identidad_interfaz.py`
- `tests/test_indemnizacion_vejez.py`
- `tests/test_linea_tiempo.py`
- `tests/test_mantenimiento_tecnico.py`
- `tests/test_mixto.py`
- `tests/test_mixto_prestaciones_cap.py`
- `tests/test_prebeta_e2e_hardening.py`
- `tests/test_proyeccion_salarios.py`
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
- `tests/test_ux4_remate_visual.py`

## 4. Categorías

### Núcleo y servicios comunes

- dinero;
- proyección salarial;
- línea temporal;
- retiro;
- historial/detalle;
- fuentes normativas.

### Motores

- SEBD;
- modalidades;
- indemnización;
- Mixto/CAP;
- SUCGS/capa solidaria/reemplazo.

### Integración

- resultados por sistema;
- comparador;
- resultado unificado;
- trazabilidad;
- E2E pre-beta.

### UX y accesibilidad

- responsive;
- temas;
- accesibilidad;
- Pasos 1–3;
- importadores;
- gestión de datos;
- tablas/scrollbars.

### Gobierno

- versionado GOV.1.2;
- estructura documental GOV.1.3.

## 5. Casos personales

Los originales reales no se versionan.

Una regresión derivada de un caso personal debe reducirse a datos sintéticos o anonimizados suficientes para preservar la propiedad que se prueba.

Consultar `tests/casos_validacion/README.md`.

## 6. Regresión SEBD anonimizada

Existe una regresión histórica anonimizada que protege una combinación conocida de cuotas, mejores años y precisión monetaria.

Su finalidad es detectar cambios matemáticos; no convierte ese caso individual en parámetro de producción.

## 7. Casos sintéticos Mixto/SUCGS

Valores como saldos, bonos o divisores usados en pruebas pueden ser deliberadamente sintéticos.

Cada prueba debe distinguir un valor de prueba de un valor normativo oficial.

## 8. Importadores

Las pruebas de importación deben cubrir:

- formato válido/inválido;
- archivos vacíos;
- límites;
- cifrado;
- texto no extraíble;
- clasificación histórica/proyectada;
- año más reciente de Ficha;
- vigencia con fecha externa;
- procedencia y confirmación;
- ausencia de persistencia del PDF;
- reconciliación de cuotas.

Los fixtures no deben contener PII real.

## 9. Fecha de referencia

Las pruebas deben poder sustituir/mokear la consulta externa.

La suite no debe depender de disponibilidad real de CSS para terminar en verde.

Se verifica que no exista fallback silencioso al reloj local.

## 10. Gestión de datos

Validar:

- limpieza por paso;
- reinicio;
- borrado local;
- invalidación descendente;
- restauración del último paso accesible;
- persistencia de metadata sin `File`;
- resultados acreditados/proyectados.

## 11. Validación manual

Sigue siendo necesaria para:

- composición visual;
- temas;
- foco/teclado;
- scroll real;
- modales;
- mensajes y jerarquía;
- interacción con selectores de archivos;
- revisión integral multidispositivo.

Una prueba estructural HTML/CSS no equivale por sí sola a una auditoría de accesibilidad.

## 12. CI

`.github/workflows/ci.yml` valida instalaciones limpias con Python soportado por el proyecto y Node para sintaxis JavaScript.

La CI debe permanecer en verde antes de considerar cerrado un hito formal.

## 13. Documentación

Las regresiones GOV.1 comprueban, entre otros:

- versión canónica;
- existencia de documentos;
- estructura de changelog/roadmap;
- separación de histórico;
- endpoints documentados;
- modelos técnicos esenciales;
- ausencia de diarios UX en documentos vigentes;
- whitespace documental.

## 14. Evidencia histórica

Las matrices de revisión R1–R23 y los conteos intermedios anteriores se conservan en:

`docs/historico/tecnico/VALIDACION_PRE_GOV1_3_R2.md`

y en las bitácoras UX.

Este documento solo mantiene la estrategia y el estado de validación vigente.
