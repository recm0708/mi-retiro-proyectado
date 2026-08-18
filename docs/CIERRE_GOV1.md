# Cierre GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta

**Estado:** Candidato de cierre GOV.1.8
**Versión formal:** `0.0.24-beta`
**Fecha:** 2026-08-18
**Clasificación:** Gobierno / Auditoría final / Pre-beta

## 1. Objetivo

GOV.1 se creó para detener temporalmente la evolución UX y revisar de forma transversal el historial, versionado, documentación, integridad Git/GitHub, observabilidad, seguridad, privacidad, terceros, licencia y proceso de release antes de continuar el desarrollo pre-beta.

Este documento consolida la decisión de cierre. No sustituye Git, CI, los ADR, las fuentes normativas ni los documentos especializados.

## 2. Resultado por bloque

| Bloque | Resultado |
|---|---|
| GOV.1.1 | reconstrucción histórica y clasificación de 80 commits completada |
| GOV.1.2 | gobierno, versionado y fuente canónica `VERSION` completados |
| GOV.1.3 | reorganización documental, normativa, privacidad y auditoría completadas |
| Prebloque firma/integridad | commits/tags firmados, 23/23 tags auditados y rulesets completados |
| GOV.1.4 | Developer Diagnostics local y estructurado completado |
| GOV.1.5 | seguridad, privacidad, threat model y procedimientos completados internamente |
| GOV.1.6 | controles GitHub, `SECURITY.md`, templates y auditoría automática completados |
| GOV.1.7 | licencia propietaria pre-beta y terceros completados |
| GOV.1.8 | auditoría final, versión `0.0.24-beta` y decisión de reanudar UX.4.6e |

## 3. Evidencia técnica

Línea base previa a GOV.1.8:

```text
530 pruebas
OK
```

GOV.1.8 añade 10 regresiones de cierre:

```text
540 pruebas esperadas
```

El cierre exige además:

- `python -m compileall app`;
- `node --check` para JavaScript;
- `git diff --check`;
- commit de rama firmado;
- Pull Request hacia `main`;
- checks `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`;
- squash `Verified`;
- validación post-merge;
- tag anotado y firmado `v0.0.24-beta`.

## 4. Evidencia Git/GitHub previa al candidato

Antes de GOV.1.8 se verificó:

- PR #15 fusionado para GOV.1.6/GOV.1.7;
- PR #16 fusionado para el hotfix documental de licencia;
- ambos squash verificados por GitHub;
- los tres workflows/checks relevantes en `success`;
- cero PR abiertos;
- solo `main` como rama remota persistente después de limpieza;
- métodos de merge configurados para squash como flujo ordinario.

Los detalles del ruleset que no expone el conector permanecen sujetos a la verificación manual documentada en `AUDITORIA_GITHUB.md`.

## 5. Versión de cierre

`0.0.24-beta` es una **versión interna pre-beta formal**.

Representa el cierre auditable de GOV.1 y no debe confundirse con:

- la primera beta pública;
- una certificación de la CSS;
- una aprobación jurídica externa;
- una declaración de Internet-ready.

La primera familia pública prevista continúa siendo:

```text
0.1.0-beta.1
```

## 6. Regla de versiones históricas

Los documentos que registran revisiones GOV.1.3, GOV.1.5 y GOV.1.7 pueden conservar `0.0.23-beta` como **versión base de revisión** cuando no fueron materialmente modificados por GOV.1.8.

GOV.1.8 deja de exigir que una regresión histórica reescriba esos documentos únicamente porque `VERSION` avance. La versión canónica actual continúa validándose de forma independiente contra runtime, README, ROADMAP y RELEASES.

## 7. Gates que NO quedan cerrados

Cerrar GOV.1 no significa que la beta pública esté lista. Permanecen, según aplique:

- revisión jurídica externa de privacidad/licencia/publicación;
- hardening específico si se decide exposición LAN/Internet;
- decisión final sobre servir Bootstrap localmente o mantener una excepción revisada;
- auditoría ampliada WCAG 2.2 con tecnologías de apoyo y dispositivos;
- cierre funcional/UX de UX.4.6e, UX.4.6f y UX.4.6g;
- definición final del alcance de la primera beta;
- inventario de licencias/NOTICE del artefacto real cuando exista empaquetado.

## 8. Decisión

Si la suite de 540 pruebas, compilación, JavaScript, `git diff --check`, CI y revisión del PR permanecen verdes:

1. GOV.1.8 se considera cerrado;
2. GOV.1 completo se considera cerrado;
3. `0.0.24-beta` pasa a ser la versión formal vigente;
4. se crea y publica el tag firmado `v0.0.24-beta`;
5. UX.4.6e queda oficialmente reanudada como siguiente bloque activo.

Si cualquier gate falla, no se crea el tag y GOV.1.8 vuelve a estado de corrección.
