# Plan maestro hacia Mi Retiro Proyectado 1.0

**Estado:** vigente  
**Último estado publicado:** G125/E01 — DOC.3 R1  
**Versión publicada:** `0.1.25.01-beta`  
**Fase en curso:** PLAN.2 R2 / #155  
**Siguiente Global disponible:** G126, libre y no reservado  
**Objetivo estable:** `1.0.0.0`  
**Fecha de reconciliación:** 2026-09-15

Este documento es la autoridad narrativa del programa vigente hacia la primera versión oficial. La matriz tabular vive en [pre-1-0-pending-matrix.md](pre-1-0-pending-matrix.md); la historia aceptada se preserva en ledger, `RELEASES.md`, `CHANGELOG.md`, tags, GitHub Releases y `docs/archive/`.

## 1. Principios

1. Ninguna fase planificada recibe Global o `VERSION` por anticipado.
2. G126 es solo el siguiente Global aritméticamente disponible.
3. Un Global se materializa únicamente con candidato real, validado y aceptable.
4. Issues y documentación versionada deben describir el mismo programa.
5. Trabajo material nuevo con responsabilidad propia se inserta inmediatamente en todos los árboles afectados antes de continuar.
6. #166 se ejecuta antes/después de cada fase material y puede insertar MANT.2 R2+.
7. Lotes internos no consumen Globals propios salvo decisión explícita.
8. Gates manuales/transversales no se convierten en Globals por inercia.
9. El programa UX es abierto: el número final UX.x se conoce solo cuando las superficies pre-1.0 están estabilizadas.
10. `1.0.0.0` se publica únicamente después de QA.1 y REL.1.

## 2. Línea base post-G125

```text
Global:  G125
Edition: E01
Version: 0.1.25.01-beta
Tag:     v0.1.25.01-beta
main:    ee077c0d83931f140c91583fa8b2c4ae6b72dec8
Release: 388866555
```

El preflight #166 inmediatamente anterior a PLAN.2 R2 quedó CLEAN y la verificación diferencial confirmó el mismo `main`, 0 PRs abiertos, 0 PRs Dependabot y el mismo Dependency Security verde. No se activó MANT.2 R2.

PLAN.2 R2 se abrió en `plan/plan2-r2-replanificacion-maestra`. `VERSION` permanece en `0.1.25.01-beta`; PLAN.2 todavía no es G126.

## 3. Árbol definitivo de dependencias

```text
G125 / DOC.3 R1 publicado
→ PLAN.2 R2
→ VER.2 R6
→ DOC.4 R1
→ #142 auditoría previsional
→ [fases funcionales obligatorias derivadas, si existen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7
→ UX.8
→ ...
→ UX.x final realmente necesario
→ #189 sin drift visual shared
→ SEC.2 R7
→ rendimiento #156
→ A11Y.2
→ REV.1
→ #153 settings GitHub
→ DOC.1 R6
→ QA.1
→ REL.1
→ 1.0.0.0
```

#166/MANT.2, DOC.3 y #189 atraviesan el árbol como políticas transversales.

## 4. Bloques materiales previos a UX

### PLAN.2 R2 — #155
Clasifica, ordena y sincroniza el programa. No implementa las fases posteriores ni reserva G126 antes de candidato real.

### VER.2 R6 — #164
Primera fase material después de PLAN.2 publicado. Reforma el contrato revision-aware antes de DOC.4 para que registry, ledger, manifests y tooling sean canonizados una sola vez sobre el modelo final.

### DOC.4 R1 — #171
Después de VER.2. Lotes internos #172 Markdown, #173 estructura/poda y #174 artefactos declarativos. #174 absorbe #176. DOC.4 crea nuevo baseline documental y reinicia la cadencia DOC.3.

### Auditoría previsional — #142
Después de DOC.4 y antes de PERSIST.1. Contrasta SEBD/Mixto/SUCGS, modalidades y prestaciones. Todo faltante obligatorio para 1.0 se crea e inserta antes de PERSIST.1.

### PERSIST.1 — #130
Persistencia voluntaria/versionada, guardar/restaurar/borrar, migraciones, privacidad, contraseña Developer y auditoría técnica transversal. Si crea una nueva superficie visual material, debe registrar la siguiente UX.x disponible antes de cerrar.

### REP.1 — #143
PDF/exportaciones finales reproducibles y trazables. Toda nueva pantalla visible de generación/exportación debe crear la siguiente UX.x disponible; no existe un número UX de informes preasignado.

### DEPLOY.1 — #157
Runtime/hosting/HTTPS/persistencia/CI-CD. Toda nueva superficie visual material del deployment debe crear la siguiente UX.x disponible antes de cerrar.

## 5. Programa UX final — UX.7 → UX.x

La ola UX comienza únicamente después de #142/derivados, PERSIST.1, REP.1 y DEPLOY.1. Esto formaliza que la revisión visual final ocurre sobre superficies funcionalmente estables.

### Regla de granularidad

**Una UX.x = una superficie, paso o modal material.** No se agrupan varios pasos de Simulación ni varias páginas Developer en una sola fase.

### Baseline conocido UX.7–UX.32

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.7 | #133 | Inicio Asegurado `/` + Inicio/Resumen Developer `/dev` autenticado |
| UX.8 | #134 | Asegurado `/simulacion` — selección Manual/Asistida antes del Paso 1 |
| UX.9 | #177 | Paso 1 — Datos personales |
| UX.10 | #178 | Paso 2 — Cuotas |
| UX.11 | #179 | Paso 3 — Historial y base salarial |
| UX.12 | #180 | Paso 4 — Proyección y línea temporal |
| UX.13 | #181 | Paso 5 — Escenarios de retiro |
| UX.14 | #182 | Paso 6 — Resultados |
| UX.15 | #183 | Asegurado `/comparar` |
| UX.16 | #184 | Asegurado `/como-se-calcula` |
| UX.17 | #185 | Asegurado `/metodologia` |
| UX.18 | #186 | modal Términos/privacidad/consentimiento |
| UX.19 | #187 | modal Gestión de datos |
| UX.20 | #188 | modal Mi Retiro Seguro |
| UX.21 | #190 | modal Ficha Digital — revisión/importación |
| UX.22 | #191 | modal Vigencia de Ficha Digital |
| UX.23 | #192 | Developer — inicio de sesión |
| UX.24 | #193 | Developer — Diagnóstico |
| UX.25 | #194 | Developer — Eventos |
| UX.26 | #195 | Developer — Archivos |
| UX.27 | #196 | Developer — Mantenimiento |
| UX.28 | #197 | Developer — Usuarios/RBAC |
| UX.29 | #198 | Developer — Privacidad |
| UX.30 | #199 | Developer — Perfil/credenciales web |
| UX.31 | #200 | Developer — Acceso técnico |
| UX.32 | #201 | Developer — Centro de desarrollo legacy si continúa soportado |

UX.7 es la única agrupación deliberada: las dos páginas de Inicio forman el punto de identidad de ambos portales. El login Developer es UX.23.

### Regla UX.33+

Si antes del cierre UX aparece otra superficie visual material:

1. crear la siguiente UX consecutiva;
2. crear Issue propio con alcance/criterio;
3. actualizar #129, #155 y fuentes vivas inmediatamente;
4. aplicar #189;
5. no renumerar UX existentes;
6. no preasignar Global/VERSION.

## 6. Sincronización visual multiportal — #189

#189 es transversal y no consume Global propio. Cada cambio visual se clasifica como `shared` o `portal-specific`.

Un cambio `shared` debe propagarse a App Asegurado, Portal Developer y portales futuros aplicables. Incluye tokens/paleta, tipografía, tamaños/pesos, colores, botones, inputs, tarjetas, tablas genéricas, badges/alerts, spacing, bordes/radios/sombras, foco, temas Claro/Oscuro/Automático/Alto contraste, forced-colors, motion, selector de apariencia, footer y patrones comunes.

Ninguna UX puede cerrar dejando drift conocido en otro portal. Si una dependencia real impide sincronizar en la misma fase, se crea un Issue derivado bloqueante antes del cierre.

## 7. Gate de salida UX y SEC.2 R7

SEC.2 R7 no se habilita por alcanzar UX.32. Se habilita únicamente cuando:

- todas las UX.x obligatorias registradas están cerradas/absorbidas explícitamente;
- no existe superficie visual material sin UX owner/clasificación;
- no existe derivado bloqueante de sincronización shared;
- #189 confirma ausencia de drift shared conocido.

Si SEC.2 R7 escala #152 y eso crea UI nueva, se crea una nueva UX.x y se vuelve a satisfacer el gate antes de continuar.

## 8. Gates finales

- **SEC.2 R7 #144:** hardening final del producto/deployment.
- **Rendimiento #156:** mediciones sobre escenario ya endurecido.
- **A11Y.2 #145:** auditoría WCAG 2.2 sobre todas las UX.x finales.
- **REV.1 #146:** revisión normativa/jurídica/privacidad final.
- **#153:** revalidación final de settings GitHub, sin Global propio mientras sea gate manual.
- **DOC.1 R6 #147:** freeze documental final.
- **QA.1 #148:** auditoría integral del candidato beta final.
- **REL.1 #149:** publicación oficial `1.0.0.0`.

## 9. Post-1.0

- #131 i18n;
- #150 sesiones/accesos avanzados;
- #151 notificaciones Developer;
- #152 credenciales Bearer granulares por defecto, salvo escalamiento explícito de SEC.2 R7.

Estas capacidades no crean UX pre-1.0 mientras permanezcan post-1.0.

## 10. Cadencia DOC.3

DOC.3 cuenta fases materiales top-level aceptadas, no lotes internos. DOC.4 crea un nuevo baseline y reinicia el contador. Por defecto la siguiente DOC.3 integral ocurre después de la segunda fase material aceptada desde ese baseline, salvo impacto documental alto que justifique adelanto/reset. No se crea ahora DOC.3 R2 ni se reserva Global.

## 11. Clasificación

### Obligatorios 1.0
#164, #171–#174, #142 y derivados obligatorios, #130, #143, #157, #129 y todas las UX.x que registre, #144, #156, #145, #146, #147, #148 y #149.

### Transversales obligatorios
#166, #189, #153 y DOC.3 por cadencia.

### Post-1.0
#131, #150, #151 y #152 por defecto.

### Absorbidos/cerrados
#176 → #174; #141 consumido/cerrado.

### Opcionales 1.0
Ninguno identificado.

## 12. Autoridades sincronizadas

- [roadmap.md](roadmap.md)
- [pre-1-0-pending-matrix.md](pre-1-0-pending-matrix.md)
- [pre-1-0-revision-ledger.md](pre-1-0-revision-ledger.md)
- `data/governance/pre-1-0-revision-ledger.json`
- `data/governance/work-block-registry.json`
- `data/governance/release-publication-manifest.json`
- `VERSIONING.md`
- `GOVERNANCE.md`
- Issues propietarios

El ledger y manifest no reservan PLAN.2 R2/G126 antes de aceptación. La historia G001–G125 permanece inmutable.

## 13. Continuidad

La siguiente fase material es VER.2 R6/#164, únicamente después de que PLAN.2 R2 sea validado, aceptado, integrado, publicado y un preflight fresco #166 vuelva a quedar limpio.