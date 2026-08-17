# Migración de firma criptográfica Git — 2026-08-17

**Estado:** Materialización criptográfica completada; controles GitHub finales pendientes
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

## 9. Resultado de la materialización

**Materialización criptográfica:** completada el 2026-08-17.

La ejecución dejó la siguiente evidencia:

- primer commit posterior a la frontera histórica firmado: `90e66a13eec554d616bb71a04e00da4ada68df54`;
- firma SSH del commit verificada localmente;
- GitHub registró ese commit con `verification.verified=true` y razón `valid`;
- la CI `Validación continua` #23 del mismo SHA terminó en `success`;
- `v0.0.1-beta` a `v0.0.21-beta` fueron materializados como tags retrospectivos firmados;
- `v0.0.22-beta` y `v0.0.23-beta` fueron reemitidos una sola vez como objetos firmados;
- 23/23 tags verificaron localmente mediante `git tag -v`;
- 23/23 objetos tag remotos fueron comprobados;
- 23/23 targets remotos fueron comprobados;
- ningún commit histórico fue reescrito;
- `main` permaneció en `90e66a13eec554d616bb71a04e00da4ada68df54` durante la operación.

La reemisión preservó:

| Tag | Objeto original sin firma | Objeto firmado nuevo | Commit objetivo preservado |
|---|---|---|---|
| `v0.0.22-beta` | `31accfc9a6014367179c97cfe54c5a223be8988f` | `bda764edb84ccaeb610a629fca1283bbd97e69a4` | `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5` |
| `v0.0.23-beta` | `609edf4bfed33c64770c88fab401002cd90f8e66` | `06b9260dadbcb2f0a7711841e1fad228e1badee8` | `07278f7a193ce964612d9697da57350691bf62c0` |

## 10. Inventario final de objetos firmados

| Tag | Objeto tag firmado | Commit objetivo |
|---|---|---|
| `v0.0.1-beta` | `3467d951c33a74e6f8a10fea3fce8f93df30b9a2` | `13ce028448244638eb63e4ff5db9bbe1e6f6205d` |
| `v0.0.2-beta` | `ac5caeb468b71c1089c77ba657efb228e1071fa3` | `eafe54d1503fe3bdc2064f2789cf98cb63ccc26b` |
| `v0.0.3-beta` | `fa67fef1da8c3c19711e45d83635628644c0831b` | `78e5188887f5c6c9fd0b42df56ce4aeea84c7965` |
| `v0.0.4-beta` | `cb1e362bf944143b0f996eba6e55eb59b15c8e8d` | `2d4dfd08a324fee18994e784159366593d6ba31f` |
| `v0.0.5-beta` | `b4b9eec17ae71a40329e2f952c70776e35a05d3c` | `8a7e3818d5d533b15cc2ee2d0a0b2921a29185bc` |
| `v0.0.6-beta` | `ea244e1907cc7ab52b852f825e0e5a6a0cf26266` | `e087d6ef106dfe1d1d975cebd4d21e7453d98990` |
| `v0.0.7-beta` | `45dae2e536117ee9eaeb48288449741cff497f59` | `e956ea985b086cc2c3a8d2eced488face7d5de69` |
| `v0.0.8-beta` | `885f9d4f2ca9674b8626de9887bd47a2933f3531` | `d599ee24afd56fe62a6d1a2a2d7d9b54e0a2fe2d` |
| `v0.0.9-beta` | `e44b4819b4266fd7d036fc535d20dcbca318eae4` | `e6b02dc86f81356bbbb65ae513b2707c0e947991` |
| `v0.0.10-beta` | `5d3dff56c81b35c305306e2ce179e61c44dfb306` | `8feb682e9b17def76c67fefe7c94e08669bc5520` |
| `v0.0.11-beta` | `833e8061882a4a2623fe536653d2c86950214e4c` | `1f350f6411df4da053fa212661d436f848b91292` |
| `v0.0.12-beta` | `1c1dda585e5f2f93311d995737fa6bccb567eb2d` | `6e6b33b484a24b9621d738a345107d0fe0b862eb` |
| `v0.0.13-beta` | `b50df4a139899e9566d954186be3d03f3cab635c` | `9f849d0facd37c238db793e2b85ef22173f2aab9` |
| `v0.0.14-beta` | `da2b12526a6fedfeb4a14e93199a8b4ae62189a2` | `f4a0d45b37271f005af6eb0b7a3a78f550aa774a` |
| `v0.0.15-beta` | `91565eb4c1107a4d44d2efc46e60492b13b09566` | `3430f2ed842c4820c207f429c87ca02b80293a5f` |
| `v0.0.16-beta` | `64cc963153356747767232a56bd6962dab805855` | `6f138da7b3ac4d1b76d69f5bddf86055b8e2ec93` |
| `v0.0.17-beta` | `546c849e3620b7335e31f36edf70b4b1a3350168` | `e55190bd5fc6fac0bb9716cfa271521b6ed9c432` |
| `v0.0.18-beta` | `428c1117b69868ab96d232eccaeda397307cadc5` | `11aefca0c7233bea8e6dd8a44e5b6a69b32ecac8` |
| `v0.0.19-beta` | `626228313e71dc875df3bb30199442bb43917ed7` | `83a67ed2e418428aa610e2f5d444c15667d5b427` |
| `v0.0.20-beta` | `bb36069d04e6eb2bd1e4c259a31d601e4bda6c1e` | `2a69fb839abd8dbdec225165be724f35d9d8f674` |
| `v0.0.21-beta` | `caa7b43958e497837cc3ddf6bb2492ce36347534` | `7941f58eac47a27b58c8a8954468ad55eab440b2` |
| `v0.0.22-beta` | `bda764edb84ccaeb610a629fca1283bbd97e69a4` | `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5` |
| `v0.0.23-beta` | `06b9260dadbcb2f0a7711841e1fad228e1badee8` | `07278f7a193ce964612d9697da57350691bf62c0` |

## 11. Controles todavía pendientes

La **materialización histórica de tags está terminada**, pero el prebloque de integridad Git/GitHub todavía no se declara cerrado.

Permanecen pendientes:

- ejecutar/auditar el workflow completo de firmas mediante `workflow_dispatch` desde `main`;
- crear el ruleset de tags para impedir modificaciones o eliminaciones posteriores;
- configurar la protección/ruleset de `main`;
- revisar configuración general de GitHub y los PR de Dependabot pendientes.

La excepción de ADR-159 para sustituir `v0.0.22-beta` y `v0.0.23-beta` **ya fue consumida y no puede repetirse**.

Desde este punto vuelve a regir la inmutabilidad de los tags publicados.

El cierre completo del prebloque se documentará únicamente después de terminar los controles GitHub pendientes.
