# Roadmap

**Estado:** vigente  
**Último estado publicado:** G125/E01 — DOC.3 R1  
**Versión publicada:** `0.1.25.01-beta`  
**`main` de línea base PLAN.2 R2:**
`ee077c0d83931f140c91583fa8b2c4ae6b72dec8`  
**Siguiente Global disponible:** G126, libre y no reservado  
**Fase en curso:** PLAN.2 R2 / Issue #155  
**Fecha de reconciliación:** 2026-09-15

Este roadmap muestra el **programa vigente** hacia la primera versión oficial.
La historia de estados aceptados y publicaciones se conserva en el ledger,
`RELEASES.md`, `CHANGELOG.md`, tags, GitHub Releases y `docs/archive/`.

## Estado de entrada de PLAN.2 R2

DOC.3 R1 quedó publicado como G125/E01 mediante el tag firmado
`v0.1.25.01-beta` y GitHub Release prerelease 388866555.

El preflight #166 inmediatamente anterior a PLAN.2 R2 quedó limpio. La
verificación diferencial al cambiar de chat confirmó que `main` no se había
movido, no había PRs abiertos ni trabajo material nuevo de dependencias y
`Dependency Security` seguía verde sobre el mismo SHA. Por ello no se insertó
MANT.2 R2 antes de PLAN.2.

PLAN.2 R2 trabaja en la rama:

```text
plan/plan2-r2-replanificacion-maestra
```

La rama nació exactamente desde el `main` publicado G125. `VERSION` continúa
en `0.1.25.01-beta`: **PLAN.2 no reserva G126 ni modifica VERSION mientras no
exista un candidato material validado y aceptable**.

## Árbol vigente hacia `1.0.0.0`

```text
G125 / DOC.3 R1 publicado
→ PLAN.2 R2
→ VER.2 R6
→ DOC.4 R1
→ auditoría previsional #142
→ [fases funcionales obligatorias derivadas, si aparecen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7–UX.20
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

Este orden representa dependencias materiales, no Globals futuros supuestos.
Cada fase recibe Global/versión únicamente cuando exista un candidato real y
validado conforme a `VERSIONING.md`.

## Decisiones de PLAN.2 R2

### VER.2 R6 antes de DOC.4

VER.2 R6/#164 reforma primero el contrato revision-aware, parsers, ledger,
registry y tooling de Release. DOC.4 Lote C revisará después esos mismos
artefactos declarativos sobre el modelo ya estabilizado; hacerlo al revés
obligaría a canonizarlos dos veces.

### DOC.4 antes de congelar alcance funcional/persistencia

DOC.4 R1/#171 ejecuta la reingeniería documental canónica mediante los lotes
#172, #173 y #174. El Lote C absorbe además #176, la deuda menor del schema
local de markdownlint. Los lotes son internos y no consumen Globals propios.

Al cerrar DOC.4, su revisión integral se convierte en nuevo baseline documental
y reinicia la cadencia de DOC.3.

### Auditoría previsional antes de PERSIST.1

#142 debe establecer qué prestaciones y modalidades SEBD/Mixto/SUCGS están
realmente soportadas. Si descubre una carencia obligatoria para 1.0, se crea e
inserta su fase funcional antes de PERSIST.1. El esquema persistente no se
congela antes de conocer el alcance funcional real.

### PERSIST.1 → REP.1 → DEPLOY.1

PERSIST.1/#130 estabiliza guardado/restauración/migraciones y la auditoría
técnica transversal. REP.1/#143 materializa informes PDF/exportaciones sobre
ese estado canónico. DEPLOY.1/#157 fija runtime, hosting, HTTPS, persistencia
y CI/CD antes de la revisión UX final.

### UX final después de superficies funcionales estables

UX.7/#133 y UX.8/#134 se conservan expresamente. PLAN.2 R2 materializó
UX.9–UX.20 como Issues #177–#188. La ola completa cubre entradas, simulación
Manual/Asistida, comparación, metodología, guía de cálculo, gestión local de
datos, informes y todas las familias visibles del Portal Developer.

La ola UX empieza después de #142/derivados, PERSIST.1, REP.1 y DEPLOY.1, y
termina antes de SEC.2 R7. Así los gates finales auditan superficies reales,
no borradores que cambiarán inmediatamente.

### Gates finales

SEC.2 R7 endurece el producto y deployment final. #156 mide rendimiento y
resiliencia sobre ese escenario endurecido. A11Y.2 ejecuta la auditoría WCAG
2.2 ampliada. REV.1 realiza la revisión normativa/jurídica/privacidad final.
#153 revalida settings GitHub. DOC.1 R6 congela documentación. QA.1 valida el
candidato beta final y REL.1 publica la primera estable.

## Programa UX pre-1.0

| UX | Issue | Superficie o flujo |
| --- | ---: | --- |
| UX.7 | #133 | Inicio App + login/dashboard Developer |
| UX.8 | #134 | Entrada a Simulación y selección Manual/Asistida |
| UX.9 | #177 | Manual — Pasos 1–3 |
| UX.10 | #178 | Manual — Pasos 4–6 y resultados |
| UX.11 | #179 | Asistido — Mi Retiro Seguro/importación inicial |
| UX.12 | #180 | Asistido — Ficha Digital/revisión/corrección |
| UX.13 | #181 | Comparación de escenarios |
| UX.14 | #182 | Metodología pública |
| UX.15 | #183 | Cómo se calcula |
| UX.16 | #184 | Gestión local de datos/persistencia/privacidad |
| UX.17 | #185 | Informes/exportación/impresión |
| UX.18 | #186 | Developer — Diagnóstico/Eventos/Archivos |
| UX.19 | #187 | Developer — Mantenimiento/Privacidad/Usuarios-RBAC |
| UX.20 | #188 | Developer — Perfil/credenciales/acceso técnico |

## Trabajo expresamente post-1.0

No bloquean `1.0.0.0`:

- i18n español/inglés #131;
- gestión avanzada/historial de sesiones Developer #150;
- centro de notificaciones Developer #151;
- administración granular de credenciales Bearer #152.

#152 conserva una excepción: SEC.2 R7 puede escalarla a obligatorio 1.0 si el
deployment aprobado demuestra que el contrato Bearer vigente no es suficiente
para operar con seguridad. Ese escalamiento debe actualizar el árbol antes de
continuar.

## Políticas transversales

### #166 — preflight, mantenimiento y limpieza

Antes y después de cada fase material se revalida Dependabot/dependencias,
PRs, ramas, working tree, Issues y gates. Si aparece trabajo material nuevo de
dependencias, se inserta MANT.2 R2+ antes de la fase prevista y se actualizan
inmediatamente las fuentes de planificación afectadas.

### DOC.3 — auditoría documental periódica

DOC.3 no es un peldaño funcional fijo. Se cuenta por fases materiales top-level
aceptadas. DOC.4 se convierte en nuevo baseline documental al cerrar y reinicia
el contador. Por defecto la siguiente auditoría integral ocurre después de la
segunda fase material aceptada desde ese baseline, salvo un evento documental
de alto impacto que justifique adelantarla y reiniciar de nuevo el contador.

No se crea ahora DOC.3 R2 ni se le reserva Global.

## Clasificación de pendientes

- **Obligatorios 1.0:** #164, #171–#174, #142 y derivados obligatorios,
  #130, #143, #157, #129/#133/#134/#177–#188, #144, #156, #145, #146,
  #147, #148 y #149.
- **Transversales obligatorios:** #166, #153 y la cadencia DOC.3.
- **Post-1.0:** #131 y #150–#152.
- **Absorbido:** #176 → #174.
- **Cerrado/consumido:** #141.
- **Opcionales 1.0 sin owner material:** ninguno identificado.

## Autoridades relacionadas

- [Plan maestro hacia 1.0](master-plan-to-1-0.md)
- [Matriz maestra de pendientes](pre-1-0-pending-matrix.md)
- [Ledger revision-aware](pre-1-0-revision-ledger.md)
- `data/governance/pre-1-0-revision-ledger.json`
- `data/governance/work-block-registry.json`
- `data/governance/release-publication-manifest.json`
- `VERSIONING.md`
- `GOVERNANCE.md`

## Regla de continuidad

La siguiente fase material después de PLAN.2 R2 es **VER.2 R6/#164**, pero no
se inicia hasta que PLAN.2 R2 tenga candidato real validado, sea aceptado,
integrado y publicado, y un preflight fresco #166 vuelva a quedar limpio.
