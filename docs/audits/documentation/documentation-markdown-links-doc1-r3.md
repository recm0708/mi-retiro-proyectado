# Auditoría de referencias navegables Markdown — DOC.1 R3

**Estado:** aceptado
**Versión de aplicación revisada:** `0.1.12.07-beta`
**Bloque:** DOC.1 R3
**Candidato revision-aware:** G113/E03 — `0.1.13.03-beta`
**Clasificación:** auditoría / documentación
**Fecha:** 2026-08-26

## 1. Objetivo

Revisar la presentación y navegabilidad de referencias a documentos y archivos
técnicos sin convertir mecánicamente cada ruta textual del repositorio en un
hipervínculo.

DOC.1 R3 parte del snapshot G112/E07 limpio y mantiene sin cambios `VERSION` y
el ledger hasta la promoción post-merge.

## 2. Línea base

La línea base contiene **145 archivos Markdown rastreados** y una suite local de
**1086 pruebas en `OK`** antes de aplicar el candidato.

La auditoría segura inicial inventarió referencias exactas sin resolver nombres
sueltos, sin modificar HTML y sin inspeccionar bloques de código.

La segunda clasificación contextual revisó **1326 referencias** y las distribuyó
así:

- `APLICABLE_R1`: **11**;
- `PRESERVAR`: **745**;
- `PRESERVAR_CONTEXTO`: **2**;
- `REVISAR_ANCLA`: **364**;
- `REVISAR_CONTEXTO`: **168**;
- `REVISAR_TABLA`: **36**.

Además, **1039 referencias** presentaron alguna relación con literales existentes
en módulos de prueba y, por tanto, no se consideraron aptas para transformación
masiva.

## 3. Decisión de alcance

La revisión aplica únicamente **11 cambios inequívocos**:

- **8 rutas técnicas** situadas en inventarios vigentes de arquitectura/modelos;
  la ruta técnica permanece visible y se vuelve clicable;
- **3 enlaces documentales** ya existentes en el marco normativo; la etiqueta
  visible cambia desde el nombre de archivo hacia el título humano del documento.

No se hace resolución por `basename` ni se infiere el destino de nombres
ambiguos.

## 4. Superficies preservadas

Se preservan deliberadamente:

- `docs/archive/`;
- `docs/audits/` previos;
- entradas históricas de `CHANGELOG.md`;
- cierres y evidencia histórica contenidos en `docs/operations/validation.md`;
- rutas usadas como dato contractual en matrices de trazabilidad;
- bloques de código;
- HTML embebido y atributos HTML;
- literales cuya forma está protegida por regresiones existentes.

Esta decisión evita que una mejora de presentación altere trazabilidad,
contratos, pruebas históricas o evidencia de estados anteriores.

## 5. Política permanente

`docs/standards/documentation-standards.md` diferencia desde esta revisión entre
una referencia cuyo propósito es navegar y una ruta cuyo propósito es registrar
un dato técnico o histórico.

Los documentos enlazados deben usar etiquetas humanas; los archivos técnicos
pueden conservar su ruta como etiqueta visible. En ambos casos se prefieren
destinos relativos dentro del repositorio.

## 6. Archivos funcionalmente modificados

- `docs/architecture/data-model.md`;
- `docs/architecture/system-architecture.md`;
- `docs/regulatory/regulatory-framework.md`;
- `docs/standards/documentation-standards.md`.

La evidencia y las regresiones del propio candidato se agregan sin modificar
runtime, motores previsionales, normativa versionada, `VERSION` ni ledger.

## 7. Criterio de cierre

Antes de confirmar DOC.1 R3 debe superar:

- `pip check`;
- auditor Markdown;
- auditor de identificadores;
- contrato revision-aware;
- compilación Python;
- sintaxis JavaScript;
- suite completa;
- `git diff --check`;
- gate pre-commit sobre staging;
- CI remota del Pull Request.

G113/E03 solo se materializa mediante la promoción post-merge correspondiente.

## 8. Resultado de aceptación

DOC.1 R3 fue integrado mediante PR #92 y squash merge `40ae5c067923699ac8be0c8a3baa79ae6ad5d3d0`. La revalidación post-merge cerró con **1092 pruebas en `OK`**, Markdown **146/146**, `pip check`, auditor de identificadores y `git diff --check` limpios. Los checks remotos requeridos `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` quedaron en `success`; Markdown Audit también quedó en `success`.

La promoción formal materializa G113/E03 (`0.1.13.03-beta`) y reserva G114/E01 (`0.1.14.01-beta`) para PERSIST.1. La versión `0.1.12.07-beta` declarada al inicio de esta auditoría se conserva como baseline histórico del candidato.
