# Matriz maestra de pendientes hacia 1.0

**Estado:** vigente / documento vivo  
**Último estado publicado:** G125/E01 — DOC.3 R1  
**Versión publicada:** `0.1.25.01-beta`  
**Fase activa:** PLAN.2 R2 / #155  
**Siguiente Global disponible:** G126, libre y no reservado  
**Última reconciliación:** 2026-09-15 — PLAN.2 R2

Esta matriz es la autoridad tabular del trabajo pendiente hacia `1.0.0.0`.
No preasigna Globals futuros. El orden expresa dependencias reales; cada estado
material aceptado recibe Global/versión únicamente cuando existe candidato
validado conforme a `VERSIONING.md`.

## 1. Reglas de uso

1. G125/E01 es el último estado publicado y permanece inmutable.
2. PLAN.2 R2 está en progreso sobre G125; todavía no es G126.
3. G126 no tiene candidato, bloque ni `VERSION` asignados.
4. Todo pendiente debe tener owner, clasificación y dependencia explícitos.
5. Si una fase descubre trabajo material con responsabilidad propia, se crea su
   Issue y se inserta en todos los árboles afectados antes de continuar.
6. #166 puede insertar MANT.2 R2+ en cualquier frontera material.
7. Los lotes internos #172–#174 no consumen Globals propios.
8. DOC.3 se ejecuta por cadencia y no recibe Global futuro por planificación.
9. Historia aceptada se consulta en ledger/RELEASES/CHANGELOG/tags/Releases.
10. Roadmap, plan maestro, esta matriz, registry y Issues deben coincidir.

## 2. Grafo canónico

```text
PLAN.2 R2
→ VER.2 R6
→ DOC.4 R1
→ #142 auditoría previsional
→ [derivados funcionales obligatorios, si existen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7–UX.20
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

## 3. Matriz de pendientes obligatorios pre-1.0

| Orden lógico | Identificador / Issue | Clasificación | Dependencia de entrada | Criterio principal de cierre | Estado |
| ---: | --- | --- | --- | --- | --- |
| 1 | **PLAN.2 R2 / #155** | obligatorio 1.0 | G125 publicado + preflight #166 CLEAN | árbol, clasificación, Issues y gobierno versionado sincronizados | **En progreso; sin Global preasignado** |
| 2 | **VER.2 R6 / #164** | obligatorio 1.0 | PLAN.2 R2 publicado + #166 | modelo revision-aware/correcciones/inserción de fases y guards reconciliados | Espera PLAN.2 |
| 3 | **DOC.4 R1 / #171** | obligatorio 1.0 | VER.2 R6 publicado + #166 | árbol documental/no-código current-state-only reingenierizado | Espera VER.2 |
| 3A | **DOC.4 Lote A / #172** | interno DOC.4 | #171 abierto | 100 % Markdown revisado 1:1 | No consume Global |
| 3B | **DOC.4 Lote B / #173** | interno DOC.4 | decisiones #172 | poda/movimientos/fusiones/enlaces reconciliados | No consume Global |
| 3C | **DOC.4 Lote C / #174** | interno DOC.4 | #171 abierto; coordina #172/#173 | artefactos declarativos/no ejecutables reconciliados; #176 resuelto | No consume Global |
| 4 | **Auditoría previsional / #142** | obligatorio 1.0 | DOC.4 publicado + #166 | cobertura SEBD/Mixto/SUCGS demostrada; faltantes con owner/clasificación | Espera DOC.4 |
| 4.x | **Derivados funcionales de #142** | condicional obligatorio 1.0 | hallazgo material de #142 | prestación/modalidad necesaria implementada y probada | Se crean solo si #142 los demuestra |
| 5 | **PERSIST.1 / #130** | obligatorio 1.0 | #142 + derivados obligatorios cerrados + #166 | persistencia voluntaria/versionada, migraciones, privacidad y auditoría técnica | Espera alcance funcional |
| 6 | **REP.1 / #143** | obligatorio 1.0 | PERSIST.1 cerrado + #166 | PDF/exportaciones reales, reproducibles, trazables y auditadas | Espera PERSIST.1 |
| 7 | **DEPLOY.1 / #157** | obligatorio 1.0 | REP.1 cerrado + #166 | runtime/hosting/HTTPS/persistencia/CI-CD/rollback definidos y validados | Espera REP.1 |
| 8 | **UX.7 / #133** | obligatorio 1.0 | #142/derivados + PERSIST/REP/DEPLOY cerrados | Inicio App + login/dashboard Developer terminados | Espera superficies finales |
| 9 | **UX.8 / #134** | obligatorio 1.0 | misma ola UX | entrada Simulación Manual/Asistida terminada | Espera superficies finales |
| 10 | **UX.9 / #177** | obligatorio 1.0 | misma ola UX | Manual Pasos 1–3 terminado | Espera superficies finales |
| 11 | **UX.10 / #178** | obligatorio 1.0 | misma ola UX | Manual Pasos 4–6/resultados terminado | Espera superficies finales |
| 12 | **UX.11 / #179** | obligatorio 1.0 | misma ola UX | Mi Retiro Seguro/import inicial terminado | Espera superficies finales |
| 13 | **UX.12 / #180** | obligatorio 1.0 | misma ola UX | Ficha Digital/revisión/corrección terminado | Espera superficies finales |
| 14 | **UX.13 / #181** | obligatorio 1.0 | misma ola UX | Comparación terminada | Espera superficies finales |
| 15 | **UX.14 / #182** | obligatorio 1.0 | misma ola UX | Metodología pública terminada | Espera superficies finales |
| 16 | **UX.15 / #183** | obligatorio 1.0 | misma ola UX | Cómo se calcula terminado | Espera superficies finales |
| 17 | **UX.16 / #184** | obligatorio 1.0 | PERSIST.1 + DEPLOY.1 | gestión local de datos/privacidad terminada | Espera superficies finales |
| 18 | **UX.17 / #185** | obligatorio 1.0 | REP.1 + DEPLOY.1 | informes/exportación/impresión terminados | Espera superficies finales |
| 19 | **UX.18 / #186** | obligatorio 1.0 | DEPLOY.1 + superficies Developer estables | Diagnóstico/Eventos/Archivos terminados | Espera superficies finales |
| 20 | **UX.19 / #187** | obligatorio 1.0 | PERSIST.1 + DEPLOY.1 | Mantenimiento/Privacidad/Usuarios-RBAC terminados | Espera superficies finales |
| 21 | **UX.20 / #188** | obligatorio 1.0 | DEPLOY.1 | Perfil/credenciales web/acceso técnico existente terminados | Espera superficies finales |
| 22 | **SEC.2 R7 / #144** | obligatorio 1.0 | UX.7–UX.20 cerradas + #166 | threat model y hardening final demostrados | Espera UX final |
| 23 | **Rendimiento / #156** | obligatorio 1.0 | SEC.2 R7 cerrado + deployment estable | línea base reproducible y problemas materiales resueltos | Espera SEC.2 R7 |
| 24 | **A11Y.2 / #145** | obligatorio 1.0 | #156 cerrado + #166 | matriz WCAG 2.2 y AT/reflow/forced-colors/exportaciones validados | Espera rendimiento |
| 25 | **REV.1 / #146** | obligatorio 1.0 | A11Y.2 cerrado + #166 | normativa/jurídica/privacidad/seguridad/terceros finales reconciliados | Espera A11Y.2 |
| 26 | **Settings GitHub / #153** | transversal obligatorio 1.0 | REV.1 cerrado | settings públicos/security/release/deploy revalidados | Sin Global propio mientras siga como gate manual |
| 27 | **DOC.1 R6 / #147** | obligatorio 1.0 | #153 cerrado + #166 | documentación final congelada y coherente | Espera #153 |
| 28 | **QA.1 / #148** | obligatorio 1.0 | todos los obligatorios previos cerrados + #166 | candidato beta final sin defectos bloqueantes conocidos | Espera DOC.1 R6 |
| 29 | **REL.1 / #149** | obligatorio 1.0 | QA.1 cerrado + #166 | build/artefactos/SBOM/firma/tag/Release oficiales publicados | Último bloque |

## 4. Programa UX — decisión explícita

UX.7 y UX.8 **se conservan** y no son absorbidas:

- UX.7/#133 — `/`, `/dev` login y dashboard;
- UX.8/#134 — entrada `/simulacion`, Manual/Asistida y cambio de modalidad.

PLAN.2 R2 materializó UX.9–UX.20 como #177–#188. La ola UX se ejecuta
después de PERSIST.1, REP.1 y DEPLOY.1 porque esas fases crean o estabilizan
superficies que deben auditarse una sola vez en su forma final.

## 5. Trabajo post-1.0

| Issue | Trabajo | Clasificación | Motivo |
| ---: | --- | --- | --- |
| #131 | i18n español + inglés | post-1.0 | 1.0 se entrega en español; arquitectura queda preparada |
| #150 | sesiones/accesos Developer avanzados | post-1.0 | controles actuales bastan para alcance 1.0; añade retención/persistencia nueva |
| #151 | notificaciones Developer | post-1.0 | no es necesaria para operar/cerrar la primera estable |
| #152 | credenciales Bearer granulares | post-1.0 por defecto | solo escala si SEC.2 R7 demuestra necesidad material de seguridad |

#152, si es escalado por SEC.2 R7, debe insertarse y sincronizarse antes de
A11Y.2/REV.1/QA.1, incluyendo su revisión UX correspondiente.

## 6. Trabajo transversal / absorbido / cerrado

| Issue / bloque | Clasificación | Owner / regla |
| --- | --- | --- |
| #166 | transversal permanente | preflight Dependabot, mantenimiento, limpieza y reconciliación por fase |
| MANT.2 R2+ | transversal condicional | se inserta si #166 descubre trabajo material de dependencias |
| DOC.3 | transversal por cadencia | auditoría documental periódica; DOC.4 crea nuevo baseline |
| #176 | absorbido | owner material #174; Issue cerrado sin perder criterios |
| #141 | cerrado | umbrella histórico consumido por PLAN.2 R2 |

## 7. Cadencia DOC.3

El contador se aplica a **fases materiales top-level aceptadas**, no a lotes
internos ni a intentos fallidos.

DOC.4 es una reingeniería integral y, al cerrar, se convierte en nuevo baseline
documental: el contador vuelve a cero. Por defecto se programa una nueva DOC.3
integral después de la segunda fase material aceptada desde ese baseline, salvo
que un evento documental de alto impacto justifique adelantarla y reiniciar de
nuevo el contador.

No se crea ahora DOC.3 R2 y no se reserva Global.

## 8. Opcionales 1.0

**Ninguno identificado.**

PLAN.2 R2 no mantiene trabajo material ambiguo como “quizá 1.0”: o es requisito
pre-1.0, gate transversal, post-1.0, absorbido o cerrado.

## 9. Invariantes de versionado durante planificación

Mientras PLAN.2 R2 no tenga candidato aceptable:

```text
VERSION = 0.1.25.01-beta
current_candidate = unassigned
next_global_available = 126
G126 = libre / no reservado
```

El ledger histórico aceptado permanece hasta G125. El manifest de publicación
permanece anclado a G125 y su `next_step` no debe preasignar bloque/version.

## 10. Autoridades sincronizadas

Esta matriz debe coincidir con:

- [roadmap.md](roadmap.md);
- [master-plan-to-1-0.md](master-plan-to-1-0.md);
- [pre-1-0-revision-ledger.md](pre-1-0-revision-ledger.md);
- `data/governance/pre-1-0-revision-ledger.json`;
- `data/governance/work-block-registry.json`;
- `data/governance/release-publication-manifest.json`;
- `VERSIONING.md`;
- `GOVERNANCE.md`;
- Issues #129–#188 según owner.

## 11. Próxima frontera

Después de validar, aceptar, integrar y publicar PLAN.2 R2, la siguiente fase
material es **VER.2 R6/#164**. Antes de abrirla se repite #166. Si aparece
mantenimiento material de dependencias, MANT.2 R2 se inserta primero y el árbol
se vuelve a sincronizar sin reservar Globals futuros.
