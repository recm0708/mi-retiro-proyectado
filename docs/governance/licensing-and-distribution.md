# Licencia y estrategia de distribución

**Estado:** Vigente — GOV.1.7
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Fecha de decisión original:** 2026-08-18
**Última revisión documental:** PLAN.1 R3B1 — 2026-08-20
**Clasificación:** Gobierno / Licencia / Distribución
**Revisión jurídica externa:** Pendiente antes de una distribución oficial/comercial o de una eventual relicencia

## 1. Objetivo evaluado

El proyecto se encuentra actualmente en **etapa beta** y su repositorio de código es público. Esa visibilidad no convierte el código en open source ni concede por sí sola derechos de uso, copia, modificación, redistribución o explotación comercial.

No existe una decisión expresa del titular de convertir el proyecto en open source, autorizar uso comercial por terceros, permitir redistribución sin control o exigir copyleft. GOV.1.7 adoptó una opción conservadora que sigue vigente durante la etapa beta.

## 2. Alternativas revisadas

### MIT

Licencia open source permisiva que permite uso comercial, distribución, modificación y uso privado, condicionada principalmente a conservar avisos.

### Apache-2.0

Licencia open source permisiva que también permite uso comercial, distribución y modificación e incorpora una concesión expresa de patentes de contribuidores y obligaciones de avisos/cambios.

### GPL-3.0 / AGPL-3.0

Licencias copyleft fuertes. GPL condiciona redistribución a compartir código bajo la misma licencia; AGPL añade obligaciones relacionadas con versiones modificadas usadas para prestar servicios por red.

### Propietaria / todos los derechos reservados

Preserva el control del titular y no concede públicamente derechos de copia, modificación, redistribución, sublicencia o explotación comercial.

## 3. Decisión GOV.1.7

GOV.1.7 adoptó, durante la etapa entonces denominada pre-beta, una **licencia propietaria / todos los derechos reservados** sobre materiales originales y añadió `LICENSE` y `THIRD_PARTY_NOTICES.md`.

PLAN.1 no cambia esa decisión de licencia. La aplicación permanece
en etapa beta; las publicaciones nuevas utilizan actualmente la familia
revision-aware `0.GG.RR.EE-beta`, mientras `0.0.N-beta` se conserva como
familia legacy histórica. La licencia propietaria continúa vigente hasta que
exista una decisión expresa diferente.

La decisión puede revisarse para versiones futuras si el titular decide abrir el proyecto y dispone de los derechos necesarios.

## 4. Terceros

`LICENSE` no relicencia dependencias Python, Bootstrap, GitHub Actions, marcas, textos legales oficiales, servicios o materiales de terceros. Consultar `THIRD_PARTY_NOTICES.md`.

## 5. Compatibilidad de dependencias

Las dependencias directas actualmente documentadas usan licencias MIT, BSD-3-Clause o Apache-2.0. El proyecto puede mantener condiciones distintas sobre su material original siempre que cumpla las obligaciones upstream de componentes que use o redistribuya.

Esta conclusión de ingeniería/documentación **no sustituye una revisión jurídica externa**.

## 6. Empaquetado

Un instalador, ejecutable autocontenido, contenedor o ZIP oficial debe generar un inventario real de componentes y adjuntar licencias/NOTICE exigidos antes de distribuirse.

REL.1 deberá relacionar el inventario real del artefacto con `VERSION`, Build, tag, hashes y avisos de terceros.

## 7. Contribuciones futuras

Antes de aceptar contribuciones externas materiales debe definirse cómo se gestionan copyright y permisos de integración/relicencia. No se presume una cesión de derechos por abrir un Pull Request.

## 8. Cambio futuro de licencia

El titular puede adoptar condiciones distintas para versiones futuras o materiales sobre los que conserve derechos suficientes.

Una concesión open source ya otorgada sobre una versión no debe tratarse retroactivamente como si nunca hubiera existido.

## 9. Referencias de decisión

- GitHub Docs — Licensing a repository.
- Choose a License — MIT, Apache-2.0 y catálogo de licencias/copyleft.

Estas referencias ayudan a comparar modelos de licencia. La revisión jurídica profesional continúa como gate antes de una eventual relicencia o de una distribución oficial/comercial que requiera validación jurídica adicional.
