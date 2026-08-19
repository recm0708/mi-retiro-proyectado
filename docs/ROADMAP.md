# Roadmap

**Estado:** vigente
**Versión de aplicación:** `0.0.25-beta`
**Fecha de revisión:** 2026-08-19

Este roadmap describe **estado actual y trabajo futuro**. La evolución detallada ya completada se conserva en `RELEASES.md`, `CHANGELOG.md` y `docs/historico/`.

## 1. Programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta

**Estado general:** cerrado el 2026-08-18.
**Decisión de cierre:** UX.4.6e queda descongelada y pasa a ser el siguiente bloque activo.

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
  - [x] `Auditoría de gobernanza` promovido al conjunto de checks requeridos junto con Python 3.13/3.14.

- [x] **GOV.1.7 — Licencia**
  - [x] objetivo de distribución evaluado;
  - [x] compatibilidad de dependencias directas revisada;
  - [x] derechos de terceros separados del código original;
  - [x] seleccionada licencia propietaria pre-beta / todos los derechos reservados;
  - [x] añadidos `LICENSE`, `THIRD_PARTY_NOTICES.md` y gates de distribución;
  - [x] futura relicencia abierta reservada a una decisión expresa del titular.

- [x] **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**
  - [x] revisión integral de GOV.1.1–GOV.1.7;
  - [x] coherencia código/pruebas/documentación;
  - [x] versión formal de cierre `0.0.24-beta`;
  - [x] tag anotado y firmado `v0.0.24-beta` creado después de merge, validación post-merge y CI verde;
  - [x] auditoría de GitHub con `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`;
  - [x] decisión de reanudar UX.4.6e;
  - [x] gates pre-publicación preservados sin declarar la beta pública lista.

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
- procedencia editable con fotografía documental original, copia de trabajo y exclusión explícita de períodos;
- gestión local de datos de simulación;
- temas Claro, Oscuro, Automático y Alto contraste;
- base responsive y accesible;
- identidad visual oficial, favicons y Social Preview propios;
- repositorio público con metadata, 20/20 topics, 21 labels e Issue Forms;
- Dependency graph, Dependabot, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting;
- CI y auditoría automática de gobernanza.

### Pendiente o incompleto

- persistencia voluntaria;
- informes PDF;
- exportación final seleccionable;
- auditoría WCAG 2.2 ampliada con tecnologías de apoyo/dispositivos;
- revisión jurídica externa previa a primera beta pública de producto;
- diseño/hardening específico si se decide un despliegue remoto;
- revisión jurídica externa de la estrategia de publicación/licencia antes de beta pública/comercial;
- parámetros oficiales que la documentación identifica como no disponibles o no reconstruibles con fidelidad.

## 3. UX.4.6 — trabajo reanudado después de GOV.1

**Bloque en cierre:** UX.4.6e — R9.1, candidato local `0.0.25-beta`.

- [ ] **UX.4.6e — Estandarización técnica, comentarios y coherencia de interfaz post-GOV.1**
  - [x] R1 — auditoría integral del código y definición del patrón documental por tecnología;
  - [x] R2 — normalización Python/tests y corrección de precisión detectada durante la auditoría; 550 pruebas en `OK`;
  - [x] R3 — normalización JavaScript y cambio definitivo de almacenamiento a `miRetiroProyectado.*`; 558 pruebas en `OK`;
  - [x] R4 — normalización Python restante, HTML/Jinja/CSS y pruebas históricas sin alterar contratos funcionales ni la cascada; 566 pruebas en `OK`;
  - [x] R5 — coherencia GOV → interfaz visible y preparación pública del repositorio; 576 pruebas en `OK`;
  - [x] R6 — documentación transversal y normalización definitiva de la secuencia UX.4.6; 586 pruebas en `OK`;
  - [x] R7 — regresiones y auditoría de coherencia código/interfaz/documentación; 598 pruebas en `OK`;
  - [x] checkpoint pre-R8 — identidad visual oficial, favicon, Social Preview, visibilidad pública y revalidación de seguridad GitHub; 624 pruebas en `OK`;
  - [x] R8 — prueba funcional manual y automática completa hasta Paso 3; reconsentimiento, procedencia editable y exclusión/reinclusión documental validados; 644 pruebas en `OK` antes del cierre documental;
  - [ ] R9 — cierre técnico y publicación del hito;
    - [x] R9.1 — candidato local `0.0.25-beta` validado con 660 pruebas en `OK`, documentación coherente y `git diff --check` limpio;
    - [ ] R9.2 — commits firmados, PR, CI, squash, validación post-merge y tag firmado `v0.0.25-beta`.
- [ ] **UX.4.6f — Paso 4 · Proyección salarial/laboral**
- [ ] **UX.4.6g — Paso 5 · Escenarios de retiro**
- [ ] **UX.4.6h — Paso 6 · Resultados y exportación**

La visibilidad pública del repositorio no cambia la etapa funcional: `0.0.25-beta` continúa siendo pre-beta de producto y la aplicación sigue orientada a ejecución local.

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

Antes de una publicación amplia de la aplicación:

- auditoría WCAG 2.2 más completa;
- pruebas con lector de pantalla;
- matriz real de dispositivos/navegadores;
- revisión de alto contraste y colores forzados;
- pruebas de teclado completas;
- revisión de exportaciones e informes accesibles.

## 7. Criterio para primera beta pública

La familia `0.1.0-beta.1` solo podrá evaluarse cuando:

- [x] GOV.1 esté cerrado;
- [x] exista una licencia decidida;
- [x] seguridad y privacidad tengan procedimientos pre-beta suficientes;
- [x] la documentación pública pre-beta esté coherente al cierre GOV.1;
- [x] la suite y CI de gobierno estén en verde;
- [x] no existan discrepancias conocidas entre versión, código y documentación de GOV.1;
- [x] las limitaciones materiales estén declaradas;
- [x] repositorio, metadata, identidad y controles de seguridad pública básicos estén configurados;
- [ ] se complete/revise el alcance funcional restante de UX.4.6e–h;
- [ ] se complete la revisión jurídica externa prevista antes de la primera beta pública de producto;
- [ ] se cierre la auditoría ampliada de accesibilidad y cualquier gate de despliegue aplicable;
- [ ] se decida expresamente qué funciones quedan dentro de la primera beta pública.
