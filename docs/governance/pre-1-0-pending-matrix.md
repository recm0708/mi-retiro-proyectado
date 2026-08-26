# Matriz maestra de pendientes hacia 1.0

**Estado:** vigente / documento vivo
**Versión base:** `0.1.13.03-beta` — G113/E03
**Checkpoint candidato:** PLAN.2 R1 — G114/E01 (`0.1.14.01-beta`) reservado, no aceptado
**Fecha de adopción propuesta:** 2026-08-26
**Clasificación:** Planificación / Producto / Arquitectura / Seguridad / QA / Release

Esta matriz ordena el trabajo pendiente antes de la primera versión oficial de
Mi Retiro Proyectado. Debe actualizarse cuando un bloque se inicia, cambia de
alcance, se divide justificadamente, se cierra o aparece una necesidad nueva
que deba resolverse antes de `1.0.0.0`.

La matriz **no preasigna Globales futuros** más allá del candidato vigente.
Cada estado material aceptado consume su `G` conforme a `VERSIONING.md`; un
candidato fallido no lo consume.

## 1. Reglas de uso

1. `VERSION` permanece en `0.1.13.03-beta` mientras PLAN.2 R1 sea candidato.
2. G114/E01 (`0.1.14.01-beta`) queda reservado para PLAN.2 R1.
3. Las etapas posteriores se ordenan por prioridad, no por un `G` futuro supuesto.
4. Una revisión que amplía un bloque existente conserva su identificador canónico.
5. `PLAN.2` y `UX.5` deben existir en el registro machine-readable antes de usarse.
6. La historia cerrada permanece preservada y no se moderniza mecánicamente.
7. Cambiar el orden o alcance exige sincronizar esta matriz, roadmap, plan maestro,
   registro y ledger de reserva cuando corresponda.

## 2. Matriz maestra

| Orden | Identificador | Trabajo pendiente | Alcance / criterio de cierre | Estado |
|---:|---|---|---|---|
| 1 | **PLAN.2 R1** | Replanificación maestra final hacia 1.0 | Formalizar esta matriz, registrar PLAN.2/UX.5, corregir la reserva G114 y reconciliar documentación viva post-G113. | **Candidato G114/E01** |
| 2 | **DOC.1 R4** | Saneamiento documental post-G113 | Corregir metadata viva, estados desactualizados y contradicciones actuales sin reescribir evidencia histórica. | Planificado |
| 3 | **REL.GOV.1 R2** | Automatización de Releases y checks | Estandarizar release notes, `gh release create`, verificación de tag/firma y lectura correcta de Actions/checks. | Planificado |
| 4 | **DEV.2 R5** | Portal Developer y acceso | Crear `/dev`; diferenciar sesión administrativa web y acceso técnico Bearer; rediseñar `/dev/login`; no persistir secretos. | Planificado |
| 5 | **DEV.2 R6** | Rediseño del Centro de desarrollo | Mejorar dashboard, navegación, estados, tablas, responsive, temas y coherencia visual de `/dev/centro-desarrollo`. | Planificado |
| 6 | **UX.5 R1** | Sistema visual integral | Nueva base visual: paleta, tipografía, espaciado, botones, tarjetas, estados, jerarquía y tokens reutilizables. | Planificado |
| 7 | **UX.5 R2** | Inicio, navegación y temas | Rediseñar Inicio/navegación y armonizar Claro, Oscuro, Automático y Alto contraste. | Planificado |
| 8 | **UX.5 R3** | Nueva entrada a Simulación | Preguntar antes del Paso 1 si la preparación será **Manual** o **Asistida** y explicar ambas modalidades. | Planificado |
| 9 | **UX.5 R4** | Flujo Manual | Mantener y mejorar el recorrido completo de Pasos 1–6 con revisión explícita de los datos. | Planificado |
| 10 | **UX.5 R5** | Flujo Asistido | Detectar/importar información confiable, pedir confirmación y conducir por los datos/decisiones faltantes sin decisiones silenciosas. | Planificado |
| 11 | **UX.5 R6** | Integración y cierre UX | Unificar Manual/Asistido, invalidación, navegación, errores, loaders, responsive, cambio de modalidad y resultados. | Planificado |
| 12 | **PERSIST.1 R1** | Arquitectura de persistencia | Separar sesión temporal de guardado voluntario; definir esquema persistente versionado, local-first y migrable. | Etapa posterior |
| 13 | **PERSIST.1 R2** | Guardar, restaurar y eliminar | Guardado explícito, listado, restauración, borrado individual y borrado completo. | Planificado |
| 14 | **PERSIST.1 R3** | Importación, exportación y migraciones | Exportación/importación controlada, validación de esquema, incompatibilidades y migraciones. | Planificado |
| 15 | **PERSIST.1 R4** | Seguridad y privacidad de persistencia | Minimización, protección/cifrado cuando aporte seguridad real, borrado y revisión de privacidad. | Planificado |
| 16 | **REP.1 R1** | Motor de informes | Generación real de PDF e informe final reproducible. | Planificado |
| 17 | **REP.1 R2** | Exportaciones finales | Formatos seleccionables, metodología, trazabilidad, metadatos y protección de datos. | Planificado |
| 18 | **REP.1 R3** | Cierre de informes | Accesibilidad del PDF, impresión, compatibilidad y validación final. | Planificado |
| 19 | **SEC.2 R7** | Hardening posterior a nuevas superficies | Reevaluar Developer, sesiones/Bearer, persistencia, archivos, exportaciones, CSP/CSRF/CORS aplicables y amenazas nuevas. | Reapertura planificada |
| 20 | **A11Y.2** | Auditoría WCAG 2.2 ampliada | Teclado, lector de pantalla, zoom, forced colors, alto contraste, navegadores, dispositivos, formularios, modales y exportaciones. | Planificado |
| 21 | **REV.1** | Revisión normativa, jurídica, privacidad y seguridad final | Revalidar fuentes, parámetros, interpretaciones, limitaciones, licencia, terceros y revisión jurídica externa prevista. | Planificado |
| 22 | **DOC.1 R5** | Congelación documental final | Última reconciliación de documentación pública/técnica antes de QA y release estable. | Reapertura planificada |
| 23 | **QA.1** | Auditoría integral de cierre beta | Código, pruebas, UX, seguridad, accesibilidad, normativa, documentación, rendimiento básico, estabilidad, compatibilidad, datos corruptos y entorno limpio. | Planificado |
| 24 | **REL.1** | Primera versión oficial | Freeze, build reproducible, SBOM/inventario, hashes, firma, instalación, soporte, release notes, validación limpia y `v1.0.0.0`. | Último bloque |

## 3. Portal Developer — alcance confirmado

La arquitectura vigente distingue:

- `/dev/login`: formulario de sesión administrativa web;
- `/dev/centro-desarrollo`: superficie protegida que redirige al login cuando
  el navegador no posee una sesión válida;
- autenticación técnica mediante `Authorization: Bearer <token>` para clientes
  técnicos autorizados.

Ambas modalidades validan el secreto administrativo configurado fuera del
repositorio. DEV.2 R5 debe crear una entrada unificada `/dev`, explicar la
diferencia y evitar que tokens terminen en `localStorage`, `sessionStorage`,
URL, logs o documentación visible.

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
- `data/work-block-registry.json`;
- ledger revision-aware cuando cambie candidato o se acepte un estado;
- `CHANGELOG.md`, `RELEASES.md` y documentación transversal pertinente.

La matriz puede crecer o cambiar si aparece una necesidad real. No debe
convertirse en una lista rígida que obligue a conservar un orden que haya
dejado de ser técnicamente correcto.
