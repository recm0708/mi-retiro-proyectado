# Matriz maestra de pendientes hacia 1.0

**Estado:** vigente / documento vivo
**Versión base:** `0.1.23.01-beta` — G123/E01 MANT.2 R1 integrado/aceptado; publicación formal pendiente
**Checkpoint candidato:** G123/E01 quedó integrado/aceptado mediante PR #168; G124 queda disponible sin bloque/candidato; MANT.1 R8/#163 continúa después de publicar G123
**Última replanificación:** 2026-09-14 — MANT.2 R1/G123 integrado y revalidado post-merge; publicación formal pendiente; DOC.3 R1 y PLAN.2 R2 permanecen como fases materiales posteriores a MANT.1 R8.
**Clasificación:** Planificación / Producto / Arquitectura / Seguridad / QA / Release


<!-- NOR3-G122-PROMOTION:START -->
## Estado post-NOR.3 / promoción G122-E01

- `VERSION` materializa `0.1.22.01-beta` para NOR.3 R8 / G122-E01.
- NOR.3 R1–R8 quedó integrado/aceptado mediante PR #162 / merge
  `b97cf61763479b80b8e8724b878089e8bb20fa00`.
- La revalidación automática de `main` quedó GREEN: Repository Quality Gate,
  Visual & Accessibility y CodeQL finalizaron en `success`.
- G123 es el siguiente Global disponible, pero **no tiene candidato ni bloque
  preasignado**.
- PERSIST.1 permanece planificado y no iniciado, sin Global preasignado.
- `v0.1.21.01-beta` / G121/E01 permanece como última publicación revision-aware
  hasta completar el tag/release firmado de G122/E01.
- `v0.1.22.01-beta` queda pendiente de creación/firma local y de la
  verificación/publicación gobernada por REL.GOV.1.
<!-- NOR3-G122-PROMOTION:END -->

Esta matriz ordena el trabajo pendiente antes de la primera versión oficial de
Mi Retiro Proyectado. Debe actualizarse cuando un bloque se inicia, cambia de
alcance, se divide justificadamente, se cierra o aparece una necesidad nueva
que deba resolverse antes de `1.0.0.0`.

La matriz **no preasigna Globales futuros** más allá del candidato vigente.
Cada estado material aceptado consume su `G` conforme a `VERSIONING.md`; un
candidato fallido no lo consume.

## 1. Reglas de uso

1. `VERSION` materializa `0.1.23.01-beta` al consolidar MANT.2 R1 como G123/E01.
2. G123/E01 queda integrado/aceptado mediante PR #168 / merge `1a3942a6c14ab047fe8bc587c21b9b96cf62f2bd`.
3. G124 es únicamente el siguiente Global disponible; no tiene candidato ni bloque preasignado.
4. PERSIST.1 permanece planificado y sin Global preasignado; no puede iniciar hasta completar #163 → #154 → #155 → #164.
5. Las etapas posteriores se ordenan por prioridad, no por un `G` futuro supuesto.
6. Una revisión que amplía un bloque existente conserva su identificador canónico.
7. Todo bloque usado por la planificación viva debe existir en el registro machine-readable.
8. La historia cerrada permanece preservada y no se moderniza mecánicamente.
9. Cambiar el orden o alcance exige sincronizar esta matriz, roadmap, plan maestro,
   registro y ledger cuando corresponda.

<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:START -->
## Secuencia intermedia obligatoria post-NOR.3

MANT.2 R1 / Issue #167 se materializa como **G123/E01**
(`0.1.23.01-beta`) para resolver el lote Dependabot detectado después de G122.
La integración coordinada quedó completada mediante PR #168 / merge
`1a3942a6c14ab047fe8bc587c21b9b96cf62f2bd`; `main` fue revalidado con
0 Dependabot alerts abiertos y checks remotos verdes. La publicación formal
queda pendiente únicamente del tag firmado y GitHub Release prerelease.

Después de publicar G123/MANT.2 R1 y antes de iniciar PERSIST.1, la continuidad
material queda fijada así:

1. **MANT.1 R8 — Issue #163:** auditoría, consolidación y saneamiento operativo
   post-NOR.3 de `scripts/`, `tests`, labels y estructura técnica.
2. **DOC.3 R1 — Issue #154:** auditoría documental integral.
3. **PLAN.2 R2 — Issue #155:** replanificación maestra hacia 1.0.
4. **VER.2 R6 — Issue #164:** reforma del versionado beta y del componente
   futuro dedicado a fases MANT.2/Dependabot.
5. **PERSIST.1 — Issue #130:** bloqueado hasta completar toda la secuencia.

G124 queda únicamente como siguiente Global disponible y no se asigna por
adelantado. Antes de iniciar cada fase futura se repite el preflight Dependabot;
un lote material nuevo inserta MANT.2 R2+.
<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->

## 2. Matriz maestra

| Orden | Identificador | Trabajo pendiente | Alcance / criterio de cierre | Estado |
| ---: | --- | --- | --- | --- |
| 1 | **PLAN.2 R1** | Replanificación maestra final hacia 1.0 | Formalizar esta matriz, registrar PLAN.2/UX.5, corregir la reserva G114 y reconciliar documentación viva post-G113. | **Cerrado/aceptado G114/E01** |
| 2 | **DOC.1 R4** | Saneamiento documental post-G113 | Corregir metadata viva, estados desactualizados y contradicciones actuales sin reescribir evidencia histórica. | **Cerrado/aceptado G115/E04** |
| 3 | **DOC.1 R5** | Normalización documental integral post-G115 | Reconciliar publicación G115, humanizar navegación Markdown, completar estándares/plantillas y añadir controles de regresión sin reescribir historia. | **Cerrado/aceptado G116/E05** |
| 4 | **REL.GOV.1 R2** | Automatización de Releases y checks | Estandarizar release notes, `gh release create`, verificación de tag/firma y lectura correcta de Actions/checks. | **Cerrado/aceptado G117/E02** |
| 5 | **DEV.2 R5** | Portal Developer y acceso | `/dev` canónico; sesión web separada de Bearer; shell/login Developer; cookie acotada a `/dev`; secretos no persistidos. | **Cerrado/aceptado G118/E04** |
| 6 | **DEV.2 R6** | Portal Developer multipágina y mantenimiento | Separar `/dev`, `/dev/diagnostico`, `/dev/eventos`, `/dev/archivos`, `/dev/mantenimiento`, `/dev/privacidad`, perfil y acceso técnico; añadir identidad persistente, RBAC, ZIP diagnóstico, filtros, métricas y mantenimiento seguro. | **Cerrado/aceptado/publicado G119/E05** |
| 7 | **UX.5 R1** | Sistema visual integral | Nueva base visual: paleta, tipografía, espaciado, botones, tarjetas, estados, jerarquía y tokens reutilizables. | **Completado dentro de G120/E01 aceptado** |
| 8 | **UX.5 R2** | Inicio, navegación y temas | Rediseñar Inicio/navegación y armonizar Claro, Oscuro, Automático y Alto contraste. | **Completado dentro de G120/E01 aceptado** |
| 9 | **UX.5 R3** | Nueva entrada a Simulación | Preguntar antes del Paso 1 si la preparación será **Manual** o **Asistida** y explicar ambas modalidades. | **Completado dentro de G120/E01 aceptado** |
| 10 | **UX.5 R4** | Flujo Manual | Mantener y mejorar el recorrido completo de Pasos 1–6 con revisión explícita de los datos. | **Completado dentro de G120/E01 aceptado** |
| 11 | **UX.5 R5** | Flujo Asistido | Procesar Mi Retiro Seguro y Ficha Digital, exigir revisión y confirmar al menos una fuente antes de habilitar el recorrido compartido. | **Completado dentro de G120/E01 aceptado** |
| 12 | **UX.5 R6** | Integración y cierre funcional UX.5 | Unificar Manual/Asistido, invalidación, navegación, completitud, errores, loaders, cambio de modalidad, resultados y consistencia de assets. | **Cerrado/aceptado G120/E01** |
| 13 | **UX.6 R1–R8** | Auditoría integral App + Developer | Identidad/shell, perfil/avatar, usuarios/RBAC, movimiento, accesibilidad, responsive, importadores, privacidad pública, ownership y hardening final. | **Cerrado/aceptado G121/E01** |
| 14 | **NOR.3 R1–R8** | Normalización estructural integral | Inventario/ownership, policy, backend/portales, templates, assets, tests, data/scripts y cierre documental según #126/#127/#128. | **Cerrado/aceptado G122/E01** |
| 15 | **MANT.2 R1** | Dependabot y remediación coordinada post-G122 | Resolver alerts/PRs Dependabot, actualizar dependencias y formalizar el preflight recurrente. | **Cerrado/aceptado G123/E01; publicación formal pendiente** |
| 16 | **MANT.1 R8** | Auditoría y consolidación post-NOR.3 de scripts y pruebas | Ejecutar #163 solo después de la publicación definitiva de G123/MANT.2 R1; clasificar, consolidar y retirar redundancias solo con cobertura equivalente; cerrar con versión beta propia. Bloquea #154. | **Planificado; no iniciado; sin Global preasignado** |
| 17 | **DOC.3 R1** | Auditoría documental integral post-MANT.1 | Ejecutar #154 después de publicar MANT.1 R8; reconciliar documentación viva/histórica, metadatos, enlaces y evidencia, con beta propia. | **Planificado; no iniciado; sin Global preasignado** |
| 18 | **PLAN.2 R2** | Replanificación maestra post-DOC.3 | Ejecutar #155 después de DOC.3 R1; reconciliar matriz, roadmap, gates restantes y continuidad hacia 1.0, con beta propia. | **Planificado; no iniciado; sin Global preasignado** |
| 19 | **VER.2 R6** | Auditoría y reforma del versionado beta | Ejecutar después de #163 → #154 → #155; formalizar revisiones, subrevisiones, correcciones materiales e inserción automática de fases nuevas. Bloquea PERSIST.1. | **Planificado; no iniciado; sin Global preasignado** |
| 20 | **PERSIST.1 R1** | Arquitectura de persistencia | Separar sesión temporal de guardado voluntario; definir esquema persistente versionado, local-first y migrable. | **Planificado; bloqueado por #163 → #154 → #155 → #164; no iniciado; sin Global preasignado** |
| 21 | **PERSIST.1 R2** | Guardar, restaurar y eliminar | Guardado explícito, listado, restauración, borrado individual y borrado completo. | Planificado |
| 22 | **PERSIST.1 R3** | Importación, exportación y migraciones | Exportación/importación controlada, validación de esquema, incompatibilidades y migraciones. | Planificado |
| 23 | **PERSIST.1 R4** | Seguridad y privacidad de persistencia | Minimización, protección/cifrado cuando aporte seguridad real, borrado y revisión de privacidad. | Planificado |
| 24 | **REP.1 R1** | Motor de informes | Generación real de PDF e informe final reproducible. | Planificado |
| 25 | **REP.1 R2** | Exportaciones finales | Formatos seleccionables, metodología, trazabilidad, metadatos y protección de datos. | Planificado |
| 26 | **REP.1 R3** | Cierre de informes | Accesibilidad del PDF, impresión, compatibilidad y validación final. | Planificado |
| 27 | **SEC.2 R7** | Hardening posterior a nuevas superficies | Reevaluar Developer, sesiones/Bearer, persistencia, archivos, exportaciones, CSP/CSRF/CORS aplicables y amenazas nuevas. | Reapertura planificada |
| 28 | **A11Y.2** | Auditoría WCAG 2.2 ampliada | Teclado, lector de pantalla, zoom, forced colors, alto contraste, navegadores, dispositivos, formularios, modales y exportaciones. | Planificado |
| 29 | **REV.1** | Revisión normativa, jurídica, privacidad y seguridad final | Revalidar fuentes, parámetros, interpretaciones, limitaciones, licencia, terceros y revisión jurídica externa prevista. | Planificado |
| 30 | **DOC.1 R6** | Congelación documental final | Última reconciliación de documentación pública/técnica antes de QA y release estable. | Reapertura planificada |
| 31 | **QA.1** | Auditoría integral de cierre beta | Código, pruebas, UX, seguridad, accesibilidad, normativa, documentación, rendimiento básico, estabilidad, compatibilidad, datos corruptos y entorno limpio. | Planificado |
| 32 | **REL.1** | Primera versión oficial | Freeze, build reproducible, SBOM/inventario, hashes, firma, instalación, soporte, release notes, validación limpia y `v1.0.0.0`. | Último bloque |

<!-- UX6-R8-CLOSURE:START -->
## 2.1. Cierre de ejecución UX.6

UX.6 R1–R8 queda consolidado como G121/E01 (`0.1.21.01-beta`) con revisión funcional R8 y ordinal E01.

- R1–R2: cerrados.
- R3–R4: cerrados.
- R5–R6: cerrados.
- R7: auditoría/reconciliación documental cerrada.
- R8: auditoría integral y hardening cerrados; promoción en PR #124.
- NOR.3 R1–R8 queda integrado/aceptado como G122/E01 mediante PR #162 / merge `b97cf61763479b80b8e8724b878089e8bb20fa00`.
- G123 queda disponible sin candidato; PERSIST.1 permanece planificado, no iniciado y sin Global preasignado.
- UX.7/UX.8 permanecen planificados y no iniciados.
<!-- UX6-R8-CLOSURE:END -->

## 3. Portal Developer — alcance confirmado

DEV.2 R5 deja aceptado el contrato base:

- `/dev`: entrada humana canónica; sin sesión muestra el login y con sesión válida muestra el centro actual;
- `/dev/login`: compatibilidad de entrada; `GET` redirige a `/dev` y el `POST` heredado continúa disponible;
- `/dev/centro-desarrollo`: conserva Bearer para clientes técnicos y evita un falso rechazo Bearer en navegación web;
- sesión web mediante `mrp_admin_session` `HttpOnly` limitada a `Path=/dev`;
- `Authorization: Bearer <token>` permanece como contrato técnico separado;
- shell Developer separado de la navegación y gestión de datos previsionales públicos;
- credencial administrativa fuera de `localStorage`, `sessionStorage`, query string, logs y documentación visible.

DEV.2 R6 queda cerrado/aceptado/publicado como G119/E05 y evolucionó el portal a páginas independientes:

- `/dev`;
- `/dev/diagnostico`;
- `/dev/eventos`;
- `/dev/archivos`;
- `/dev/mantenimiento`;
- `/dev/privacidad`.

R6 añadió el ZIP diagnóstico descargable, mantenimiento sobre artefactos diagnósticos conocidos, identidad humana persistente, RBAC y superficies separadas de perfil y acceso técnico. Las operaciones destructivas implementadas revalidan autorización, se limitan a superficies permitidas, registran evidencia sanitizada y aplican confirmación reforzada cuando corresponde.

## 4. Simulación Manual / Asistida

La nueva experiencia conserva los contratos de Pasos 1–6:

- **Manual:** el usuario completa y revisa todo el recorrido;
- **Asistida:** la aplicación procesa información compatible, muestra lo
  detectado, exige confirmación y dirige a las secciones faltantes.

La modalidad asistida no puede convertir una detección en una decisión
previsional silenciosa. Todo dato importado o inferido debe permanecer
revisable y trazable.

## 5. Gates transversales antes de 1.0

El cierre final debe demostrar, como mínimo:

- tres motores previsionales validados para su alcance documentado;
- límites oficiales no reconstruibles explícitos, sin parámetros inventados;
- dependencias y avisos de terceros reevaluados;
- seguridad de nuevas superficies;
- accesibilidad ampliada;
- compatibilidad y responsive;
- recuperación ante estado o archivo corrupto;
- estabilidad y rendimiento básico razonable;
- instalación/ejecución en entorno limpio;
- build oficial reproducible;
- SBOM/inventario, hashes y firma;
- documentación final de instalación, uso, soporte y release;
- revisión normativa/jurídica prevista.

## 6. Política de actualización

Al cerrar una revisión se actualizan, cuando resulten afectados:

- esta matriz;
- `docs/governance/roadmap.md`;
- `docs/governance/master-plan-to-1-0.md`;
- `data/governance/work-block-registry.json`;
- ledger revision-aware cuando cambie candidato o se acepte un estado;
- `CHANGELOG.md`, `RELEASES.md` y documentación transversal pertinente.

La matriz puede crecer o cambiar si aparece una necesidad real. No debe
convertirse en una lista rígida que obligue a conservar un orden que haya
dejado de ser técnicamente correcto.
