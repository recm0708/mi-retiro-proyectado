# Línea base de ownership y estructura NOR.3 R1

**Proyecto:** Mi Retiro Proyectado

**Fase:** NOR.3 R1 — Inventario y contrato estructural

**Issue umbrella:** #126

**Issues estructurales:** #127 y #128

**Base:** `eb4795007ac16807661eaace675a093ee19cbf49`

**Rama:** `feat/nor3-r1-inventario-estructural`

**Estado material aceptado:** G121/E01 — `0.1.21.01-beta`

**Candidato reservado/no aceptado:** NOR.3 R1 — G122/E01 — `0.1.22.01-beta`

**Estado de esta evidencia:** inventario y decisiones estructurales; no ejecuta movimientos físicos.

## Objetivo

NOR.3 R1 fija la frontera de ownership del repositorio antes de cualquier
migración física. La fuente de verdad de esta revisión es el árbol versionado
obtenido mediante `git ls-files`, complementado con análisis AST, consumidores
de templates/assets, imports Python y revisión manual de los casos ambiguos.

El inventario automatizado asociado se conserva en
`repository-ownership-inventory-nor3-r1.txt`.

SHA-256 del inventario de precisión original:

`8a8594209bd653e4f08c5e84839547a996cb9dc92bdc98e8578bf453eddf3cb1`

## Línea base cuantitativa

- archivos versionados: **613**;
- rutas FastAPI detectadas: **55**;
- rutas App Asegurado: **24**;
- rutas Portal Developer: **29**;
- rutas Shared/Platform: **2**;
- templates runtime auditados: **29**;
- assets runtime auditados: **44**;
- tests auditados: **207**;
- directorios auditados: **59**;
- `app/main.py`: **3227 líneas**, **77 símbolos top-level**;
- profundidad máxima observada: **6**, concentrada principalmente en fuentes
  regulatorias oficiales.

R1 no interpreta profundidad alta como error por sí misma.

## Taxonomía de ownership

### App Asegurado

Superficies HTTP, templates y assets exclusivos de la experiencia pública de
simulación, comparación, metodología, cálculo, importación, privacidad,
resultados y demás flujos del asegurado.

### Portal Developer

Login humano Developer, sesiones, identidad, provisioning, almacenamiento,
RBAC, auditoría de usuarios, mantenimiento, diagnóstico, archivos, perfil,
acceso técnico y demás superficies `/dev`.

### Shared multiportal

Solo recursos consumidos realmente por App Asegurado y Portal Developer o que
constituyen contrato visual/plataforma común: Design System, marca, temas,
accesibilidad, motion, shell primitives y partials realmente reutilizados.

`shared` no se utiliza para almacenar código simplemente porque no tenga un
owner evidente.

### Dominio

Motores previsionales, modelos y servicios de negocio. Se consideran dominio
compartido de producto, pero **no** se trasladan automáticamente al namespace
Shared multiportal.

### Platform

Configuración, observabilidad y versionado transversal del runtime.

### Tooling / Governance / Security

Automatización, release governance, auditorías, políticas, workflows y pruebas
transversales que no pertenecen a un portal funcional concreto.

## Matriz backend

| Ruta actual | Owner | Consumidores principales | Decisión R1 | Revisión |
| --- | --- | --- | --- | --- |
| `app/main.py` | Mixto transicional | 55 rutas y 31 tests/importadores detectados | Reducir a composition root; separar routers sin cambiar URLs | R3 |
| rutas `/`, `/simulacion`, `/comparar`, `/metodologia`, `/como-se-calcula`, `/api/simulacion/*` | App Asegurado | templates, JS y servicios de dominio | Extraer a router/controlador Asegurado | R3 |
| rutas `/dev*` | Portal Developer | módulos Developer, templates Developer y tests | Extraer a router/controlador Developer | R3 |
| `/favicon.ico`, `/salud` | Platform | navegador / health checks | Mantener como endpoints de plataforma/composición | R3 |
| `app/core/admin_security.py` | Portal Developer | `main.py`, tests SEC.2 | Mover fuera de `core/` | R3 |
| `app/core/admin_session.py` | Portal Developer | `main.py`, Developer/SEC/UX tests | Mover fuera de `core/` | R3 |
| `app/core/developer_avatar.py` | Portal Developer | `main.py`, Developer tests | Mover a namespace Developer | R3 |
| `app/core/developer_identity.py` | Portal Developer | CLI, módulos Developer, tests | Mover a namespace Developer | R3 |
| `app/core/developer_provisioning.py` | Portal Developer | CLI, Developer, tests | Mover a namespace Developer | R3 |
| `app/core/developer_store.py` | Portal Developer | Developer modules, `main.py`, tests | Mover a namespace Developer | R3 |
| `app/core/developer_user_admin.py` | Portal Developer | `main.py`, UX.6 tests | Mover a namespace Developer | R3 |
| `app/core/developer_user_audit.py` | Portal Developer | user-admin, `main.py`, tests | Mover a namespace Developer | R3 |
| `app/core/developer_web_security.py` | Portal Developer | `main.py`, Developer tests | Mover a namespace Developer | R3 |
| `app/services/development_center.py` | Portal Developer | `main.py`, Developer tests | Mover a namespace Developer | R3 |
| `app/cli/admin.py` | Portal Developer / entry point | CLI documentada y tests | Conservar entry point o wrapper estable; delegar implementación Developer | R3 |
| `app/core/pdf_files.py` | App Asegurado / API boundary | endpoints PDF de simulación | Mover al boundary Asegurado; no promover a Shared | R3 |
| `app/core/constants.py` | Sin consumidor | ninguno detectado | Eliminar si la verificación final confirma ausencia de import dinámico | R3 |
| `app/core/config.py` | Platform | runtime y gobierno/versionado | Conservar en `core/` | R3 |
| `app/core/observability.py` | Platform | App, Developer y diagnóstico | Conservar transversal | R3 |
| `app/core/version.py` | Platform | runtime, tests y documentación | Conservar transversal | R3 |
| `app/core/version_ledger.py` | Tooling/Governance | tests revision-aware | Conservar ruta por compatibilidad durante NOR.3 | R3/R7 |
| `app/core/money.py` | Dominio | engines/models/services | Conservar; no convertir en Shared multiportal | R3 |
| `app/core/normativa.py` | Dominio | engines/services | Conservar; no convertir en Shared multiportal | R3 |
| `app/engines/` | Dominio | App APIs y servicios | Conservar estructura | R3 |
| `app/models/` | Dominio | engines/services/tests | Conservar estructura | R3 |
| servicios previsionales en `app/services/` | Dominio | App APIs y otros servicios | Conservar salvo owner exclusivo demostrado | R3 |

### Arquitectura backend objetivo

La forma objetivo inicial queda fijada como:

```text
app/
├── core/                       # Platform transversal
├── engines/                    # Dominio
├── models/                     # Dominio
├── services/                   # Servicios de dominio no exclusivos
├── portals/
│   ├── asegurado/
│   │   └── router.py
│   └── developer/
│       ├── router.py
│       └── ...                 # identidad, sesión, store, RBAC, etc.
└── main.py                     # composition root
```

No se obliga a que toda utilidad de dominio se traslade a `shared/`.

## Matriz de templates

### App Asegurado — R4

Mover bajo `app/templates/asegurado/`:

- `base.html`;
- `index.html`;
- `simulation.html`;
- `comparison.html`;
- `methodology.html`;
- `calculation_guide.html`;
- partials de preparación asistida;
- detalle del año actual;
- gestión de datos;
- Ficha Digital;
- referencia Mi Retiro Seguro;
- importación oficial;
- consentimiento/privacidad;
- resultados;
- retiro;
- historial salarial.

`base.html` **no es Shared**. La clasificación automatizada inicial fue un falso
positivo causado por la coincidencia textual `base.html` dentro de
`dev_base.html`.

`partials/mi_retiro_seguro_reference.html` pertenece semánticamente a App
Asegurado, pero no presentó consumidor runtime directo en el inventario.
R4 debe verificar si continúa siendo una superficie cargada indirectamente o
si quedó huérfana antes de conservarla.

### Portal Developer — R4

Mover bajo `app/templates/developer/`:

- `dev_base.html`;
- `dev_dashboard.html`;
- `dev_development_center.html`;
- `dev_diagnostics.html`;
- `dev_events.html`;
- `dev_files.html`;
- `dev_login.html`;
- `dev_maintenance.html`;
- `dev_privacy.html`;
- `dev_profile.html`;
- `dev_technical_access.html`;
- `dev_users.html`.

Los prefijos redundantes `dev_` pueden retirarse dentro del namespace
`developer/` siempre que templates, tests y referencias se actualicen en el
mismo lote.

### Shared — R4

- `partials/global_footer.html`.

Es el partial con evidencia directa de consumo por ambos shells.

## Matriz de assets

### Shared multiportal — R5

CSS:

- `accessibility.css`;
- `brand.css`;
- `design-system.css`;
- `motion.css`.

JavaScript:

- `accessibility.js`;
- `datetime_ui.js`;
- `interaction_ui.js`;
- `shell_state_boot.js`;
- `shell_ui.js`;
- `theme.js`.

Marca runtime:

- todos los derivados de `app/static/img/brand/`.

Estos recursos mantienen autoridad única; no se duplican por portal.

### Portal Developer — R5

- `developer-portal.css`;
- `developer_forms.js`;
- `developer_portal.js`.

### App Asegurado — R5

CSS:

- `calculation-guide.css`;
- `editable-provenance.css`;
- `results.css`.

JavaScript:

- `app_shell.js`;
- `assisted_flow.js`;
- `attachment_processing.js`;
- `comparator.js`;
- `currency.js`;
- `current_year_detail.js`;
- `data_management.js`;
- `editable_provenance.js`;
- `mi_retiro_seguro_reference.js`;
- `official_data_import.js`;
- `privacy.js`;
- `results.js`;
- `results_orchestration.js`;
- `retirement.js`;
- `salary_history.js`;
- `simulation.js`;
- `simulation_mode.js`;
- `timeline.js`;
- `wizard_navigation.js`.

### Asset transicional

`app/static/css/style.css` es consumido por ambos shells, pero el consumo doble
no demuestra que todo su contenido sea multiportal.

**Decisión:** R5 debe separar las reglas realmente comunes de las reglas
específicas de App Asegurado antes de decidir su ubicación final. No se mueve
el archivo completo a Shared por conveniencia.

## Tests

Se auditaron los **207 tests** antes de autorizar R6.

El inventario conserva ownership por consumidores y distingue:

- App Asegurado;
- Portal Developer;
- Shared;
- integraciones entre owners;
- Tooling/Governance;
- Security;
- regresiones históricas.

Los 14 casos que la heurística inicial dejó sin clasificación fueron revisados
manualmente.

### Resoluciones manuales

| Test | Clasificación R1 |
| --- | --- |
| `test_identidad_publica_github_pre_r8.py` | Tooling/Governance — publicación e identidad pública |
| `test_post_sec2_integral_audit.py` | Security / regresión transversal |
| `test_sec2_r1_codeql_workflow_hardening.py` | Security / integración |
| `test_ux46d_revision22_cierre_paso3.py` | App Asegurado |
| `test_ux46e_auditoria_coherencia.py` | Tooling/Governance / gate transversal |
| `test_ux46e_estandar_runtime.py` | Repository/Governance |
| `test_ux46e_preparacion_publica.py` | Tooling/Governance con integración App |
| `test_ux46e_r81_editable_provenance.py` | App Asegurado |
| `test_ux46e_r8_cierre_funcional.py` | Regression / cierre histórico |
| `test_ux46e_r8_reconsentimiento_borrado.py` | App Asegurado |
| `test_ux46e_renumeracion_documental.py` | Tooling/Governance |
| `test_ux46h_r1_resultados_exportacion.py` | App Asegurado |
| `test_ux6_r5_r6_manual_privacy_scope.py` | App Asegurado |
| `test_ux6_r5_r6_public_terms_final.py` | App Asegurado |

R6 organizará por propósito y ownership, no únicamente por prefijo histórico.

Objetivo orientativo aceptado:

```text
tests/
├── domain/
├── portals/
│   ├── asegurado/
│   └── developer/
├── shared/
├── repository/
├── governance/
├── security/
├── regression/
└── validation_cases/
```

Los nombres históricos que aporten trazabilidad pueden conservarse dentro de
su nuevo namespace.

## Directorios y profundidad

Se auditaron **59 directorios**.

### Single-child preservados

Se preservan por frontera semántica:

- `app/static/img/` → `brand/`;
- `assets/social/`;
- `docs/regulatory/sources/` → `official/`;
- `docs/regulatory/sources/official/pensions/reference/`;
- `docs/regulatory/sources/official/privacy/` → `normative/`;
- `tests/validation_cases/`.

`tests/validation_cases/` se conserva porque #128 lo define expresamente como
namespace estructural previsto.

### Profundidad regulatoria

Las rutas de profundidad 6 bajo
`docs/regulatory/sources/official/...` son una excepción justificada por:

- procedencia;
- dominio;
- naturaleza normativa o de referencia;
- preservación de fuente oficial.

NOR.3 no fija una profundidad máxima universal.

## Data — R7

| Ruta actual | Clasificación | Decisión |
| --- | --- | --- |
| `data/pre-1-0-revision-ledger.json` | Governance | mover a `data/governance/` con consumidores reconciliados |
| `data/release-publication-manifest.json` | Governance | mover a `data/governance/` |
| `data/work-block-registry.json` | Governance | mover a `data/governance/` |
| `data/doc2-legacy-changelog-evidence.json` | Audit evidence | mover a `data/audits/` |
| `data/git-history-attestation.json` | Audit evidence | mover a `data/audits/` |
| `data/.gitkeep` | Residuo | eliminar cuando se materialice la nueva estructura |

No se inicia ni se implementa `data/developer/` como parte de PERSIST.1.

## Scripts — R7

Los scripts actuales son entry points canónicos con consumidores en workflows,
hooks, documentación y tests.

**Decisión R1:** conservar `scripts/` plano durante NOR.3 salvo que R7 demuestre
una ganancia semántica concreta. No se crean subdirectorios únicamente para
reducir cantidad de archivos.

`scripts/package.json` y `scripts/package-lock.json` permanecen junto al tooling
Node/Playwright de auditoría visual.

## Raíz y tooling

Se conservan como raíces autorizadas:

- `.githooks/`;
- `.github/`;
- `.vscode/`;
- `app/`;
- `assets/`;
- `data/`;
- `docs/`;
- `regulations/`;
- `scripts/`;
- `tests/`.

`assets/` conserva fuentes/masters y derivados de publicación; no es equivalente
a `app/static/`, que contiene assets runtime.

`regulations/` conserva configuración normativa consumida por el dominio.

`requirements.txt` y `requirements-dev.txt` permanecen separados.

No se introduce `pyproject.toml` en NOR.3 sin una mejora contractual
independientemente justificada.

## Secuencia NOR.3 fijada por R1

- **R1:** inventario, ownership, consumidores y contrato estructural.
- **R2:** política machine-readable y gates.
- **R3:** backend Developer/Asegurado/Platform y reducción de `main.py`.
- **R4:** templates.
- **R5:** CSS/JS/img.
- **R6:** tests.
- **R7:** data, scripts y aplanamiento semántico justificado.
- **R8:** documentación, auditoría integral #154 y cierre.

El bootstrap de gobierno #135–#140/#158 se ejecuta temprano dentro de NOR.3,
sin absorber PERSIST.1 ni UX.7+.

## Exclusiones R1

R1 no:

- implementa PERSIST.1;
- consume G122;
- modifica `VERSION`;
- inicia UX.7 o UX.8;
- mueve físicamente módulos/templates/assets/tests/data;
- reescribe `docs/archive/`;
- impone profundidad máxima ciega;
- duplica Design System por portal.

## Resultado de R1

La arquitectura deja de depender de nombres heurísticos para determinar
ownership.

Los movimientos posteriores deben actualizar consumidores en el mismo lote y
mantener:

- las 55 rutas HTTP vigentes;
- imports o wrappers compatibles;
- CLI documentada;
- rutas Jinja;
- Design System único;
- temas y accesibilidad;
- `unittest` y pytest;
- trazabilidad histórica.

R1 queda listo para validación y para abrir R2 únicamente después de aceptar
formalmente esta evidencia.
