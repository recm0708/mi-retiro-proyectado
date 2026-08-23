# Cierre GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta

**Estado:** Cerrado
**Versión formal:** `0.0.24-beta`
**Fecha de cierre:** 2026-08-18
**Clasificación:** Gobierno / Auditoría final / Pre-beta

## 1. Objetivo

GOV.1 se creó para detener temporalmente la evolución UX y revisar de forma transversal historial, versionado, documentación, integridad Git/GitHub, observabilidad, seguridad, privacidad, terceros, licencia y proceso de release antes de continuar el desarrollo pre-beta.

Este documento consolida la evidencia definitiva de cierre. No sustituye Git, CI, los ADR, las fuentes normativas ni los documentos especializados.

## 2. Resultado por bloque

| Bloque | Resultado |
|---|---|
| GOV.1.1 | reconstrucción histórica y clasificación de 80 commits completada |
| GOV.1.2 | gobierno, versionado y fuente canónica `VERSION` completados |
| GOV.1.3 | reorganización documental, normativa, privacidad y auditoría completadas |
| Prebloque firma/integridad | firma SSH adoptada, 23/23 tags iniciales auditados y rulesets completados |
| GOV.1.4 | Developer Diagnostics local y estructurado completado |
| GOV.1.5 | seguridad, privacidad, threat model y procedimientos completados internamente |
| GOV.1.6 | controles GitHub, `SECURITY.md`, templates y auditoría automática completados |
| GOV.1.7 | licencia propietaria pre-beta y terceros completados |
| GOV.1.8 | auditoría final, versión `0.0.24-beta`, cierre GOV.1 y reanudación de UX.4.6e completados |

## 3. Evidencia técnica final

Línea base previa a GOV.1.8:

```text
530 pruebas
OK
```

GOV.1.8 añadió 10 regresiones de cierre. La validación final integrada fue:

```text
540 pruebas
OK
```

También quedaron confirmados:

- `python -m compileall app`: correcto;
- validación sintáctica JavaScript mediante `node --check`: correcta;
- `git diff --check`: limpio;
- commit de rama firmado;
- Pull Request #17 hacia `main`;
- checks `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`: `success`;
- integración mediante `Squash and merge`;
- commit final de `main`: `653900cebd84019fbbaa3ff3cfd91536ccab76eb`;
- validación post-merge: 540/540 en `OK`;
- tag anotado y firmado `v0.0.24-beta`;
- objeto tag: `3cdf6f84804c1bb4bdda9e449eb0932528557aa3`.

## 4. Evidencia Git/GitHub de cierre

Se verificó:

- PR #15 fusionado para GOV.1.6/GOV.1.7;
- PR #16 fusionado para el hotfix documental de licencia;
- PR #17 fusionado para GOV.1.8 y cierre integral GOV.1;
- checks requeridos en verde en el flujo de cierre;
- `main` como rama remota persistente después de la limpieza de ramas de trabajo;
- flujo ordinario configurado mediante Pull Request y squash;
- tags publicados protegidos por la política de integridad documentada;
- `v0.0.24-beta` verificado localmente con firma SSH válida.

La auditoría post-GOV.1 posterior confirmó **24/24 tags con firma SSH válida**. Esa auditoría no reescribe el tag de cierre ni cambia `VERSION`; se documenta por separado en `AUDITORIA_REPOSITORIO_2026-08-18.md`.

## 5. Versión de cierre

`0.0.24-beta` es una **versión interna pre-beta formal** según la terminología vigente cuando GOV.1 fue cerrado.

Representa el cierre auditable de GOV.1 y no debe confundirse con:

- la primera beta pública;
- una certificación de la CSS;
- una aprobación jurídica externa;
- una declaración de aptitud automática para Internet.

La primera familia pública prevista en el momento de este cierre era:

```text
0.1.0-beta.1
```

> **Nota posterior — PLAN.1 / 2026-08-20:** esa planificación fue sustituida. La línea vigente `0.0.N-beta` se trata como etapa beta de desarrollo y continúa hasta cerrar los gates del producto. La siguiente transición prevista ya no es `0.1.0-beta.1`, sino la primera versión oficial `1.0.0.0` con `Build 000001`. Esta nota no reescribe la decisión histórica de GOV.1; documenta su sustitución posterior.

## 6. Regla de versiones históricas

Los documentos que registran revisiones GOV.1.3, GOV.1.5 y GOV.1.7 pueden conservar `0.0.23-beta` como **versión base de revisión** cuando ese valor describe el hito que originó el documento.

GOV.1.8 dejó de exigir que una regresión histórica reescriba esos documentos únicamente porque `VERSION` avance. La versión canónica actual se valida de forma independiente contra runtime, README, ROADMAP y RELEASES.

Los snapshots bajo `docs/archive/` preservan su contexto original y no se corrigen retroactivamente para aparentar el estado actual.

## 7. Gates que no quedaron cerrados

Al cerrar GOV.1 todavía quedaban pendientes, según el criterio vigente entonces:

- revisión jurídica externa de privacidad/licencia/publicación;
- hardening específico si se decide exposición LAN/Internet;
- decisión final sobre servir Bootstrap localmente o mantener una excepción revisada;
- auditoría ampliada WCAG 2.2 con tecnologías de apoyo y dispositivos;
- cierre funcional/UX de UX.4.6e, UX.4.6f y UX.4.6g (numeración prospectiva vigente al momento del cierre GOV.1);
- definición final del alcance de publicación;
- inventario de licencias/NOTICE del artefacto real cuando exista empaquetado.

> **Nota posterior — UX.4.6e R6:** al cerrar GOV.1, la secuencia prospectiva reservaba UX.4.6e/UX.4.6f/UX.4.6g para los Pasos 4/5/6. Durante la estandarización post-GOV.1 se reasignó UX.4.6e al bloque transversal y esos pasos pasaron a UX.4.6f/UX.4.6g/UX.4.6h. Las referencias anteriores se conservan como evidencia histórica y no se reinterpretan retroactivamente.

> **Nota posterior — PLAN.1:** los gates restantes se reorganizan en el plan maestro de 14 bloques hacia `1.0.0.0`. La referencia histórica a una «primera beta pública» deja de ser el objetivo vigente y se sustituye por el gate de primera versión oficial.

## 8. Decisión final

Con todos los gates de cierre ejecutados satisfactoriamente:

1. GOV.1.8 queda cerrado;
2. GOV.1 completo queda cerrado;
3. `0.0.24-beta` es la versión formal vigente de ese cierre;
4. `v0.0.24-beta` permanece publicado e inmutable;
5. UX.4.6e quedó reanudada como bloque funcional posterior y fue cerrada más adelante en `0.0.25-beta`.

El saneamiento documental/repositorio posterior al tag se registra en `[Unreleased]` y **no modifica retroactivamente el contenido criptográficamente identificado por `v0.0.24-beta`**.
