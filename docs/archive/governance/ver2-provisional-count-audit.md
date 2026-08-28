# VER.2 — Conteo de segunda pasada

**Estado:** segunda pasada contable cerrada; pendiente materialización técnica del ledger.
**Base:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`.
**Fuente de decisión:** `MATRIZ_DECISION_REVISIONES_VER2.md`.

## 1. Conteos anteriores superados

La primera pasada propuso G057. Una corrección intermedia llevó provisionalmente a G060. Ambos quedan superados porque todavía comprimían estados técnicos y de gobierno materialmente distintos.

La segunda pasada cruzó:

- historia Git;
- releases y changelog;
- bitácoras históricas UX;
- Pull Requests integrados;
- gates de pruebas;
- documentación de cierre;
- conversaciones de desarrollo recuperadas.

## 2. Resultado

El último estado aceptado antes de VER.2 es:

```text
G070
```

Distribución:

| Tramo | Cantidad |
|---|---:|
| Estados legado `0.0.1-beta`–`0.0.21-beta` | 21 |
| GOV.1.2 | 1 |
| GOV.1.3 R1–R4 | 4 |
| Prebloque firma/integridad Git/GitHub | 5 |
| GOV.1.4 | 1 |
| GOV.1.5 R1–R3 | 3 |
| GOV.1.6 | 1 |
| GOV.1.7 | 1 |
| Hotfix de licencia | 1 |
| GOV.1.8 | 1 |
| Saneamiento post-GOV.1 | 1 |
| UX.4.6e | 10 |
| PLAN.1 | 10 |
| UX.4.6f | 4 |
| UX.4.6g | 1 |
| UX.4.6h | 3 |
| UX.4.6i | 2 |
| **TOTAL** | **70** |

## 3. Correcciones que explican la diferencia frente a G057

La diferencia neta es **+13**:

- prebloque firma/integridad: cinco estados reales en lugar de uno → `+4`;
- GOV.1.5 R1/R2/R3 en lugar de un único cierre → `+2`;
- hotfix de formato de licencia integrado y validado → `+1`;
- saneamiento post-GOV.1 integrado y validado → `+1`;
- identidad visual/publicación pre-R8 como hito transversal separado → `+1`;
- PLAN.1 R4.1 y R4.2 fueron dos revisiones aceptadas sucesivas → `+1`;
- mantenimiento de dependencias post-UX.4.6f R1 → `+1`;
- UX.4.6h R1.1 omitida en primera pasada → `+1`;
- UX.4.6i R1 aceptada antes de R1.4 → `+1`.

No se resta PR #31: aunque R2 ya había cerrado funcionalmente el Paso 4, PR #31 añadió un `pre-commit` reproducible, cinco regresiones y un estado técnico nuevo con 762 pruebas; por tanto sí consume revisión.

## 4. Exclusiones relevantes

No consumen Global adicional:

- UX.2.1: real, pero absorbida dentro del snapshot legado de `0.0.9-beta`;
- revisiones internas no aceptadas de UX.4.6a–d;
- UX.4.6d R1–R22, cuya validación integral seguía pendiente hasta R23;
- PR #19 como checkpoint que consolida estados UX.4.6e ya contabilizados y deja R8 pendiente;
- UX.4.6e R8.1, corregida antes de la aceptación de R8.2;
- PR #22 y PR #25 como materializaciones documentales de estados ya contabilizados;
- UX.4.6f R1 por separado: R1/R1.1 se aceptaron conjuntamente;
- UX.4.6g R1.2/R1.3/R1.4/R1.4.2/R1.4.3 sin evidencia de aceptación diferenciada;
- UX.4.6h R1 fallida;
- UX.4.6i R1.1 inexistente como revisión independiente;
- UX.4.6i R1.2/R1.3 sin evidencia de aceptación diferenciada;
- PR Dependabot cerrados/sustituidos que no llegaron a constituir el estado aceptado final.

## 5. Secuencia provisional final antes de materializar el ledger

Desde G022:

```text
G022      GOV.1.2
G023-026  GOV.1.3 R1-R4
G027-031  Prebloque firma/integridad
G032      GOV.1.4
G033-035  GOV.1.5 R1-R3
G036      GOV.1.6
G037      GOV.1.7
G038      Hotfix licencia
G039      GOV.1.8
G040      Saneamiento post-GOV.1
G041-050  UX.4.6e
G051-060  PLAN.1
G061-064  UX.4.6f
G065      UX.4.6g
G066-068  UX.4.6h
G069-070  UX.4.6i
```

## 6. Consecuencia para VER.2

Si el ledger estructurado, su validador, las regresiones y el gate completo no revelan otra contradicción, el cierre real de VER.2 consumirá:

```text
G071
```

El candidato revision-aware correspondiente se decidirá al materializar G071. Hasta entonces `VERSION` no debe darse por promovida y el PR #35 permanece en draft.
