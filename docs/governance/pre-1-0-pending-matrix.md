# Matriz maestra de pendientes hacia 1.0

**Estado:** vigente / documento vivo
**Baseline publicado:** G129/E03/C0 — `0.129.3.0-beta`
**Fase material activa:** DOC.4 R1 / #171
**Siguiente Global aritmético:** G130, libre y sin candidato
**Objetivo:** `1.0.0.0`

## 1. Función

Esta matriz es la autoridad tabular del **trabajo todavía pendiente** hacia
`1.0.0.0`.

Los estados ya cerrados no se mantienen como filas “pendientes”; su evidencia
está en ledger, Releases, Git e Issues cerradas.

## 2. Reglas

1. Todo pendiente tiene owner y dependencia identificables.
2. No se preasignan Globals o `VERSION` a trabajo planificado.
3. Una fase activa puede existir con `current_candidate = unassigned`.
4. Trabajo material nuevo se inserta antes de continuar.
5. #166 puede insertar MANT.2 cuando aparezca deuda material de dependencias.
6. Los lotes internos de DOC.4 no consumen Globals propios.
7. DOC.3 se ejecuta por cadencia, no por reserva anticipada.
8. UX.7–UX.32 es el baseline conocido; UX.33+ se crea si aparece otra
   superficie pre-1.0.
9. #189 gobierna sincronización visual multiportal.
10. Roadmap, plan maestro, registry, ledger e Issues deben coincidir.

## 3. Grafo canónico

```text
DOC.4 R1
→ #142 auditoría previsional
→ [derivados funcionales obligatorios, si existen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7 → UX.x final necesario
→ #189 sin drift shared
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

#166, #203, #214, DOC.3 y #189 son transversales.

## 4. Pendientes obligatorios pre-1.0

| Orden | Identificador / Issue | Clasificación | Dependencia | Criterio principal de cierre | Estado actual |
| ---: | --- | --- | --- | --- | --- |
| 1 | DOC.4 R1 / #171 | obligatorio 1.0 | G129 publicado + #166 CLEAN | corpus documental/no ejecutable current-state-only, autoridades y árbol reconciliados | **En ejecución**; sin Global asignado |
| 1A | DOC.4 Lote A / #172 | interno DOC.4 | #171 activo | 100 % Markdown revisado 1:1 | En ejecución |
| 1B | DOC.4 Lote B / #173 | interno DOC.4 | decisiones documentales | poda/movimientos/fusiones/renombres/enlaces reconciliados | En ejecución |
| 1C | DOC.4 Lote C / #174 | interno DOC.4 | #171 activo | artefactos declarativos reconciliados; #176 absorbido | En ejecución |
| 1D | Saneamiento / #209 | interno DOC.4 | #171 activo | rutas/nombre heredado/.venv clasificados y saneados | En ejecución; parte local pendiente |
| 1E | Guardas documentales / #215 | interno DOC.4 | cambios de Lotes A/B/C | tests/auditores protegen invariantes actuales sin reinstalar historia | En ejecución |
| 2 | Auditoría previsional / #142 | obligatorio 1.0 | DOC.4 cerrado/publicado + #166 | cobertura SEBD/Mixto/SUCGS demostrada; faltantes con owner | Espera DOC.4 |
| 2.x | Derivados de #142 | condicional obligatorio | hallazgo material #142 | prestación/modalidad requerida implementada y probada | Se crean solo si existe necesidad |
| 3 | PERSIST.1 / #130 | obligatorio 1.0 | #142 + derivados + #166 | persistencia voluntaria/versionada, migraciones y auditoría técnica | Espera alcance funcional |
| 4 | REP.1 / #143 | obligatorio 1.0 | PERSIST.1 + #166 | informes/exportaciones reales y reproducibles | Espera PERSIST.1 |
| 5 | DEPLOY.1 / #157 | obligatorio 1.0 | REP.1 + #166 | runtime/hosting/HTTPS/CI-CD definidos | Espera REP.1 |
| 6…x | Programa UX / #129 | obligatorio 1.0 | #142/derivados + PERSIST + REP + DEPLOY | todas las UX.x necesarias cerradas y sin superficies huérfanas | Baseline UX.7–UX.32; extensible |
| x+1 | UX/GOV / #189 | transversal UX | durante toda la ola UX | sin drift shared ni derivados bloqueantes | Política activa |
| x+2 | SEC.2 R7 / #144 | obligatorio 1.0 | UX completa + #189 + #166 | hardening final | Espera UX |
| x+3 | Rendimiento / #156 | obligatorio 1.0 | SEC.2 R7 | línea base reproducible y problemas materiales resueltos | Espera SEC.2 |
| x+4 | A11Y.2 / #145 | obligatorio 1.0 | #156 + #166 | auditoría accesibilidad final | Espera rendimiento |
| x+5 | REV.1 / #146 | obligatorio 1.0 | A11Y.2 + #166 | revisión normativa/jurídica/privacidad/terceros | Espera A11Y.2 |
| x+6 | Settings GitHub / #153 | transversal final | REV.1 | configuración revalidada | Espera REV.1 |
| x+7 | DOC.1 R6 / #147 | obligatorio 1.0 | #153 + #166 | freeze documental final | Espera #153 |
| x+8 | QA.1 / #148 | obligatorio 1.0 | todos los previos + #166 | candidato beta final sin bloqueantes | Espera DOC.1 R6 |
| x+9 | REL.1 / #149 | obligatorio 1.0 | QA.1 + #166 | Build/SBOM/firma/tag/Release oficiales | Último bloque |

## 5. Baseline UX conocido

### Inicio y simulación

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.7 | #133 | Inicio Asegurado `/` + Inicio/Resumen Developer `/dev` autenticado |
| UX.8 | #134 | `/simulacion` — entrada y selección Manual/Asistida |
| UX.9 | #177 | Paso 1 — Datos personales |
| UX.10 | #178 | Paso 2 — Cuotas |
| UX.11 | #179 | Paso 3 — Historial y base salarial |
| UX.12 | #180 | Paso 4 — Proyección y línea temporal |
| UX.13 | #181 | Paso 5 — Escenarios de retiro |
| UX.14 | #182 | Paso 6 — Resultados |

### Otras superficies Asegurado

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.15 | #183 | `/comparar` |
| UX.16 | #184 | `/como-se-calcula` |
| UX.17 | #185 | `/metodologia` |
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

UX.7 mantiene la agrupación deliberada ya definida para las dos páginas de
Inicio. El login Developer conserva UX.23 propia.

## 6. Expansión UX.33+

Si #142/derivados, PERSIST.1, REP.1, DEPLOY.1 o una UX descubre/crea otra
superficie material:

1. crear la siguiente UX consecutiva;
2. crear Issue propietario;
3. actualizar #129 y autoridades vivas;
4. aplicar #189;
5. no renumerar UX existentes;
6. no preasignar Global/VERSION.

## 7. Gate de salida UX

La ola UX termina cuando:

- todas las UX.x obligatorias están cerradas/absorbidas;
- ninguna superficie pre-1.0 carece de owner;
- no existe derivado bloqueante shared;
- #189 confirma ausencia de drift shared conocido;
- todo hallazgo fuera de alcance tiene owner.

Solo entonces se habilita SEC.2 R7.

## 8. Políticas y trabajo transversal

| Issue / bloque | Función | Global propio |
| --- | --- | --- |
| #166 | preflight Dependabot/limpieza por fase | No |
| #203 | workspace remoto, SYNC POINTS y transferencia canónica | No |
| #214 | briefing/aprobación antes de una fase nueva | No |
| DOC.3 | auditoría documental por cadencia | Solo si materializa una fase propia aceptada |
| #189 | sincronización visual multiportal | No |
| #153 | settings GitHub final | No mientras sea gate manual |
| #176 | absorbido por #174 | No |

## 9. Post-1.0

| Issue | Trabajo | Estado programático |
| ---: | --- | --- |
| #131 | i18n español/inglés | post-1.0 |
| #150 | sesiones/accesos Developer avanzados | post-1.0 |
| #151 | notificaciones Developer | post-1.0 |
| #152 | Bearer granular | post-1.0 por defecto; escalable por SEC.2 R7 |

Si una capacidad se escala a pre-1.0 y crea UI, recibe también una UX.x.

## 10. Cadencia DOC.3

DOC.4 crea un nuevo baseline y reinicia el contador de cadencia documental.

La siguiente DOC.3 integral ocurre por defecto después de la segunda fase
material top-level aceptada desde ese baseline, salvo impacto alto que
justifique adelanto. No se reserva ahora una DOC.3 futura ni un Global.

## 11. Invariantes actuales

```text
VERSION = 0.129.3.0-beta
accepted_baseline = G129/E03/C0 / MANT.2 R3
active_phase = DOC.4 R1 / #171
current_candidate = unassigned
next_global_available = 130
G130 = libre / sin bloque / sin VERSION
```

El manifest vigente corresponde al estado G129 y su `next_step` debe describir
la situación posterior a la publicación sin convertir G130 en candidato.

## 12. Próxima frontera

La siguiente fase ordinaria después de DOC.4 es #142. Antes de abrirla debe
existir cierre/publicación de DOC.4 y un preflight #166 fresco que la habilite.

Si #166 detecta mantenimiento material, ese trabajo se inserta antes de #142.
