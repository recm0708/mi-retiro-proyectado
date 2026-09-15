# Plan maestro hacia Mi Retiro Proyectado 1.0

**Estado:** vigente  
**Último estado publicado:** G125/E01 — DOC.3 R1  
**Versión publicada:** `0.1.25.01-beta`  
**Fase en curso:** PLAN.2 R2 / #155  
**Siguiente Global disponible:** G126, libre y no reservado  
**Objetivo estable:** `1.0.0.0`  
**Fecha de reconciliación:** 2026-09-15

Este documento es la autoridad narrativa del **programa vigente** hacia la
primera versión oficial. La clasificación tabular detallada vive en
[pre-1-0-pending-matrix.md](pre-1-0-pending-matrix.md); la historia aceptada se
preserva en el ledger, `RELEASES.md`, `CHANGELOG.md`, tags, GitHub Releases y
`docs/archive/`.

## 1. Principios de planificación

1. Ninguna fase planificada recibe Global o `VERSION` por anticipado.
2. G126 es únicamente el siguiente Global aritméticamente disponible.
3. Un Global se materializa solo cuando existe un candidato real, validado y
   aceptable conforme a `VERSIONING.md`.
4. Issues y documentación versionada deben describir el mismo programa.
5. Una fase descubierta durante otra fase se inserta inmediatamente en todos
   los árboles pendientes antes de continuar, si tiene responsabilidad y
   criterio de cierre propios.
6. #166 se ejecuta antes y después de toda fase material.
7. Si #166 detecta trabajo material de dependencias, MANT.2 R2+ se antepone a
   la fase prevista.
8. Los lotes internos de una fase no consumen Globals propios salvo que se
   conviertan explícitamente en estados materiales independientes.
9. Los gates manuales/transversales no se convierten en Globals por inercia.
10. `1.0.0.0` se publica únicamente después de QA.1 y REL.1.

## 2. Línea base post-G125

DOC.3 R1/#154 quedó publicado como:

```text
Global:  G125
Edition: E01
Version: 0.1.25.01-beta
Tag:     v0.1.25.01-beta
main:    ee077c0d83931f140c91583fa8b2c4ae6b72dec8
Release: 388866555
```

El preflight #166 inmediatamente anterior a PLAN.2 R2 quedó CLEAN. La
verificación diferencial de apertura confirmó el mismo `main`, 0 PRs abiertos,
0 PRs Dependabot abiertos y el mismo `Dependency Security` verde sobre G125.
No se activó MANT.2 R2.

PLAN.2 R2 se abrió sobre:

```text
plan/plan2-r2-replanificacion-maestra
```

`VERSION` permanece en `0.1.25.01-beta`. PLAN.2 R2 todavía no es G126.

## 3. Árbol definitivo de dependencias hacia 1.0

```text
G125 / DOC.3 R1 publicado
→ PLAN.2 R2
→ VER.2 R6
→ DOC.4 R1
→ #142 auditoría previsional integral
→ [fases funcionales obligatorias derivadas, si existen]
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

#166/MANT.2 y DOC.3 atraviesan el árbol como políticas transversales. No son
peldaños funcionales con Globals futuros preasignados.

## 4. Fases obligatorias pre-1.0

### 4.1. PLAN.2 R2 — #155

Estado: **en progreso**.

Responsabilidad:

- clasificar todos los pendientes;
- construir el grafo real;
- materializar UX.9+;
- sincronizar Issues y gobierno versionado;
- cerrar #141 cuando todos sus derivados tengan owner;
- preservar G126 libre hasta existir candidato validado.

PLAN.2 no implementa las fases que ordena.

### 4.2. VER.2 R6 — #164

Primera fase material después de PLAN.2 publicado.

Debe reformar el contrato revision-aware antes de DOC.4 porque DOC.4/Lote C
revisará registry, ledger, manifests y configuración declarativa. El orden evita
canonizar esos artefactos antes de una reforma inmediata.

VER.2 debe formalizar revisiones/subrevisiones/correcciones materiales,
inserción de fases nuevas, guards de sincronización y transición estable hacia
`1.0.0.0`, sin mover historia publicada.

### 4.3. DOC.4 R1 — #171

Se ejecuta después de VER.2 y antes de #142/PERSIST.

Lotes internos:

- #172 — revisión y reescritura 1:1 de Markdown;
- #173 — poda/movimiento/fusión/renombre del árbol documental;
- #174 — artefactos textuales/declarativos no ejecutables.

#174 absorbe #176, la deuda menor del schema local de markdownlint. Los lotes no
consumen Global propio.

DOC.4 se convierte en nuevo baseline documental y reinicia el contador de
DOC.3.

### 4.4. Auditoría previsional integral — #142

Se ejecuta después de DOC.4 y antes de PERSIST.1.

Debe contrastar SEBD, Mixto y SUCGS contra normativa, parámetros, elegibilidad,
fórmulas, modalidades, resultados de referencia y pruebas. Incluye revisión de
pensión normal, retiro anticipado, proporcionales, indemnización, invalidez y
otras prestaciones legalmente aplicables.

Si #142 descubre una capacidad obligatoria para 1.0 que no existe, debe crear
un Issue/fase con criterio de cierre propio e insertarla **antes de PERSIST.1**.
No se congela el modelo persistente con alcance funcional desconocido.

### 4.5. PERSIST.1 — #130

Se abre solo después de cerrar #142 y todos sus derivados obligatorios.

Alcance consolidado:

- arquitectura local-first y guardado voluntario;
- guardar/restaurar/eliminar;
- importación/exportación/migraciones;
- seguridad/privacidad/corrupción;
- política de contraseña Developer con minúscula;
- auditoría técnica transversal de código, CSS, JS, templates y persistencia
  Developer existente.

No absorbe #150–#152.

### 4.6. REP.1 — #143

Después de PERSIST.1.

Debe entregar PDF real y exportaciones finales reproducibles, trazables y
coherentes con el backend, sin lógica paralela de cálculo y con revisión de PII,
metadata, impresión y accesibilidad.

### 4.7. DEPLOY.1 — #157

Después de REP.1 y antes de la ola UX final.

Debe decidir e implementar el runtime/hosting real de 1.0. La hipótesis
preferida es FastAPI remoto con HTTPS, persistencia apropiada y CI/CD seguro.
GitHub Pages puede usarse únicamente para contenido estático si se adopta ese
alcance; no puede ejecutar el producto completo actual.

DEPLOY.1 fija dominio/URLs, secretos, almacenamiento, health checks, backups,
rollback y exposición del Portal Developer para que UX/SEC/performance auditen
el escenario real.

## 5. Programa UX final — UX.7 a UX.20

La ola UX ocurre **después de #142/derivados, PERSIST.1, REP.1 y DEPLOY.1**.
La recomendación previa de refinar UX después de estabilizar persistencia e
informes queda confirmada formalmente.

### UX preservadas

- UX.7/#133 — `/`, login Developer y dashboard Developer;
- UX.8/#134 — `/simulacion`, Manual/Asistida y transición de modalidad.

Ninguna se absorbe ni desaparece.

### UX materializadas por PLAN.2 R2

| UX | Issue | Alcance |
| --- | ---: | --- |
| UX.9 | #177 | Manual — Pasos 1–3 |
| UX.10 | #178 | Manual — Pasos 4–6 y resultados |
| UX.11 | #179 | Mi Retiro Seguro/importación inicial |
| UX.12 | #180 | Ficha Digital/revisión/corrección |
| UX.13 | #181 | Comparación |
| UX.14 | #182 | Metodología |
| UX.15 | #183 | Cómo se calcula |
| UX.16 | #184 | Gestión local de datos/persistencia/privacidad |
| UX.17 | #185 | Informes/exportación/impresión |
| UX.18 | #186 | Developer Diagnóstico/Eventos/Archivos |
| UX.19 | #187 | Developer Mantenimiento/Privacidad/Usuarios-RBAC |
| UX.20 | #188 | Developer Perfil/credenciales/acceso técnico |

Cada revisión debe cubrir temas, forced-colors, responsive/reflow,
teclado/foco, reduced-motion, estados y ownership CSS/JS pertinentes.

## 6. Gates finales pre-1.0

### SEC.2 R7 — #144

Después de UX final. Reevalúa threat model, autenticación/RBAC, CSRF/CORS/CSP,
sesiones, uploads/parsing, persistencia, exportaciones, secretos, logging,
terceros y deployment real.

#152 permanece post-1.0 por defecto. SEC.2 R7 puede escalarla a 1.0 únicamente
si demuestra que el contrato Bearer vigente es insuficiente para el deployment
aprobado. El escalamiento obliga a actualizar el árbol antes de seguir.

### Rendimiento — #156

Después de SEC.2 R7. Mide arranque, rutas, motores, imports, persistencia,
reportes, concurrencia y recursos sobre el deployment ya endurecido.

### A11Y.2 — #145

Después de rendimiento. Auditoría WCAG 2.2 ampliada con teclado, tecnologías de
apoyo, reflow/zoom, forced-colors, reduced-motion, móvil, Portal Developer,
persistencia e informes/exportaciones.

### REV.1 — #146

Después de A11Y.2. Revisión normativa, jurídica, privacidad, seguridad, fuentes,
limitaciones, terceros/licencias y revisión jurídica externa prevista sobre el
producto final estabilizado.

### Settings GitHub — #153

Gate transversal obligatorio después de REV.1. Revalida metadata, labels,
Issue Forms, rulesets, required checks, Dependabot, CodeQL, secret scanning,
Actions, Releases y Pages/environments si DEPLOY.1 los usa. No consume Global
propio mientras permanezca como verificación/configuración manual.

### DOC.1 R6 — #147

Freeze documental final después de #153. No sustituye DOC.4 ni la cadencia de
DOC.3; sincroniza documentación pública/técnica/gobierno con el candidato beta
final antes de QA.

### QA.1 — #148

Auditoría integral final de la etapa beta: suites/checks, motores, persistencia,
imports, informes, UX, seguridad, accesibilidad, normativa, deployment,
documentación y entorno limpio. Bloquea REL.1 mientras exista defecto material
incompatible con 1.0.

### REL.1 — #149

Último bloque. Congela candidato, Build, artefactos reproducibles, SBOM,
hashes, firma, instalación, release notes, tag y GitHub Release de la primera
estable. El objetivo histórico sigue siendo `1.0.0.0` y Build `000001`, sujeto
a la semántica final publicada por VER.2 R6.

## 7. Trabajo post-1.0 confirmado

- #131 — internacionalización español/inglés;
- #150 — historial/gestión avanzada de sesiones/accesos Developer;
- #151 — centro/campana de notificaciones Developer;
- #152 — administración granular de credenciales Bearer, salvo escalamiento
  explícito de SEC.2 R7 por necesidad de seguridad material.

Estas capacidades no bloquean REL.1 por defecto y no forman parte de
UX.7–UX.20.

## 8. Políticas transversales

### 8.1. #166 — preflight y limpieza por fase

Antes de abrir una fase material se revisan PRs, Dependabot, auditorías de
dependencias, `main`, ramas e Issues. Si aparece trabajo material nuevo de
dependencias se inserta MANT.2 R2+ y se sincronizan inmediatamente todos los
árboles de fases pendientes antes de continuar.

Después de publicar una fase se limpia/reconcilia repositorio local/remoto,
ramas, PRs, Issues y artefactos conforme a #166.

### 8.2. Cadencia DOC.3

DOC.3 cuenta fases materiales top-level aceptadas, no lotes internos. DOC.4,
por ser una reingeniería documental integral, se convierte en nuevo baseline y
reinicia el contador.

Por defecto la siguiente auditoría DOC.3 integral se ejecuta después de la
segunda fase material aceptada desde el último baseline, salvo una fase de alto
impacto documental que justifique adelanto y nuevo reset. No se crea ahora
DOC.3 R2 ni se reserva Global.

## 9. Clasificación completa

### Obligatorios 1.0

#164, #171–#174, #142 y derivados obligatorios, #130, #143, #157,
#129/#133/#134/#177–#188, #144, #156, #145, #146, #147, #148 y #149.

### Transversales obligatorios

#166, #153 y la cadencia DOC.3.

### Post-1.0

#131, #150, #151 y #152 por defecto.

### Absorbidos/cerrados

- #176 → #174;
- #141 — umbrella histórico consumido y cerrado por PLAN.2 R2.

### Opcionales 1.0

No se identificó ningún bloque material opcional necesario para permanecer en
el árbol pre-1.0. Una capacidad no obligatoria queda fuera del release o debe
recibir clasificación explícita posterior; no permanece como ambigüedad.

## 10. Fuentes canónicas y sincronización

Este plan debe permanecer sincronizado con:

- [roadmap.md](roadmap.md);
- [pre-1-0-pending-matrix.md](pre-1-0-pending-matrix.md);
- [pre-1-0-revision-ledger.md](pre-1-0-revision-ledger.md);
- `data/governance/pre-1-0-revision-ledger.json`;
- `data/governance/work-block-registry.json`;
- `data/governance/release-publication-manifest.json`;
- `VERSIONING.md`;
- `GOVERNANCE.md`;
- Issues propietarios.

El ledger y el manifest no se usan para reservar PLAN.2 R2/G126 antes de su
aceptación. La historia G001–G125 permanece inmutable.

## 11. Regla de continuidad

La siguiente fase material es **VER.2 R6/#164**, pero únicamente después de que
PLAN.2 R2 tenga candidato validado, sea aceptado/integrado/publicado y un
preflight fresco #166 confirme nuevamente que no apareció mantenimiento de
dependencias que deba anteponerse.
