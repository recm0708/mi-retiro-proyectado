# Migración de firma criptográfica Git — 2026-08-17

**Estado:** Preparada; pendiente materialización y verificación remota de tags
**Versión de aplicación:** `0.0.23-beta`
**Responsable:** Rubén Enrique Cañizares Miranda (`@recm0708`)
**Clasificación:** Gobierno / Integridad Git / Auditoría

Este documento registra la adopción de firma SSH para commits y tags de Mi Retiro Proyectado y define una migración histórica controlada.

## 1. Objetivos

- exigir firma criptográfica en commits nuevos;
- exigir firma criptográfica en tags formales nuevos;
- materializar `v0.0.1-beta` a `v0.0.21-beta` como tags retrospectivos firmados;
- reemitir una sola vez `v0.0.22-beta` y `v0.0.23-beta`, originalmente anotados pero sin firma;
- mantener intactos todos los commits históricos;
- impedir que la materialización posterior se confunda con una publicación ocurrida en la fecha histórica del hito.

## 2. Frontera de integridad

No se reescriben commits antiguos para añadirles firma.

Una firma forma parte del objeto Git. Reescribir commits históricos cambiaría sus SHA y alteraría la evidencia primaria.

La frontera adoptada es:

- commits hasta `07278f7a193ce964612d9697da57350691bf62c0`: historial anterior a la obligatoriedad de firma;
- primer commit posterior: firma SSH obligatoria;
- tags `v0.0.1-beta` a `v0.0.23-beta`: materialización/reemisión firmada durante esta migración;
- tags posteriores: firma obligatoria desde su creación original.

## 3. Clave autorizada

Principal:

```text
ruben.canizares@outlook.com
```

Clave pública:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHCHPb06tSFpOrMQVLSrqdAgY938DM50z3o5mmsTa3G8 ruben.canizares@outlook.com
```

Fingerprint validado localmente:

```text
SHA256:L9ssEgeNj4O/yDcAwwynYRfDas4ICGsG9UOnYSRyAO8
```

La clave privada nunca se versiona. `.github/allowed_signers` contiene únicamente material público.

## 4. Evidencia previa

Antes de la migración se generaron:

- `tags_pre_firma_2026-08-17.txt`;
- `calculadora-pension-css_pre_firma_2026-08-17.bundle`;
- `tags_formales_unsigned_pre_migracion.txt`.

El bundle fue verificado como historial completo.

| Tag | Objeto tag original | Commit objetivo |
|---|---|---|
| `v0.0.22-beta` | `31accfc9a6014367179c97cfe54c5a223be8988f` | `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5` |
| `v0.0.23-beta` | `609edf4bfed33c64770c88fab401002cd90f8e66` | `07278f7a193ce964612d9697da57350691bf62c0` |

## 5. Mapa de tags

Las fechas de **Cierre histórico** no son fechas de creación del tag retrospectivo.

| Tag | Commit objetivo | Cierre histórico | Naturaleza |
|---|---|---|---|
| `v0.0.1-beta` | `13ce028` | 2026-08-10 | retrospectivo |
| `v0.0.2-beta` | `eafe54d` | 2026-08-11 | retrospectivo |
| `v0.0.3-beta` | `78e5188` | 2026-08-11 | retrospectivo |
| `v0.0.4-beta` | `2d4dfd0` | 2026-08-11 | retrospectivo |
| `v0.0.5-beta` | `8a7e381` | 2026-08-11 | retrospectivo |
| `v0.0.6-beta` | `e087d6e` | 2026-08-11 | retrospectivo |
| `v0.0.7-beta` | `e956ea9` | 2026-08-12 | retrospectivo |
| `v0.0.8-beta` | `d599ee2` | 2026-08-12 | retrospectivo |
| `v0.0.9-beta` | `e6b02dc` | 2026-08-12 | retrospectivo |
| `v0.0.10-beta` | `8feb682` | 2026-08-12 | retrospectivo |
| `v0.0.11-beta` | `1f350f6` | 2026-08-12 | retrospectivo |
| `v0.0.12-beta` | `6e6b33b` | 2026-08-12 | retrospectivo |
| `v0.0.13-beta` | `9f849d0` | 2026-08-12 | retrospectivo |
| `v0.0.14-beta` | `f4a0d45` | 2026-08-13 | retrospectivo |
| `v0.0.15-beta` | `3430f2e` | 2026-08-13 | retrospectivo |
| `v0.0.16-beta` | `6f138da` | 2026-08-13 | retrospectivo |
| `v0.0.17-beta` | `e55190b` | 2026-08-13 | retrospectivo |
| `v0.0.18-beta` | `11aefca` | 2026-08-13 | retrospectivo |
| `v0.0.19-beta` | `83a67ed` | 2026-08-13 | retrospectivo |
| `v0.0.20-beta` | `2a69fb8` | 2026-08-13 | retrospectivo |
| `v0.0.21-beta` | `7941f58` | 2026-08-17 | retrospectivo |
| `v0.0.22-beta` | `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5` | 2026-08-17 | formal; reemisión firmada única |
| `v0.0.23-beta` | `07278f7a193ce964612d9697da57350691bf62c0` | 2026-08-17 | formal; reemisión firmada única |

## 6. Semántica de las fechas

No se modificará `GIT_COMMITTER_DATE` ni otra variable para hacer que un tag nuevo aparente haber sido creado en el pasado.

Cada tag retrospectivo declarará por separado la fecha real de materialización y la fecha histórica de cierre.

## 7. Excepción única para 22 y 23

`v0.0.22-beta` y `v0.0.23-beta` ya fueron publicados como tags anotados sin firma.

La migración autoriza sustituir una sola vez esos objetos tag si:

1. el commit objetivo permanece exactamente igual;
2. los objetos anteriores quedan documentados;
3. el nuevo objeto está firmado con una clave autorizada;
4. no se usa un force global sobre todos los tags;
5. después vuelve a regir la inmutabilidad estricta.

## 8. Verificación

Tres niveles:

1. `git tag -v`;
2. verificación remota de GitHub;
3. `.github/workflows/verificar-tags.yml`.

Para tags retrospectivos cuyo commit es anterior al workflow, la auditoría completa se ejecuta mediante `workflow_dispatch` desde `main`.

## 9. Estado de cierre

Esta revisión solo autoriza y prepara la migración.

No se marcará completada hasta verificar:

- 23/23 tags localmente;
- 23/23 refs remotos;
- targets exactos;
- firma válida;
- verificación remota;
- ruleset de tags posterior a la migración.

El cierre se registrará en un commit firmado posterior.
