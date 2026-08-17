# Índice de documentación

Este archivo es el punto de entrada para la documentación técnica, funcional y normativa del proyecto.

## 1. Lectura recomendada

1. [README principal](../README.md) — instalación, estado del proyecto y uso general.
2. [Especificación funcional](ESPECIFICACION_FUNCIONAL.md) — qué hace el asistente y qué requisitos cubre.
3. [Motor de cálculo](MOTOR_DE_CALCULO.md) — flujo de cálculo y reglas implementadas.
4. [Normativa](NORMATIVA.md) — cómo se versionan e interpretan los parámetros legales.
5. [Fuentes normativas](FUENTES_NORMATIVAS.md) — enlaces oficiales, leyes, artículos, reglamentos y resoluciones.
6. [Validación](VALIDACION.md) — pruebas automáticas y casos manuales de regresión.

## 2. Documentos por tema

| Documento | Propósito |
|---|---|
| [ARQUITECTURA.md](ARQUITECTURA.md) | Capas, módulos, endpoints, estado temporal y dependencias técnicas. |
| [DECISIONES.md](DECISIONES.md) | ADR consecutivos con decisiones técnicas y jurídicas de implementación. |
| [ESPECIFICACION_FUNCIONAL.md](ESPECIFICACION_FUNCIONAL.md) | Requisitos funcionales y flujo de los seis pasos. |
| [MODELO_DE_DATOS.md](MODELO_DE_DATOS.md) | Modelos Pydantic y estructuras de datos usadas por servicios y motores. |
| [MOTOR_DE_CALCULO.md](MOTOR_DE_CALCULO.md) | Algoritmos comunes y motores SEBD, Mixto y SUCGS. |
| [NORMATIVA.md](NORMATIVA.md) | Reglas de versionado normativo, parámetros y limitaciones. |
| [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md) | Catálogo de fuentes oficiales y mapa de artículos. |
| [MODALIDADES_SEBD.md](MODALIDADES_SEBD.md) | Modalidades del Subsistema Exclusivamente de Beneficio Definido. |
| [MODALIDADES_MIXTO.md](MODALIDADES_MIXTO.md) | Componentes y prestaciones del Subsistema Mixto. |
| [MODALIDADES_SUCGS.md](MODALIDADES_SUCGS.md) | Capas del Sistema Único de Capitalización con Garantía Solidaria. |
| [VALIDACION.md](VALIDACION.md) | Estrategia de pruebas, regresiones y casos sintéticos. |
| [SEGURIDAD_PRIVACIDAD.md](SEGURIDAD_PRIVACIDAD.md) | Modelo de privacidad local, validación de documentos, CI y límites de la beta. |
| [POLITICA_PRIVACIDAD.md](POLITICA_PRIVACIDAD.md) | Política pública de privacidad, finalidades, almacenamiento, derechos y exportaciones. |
| [TERMINOS_USO_PRIVACIDAD.md](TERMINOS_USO_PRIVACIDAD.md) | Condiciones de uso, tratamiento de datos y alcance no oficial de la herramienta. |
| [CUMPLIMIENTO_LEY_81.md](CUMPLIMIENTO_LEY_81.md) | Matriz técnica de alineación y pendientes pre-beta frente a Ley 81/Decreto 285. |
| [ROADMAP.md](ROADMAP.md) | Fases terminadas, cierre de 6F y trabajo posterior. |
| [GUIA_INTERNA_DESARROLLO.md](GUIA_INTERNA_DESARROLLO.md) | Convenciones internas de marca, terminología, tipografía y contenido no visible. |
| [UX_4_6A_REDISENO_VISUAL.md](UX_4_6A_REDISENO_VISUAL.md) | Cierre del rediseño visual integral, nueva página de Inicio y criterio de validación UX.4.6a. |
| [UX_4_6B_PASO1_DATOS_PERSONALES.md](UX_4_6B_PASO1_DATOS_PERSONALES.md) | Implementación y revisión del Paso 1, consentimiento, importación y navegación común. |
| [UX_4_6C_PASO2_CUOTAS.md](UX_4_6C_PASO2_CUOTAS.md) | Cierre del Paso 2, cuotas acreditadas, supuestos futuros e importación contextual. |
| [UX_4_6D_PASO3_HISTORIAL.md](UX_4_6D_PASO3_HISTORIAL.md) | Revisión del Paso 3, historial anual, Ficha Digital, detalle reciente y base salarial. |

## 3. Archivos normativos versionados

| Archivo | Contenido principal |
|---|---|
| [`normativa/parametros_generales.json`](../normativa/parametros_generales.json) | Edades de referencia y metadatos comunes. |
| [`normativa/sebd.json`](../normativa/sebd.json) | Parámetros SEBD, factores anticipados, máximos e indemnización. |
| [`normativa/mixto.json`](../normativa/mixto.json) | Componente BD, CAP, transición, devolución y garantías del Mixto. |
| [`normativa/sucgs.json`](../normativa/sucgs.json) | Tabla actuarial, capa solidaria y garantía de reemplazo SUCGS. |

## 4. Gobierno, versionado, colaboración y control de cambios

- [GOVERNANCE.md](../GOVERNANCE.md) — gobierno, responsabilidades, revisión y decisiones del proyecto.
- [VERSIONING.md](../VERSIONING.md) — política formal de versiones, fuente canónica y tags.
- [RELEASES.md](../RELEASES.md) — reconstrucción histórica y versiones formales desde GOV.1.2.
- [`VERSION`](../VERSION) — versión canónica de la aplicación.
- [CONTRIBUTING.md](../CONTRIBUTING.md) — reglas para cambios, pruebas, commits y normativa.
- [CHANGELOG.md](../CHANGELOG.md) — cambios acumulados para la próxima versión.
- [Casos de validación](../tests/casos_validacion/README.md) — reglas para almacenar pruebas anonimizadas.

## 5. Regla de mantenimiento

Cuando un cambio altere una fórmula, parámetro, flujo o fuente legal, no se debe actualizar documentación de forma indiscriminada. Deben modificarse únicamente los documentos afectados, conservando consistencia entre:

- código;
- `normativa/*.json`;
- pruebas;
- documentación técnica;
- fuentes oficiales.

## 6. Consulta desde la interfaz

La aplicación expone `/metodologia` como versión navegable de la metodología y de las principales fuentes oficiales para el Asegurado(a). Los detalles de estructura del repositorio y mantenimiento permanecen exclusivamente en esta documentación técnica.

## Consentimiento y privacidad UX.4.6b R4

- [Términos de uso, privacidad y tratamiento de datos](TERMINOS_USO_PRIVACIDAD.md)
- [Política de privacidad](POLITICA_PRIVACIDAD.md)
- [Matriz interna de alineación con Ley 81](CUMPLIMIENTO_LEY_81.md)
- [UX.4.6b — Paso 1](UX_4_6B_PASO1_DATOS_PERSONALES.md)

## UX.4.6c — Paso 2

- [UX.4.6c — Simular / Paso 2 · Cuotas](UX_4_6C_PASO2_CUOTAS.md)

## UX.4.6d — Paso 3

- [UX.4.6d — Simular / Paso 3 · Historial](UX_4_6D_PASO3_HISTORIAL.md) — cerrada tras R23; integración Pasos 1–3 validada y suite final de 396 pruebas en OK

- [Gestión de datos de la simulación](GESTION_DATOS_SIMULACION.md) — limpieza por paso, reinicio completo y borrado local integral

### R15 de UX.4.6d

La documentación de Paso 1, Paso 2, arquitectura, privacidad y validación incorpora el contrato visual de campos bloqueados, terminología documental neutral y limpieza semántica de cotización futura.

### R16 de UX.4.6d

- Revalidación silenciosa de cuotas cuando Paso 3 solo perdió un resultado derivado.
- Restauración al último paso realmente accesible.
- Ficha Digital integrada dentro de Detalle salarial del año actual y antes de su tabla mensual.


- **UX.4.6d R17:** auditoría de trazabilidad documental en Pasos 1–3: checkboxes bloqueados vs. seleccionados, cuotas acreditadas vs. proyectadas, advertencias de coherencia del comprobante y procedencia de campos editados. Véase `UX_4_6D_PASO3_HISTORIAL.md`, `DECISIONES.md` (ADR-136 a ADR-140) y `VALIDACION.md`.

### Actualización UX.4.6d R18
- `UX_4_6D_PASO3_HISTORIAL.md`: procedencia transversal y persistencia visual de importaciones.
- `GESTION_DATOS_SIMULACION.md`: alcance de `nombre_archivo_origen` en estado local.
- `SEGURIDAD_PRIVACIDAD.md` / `POLITICA_PRIVACIDAD.md`: aclaración de que el nombre del documento puede persistir temporalmente, pero no el archivo.

- **Fecha de referencia y vigencia de Ficha Digital:** `ARQUITECTURA.md` (UX.4.6d R21), `SEGURIDAD_PRIVACIDAD.md`, `UX_4_6D_PASO3_HISTORIAL.md`.

- **UX.4.6d R22:** cierre robusto del Paso 3, reconciliación de cuotas y mensajes de validación accionables. Véanse `DECISIONES.md` ADR-152 a ADR-154, `ESPECIFICACION_FUNCIONAL.md` RF-328 a RF-331 y `UX_4_6D_PASO3_HISTORIAL.md`.


- **UX.4.6d R23:** Ficha Digital más reciente puede ampliar la referencia de cuotas del año actual sin navegación regresiva; nunca la reduce silenciosamente. Véanse `DECISIONES.md` ADR-155–156, `ESPECIFICACION_FUNCIONAL.md` RF-332–336 y `UX_4_6D_PASO3_HISTORIAL.md`.

## Próximas revisiones UX.4.6

- **UX.4.6e — Paso 4 · Proyección salarial/laboral** — siguiente fase recomendada.
- **UX.4.6f — Paso 5 · Escenarios de retiro** — posterior a UX.4.6e.
- **UX.4.6g — Paso 6 · Resultados/exportación** — cierre de resultados y exportación orientativa.
