# Observabilidad y Developer Diagnostics

**Estado:** Vigente — GOV.1.4 cerrado / SEC.2 R1–R6 integrado / DEV.2 R6 aceptado/publicado G119/E05
**Versión de aplicación revisada:** `0.1.20.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Fecha de cierre original:** 2026-08-17
**Última revisión documental:** AUD.SEC2 R1 — 2026-08-25
**Clasificación:** Técnica / Desarrollo / Privacidad

## Nota de lectura post-MANT.1

Developer Diagnostics continúa como herramienta exclusiva de desarrollo local.
Permanece desactivado por defecto y no constituye telemetría de producto.

GOV.1.4 no modificó fórmulas previsionales, motores de cálculo ni reglas normativas.
Su alcance correspondió exclusivamente a observabilidad técnica y diagnóstico.

DEV.2 R1–R4 conserva la evolución histórica de Developer Diagnostics.
DEV.2 R5–R6 amplía esa base con el Portal Developer humano, identidad,
RBAC, diagnóstico, eventos, archivos, mantenimiento, privacidad, perfil y
acceso técnico. G119/E05 constituye su cierre aceptado y publicado.

## 1. Activación

Developer Diagnostics se activa mediante:

```powershell
$env:MRP_DEV_MODE = "1"
```

Inicio normal de la aplicación:

```powershell
python -m uvicorn app.main:app --reload
```

## 2. Esquema de diagnóstico

Los eventos utilizan metadata técnica:

- schema_version;
- timestamp UTC;
- level;
- event;
- component;
- app_version;
- correlation_id;
- duration_ms;
- outcome;
- metadata.

## 3. Protección de información

Developer Diagnostics no registra:

- cuerpos de solicitudes;
- cuerpos de respuestas;
- contenido PDF;
- texto extraído de documentos;
- datos personales;
- salarios;
- cuotas;
- montos de pensión;
- cookies;
- tokens;
- secretos;
- credenciales;
- mensajes originales de excepciones.

Los logs son locales y están excluidos del repositorio mediante `.gitignore`.

No existe telemetría remota automática.

No existe envío de logs a terceros.

## 4. Integración SEC.2

SEC.2 R4 incorpora auditoría administrativa dentro del modelo de observabilidad.

Los eventos administrativos permiten identificar:

- accesos administrativos permitidos;
- accesos rechazados;
- superficie administrativa bloqueada;
- endpoint relacionado.

La auditoría utiliza metadata mínima y nunca almacena tokens o secretos.

## 5. Evidencia histórica

La evolución de Developer Diagnostics conserva la evidencia histórica del cierre funcional:

- DEV.2 R1–R4: evolución histórica del bloque de diagnóstico.
- GOV.1.4: integración de observabilidad segura.
- 487/487: evidencia histórica de pruebas de la etapa inicial.
- DEV.2 R5–R6: Portal Developer, acceso humano y superficies
  administrativas sobre la misma base diagnóstica sanitizada.
- G119/E05: cierre aceptado/publicado de DEV.2.

## 6. Revisión de seguridad GOV.1.5

La revisión de seguridad GOV.1.5 estableció controles base de privacidad, modelo de amenazas y protección de información técnica.

Estos controles permanecen vigentes como fundamento de SEC.2.

## 7. Riesgo residual y metadata futura

La metadata futura debe mantener:

- mínima información necesaria;
- ausencia de datos personales;
- ausencia de información previsional;
- ausencia de credenciales;
- orientación exclusiva a diagnóstico técnico.

La observabilidad no debe convertirse en una segunda base de datos de simulaciones.

## 8. Cierre SEC.2

SEC.2 queda integrado con:

- autenticación administrativa;
- protección centralizada de endpoints;
- auditoría de accesos;
- observabilidad segura;
- documentación transversal actualizada.

El alcance continúa limitado al escenario beta local soportado.

## Sesiones administrativas y observabilidad post-SEC.2

Los eventos `admin.access.*` y `admin.session.revoked` pueden registrar endpoint,
outcome y motivo técnico controlado. Nunca registran el valor de
`MRP_ADMIN_SECRET`, cabeceras Authorization completas, Bearer, identificadores
de sesión ni cookies. AUD.SEC2 R1 extiende `Cache-Control: no-store` a `/dev/`
y mantiene esta superficie separada de la telemetría de producto.

## 9. Integración DEV.2 R6

Developer Diagnostics y el Portal Developer son capacidades relacionadas,
pero no equivalentes.

Developer Diagnostics:

- se habilita mediante `MRP_DEV_MODE=1`;
- genera eventos técnicos sanitizados;
- no autentica personas;
- no constituye telemetría de producto.

El Portal Developer:

- se habilita mediante `MRP_ADMIN_ENABLED=1`;
- utiliza identidades Developer persistentes;
- utiliza sesiones web temporales;
- aplica roles y permisos;
- consume eventos y artefactos diagnósticos permitidos;
- puede ejecutar operaciones administrativas autorizadas.

La identidad administrativa, el rol, la revisión de seguridad y los hashes
de credenciales no deben escribirse como contenido sensible de los logs.

Los eventos de acceso y mantenimiento solo deben conservar metadata técnica
mínima, outcome y motivos controlados.
