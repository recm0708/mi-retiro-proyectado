# Observabilidad y Developer Diagnostics

**Estado:** Vigente — GOV.1.4 cerrado / SEC.2 R1–R6 integrado
**Versión de aplicación revisada:** `0.0.71.01-beta`
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

El bloque DEV.2 permanece como cierre funcional histórico asociado a esta capacidad.

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

- DEV.2: cierre del bloque de diagnóstico.
- GOV.1.4: integración de observabilidad segura.
- 487/487: evidencia histórica de pruebas asociadas al cierre del bloque.

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
