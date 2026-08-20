# Auditoría integral PLAN.1 R4

**Estado:** R4.2 — PR #23 integrado; higiene pre-tag pendiente
**Versión candidata:** `0.0.26-beta`
**Versión base del programa:** `0.0.25-beta`
**Fecha:** 2026-08-20
**Clasificación:** Gobierno / QA / Release

## 1. Objetivo

Cerrar la alineación maestra iniciada después de `v0.0.25-beta` sin adelantar trabajo funcional de UX.4.6f. R4 verifica que la nueva política de versionado, documentación, privacidad, seguridad, release y regresiones sea coherente antes de integrar el hito.

## 2. Evidencia previa

PLAN.1 llegó a R4 con los siguientes gates locales ejecutados:

| Revisión | Evidencia |
|---|---:|
| R1 | 665 pruebas en `OK` |
| R2A | 670 pruebas en `OK` |
| R2B1 | 676 pruebas en `OK` |
| R2B2 | 684 pruebas en `OK` |
| R2C | 689 pruebas en `OK` |
| R3A | 695 pruebas en `OK` |
| R3B1 | 702 pruebas en `OK` |
| R3B2 | 710 pruebas en `OK` |

En los gates reportados, `git diff --check` permaneció limpio y `VERSION` continuó en `0.0.25-beta` hasta R4.

## 3. Cambios auditados

R4.1 comprueba de forma conjunta:

- `VERSION` y `APP_VERSION`;
- validador de beta `0.0.N-beta` y futura versión oficial de cuatro componentes;
- ADR-168;
- plan maestro de 14 bloques;
- README, ROADMAP, RELEASES y CHANGELOG;
- proceso de release y reglas de tags firmados;
- seguridad, privacidad, terceros y licencia;
- documentación técnica/normativa viva;
- guard de referencias históricas;
- preservación de `v0.0.25-beta` y de evidencia GOV.1/UX.4.6e.

No se modifica el algoritmo previsional, los motores SEBD/Mixto/SUCGS ni los valores de `normativa/*.json`.

## 4. Promoción de candidato

R4.1 asigna:

```text
VERSION = 0.0.26-beta
```

No se crea un Build oficial. `Build 000001` continúa reservado para REL.1.

`v0.0.26-beta` tampoco se crea en R4.1. Un tag publicado antes de PR y CI violaría el proceso de release vigente.

## 5. Gate local R4.1

Después de incorporar 10 regresiones específicas, el gate local ejecutado fue:

```text
Ran 720 tests
OK
```

También deben quedar correctos:

- `python -m compileall app`;
- `node --check` para JavaScript versionado;
- `git diff --check`;
- `VERSION == APP_VERSION`;
- working tree limitado a los cambios deliberados de PLAN.1.

La ejecución local confirmó **720 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` limpio. La documentación de cierre local se vuelve a validar con el mismo conteo antes de iniciar R4.2.

## 6. Gate remoto R4.2

Evidencia ya materializada:

1. commit de rama firmado: `7c50d989f5c6d266db26c9625367dd82e9895aba`;
2. PR #23 abierto contra `main`;
3. `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` en `success`;
4. integración por squash;
5. `main` resultante: `497097f720c98f6e5a7ed689cf91368011a96be1`, verificado por GitHub;
6. sincronización local de `main`;
7. gate post-merge: **720 pruebas en `OK`**, compilación Python, sintaxis JavaScript y `git diff --check` correctos.

La suite post-merge produjo un `SyntaxWarning` en una regresión documental por usar `.\VERSION` dentro de una cadena normal de Python. La advertencia no cambió el resultado de las 720 pruebas, pero viola el criterio de cierre limpio adoptado para el tag.

Higiene pre-tag:

- convertir el literal a cadena raw sin alterar el texto esperado;
- mantener exactamente 720 pruebas;
- integrar la corrección mediante PR y CI requerida;
- sincronizar el nuevo `main`;
- repetir el gate sin `SyntaxWarning`;
- solo entonces crear y verificar el tag firmado `v0.0.26-beta`.

Hasta completar esos puntos PLAN.1 permanece en R4.2.

## 7. Siguiente bloque

Después del cierre formal de PLAN.1, el siguiente bloque funcional es:

```text
UX.4.6f — Paso 4 · Proyección salarial/laboral
```
