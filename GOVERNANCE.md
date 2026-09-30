# Gobierno del proyecto

**Estado:** vigente
**Mantenedor:** Rubén Enrique Cañizares Miranda (`@recm0708`)

## Propósito

Este documento define cómo se gobierna Mi Retiro Proyectado: quién mantiene el
repositorio, cómo se adoptan decisiones, qué controles deben cumplirse y cómo se
integra trabajo a la rama principal.

La historia de fases, promociones y publicaciones no se mantiene aquí. Se
conserva en Git, Issues, Pull Requests, ADR, auditorías, `CHANGELOG.md`,
`RELEASES.md` y los registros específicamente históricos.

## Autoridades relacionadas

- [Política de versionado](VERSIONING.md) — numeración, aceptación y tags.
- [Proceso de release](docs/operations/release-process.md) — publicación y
  validación de Releases.
- [Gobierno de Issues y Pull Requests](docs/governance/github-issues-pr-governance.md)
  — flujo operativo de trabajo, checkpoints y revisión.
- [Estándares del repositorio](docs/standards/README.md) — estructura,
  nomenclatura, documentación y ciclo de vida.
- [Registro de decisiones](docs/decisions/README.md) — ADR.
- [Política de seguridad](SECURITY.md) — reporte de vulnerabilidades.

Cuando una autoridad especializada define un contrato con mayor detalle, este
documento no lo duplica.

## Mantenimiento y ownership

El mantenedor principal y responsable de revisión es **Rubén Enrique Cañizares
Miranda** (`@recm0708`).

`.github/CODEOWNERS` materializa el ownership técnico. CODEOWNERS no constituye
certificación jurídica ni aprobación de la Caja de Seguro Social de Panamá.

Mientras exista un único mantenedor, las áreas especialmente críticas son:

- `regulations/`;
- `app/engines/`;
- `app/core/`;
- documentación normativa, de seguridad y privacidad;
- `.github/`;
- `VERSION` y artefactos de versionado/publicación.

Si se incorporan nuevos mantenedores, CODEOWNERS debe granularizar las
responsabilidades sin crear ownership implícito o informal.

## Principios de gobierno

1. **Trazabilidad:** un cambio relevante debe poder rastrearse desde Git hasta
   su Issue, código, pruebas, documentación y evidencia aplicable.
2. **Separación normativa:** una decisión técnica no se presenta como requisito
   jurídico sin fuente oficial.
3. **Transparencia:** no se introducen comportamientos deliberadamente ocultos
   al modelo documental y de auditoría.
4. **Privacidad por defecto:** pruebas y observabilidad no justifican almacenar
   datos personales reales innecesarios.
5. **Reproducibilidad:** una afirmación técnica importante debe poder
   verificarse mediante código, prueba, fuente o procedimiento documentado.
6. **Historia íntegra:** una decisión sustituida permanece en su autoridad
   histórica; la documentación viva no la copia para aparentar continuidad.
7. **Independencia institucional:** el proyecto no se presenta como producto
   oficial de la CSS.
8. **Sincronización transversal:** cuando cambia un contrato compartido se
   revisan sus consumidores de código, pruebas, interfaz, normativa,
   documentación y release.
9. **Trabajo verificable:** las Issues materiales mantienen checklist,
   evidencia y criterio de cierre.

## Decisiones

Las decisiones técnicas o arquitectónicas relevantes se documentan mediante ADR
con numeración consecutiva en
[Registro de decisiones](docs/decisions/README.md).

Una decisión puede quedar vigente, sustituida parcialmente, sustituida o
rechazada. Las decisiones anteriores no se eliminan para hacer coincidir la
historia con el criterio actual.

## Ciclo de vida de Issues y fases

Toda Issue material debe contener un checklist Markdown verificable que cubra,
cuando aplique:

- dependencias y condiciones de entrada;
- trabajo principal;
- pruebas y gates;
- documentación y trazabilidad;
- remanentes o Issues derivadas;
- criterio de cierre.

Una casilla solo se marca como completada cuando exista evidencia suficiente.
Si aparece trabajo fuera de alcance, debe transferirse a una Issue o owner
explícito antes del cierre.

### Gate de apertura de fase

Al iniciar una fase o revisión material en un chat nuevo, primero se presenta un
briefing de alcance. Como mínimo debe explicar:

- objetivo y problema que resuelve;
- alcance incluido y exclusiones;
- baseline, dependencias e Issues relacionadas;
- orden de trabajo y checkpoints;
- validaciones previstas;
- riesgos y posibles efectos colaterales;
- recomendaciones adicionales que convenga incorporar;
- reparto de trabajo remoto/local;
- posible impacto de versionado/publicación;
- criterio de cierre.

La ejecución material comienza únicamente después de la aprobación explícita
del operador. Las verificaciones de solo lectura necesarias para confirmar el
estado real pueden realizarse antes de esa aprobación.

## Tipos de cambio

### Funcionalidad y UX

Requieren implementación, regresiones razonables, validación manual cuando el
comportamiento sea visual/interactivo y actualización de las autoridades
documentales afectadas.

### Motores y normativa

Un cambio de fórmula, parámetro, fecha, tabla o interpretación previsional
requiere fuente oficial identificable, pruebas, actualización de
`regulations/` cuando corresponda, documentación técnica/normativa y ADR si
existe una decisión no trivial.

### Seguridad, privacidad y observabilidad

Debe revisarse el tratamiento de datos, retención, exposición, logs, mensajes
de error, terceros, documentación pública y regresiones de seguridad.

### Gobierno, documentación y releases

Los cambios de gobierno, versionado, licencia, CI, estructura documental o
publicación deben quedar respaldados por una autoridad canónica y no depender
de convenciones orales o texto duplicado.

## Integración a `main`

El flujo ordinario es:

1. Issue/alcance aprobado;
2. rama de trabajo;
3. cambios y validación local;
4. commit firmado;
5. push de la rama;
6. Pull Request;
7. checks requeridos y revisión;
8. `Squash and merge` cuando el candidato sea aceptable.

No se usa push directo ordinario a `main`.

Los commits canónicos nuevos deben incorporar firma criptográfica SSH. Antes de
publicar una rama se verifica, como mínimo:

```powershell
git verify-commit HEAD
git log --show-signature -1
```

La rama principal está protegida por reglas remotas. Los required checks
canónicos son `Repository Quality Gate` y `Python Compatibility`; otros
controles, como Dependency Security, Visual & Accessibility y CodeQL, se
ejecutan según su contrato y alcance.

Los tags formales `v*` son inmutables una vez publicados. La creación de un
tag o Release no se utiliza como mecanismo para corregir un árbol todavía no
aceptado.

## Versionado y publicación

`VERSION` es la fuente canónica de la versión de aplicación.

La política de numeración y el criterio para consumir Global/Edition/Correction
se mantienen exclusivamente en [Política de versionado](VERSIONING.md). La
publicación de tags y GitHub Releases se rige por
[Proceso de release](docs/operations/release-process.md).

Una fase planificada no recibe Global, Edition o `VERSION` por anticipado. La
materialización ocurre cuando existe un estado real, validado y aceptable bajo
el contrato de versionado.

## Seguridad e incidentes

Las vulnerabilidades explotables, credenciales, datos personales y evidencia
sensible no se publican en Issues. Se sigue
[Política de seguridad](SECURITY.md) y, para incidentes,
[Procedimiento de respuesta](docs/security/security-incident-procedure.md).

Dependabot, CodeQL, secret scanning y otros controles automatizados reducen
riesgo, pero no sustituyen revisión humana ni pruebas de regresión.

## Licencia

Los materiales originales se mantienen bajo la licencia definida en
[`LICENSE`](LICENSE). Los componentes de terceros conservan sus propias
licencias y avisos, documentados en [Avisos de terceros](THIRD_PARTY_NOTICES.md).

Cualquier relicencia futura requiere una decisión expresa y derechos suficientes
sobre las contribuciones incorporadas.

## Cambios a este documento

Una modificación sustancial de gobierno debe:

1. tener Issue o decisión rastreable;
2. explicar el motivo;
3. actualizar autoridades relacionadas;
4. ajustar guardas o plantillas que implementen la regla;
5. conservar la historia en Git o en su autoridad histórica, no mediante
   cronologías incrustadas en esta política.
