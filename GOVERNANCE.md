# Gobierno del proyecto

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2
**Fecha:** 2026-08-17

## 1. Propósito

Este documento define quién mantiene el proyecto, cómo se adoptan decisiones y qué controles mínimos deben cumplirse antes de integrar cambios. Su finalidad es facilitar mantenimiento, revisión independiente y auditoría.

## 2. Mantenimiento actual

El mantenedor y responsable de revisión actual del repositorio es:

- **Rubén Enrique Cañizares Miranda** (`@recm0708`).

`.github/CODEOWNERS` refleja esta responsabilidad técnica. CODEOWNERS no constituye una certificación jurídica ni una aprobación de la Caja de Seguro Social de Panamá.

## 3. Principios de gobierno

1. **Trazabilidad:** todo cambio relevante debe poder rastrearse desde Git hasta código, pruebas y documentación.
2. **Separación normativa:** las decisiones técnicas no deben presentarse como requisitos legales sin una fuente oficial.
3. **Transparencia:** no se introducen comportamientos deliberadamente ocultos al modelo documental y de auditoría del proyecto.
4. **Privacidad por defecto:** observabilidad y pruebas no justifican almacenar datos personales reales innecesarios.
5. **Reproducibilidad:** una afirmación técnica importante debe poder verificarse mediante código, prueba, fuente o procedimiento documentado.
6. **Historia preservada:** una decisión sustituida se marca como tal; no se elimina para aparentar que nunca existió.
7. **Independencia institucional:** el proyecto no debe presentarse como producto oficial de la CSS.

## 4. Tipos de cambio

### 4.1. Funcionalidad y UX

Requieren:

- implementación;
- regresiones automatizadas cuando sean razonables;
- validación manual cuando el comportamiento sea visual o interactivo;
- actualización de documentación dependiente.

### 4.2. Motores y normativa

Todo cambio de fórmula, parámetro, fecha, tabla o interpretación previsional requiere:

- fuente oficial identificable;
- prueba de regresión;
- actualización de `normativa/` cuando corresponda;
- documentación técnica/normativa;
- ADR cuando exista interpretación o decisión no trivial.

### 4.3. Seguridad, privacidad y observabilidad

Requieren revisión de:

- datos tratados;
- datos registrados;
- retención;
- exposición externa;
- mensajes de error;
- documentación pública y técnica;
- pruebas de no regresión.

### 4.4. Gobierno y releases

Cambios en versionado, licencia, gobernanza, CI o proceso de publicación deben quedar documentados y no pueden depender únicamente de una convención oral.

## 5. Decisiones

Las decisiones relevantes se documentan mediante ADR consecutivos en `docs/DECISIONES.md`.

Un ADR puede estar:

- vigente;
- sustituido parcialmente;
- sustituido;
- rechazado, cuando resulte útil conservar la alternativa evaluada.

Una decisión antigua no se borra solo porque una revisión posterior cambie el criterio.

## 6. Integración a `main`

Antes de integrar un hito cerrado se exige, como mínimo:

```powershell
python -m compileall app
python -m unittest discover -s tests -q
git diff --check
```

Para JavaScript modificado se valida además `node --check`.

Desde la migración criptográfica del 2026-08-17, todo commit nuevo debe incorporar **firma criptográfica SSH**. Antes del push se verifica con:

```powershell
git verify-commit HEAD
git log --show-signature -1
```

La CI remota debe permanecer en verde. La protección de `main` y los rulesets de tags se activarán después de completar la migración histórica.

## 7. Versiones y tags

La política aplicable está en `VERSIONING.md`.

- `VERSION` es la fuente canónica.
- Los tags formales empiezan con `v`.
- `0.0.1-beta` a `0.0.21-beta` fueron reconstruidas documentalmente y pueden materializarse posteriormente como tags retrospectivos firmados sin aparentar existencia histórica.
- `v0.0.22-beta` y `v0.0.23-beta` pueden reemitirse una sola vez como objetos firmados sin cambiar sus commits objetivo.
- Después de la migración, todo commit nuevo y todo tag nuevo deben estar firmados.
- La clave privada nunca se versiona.

## 8. Propiedad y revisión de áreas críticas

Mientras exista un único mantenedor, `@recm0708` revisa todo el repositorio. Se consideran especialmente críticas:

- `normativa/`;
- `app/motores/`;
- `app/core/`;
- documentación de seguridad, privacidad, normativa y auditoría;
- `.github/`;
- archivos de versionado y publicación.

Cuando existan nuevos mantenedores, CODEOWNERS deberá granularizar estas responsabilidades.

## 9. Licencia

**Pendiente en GOV.1.7.**

La ausencia temporal de `LICENSE` es deliberada mientras se revisan alcance de distribución, derechos de reutilización y compatibilidad con dependencias. La visibilidad o posibilidad de auditoría del código no debe interpretarse automáticamente como permiso de reutilización.

## 10. Incidentes y vulnerabilidades

La política pública de reporte se formalizará en `SECURITY.md` durante GOV.1.5/GOV.1.6. Hasta entonces no se deben publicar credenciales, datos personales reales o detalles explotables en ejemplos de documentación.

## 11. Cambios a este documento

Toda modificación sustancial de gobierno debe:

- quedar registrada en Git;
- explicar su motivo;
- actualizar documentos relacionados;
- respetar el historial anterior.
