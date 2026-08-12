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
| [ROADMAP.md](ROADMAP.md) | Fases terminadas, cierre de 6F y trabajo posterior. |

## 3. Archivos normativos versionados

| Archivo | Contenido principal |
|---|---|
| [`normativa/parametros_generales.json`](../normativa/parametros_generales.json) | Edades de referencia y metadatos comunes. |
| [`normativa/sebd.json`](../normativa/sebd.json) | Parámetros SEBD, factores anticipados, máximos e indemnización. |
| [`normativa/mixto.json`](../normativa/mixto.json) | Componente BD, CAP, transición, devolución y garantías del Mixto. |
| [`normativa/sucgs.json`](../normativa/sucgs.json) | Tabla actuarial, capa solidaria y garantía de reemplazo SUCGS. |

## 4. Documentos de colaboración y control de cambios

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

La aplicación expone `/metodologia` como versión navegable de la metodología y de las principales fuentes oficiales. Para mantenimiento técnico y trazabilidad completa siguen siendo autoritativos los documentos de este directorio y `normativa/*.json`.
