# Documentación de Mi Retiro Proyectado

## Propósito

Este índice organiza la documentación versionada y define **dónde se encuentra
la autoridad canónica de cada tema**. Su función es facilitar navegación y
evitar que un mismo contrato se mantenga en varios documentos con estados
distintos.

La documentación viva describe el estado y las reglas vigentes. Git, tags,
Releases, auditorías, ADR, registros acumulativos y `docs/archive/` conservan
la historia cuando esa historia forma parte legítima de su función.

## Mapa de autoridades

| Tema | Autoridad principal | Complementos |
| --- | --- | --- |
| Presentación general del proyecto | [README raíz](../README.md) | [Soporte](../SUPPORT.md) |
| Comportamiento funcional | [Especificación funcional](product/functional-specification.md) | [Limitaciones conocidas](product/known-limitations.md), [Transparencia](product/transparency.md) |
| Explicación de resultados y cálculo | [Guía de cálculo](product/calculation-guide.md) | [Motor de cálculo](architecture/calculation-engine.md) |
| Arquitectura | [Arquitectura del sistema](architecture/system-architecture.md) | [Modelo de datos](architecture/data-model.md), [Centro de desarrollo](architecture/development-center.md) |
| Marco previsional | [Marco normativo](regulatory/regulatory-framework.md) | [Fuentes regulatorias](regulatory/regulatory-sources.md) |
| SEBD | [Modalidades SEBD](regulatory/sebd-modalities.md) | [Fuentes regulatorias](regulatory/regulatory-sources.md) |
| Subsistema Mixto | [Modalidades Mixto](regulatory/mixto-modalities.md) | [Fuentes regulatorias](regulatory/regulatory-sources.md) |
| SUCGS | [Modalidades SUCGS](regulatory/sucgs-modalities.md) | [Fuentes regulatorias](regulatory/regulatory-sources.md) |
| Privacidad y seguridad técnica | [Seguridad y privacidad](security/security-and-privacy.md) | [Política de privacidad](security/privacy-policy.md), [Modelo de amenazas](security/threat-model.md) |
| Desarrollo local | [Guía de desarrollo](operations/development-guide.md) | [Validación](operations/validation.md) |
| Observabilidad | [Observabilidad y logs](operations/observability-and-logs.md) | [Centro de desarrollo](architecture/development-center.md) |
| Dependencias de terceros | [Dependencias de terceros](operations/third-party-dependencies.md) | [Avisos de terceros](../THIRD_PARTY_NOTICES.md) |
| Releases | [Proceso de release](operations/release-process.md) | [Releases](../RELEASES.md), [Changelog](../CHANGELOG.md) |
| Gobierno del proyecto | [Gobierno](../GOVERNANCE.md) | [Gobierno de Issues y PR](governance/github-issues-pr-governance.md) |
| Versionado | [Política de versionado](../VERSIONING.md) | [Ledger pre-1.0](governance/pre-1-0-revision-ledger.md) y su representación machine-readable |
| Planificación hacia 1.0 | [Plan maestro](governance/master-plan-to-1-0.md) | [Roadmap](governance/roadmap.md), [Matriz de pendientes](governance/pre-1-0-pending-matrix.md) |
| Estructura del repositorio | [Estructura del repositorio](standards/repository-structure.md) | [Política estructural](governance/repository-structure-policy.md) |
| Estándares | [Índice de estándares](standards/README.md) | Documentos específicos dentro de `standards/` |
| Decisiones técnicas | [Registro de decisiones](decisions/README.md) | ADR individuales cuando existan |
| Auditorías | [Índice de auditorías](audits/README.md) | `audits/documentation/`, `audits/governance/`, `audits/repository/`, `audits/security/` |
| Historia preservada | [Índice del archivo](archive/README.md) | Subíndices de `archive/` |
| Plantillas | [Índice de plantillas](templates/README.md) | `templates/documentation/`, `templates/file-structure/` |

Cuando dos documentos parecen competir por el mismo tema, debe resolverse la
duplicación asignando una autoridad principal y haciendo que los demás
referencien ese contrato en vez de copiarlo.

## Áreas documentales

### Producto

`product/` explica comportamiento, alcance y comunicación de resultados:

- [Especificación funcional](product/functional-specification.md);
- [Guía de cálculo](product/calculation-guide.md);
- [Limitaciones conocidas](product/known-limitations.md);
- [Gestión de datos de simulación](product/simulation-data-management.md);
- [Matriz de trazabilidad](product/traceability-matrix.md);
- [Transparencia](product/transparency.md);
- [Identidad visual](product/visual-identity.md).

### Arquitectura

`architecture/` documenta contratos técnicos internos:

- [Arquitectura del sistema](architecture/system-architecture.md);
- [Modelo de datos](architecture/data-model.md);
- [Motor de cálculo](architecture/calculation-engine.md);
- [Centro de desarrollo](architecture/development-center.md).

### Normativa

`regulatory/` conserva el marco normativo y las fuentes aplicadas:

- [Marco normativo](regulatory/regulatory-framework.md);
- [Fuentes regulatorias](regulatory/regulatory-sources.md);
- [Alineación con Ley 81](regulatory/law-81-compliance.md);
- [Modalidades SEBD](regulatory/sebd-modalities.md);
- [Modalidades Mixto](regulatory/mixto-modalities.md);
- [Modalidades SUCGS](regulatory/sucgs-modalities.md);
- [Fuentes oficiales preservadas](regulatory/sources/official/README.md).

Las copias oficiales conservadas bajo `regulatory/sources/official/` son
evidencia de procedencia; su existencia no reemplaza la necesidad de identificar
la fuente oficial y su fecha de consulta.

### Seguridad y privacidad

`security/` contiene políticas técnicas, procedimientos y evaluaciones:

- [Seguridad y privacidad](security/security-and-privacy.md);
- [Política de privacidad](security/privacy-policy.md);
- [Términos de uso y privacidad](security/terms-and-privacy.md);
- [Modelo de amenazas](security/threat-model.md);
- [Procedimiento de derechos del titular](security/data-subject-rights-procedure.md);
- [Procedimiento de incidentes](security/security-incident-procedure.md);
- [Evaluación de terceros y despliegue](security/third-party-deployment-assessment.md).

La política pública para reportar vulnerabilidades se mantiene en
[`SECURITY.md`](../SECURITY.md).

### Operaciones

`operations/` contiene el contrato operativo del proyecto:

- [Guía de desarrollo](operations/development-guide.md);
- [Validación](operations/validation.md);
- [Observabilidad y logs](operations/observability-and-logs.md);
- [Proceso de release](operations/release-process.md);
- [Dependencias de terceros](operations/third-party-dependencies.md);
- [Preparación del repositorio público](operations/github-public-repository.md).

### Gobierno y planificación

`governance/` concentra contratos de gobierno que no pertenecen a la raíz:

- [Plan maestro hacia 1.0](governance/master-plan-to-1-0.md);
- [Roadmap](governance/roadmap.md);
- [Matriz de pendientes pre-1.0](governance/pre-1-0-pending-matrix.md);
- [Ledger de revisiones pre-1.0](governance/pre-1-0-revision-ledger.md);
- [Gobierno de Issues y Pull Requests](governance/github-issues-pr-governance.md);
- [Licencia y distribución](governance/licensing-and-distribution.md);
- [Política estructural](governance/repository-structure-policy.md).

Estos documentos tienen funciones distintas: el plan maestro define la
secuencia y dependencias; el roadmap comunica la ruta vigente; la matriz de
pendientes enumera trabajo no completado; el ledger registra estados aceptados.

### Estándares

`standards/` define las reglas canónicas de estructura, nombres, documentación
y ciclo de vida de artefactos. El punto de entrada es
[Índice de estándares](standards/README.md).

### Decisiones

`decisions/` contiene ADR y el registro vivo de decisiones técnicas. Las
decisiones históricas aceptadas no se reescriben para reflejar criterios
posteriores; cuando una decisión cambia se documenta la relación de sustitución.

### Auditorías

`audits/` conserva auditorías y evidencia versionable. Una auditoría puede
describir un estado anterior sin que ese estado deba copiarse a documentación
viva. Consulta [Índice de auditorías](audits/README.md).

### Archivo histórico

`archive/` conserva únicamente documentación cerrada que mantiene valor
independiente de trazabilidad o contexto. No es una segunda documentación viva
ni debe consultarse para conocer el estado actual. Consulta
[Índice del archivo](archive/README.md).

### Plantillas

`templates/` proporciona puntos de partida para documentación y estructuras de
archivo. Las plantillas no obligan a conservar secciones vacías ni a uniformar
documentos con funciones distintas.

## Clasificación y conservación de historia

La historia se conserva de acuerdo con la función del artefacto:

- **documentación viva:** describe el contrato o estado vigente;
- **estándar/política:** define reglas vigentes y excepciones explícitas;
- **auditoría/evidencia:** conserva el estado observado y el método usado;
- **ADR/decisión:** conserva la decisión en su contexto y su relación con
  decisiones posteriores;
- **registro vivo acumulativo:** mantiene historia solo cuando esa secuencia es
  parte inseparable del propio contrato;
- **archivo histórico:** preserva evidencia cerrada con valor independiente;
- **Git, tags y Releases:** conservan la evolución del árbol y las publicaciones.

Un documento vivo no necesita una sección histórica para demostrar que una fase
existió. Cuando el contexto histórico sea necesario se enlaza a la autoridad que
lo conserva.

## Reglas de mantenimiento

1. Cada documento debe tener una función identificable.
2. Una misma política o contrato vigente debe tener una sola autoridad principal.
3. Los documentos relacionados enlazan a la autoridad en lugar de copiarla.
4. Los README de cada área explican esa área; no son bitácoras de todas las fases
   que la modificaron.
5. Los enlaces de documentación viva deben resolver contra el árbol actual.
6. Los movimientos y renombres deben actualizar consumidores, índices y pruebas
   documentales relacionadas.
7. La evidencia histórica no se moderniza mecánicamente si hacerlo falsearía el
   estado que documenta.
8. Git conserva las versiones anteriores aunque un archivo deje de formar parte
   del árbol vigente.

Los estándares completos se encuentran en
[Estándares de documentación](standards/documentation-standards.md) y
[Política de Markdown](standards/markdown-style-and-lint.md).
