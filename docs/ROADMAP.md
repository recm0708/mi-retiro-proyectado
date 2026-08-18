# Roadmap

**Estado:** vigente
**Versión de aplicación:** `0.0.23-beta`
**Fecha de revisión:** 2026-08-18

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

- [x] **GOV.1.3 — Reorganización y alineación integral de documentación**
  - [x] diagnóstico documental;
  - [x] R1 — documentos de entrada, archivo histórico y estructura;
  - [x] R2 — documentación técnica vigente;
  - [x] R3 — normativa, seguridad y privacidad documental;
  - [x] R4 — capa de auditoría documental y controles de consistencia;
  - versión de cierre: `0.0.23-beta`.

- [x] **Prebloque transversal — Firma e integridad Git/GitHub**
  - [x] respaldo completo previo a la migración;
  - [x] clave SSH Ed25519 dedicada y verificación local;
  - [x] política de firma, allowed signers, ADR y workflow preparados;
  - [x] primer commit nuevo firmado y verificado por GitHub;
  - [x] materialización firmada de `v0.0.1-beta` a `v0.0.21-beta`;
  - [x] reemisión firmada única de `v0.0.22-beta` y `v0.0.23-beta`;
  - [x] auditoría local/remota 23/23 tags;
  - [x] ruleset de tags;
  - [x] protección/ruleset de `main`;
  - [x] revisión de configuración GitHub y PR de Dependabot.

- [x] **GOV.1.4 — Observabilidad y Developer Diagnostics**
  - [x] modo exclusivo de desarrollo;
  - [x] logging estructurado;
  - [x] niveles y categorías;
  - [x] correlación de operaciones;
  - [x] registro de errores, conexiones e hitos técnicos sin duplicar cálculos;
  - [x] redacción y prohibición de datos sensibles;
  - [x] rotación/retención local;
  - [x] exportación diagnóstica controlada;
  - [x] documentación de esquema y operación;
  - [x] 13 regresiones específicas y suite completa de 487 pruebas en `OK`.

- [x] **GOV.1.5 — Seguridad, privacidad y transparencia**
  - [x] threat model;
  - [x] procedimiento de incidentes;
  - [x] procedimiento de derechos del titular;
  - [x] revisión de logs y datos sensibles;
  - [x] terceros y recursos externos;
  - [x] criterios TLS/despliegue;
  - [x] gate y paquete documental para revisión jurídica externa previa a publicación.

- [x] **GOV.1.6 — Controles GitHub y auditoría automática**
  - [x] plantillas estructuradas de issues y Pull Request;
  - [x] `SECURITY.md`;
  - [x] controles documentales de repositorio;
  - [x] workflow adicional `Auditoría de gobernanza`;
  - [x] política de rama/revisión documentada y compatible con la etapa del proyecto;
  - [x] gate para promover `Auditoría de gobernanza` a check requerido después de su primera ejecución exitosa.

- [x] **GOV.1.7 — Licencia**
  - [x] objetivo de distribución evaluado;
  - [x] compatibilidad de dependencias directas revisada;
  - [x] derechos de terceros separados del código original;
  - [x] seleccionada licencia propietaria pre-beta / todos los derechos reservados;
  - [x] añadidos `LICENSE`, `THIRD_PARTY_NOTICES.md` y gates de distribución;
  - [x] futura relicencia abierta reservada a una decisión expresa del titular.

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
- CI y Dependabot;
- plantillas GitHub, política de seguridad y auditoría automática de gobernanza.

### Pendiente o incompleto

- persistencia voluntaria;
- informes PDF;
- exportación final seleccionable;
- auditoría WCAG 2.2 ampliada con tecnologías de apoyo/dispositivos;
- Developer Diagnostics implementado y revisado internamente bajo GOV.1.5;
- revisión jurídica externa previa a beta pública;
- diseño/hardening específico si se decide un despliegue remoto;
- revisión jurídica externa de la estrategia de publicación/licencia antes de beta pública/comercial;
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
