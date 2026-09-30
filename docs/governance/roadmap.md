# Roadmap

**Estado:** vigente
**Baseline publicado:** G129/E03/C0 — MANT.2 R3
**Versión publicada:** `0.129.3.0-beta`
**Fase material activa:** DOC.4 R1 / #171
**Siguiente Global aritmético:** G130, libre y sin candidato
**Objetivo estable:** `1.0.0.0`

## Propósito

Este roadmap presenta la **ruta vigente** hacia la primera versión oficial. No
funciona como historial de promociones ni como inventario detallado de todas las
Issues.

- El programa narrativo completo está en
  [Plan maestro hacia 1.0](master-plan-to-1-0.md).
- El trabajo pendiente exacto está en
  [Matriz maestra de pendientes](pre-1-0-pending-matrix.md).
- Los estados aceptados se conservan en
  [Ledger pre-1.0](pre-1-0-revision-ledger.md).

## Situación actual

G129/E03/C0 está integrado y publicado como `0.129.3.0-beta` sobre
`main@dca3871c3472e20074cf51d85d28eeeccb9b6f32`, con tag firmado
`v0.129.3.0-beta` y GitHub Release prerelease 399260564.

El preflight #166 posterior a esa publicación quedó CLEAN y habilitó
**DOC.4 R1/#171**, actualmente en ejecución.

DOC.4 trabaja sobre el baseline G129 sin reservar G130 ni modificar
`VERSION` hasta que exista un candidato material validado.

## Ruta vigente hacia `1.0.0.0`

```text
DOC.4 R1
→ auditoría previsional #142
→ [derivados funcionales obligatorios, si aparecen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7 → UX.x final necesario
→ gate UX/GOV #189 sin drift shared
→ SEC.2 R7
→ rendimiento #156
→ A11Y.2
→ REV.1
→ settings GitHub #153
→ DOC.1 R6
→ QA.1
→ REL.1
→ 1.0.0.0
```

El orden expresa dependencias reales. No supone Globals futuros.

## Frontera actual — DOC.4

DOC.4 reestructura el corpus documental/no ejecutable para que cada artefacto
tenga una autoridad y una función claras.

Subtrabajos internos:

- #172 — revisión Markdown 1:1;
- #173 — poda, movimientos, fusiones, renombres e índices;
- #174 — artefactos declarativos/textuales no ejecutables;
- #209 — rutas/nombres/entorno heredados;
- #215 — guardas que fuerzan historia dentro de documentación viva.

Esos subtrabajos no consumen Global propio.

Al cerrar DOC.4:

- el árbol documental debe representar el estado vigente;
- la historia legítima debe permanecer en sus autoridades históricas;
- se establece un nuevo baseline documental;
- la cadencia de DOC.3 reinicia desde ese baseline.

## Auditoría previsional antes de PERSIST.1

#142 debe contrastar cobertura real de SEBD, Subsistema Mixto y SUCGS,
modalidades y prestaciones.

Si descubre una carencia obligatoria para 1.0, esa carencia recibe owner y se
inserta **antes** de congelar el esquema persistente.

## PERSIST.1 → REP.1 → DEPLOY.1

La secuencia evita diseñar UX final sobre superficies aún inestables:

1. **PERSIST.1/#130:** persistencia voluntaria, guardar/restaurar/borrar,
   migraciones, privacidad y auditoría técnica.
2. **REP.1/#143:** informes y exportaciones reproducibles.
3. **DEPLOY.1/#157:** runtime, hosting, HTTPS, persistencia operativa y CI/CD.

Toda superficie visual nueva creada por estos bloques debe recibir la siguiente
UX.x disponible antes de cerrar el bloque que la introdujo.

## Programa UX

El programa UX final está gobernado por #129 y #189.

El baseline conocido es **UX.7–UX.32**, pero el extremo superior es dinámico:
UX.33+ se crea consecutivamente cuando aparece otra superficie pre-1.0 material.

La lista exacta de superficies e Issues vive en la
[Matriz maestra de pendientes](pre-1-0-pending-matrix.md).

SEC.2 R7 no se habilita por alcanzar un número específico de UX. Se habilita
cuando:

- todas las UX.x obligatorias registradas están cerradas o absorbidas;
- no queda superficie material sin owner UX;
- no existe derivado bloqueante de sincronización shared;
- #189 confirma ausencia de drift visual shared conocido.

## Gates finales

Después de la ola UX real:

- **SEC.2 R7/#144:** hardening final;
- **#156:** rendimiento;
- **A11Y.2/#145:** accesibilidad final;
- **REV.1/#146:** revisión normativa/jurídica/privacidad;
- **#153:** settings GitHub;
- **DOC.1 R6/#147:** freeze documental final;
- **QA.1/#148:** validación integral del candidato beta final;
- **REL.1/#149:** publicación oficial `1.0.0.0`.

## Políticas transversales

- **#166:** preflight, Dependabot y limpieza antes/después de fases materiales;
- **#203:** checkpoints remotos, workspace asistido y handoff canónico;
- **#214:** briefing y aprobación explícita antes de iniciar una fase en un
  chat nuevo;
- **DOC.3:** auditoría documental por cadencia;
- **#189:** sincronización visual multiportal;
- **#153:** gate manual final de configuración GitHub.

Una política transversal no consume Global solo por ejecutarse.

## Post-1.0

Mientras no sean escalados por un hallazgo material, quedan fuera de
`1.0.0.0`:

- i18n #131;
- sesiones/accesos Developer avanzados #150;
- notificaciones Developer #151;
- credenciales Bearer granulares #152.

## Autoridades relacionadas

- [Plan maestro hacia 1.0](master-plan-to-1-0.md);
- [Matriz maestra de pendientes](pre-1-0-pending-matrix.md);
- [Ledger pre-1.0](pre-1-0-revision-ledger.md);
- [Política de versionado](../../VERSIONING.md);
- [Gobierno del proyecto](../../GOVERNANCE.md);
- [Índice documental](../README.md).

## Regla de continuidad

Mientras DOC.4 esté en ejecución:

- baseline aceptado/publicado = G129/E03/C0;
- `VERSION = 0.129.3.0-beta`;
- fase activa = DOC.4 R1/#171;
- candidato Global = no asignado;
- G130 = siguiente Global aritmético libre.

La siguiente fase ordinaria después del cierre/publicación de DOC.4 es #142,
salvo que el preflight #166 detecte trabajo material que deba insertarse antes.
