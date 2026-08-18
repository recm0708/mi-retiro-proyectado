# Licencia y estrategia de distribución

**Estado:** Vigente — GOV.1.7
**Versión de aplicación revisada:** `0.0.23-beta`
**Fecha:** 2026-08-18
**Clasificación:** Gobierno / Licencia / Distribución
**Revisión jurídica externa:** Pendiente antes de publicación pública/comercial

## 1. Objetivo evaluado

El proyecto contempla una beta futura, pero no existe una decisión expresa del titular de convertir el código en open source, autorizar uso comercial por terceros, permitir redistribución sin control o exigir copyleft. GOV.1.7 adopta una opción conservadora que no añade una concesión amplia de derechos en esta etapa.

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

Se adopta para la etapa pre-beta una **licencia propietaria / todos los derechos reservados** sobre materiales originales. Se añaden `LICENSE` y `THIRD_PARTY_NOTICES.md`.

La decisión es deliberadamente conservadora y puede revisarse para versiones futuras si el titular decide abrir el proyecto y dispone de los derechos necesarios.

## 4. Terceros

`LICENSE` no relicencia dependencias Python, Bootstrap, GitHub Actions, marcas, textos legales oficiales, servicios o materiales de terceros. Consultar `THIRD_PARTY_NOTICES.md`.

## 5. Compatibilidad de dependencias

Las dependencias directas actualmente documentadas usan licencias MIT, BSD-3-Clause o Apache-2.0. El proyecto puede mantener condiciones distintas sobre su material original siempre que cumpla las obligaciones upstream de componentes que use o redistribuya. Esta conclusión de ingeniería/documentación **no sustituye una revisión jurídica externa**.

## 6. Empaquetado

Un instalador, ejecutable autocontenido o contenedor futuro debe generar un inventario real de componentes y adjuntar licencias/NOTICE exigidos antes de publicarse.

## 7. Contribuciones futuras

Antes de aceptar contribuciones externas materiales debe definirse cómo se gestionan copyright y permisos de integración/relicencia. No se presume una cesión de derechos por abrir un Pull Request.

## 8. Cambio futuro de licencia

El titular puede adoptar condiciones distintas para versiones futuras o materiales sobre los que conserve derechos suficientes. Una concesión open source ya otorgada sobre una versión no debe tratarse retroactivamente como si nunca hubiera existido.

## 9. Referencias de decisión

- GitHub Docs — Licensing a repository.
- Choose a License — MIT, Apache-2.0 y catálogo de licencias/copyleft.

Estas referencias ayudan a comparar modelos de licencia; la revisión jurídica profesional continúa como gate antes de publicación pública/comercial.
