# Roadmap

**Estado:** vigente
**Versión de aplicación:** `0.0.22-beta`
**Fecha de revisión:** 2026-08-17

Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md` y `docs/historico/`.

## 1. Programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta

**Estado general:** en ejecución.
**Regla:** UX.4.6e permanece congelada hasta completar GOV.1.

- [x] **GOV.1.1 — Inventario y reconstrucción histórica**
  - inventario del repositorio;
  - reconstrucción de 80 commits;
  - clasificación retrospectiva `0.0.1-beta` a `0.0.21-beta`.

- [x] **GOV.1.2 — Gobierno y versionado**
  - `VERSION`;
  - `VERSIONING.md`;
  - `GOVERNANCE.md`;
  - `RELEASES.md`;
  - `.github/CODEOWNERS`;
  - primera versión formal `0.0.22-beta`;
  - tag `v0.0.22-beta`.

- [ ] **GOV.1.3 — Reorganización y alineación integral de documentación**
  - [x] diagnóstico documental;
  - [x] R1 — documentos de entrada, archivo histórico y estructura;
  - [x] R2 — documentación técnica vigente;
  - [ ] R3 — normativa, seguridad y privacidad documental;
  - [ ] R4 — capa de auditoría documental y controles de consistencia;
  - versión objetivo al cierre: `0.0.23-beta`.

- [ ] **GOV.1.4 — Observabilidad y Developer Diagnostics**
  - modo exclusivo de desarrollo;
  - logging estructurado;
  - niveles y categorías;
  - correlación de operaciones;
  - registro de errores, advertencias, conexiones e hitos técnicos;
  - redacción de datos sensibles;
  - rotación/retención;
  - exportación diagnóstica controlada;
  - documentación de esquema y operación.

- [ ] **GOV.1.5 — Seguridad, privacidad y transparencia**
  - threat model;
  - procedimiento de incidentes;
  - procedimiento de derechos del titular;
  - revisión de logs y datos sensibles;
  - terceros y recursos externos;
  - TLS/despliegue;
  - revisión jurídica previa a publicación.

- [ ] **GOV.1.6 — Controles GitHub y auditoría automática**
  - plantillas de issues/PR;
  - `SECURITY.md`;
  - controles de documentación;
  - workflows adicionales cuando aporten valor;
  - políticas de rama/revisión compatibles con la etapa del proyecto.

- [ ] **GOV.1.7 — Licencia**
  - evaluar objetivo de distribución;
  - compatibilidad de dependencias;
  - derechos de terceros;
  - seleccionar licencia;
  - añadir `LICENSE` y avisos necesarios.

- [ ] **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**
  - revisión integral;
  - coherencia código/pruebas/documentación;
  - release y tag;
  - decisión de reanudar UX.4.6e.

## 2. Estado funcional del producto

### Implementado

- asistente de seis pasos;
- motores SEBD, Mixto y SUCGS para el alcance general documentado;
- comparación de escenarios;
- trazabilidad de cálculo;
- metodología y fuentes;
- resultado transversal;
- importación revisable de Mi Retiro Seguro;
- importación revisable de Ficha Digital;
- gestión local de datos de simulación;
- temas Claro, Oscuro, Automático y Alto contraste;
- base responsive y accesible;
- CI y Dependabot.

### Pendiente o incompleto

- persistencia voluntaria;
- informes PDF;
- exportación final seleccionable;
- auditoría WCAG 2.2 ampliada con tecnologías de apoyo/dispositivos;
- observabilidad estructurada;
- procedimientos formales de seguridad/privacidad pre-publicación;
- revisión jurídica externa;
- licencia;
- parámetros oficiales que la documentación identifica como no disponibles o no reconstruibles con fidelidad.

## 3. UX.4.6 pendiente después de GOV.1

- [ ] **UX.4.6e — Paso 4 · Proyección salarial/laboral**
- [ ] **UX.4.6f — Paso 5 · Escenarios de retiro**
- [ ] **UX.4.6g — Paso 6 · Resultados y exportación**

Las revisiones UX futuras deben reutilizar los contratos visuales, de navegación, procedencia, privacidad y validación ya consolidados.

## 4. Persistencia e informes

Fase futura:

- SQLite o mecanismo equivalente solo si existe una necesidad aprobada;
- guardado voluntario;
- versionado/migración de esquema;
- importación/exportación controlada;
- informes PDF;
- separación configurable de identificadores personales;
- inclusión de versión de aplicación/metodología en salidas auditables.

Cualquier persistencia modifica el análisis de privacidad y exige revisión antes de implementarse.

## 5. Normativa y motores

Trabajo continuo:

- revalidar parámetros que cambien oficialmente;
- mantener historial de valores normativos por fecha;
- incorporar regímenes especiales únicamente con fuente y pruebas propias;
- no reconstruir saldos/bonos actuariales sin fuente suficiente;
- mantener visibles las limitaciones del modelo.

## 6. Accesibilidad y calidad

Antes de una publicación amplia:

- auditoría WCAG 2.2 más completa;
- pruebas con lector de pantalla;
- matriz real de dispositivos/navegadores;
- revisión de alto contraste y colores forzados;
- pruebas de teclado completas;
- revisión de exportaciones e informes accesibles.

## 7. Criterio para primera beta pública

La familia `0.1.0-beta.1` solo podrá evaluarse cuando:

- GOV.1 esté cerrado;
- exista una licencia decidida;
- seguridad y privacidad tengan procedimientos pre-beta suficientes;
- la documentación pública esté coherente;
- la suite y CI estén en verde;
- no existan discrepancias conocidas entre versión, código y documentación;
- las limitaciones materiales estén declaradas;
- se haya decidido expresamente qué funciones quedan dentro de la beta.
