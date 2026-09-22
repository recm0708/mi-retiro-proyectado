# Roadmap

**Estado:** vigente
**Último estado publicado:** G127/E02 — MANT.2 R2
**Versión publicada:** `0.1.27.02-beta`
**`main` publicado de entrada a VER.2 R6:** `2df33a5c24d1c7cea1a6db91539a92da02c91500`
**Siguiente Global aritmético:** G129, libre y no reservado
**Fase en curso:** VER.2 R6 / #164 — G128/E02/C0 `0.128.2.0-beta` aceptado, integración/publicación pendiente
**Fecha de reconciliación:** 2026-09-21

Este roadmap muestra el programa vigente hacia `1.0.0.0`. La historia de estados aceptados permanece en ledger, `RELEASES.md`, `CHANGELOG.md`, tags, GitHub Releases y `docs/archive/`.

## Línea base

G127/E02 — MANT.2 R2 está integrado y publicado como `0.1.27.02-beta`
sobre `main@2df33a5c24d1c7cea1a6db91539a92da02c91500`, mediante PR #207,
tag firmado `v0.1.27.02-beta` y GitHub Release prerelease 392412590.

El preflight #166 posterior a G127 quedó CLEAN y habilitó VER.2 R6/#164.
VER.2 R6 materializó G128/E02/C0 (`0.128.2.0-beta`) mediante Draft PR #208.
G128 aún no está publicado; G129 permanece libre.

<!-- VER2-CP6A-HISTORICAL-ANCHORS:START -->
## Anclas históricas preservadas

Estas líneas son referencias históricas de compatibilidad para auditorías
anteriores; **no describen el estado operativo vigente**:

- DOC.3 R1 fue publicado como **G125/E01**.
- **PLAN.2 R2** fue publicado como **G126/E01**.
- **Versión publicada:** `0.1.26.01-beta` — referencia histórica de PLAN.2 R2.
- **Fase en curso:** MANT.2 R2 / #206 — referencia histórica anterior a la
  publicación G127/E02.
- MANT.2 R2 quedó después publicado como G127/E02 (`0.1.27.02-beta`).
- G128, libre y no reservado — ancla histórica del estado inmediatamente anterior a la materialización CP7.
<!-- VER2-CP6A-HISTORICAL-ANCHORS:END -->

## Árbol vigente hacia `1.0.0.0`

```text
G127 / MANT.2 R2 publicado
→ VER.2 R6
→ DOC.4 R1
→ auditoría previsional #142
→ [fases funcionales obligatorias derivadas, si aparecen]
→ PERSIST.1
→ REP.1
→ DEPLOY.1
→ UX.7
→ UX.8
→ ...
→ UX.x final realmente necesario
→ gate UX/GOV #189 sin drift visual shared
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

El orden expresa dependencias materiales, no Globals futuros supuestos.

## Decisiones principales

### MANT.2 R2 antes de VER.2

MANT.2 R2/#206 reconcilió los PRs Dependabot #204/#205 detectados por el
preflight #166 y quedó cerrado/publicado como G127/E02
(`0.1.27.02-beta`). El preflight posterior #166 quedó CLEAN y habilitó
VER.2 R6/#164, que ya materializó G128/E02/C0 (`0.128.2.0-beta`) y está listo para integración mediante PR #208.

### VER.2 R6 antes de DOC.4

VER.2 R6/#164 reforma primero el contrato revision-aware, parsers, ledger, registry y tooling de Release. DOC.4/Lote C revisa después esos artefactos declarativos sobre el modelo estabilizado.

### DOC.4 antes de #142/PERSIST

DOC.4 R1/#171 ejecuta la reingeniería documental canónica mediante #172/#173/#174. #174 absorbe #176. Al cerrar, DOC.4 se convierte en nuevo baseline documental y reinicia la cadencia de DOC.3.

### #142 antes de PERSIST.1

#142 debe demostrar qué prestaciones/modalidades SEBD/Mixto/SUCGS están realmente cubiertas. Un faltante obligatorio para 1.0 se inserta antes de PERSIST.1. El esquema persistente no se congela con alcance funcional desconocido.

### PERSIST.1 → REP.1 → DEPLOY.1 → UX

PERSIST estabiliza datos; REP materializa informes/exportaciones; DEPLOY fija runtime/hosting/URLs/condiciones operativas. Solo después se ejecuta la auditoría visual final para evitar rehacer superficies.

## Programa UX dinámico

El programa se rige por #129 y la política transversal #189.

**Regla:** una UX.x corresponde a una superficie, paso o modal material suficientemente pequeño para revisarlo al detalle. La numeración es abierta y consecutiva. El baseline conocido es UX.7–UX.32; UX.33+ se crea si antes del cierre aparece una nueva superficie pre-1.0.

### Baseline conocido UX.7–UX.32

| UX | Issue | Superficie |
| --- | ---: | --- |
| UX.7 | #133 | Inicio Asegurado `/` + Inicio/Resumen Developer `/dev` autenticado |
| UX.8 | #134 | Asegurado `/simulacion` — entrada Manual/Asistida antes del Paso 1 |
| UX.9 | #177 | Paso 1 — Datos personales |
| UX.10 | #178 | Paso 2 — Cuotas |
| UX.11 | #179 | Paso 3 — Historial y base salarial |
| UX.12 | #180 | Paso 4 — Proyección y línea temporal |
| UX.13 | #181 | Paso 5 — Escenarios de retiro |
| UX.14 | #182 | Paso 6 — Resultados |
| UX.15 | #183 | Asegurado `/comparar` — Escenarios/Comparación |
| UX.16 | #184 | Asegurado `/como-se-calcula` |
| UX.17 | #185 | Asegurado `/metodologia` — Fuentes/Metodología |
| UX.18 | #186 | modal Términos, privacidad y consentimiento |
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
| UX.32 | #201 | Developer — Centro de desarrollo legacy, si sigue soportado |

UX.7 es la única agrupación deliberada: revisa las dos superficies de Inicio por compartir la identidad de entrada de ambos portales. El login Developer se audita aparte en UX.23.

### Regla de expansión UX.33+

Si #142/derivados, PERSIST.1, REP.1, DEPLOY.1 o una UX previa crea/descubre una nueva superficie visual material:

1. se crea la siguiente UX consecutiva;
2. recibe Issue propio con alcance y criterio de cierre;
3. se actualizan #129, #155 y fuentes vivas antes de continuar;
4. se aplica #189;
5. no se renumeran UX existentes;
6. no se preasigna Global/VERSION.

## Sincronización visual multiportal — #189

#189 es transversal y no consume Global propio. Todo cambio visual debe clasificarse como `shared` o `portal-specific`.

Cuando sea shared debe sincronizarse en App Asegurado, Portal Developer y futuros portales aplicables. Esto incluye especialmente tokens/paleta, tipografía, tamaños/pesos, colores de texto, botones, inputs, tarjetas, tablas genéricas, badges/alerts, spacing, bordes/radios/sombras, foco, temas Claro/Oscuro/Automático/Alto contraste, forced-colors, motion, selector de apariencia, footer y patrones visuales comunes.

Una UX.x no puede cerrar si dejó otro portal desincronizado por un cambio shared. Si una dependencia real impide resolverlo en la misma fase, debe crear un Issue derivado bloqueante antes del cierre.

## Gate antes de SEC.2 R7

SEC.2 R7 no se habilita por alcanzar UX.32. Se habilita cuando:

- todas las UX.x obligatorias registradas estén cerradas o absorbidas explícitamente;
- no quede superficie visual material pre-1.0 sin UX owner/clasificación;
- no exista derivado bloqueante de sincronización shared;
- #189 confirme ausencia de drift visual shared conocido.

## Gates finales

Después del cierre real de UX.7→UX.x: SEC.2 R7 endurece el producto/deployment; #156 mide rendimiento; A11Y.2 audita WCAG 2.2; REV.1 revisa normativa/jurídica/privacidad; #153 revalida settings GitHub; DOC.1 R6 congela documentación; QA.1 valida el candidato; REL.1 publica 1.0.

## Trabajo post-1.0

No bloquean `1.0.0.0`:

- i18n #131;
- sesiones/accesos Developer avanzados #150;
- notificaciones Developer #151;
- credenciales Bearer granulares #152 por defecto.

#152 puede escalarse si SEC.2 R7 demuestra necesidad material. Si ese escalamiento introduce una superficie visible, debe crear una nueva UX.x antes de continuar.

## Políticas transversales

- **#166:** preflight/limpieza antes y después de cada fase; puede insertar MANT.2 R3+ si aparece trabajo material nuevo.
- **DOC.3:** auditoría documental periódica; DOC.4 crea nuevo baseline/reset.
- **#189:** sincronización visual multiportal y expansión UX.x.
- **#153:** revalidación final de settings GitHub.

## Clasificación

- **Intermedio obligatorio cerrado:** MANT.2 R2/#206, insertado por #166 y publicado como G127/E02.
- **Obligatorios 1.0:** #164, #171–#174, #142 y derivados obligatorios, #130, #143, #157, #129 y todas sus UX.x, #144, #156, #145, #146, #147, #148 y #149.
- **Transversales obligatorios:** #166, #189, #153 y DOC.3 por cadencia.
- **Post-1.0:** #131 y #150–#152.
- **Absorbido:** #176 → #174.
- **Cerrado/consumido:** #141.
- **Opcionales 1.0 sin owner material:** ninguno.

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

La fase material activa es VER.2 R6/#164 con G128/E02/C0 (`0.128.2.0-beta`) aceptado localmente; G129 permanece libre y sin candidato. Después de publicar VER.2 corresponde DOC.4 R1/#171, salvo que un preflight #166 obligue a insertar MANT.2 R3+.
