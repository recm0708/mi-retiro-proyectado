# Matriz maestra de pendientes hacia 1.0

**Estado:** vigente / documento vivo
**Último estado publicado:** G127/E02 — MANT.2 R2
**Versión publicada:** `0.1.27.02-beta`
**Fase activa:** VER.2 R6 / #164 — G128/E02/C0 `0.128.2.0-beta` aceptado pendiente de integración/publicación
**Siguiente Global aritmético:** G129, libre y no reservado
**Última reconciliación:** 2026-09-21 — CP6A-R1 cerrado; CP6B en curso

Esta matriz es la autoridad tabular del trabajo pendiente hacia `1.0.0.0`. No preasigna Globals futuros. El orden expresa dependencias reales; cada estado material aceptado recibe Global/versión únicamente con candidato validado conforme a `VERSIONING.md`.

Como antecedentes inmediatos preservados, G125/E01 — DOC.3 R1 y G126/E01 — PLAN.2 R2 permanecen en el ledger histórico; el estado publicado vigente es G127/E02 — MANT.2 R2.

El baseline publicado vigente es **G127/E02 — MANT.2 R2** (`0.1.27.02-beta`). VER.2 R6/#164 materializó **G128/E02/C0** (`0.128.2.0-beta`) como candidato aceptado pendiente de integración/publicación; G129 permanece libre.

## 1. Reglas

1. G127/E02 — MANT.2 R2 es el último estado publicado e inmutable.
2. VER.2 R6/#164 materializó G128/E02/C0 como `0.128.2.0-beta` y está pendiente de integración/publicación.
3. G129 permanece libre, sin candidato, bloque ni VERSION asignados.
4. Todo pendiente debe tener owner, clasificación y dependencia explícitos.
5. Trabajo material nuevo se inserta en todos los árboles afectados antes de continuar.
6. #166 puede insertar MANT.2 R2+ en cualquier frontera material.
7. #172–#174 son lotes internos DOC.4 y no consumen Globals propios.
8. DOC.3 se ejecuta por cadencia y no recibe Global por planificación.
9. El programa UX es dinámico: UX.7–UX.32 es el baseline conocido; UX.33+ se crea consecutivamente si aparece una nueva superficie visual pre-1.0.
10. #189 gobierna la sincronización visual multiportal y no consume Global propio.
11. SEC.2 R7 no se habilita hasta cerrar **toda** UX.x obligatoria realmente registrada y el gate #189 sin drift.
12. Roadmap, plan maestro, esta matriz, registry e Issues deben coincidir.

## 2. Grafo canónico

```text
G126 / PLAN.2 R2 publicado
→ G127 / MANT.2 R2 publicado
→ VER.2 R6
→ DOC.4 R1
→ #142 auditoría previsional
→ [derivados funcionales obligatorios, si existen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7 → UX.8 → ... → UX.x final necesario
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

#166/MANT.2 y DOC.3 son transversales al grafo.

## 3. Pendientes obligatorios pre-1.0

| Orden lógico | Identificador / Issue | Clasificación | Dependencia de entrada | Criterio principal de cierre | Estado |
| ---: | --- | --- | --- | --- | --- |
| 1 | MANT.2 R2 / #206 | baseline cerrado | G126 publicado + #166 | dependencias reconciliadas y publicación formal | Cerrado/publicado G127/E02 |
| 2 | VER.2 R6 / #164 | obligatorio 1.0 | G127 publicado + #166 CLEAN | modelo revision-aware, documentación y guards reconciliados | En ejecución; G128 libre |
| 3 | DOC.4 R1 / #171 | obligatorio 1.0 | VER.2 publicado + #166 | documentación/no-código current-state-only reingenierizados | Espera VER.2 |
| 3A | DOC.4 Lote A / #172 | interno DOC.4 | #171 abierto | 100 % Markdown revisado 1:1 | Sin Global |
| 3B | DOC.4 Lote B / #173 | interno DOC.4 | decisiones #172 | poda/movimientos/fusiones/enlaces reconciliados | Sin Global |
| 3C | DOC.4 Lote C / #174 | interno DOC.4 | #171 abierto | artefactos declarativos reconciliados; #176 resuelto | Sin Global |
| 4 | Auditoría previsional / #142 | obligatorio 1.0 | DOC.4 publicado + #166 | cobertura SEBD/Mixto/SUCGS demostrada; faltantes con owner | Espera DOC.4 |
| 4.x | Derivados funcionales #142 | condicional obligatorio 1.0 | hallazgo material #142 | prestación/modalidad necesaria implementada/probada | Se crean solo si se demuestra necesidad |
| 5 | PERSIST.1 / #130 | obligatorio 1.0 | #142 + derivados cerrados + #166 | persistencia voluntaria/versionada + auditoría técnica | Espera alcance funcional |
| 6 | REP.1 / #143 | obligatorio 1.0 | PERSIST.1 + #166 | PDF/exportaciones reales; nueva UI con UX owner si aparece | Espera PERSIST.1 |
| 7 | DEPLOY.1 / #157 | obligatorio 1.0 | REP.1 + #166 | runtime/hosting/HTTPS/CI-CD y toda nueva UI con UX owner | Espera REP.1 |
| 8…x | Programa UX / #129 | obligatorio 1.0 | #142/derivados + PERSIST + REP + DEPLOY | toda UX.x registrada cerrada/absorbida; ninguna superficie sin owner | Baseline UX.7–UX.32; extensible |
| x+1 | UX/GOV / #189 | transversal obligatorio | durante toda la ola UX | sin drift visual shared ni derivados bloqueantes | Política activa, sin Global |
| x+2 | SEC.2 R7 / #144 | obligatorio 1.0 | toda UX.x cerrada + #189 sin drift + #166 | threat model/hardening final | Espera cierre real UX |
| x+3 | Rendimiento / #156 | obligatorio 1.0 | SEC.2 R7 | línea base reproducible; problemas materiales resueltos | Espera SEC.2 |
| x+4 | A11Y.2 / #145 | obligatorio 1.0 | #156 + #166 | WCAG 2.2/AT/reflow/forced-colors en superficies finales | Espera rendimiento |
| x+5 | REV.1 / #146 | obligatorio 1.0 | A11Y.2 + #166 | normativa/jurídica/privacidad/terceros finales | Espera A11Y.2 |
| x+6 | Settings GitHub / #153 | transversal obligatorio | REV.1 | settings públicos/security/release/deploy revalidados | Sin Global mientras sea gate manual |
| x+7 | DOC.1 R6 / #147 | obligatorio 1.0 | #153 + #166 | documentación final congelada | Espera #153 |
| x+8 | QA.1 / #148 | obligatorio 1.0 | todos los previos + #166 | candidato beta final sin bloqueantes | Espera DOC.1 R6 |
| x+9 | REL.1 / #149 | obligatorio 1.0 | QA.1 + #166 | build/SBOM/firma/tag/Release oficiales | Último bloque |

## 4. Baseline UX conocido

### Inicio y Simulación

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.7 | #133 | Inicio Asegurado `/` + Inicio/Resumen Developer `/dev` autenticado |
| UX.8 | #134 | `/simulacion` — entrada y selección Manual/Asistida antes del Paso 1 |
| UX.9 | #177 | Paso 1 — Datos personales |
| UX.10 | #178 | Paso 2 — Cuotas |
| UX.11 | #179 | Paso 3 — Historial y base salarial |
| UX.12 | #180 | Paso 4 — Proyección y línea temporal |
| UX.13 | #181 | Paso 5 — Escenarios de retiro |
| UX.14 | #182 | Paso 6 — Resultados |

### Otras superficies Asegurado

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.15 | #183 | `/comparar` — Escenarios/Comparación |
| UX.16 | #184 | `/como-se-calcula` |
| UX.17 | #185 | `/metodologia` — Fuentes/Metodología |
| UX.18 | #186 | modal Términos/privacidad/consentimiento |
| UX.19 | #187 | modal Gestión de datos |
| UX.20 | #188 | modal Mi Retiro Seguro |
| UX.21 | #190 | modal Ficha Digital — revisión/importación |
| UX.22 | #191 | modal Vigencia de Ficha Digital |

### Portal Developer

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.23 | #192 | inicio de sesión |
| UX.24 | #193 | Diagnóstico |
| UX.25 | #194 | Eventos |
| UX.26 | #195 | Archivos |
| UX.27 | #196 | Mantenimiento |
| UX.28 | #197 | Usuarios/RBAC |
| UX.29 | #198 | Privacidad |
| UX.30 | #199 | Perfil/credenciales web |
| UX.31 | #200 | Acceso técnico |
| UX.32 | #201 | Centro de desarrollo legacy, si continúa soportado |

UX.7 es la única combinación deliberada de dos superficies porque ambas representan la página de Inicio/identidad de cada portal. El login Developer tiene UX.23 propia.

## 5. Expansión UX.33+

Si #142/derivados, PERSIST.1, REP.1, DEPLOY.1 o una UX previa crea/descubre una nueva superficie material:

1. crear la siguiente UX.x consecutiva;
2. crear Issue propietario;
3. incorporar inmediatamente la nueva UX a #129/#155 y fuentes vivas;
4. aplicar #189;
5. no renumerar UX existentes;
6. no preasignar Global/VERSION.

## 6. Contrato visual multiportal #189

Todo cambio debe clasificarse como `shared` o `portal-specific`. Si es shared —tokens, tipografía, colores, botones, inputs, tarjetas, tablas genéricas, badges/alerts, spacing, bordes/radios/sombras, foco, temas, forced-colors, motion, selector de apariencia, footer u otros patrones comunes— debe implementarse/sincronizarse donde aplique en todos los portales.

Una UX.x no puede cerrar dejando otro portal desincronizado. Si una dependencia real impide sincronizar en la misma fase, debe existir un Issue derivado bloqueante antes del cierre.

## 7. Gate de salida UX

La ola termina cuando:

- [ ] todas las UX.x obligatorias registradas están cerradas/absorbidas;
- [ ] ninguna superficie visual material pre-1.0 carece de UX owner/clasificación;
- [ ] no existe derivado bloqueante de sincronización shared;
- [ ] #189 confirma ausencia de drift visual shared conocido;
- [ ] todo hallazgo fuera de alcance fue transferido.

Solo entonces se habilita SEC.2 R7.

## 8. Post-1.0

| Issue | Trabajo | Clasificación |
| ---: | --- | --- |
| #131 | i18n español/inglés | post-1.0 |
| #150 | sesiones/accesos Developer avanzados | post-1.0 |
| #151 | notificaciones Developer | post-1.0 |
| #152 | Bearer granular | post-1.0 por defecto; escalable por SEC.2 R7 |

Si una capacidad post-1.0 se escala antes de 1.0 y crea UI visible, debe crear una nueva UX.x y volver a cerrar el gate #129/#189.

## 9. Transversales / absorbidos / cerrados

| Issue / bloque | Clasificación | Owner / regla |
| --- | --- | --- |
| #166 | transversal permanente | preflight Dependabot/limpieza por fase |
| MANT.2 R2+ | transversal condicional | inserción por dependencia material |
| DOC.3 | transversal por cadencia | auditoría periódica; DOC.4 resetea baseline |
| #189 | transversal UX | sincronización multiportal y expansión UX.x |
| #153 | transversal final | settings GitHub |
| #176 | absorbido | #174 |
| #141 | cerrado | umbrella consumido por PLAN.2 R2 |

## 10. Cadencia DOC.3

Cuenta fases materiales top-level aceptadas, no lotes internos. DOC.4 crea nuevo baseline y reinicia el contador. Por defecto la siguiente DOC.3 integral ocurre después de la segunda fase material aceptada desde ese baseline, salvo impacto documental alto que justifique adelanto/reset. No se crea ahora DOC.3 R2 ni se reserva Global.

## 11. Opcionales 1.0

**Ninguno identificado.**

## 12. Invariantes de versionado durante VER.2 R6

```text
VERSION = 0.128.2.0-beta
accepted_baseline = G128/E02/C0 / VER.2 R6
published_baseline = G127/E02 / MANT.2 R2
active_phase = VER.2 R6 / #164
current_candidate = accepted_pending_integration
next_global_available = 129
G129 = libre / no reservado
```

El ledger v2 registra historia aceptada y candidato; el registry declara el
baseline G127/E02 y VER.2 R6 como fase activa. El manifest de G127 es un
snapshot `release-input`; los hechos de publicación se resuelven en runtime.

## 13. Próxima frontera

VER.2 R6/#164 materializó G128/E02/C0 (`0.128.2.0-beta`) sobre el baseline publicado G127/E02. G129 continúa libre. La siguiente fase material ordinaria es DOC.4 R1/#171 después de publicar VER.2, salvo que #166 detecte trabajo material nuevo y requiera insertar MANT.2 R3+.
