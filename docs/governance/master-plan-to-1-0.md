# Plan maestro hacia Mi Retiro Proyectado 1.0

**Estado:** vigente
**Baseline publicado:** G129/E03/C0 — `0.129.3.0-beta`
**Fase material activa:** DOC.4 R1 / #171
**Siguiente Global aritmético:** G130, libre y sin candidato
**Objetivo estable:** `1.0.0.0`

## 1. Función del plan

Este documento es la autoridad narrativa de **dependencias, orden y reglas del
programa pre-1.0**.

No es:

- un ledger de versiones;
- un changelog;
- una réplica de cada Issue;
- una tabla exhaustiva de superficies UX.

La historia aceptada está en el ledger/Git/Releases. El detalle tabular del
trabajo pendiente está en
[Matriz maestra de pendientes](pre-1-0-pending-matrix.md).

## 2. Principios

1. Ninguna fase planificada recibe Global, Edition o `VERSION` por anticipado.
2. Un Global se materializa únicamente cuando existe candidato real validable.
3. Un intento fallido no consume otro Global.
4. Trabajo material nuevo con responsabilidad propia recibe owner antes de
   continuar.
5. #166 puede insertar mantenimiento de dependencias cuando el preflight lo
   exija.
6. Los lotes internos no consumen Globals independientes salvo decisión
   explícita.
7. Gates manuales o transversales no se convierten en versiones por inercia.
8. La frontera UX permanece dinámica hasta estabilizar todas las superficies
   pre-1.0.
9. El producto no alcanza `1.0.0.0` por un número determinado de Globals:
   debe cerrar sus gates.
10. Documentación, Issues, registry, ledger y matriz deben expresar el mismo
    programa vigente.

## 3. Baseline de entrada vigente

G129/E03/C0 — MANT.2 R3 está cerrado e integrado en:

```text
VERSION: 0.129.3.0-beta
main:    dca3871c3472e20074cf51d85d28eeeccb9b6f32
tag:     v0.129.3.0-beta
Release: 399260564
```

El #166 fresco posterior a G129 quedó CLEAN.

DOC.4 R1 inició sobre ese baseline sin asignar G130. La separación actual es:

```text
accepted_baseline = G129/E03/C0
active_phase       = DOC.4 R1 / #171
current_candidate  = unassigned
next_global        = G130 libre
```

## 4. Grafo canónico pre-1.0

```text
DOC.4 R1 / #171
→ auditoría previsional / #142
→ [fases funcionales obligatorias derivadas, si existen]
→ PERSIST.1 / #130
→ REP.1 / #143
→ DEPLOY.1 / #157
→ programa UX / #129: UX.7 → UX.x
→ gate visual multiportal / #189
→ SEC.2 R7 / #144
→ rendimiento / #156
→ A11Y.2 / #145
→ REV.1 / #146
→ settings GitHub / #153
→ DOC.1 R6 / #147
→ QA.1 / #148
→ REL.1 / #149
→ 1.0.0.0
```

#166, #203, #214, DOC.3 y #189 son transversales y no sustituyen esos bloques.

## 5. DOC.4 R1 — baseline documental nuevo

DOC.4 elimina la acumulación de estados históricos dentro de documentación
viva y racionaliza artefactos documentales/no ejecutables.

Incluye:

- revisión individual de Markdown (#172);
- decisiones de conservar, reescribir, fusionar, dividir, mover, renombrar o
  eliminar;
- reestructuración física e índices (#173);
- revisión de artefactos declarativos (#174);
- saneamiento de rutas/nombres/entorno heredado (#209);
- reconciliación de guardas documentales obsoletas (#215).

El cierre de DOC.4 reinicia la cadencia de DOC.3 y deja una autoridad clara por
tema.

## 6. Auditoría previsional — #142

Debe ocurrir después de DOC.4 y antes de persistencia.

Objetivo:

- contrastar cobertura real de SEBD, Mixto y SUCGS;
- revisar modalidades y prestaciones relevantes;
- identificar faltantes funcionales obligatorios para 1.0;
- crear Issues derivadas cuando exista una carencia material.

Un derivado obligatorio se inserta antes de PERSIST.1 para evitar congelar
persistencia sobre un dominio incompleto.

## 7. PERSIST.1 — #130

PERSIST.1 define persistencia voluntaria y segura:

- guardar/restaurar/borrar;
- esquema y migraciones;
- separación de datos Asegurado/Developer;
- privacidad y retención;
- controles Developer aplicables;
- auditoría técnica de persistencia.

Si introduce UI nueva, esa superficie recibe una UX.x antes del cierre.

## 8. REP.1 — #143

REP.1 materializa informes/exportaciones reproducibles y trazables.

Debe definir formato, contenido, fuentes, privacidad y reproducibilidad. Una
pantalla/modal nueva recibe una UX.x; no se reserva hoy un número UX para ella.

## 9. DEPLOY.1 — #157

DEPLOY.1 fija el contrato operativo de despliegue:

- runtime;
- hosting;
- HTTPS;
- secretos/configuración;
- persistencia operativa;
- CI/CD;
- condiciones de soporte.

Cualquier superficie visual de deployment queda bajo el programa UX dinámico.

## 10. Programa UX final

La ola UX ocurre después de #142/derivados, PERSIST.1, REP.1 y DEPLOY.1 para
revisar superficies funcionalmente estables.

Regla de granularidad:

> Una UX.x corresponde a una superficie, paso o modal material.

El baseline conocido es UX.7–UX.32. La lista exacta de Issues/superficies está
en la matriz de pendientes.

Si aparece otra superficie material:

1. se crea la siguiente UX consecutiva después del baseline registrado;
2. recibe Issue propio;
3. se actualizan #129 y las autoridades vivas;
4. se aplica #189;
5. no se renumeran UX existentes;
6. no se preasigna Global.

UX.7 mantiene la única agrupación deliberada ya definida para las páginas de
Inicio de ambos portales; el login Developer conserva su UX independiente.

## 11. Gate multiportal — #189

Todo cambio visual se clasifica como `shared` o `portal-specific`.

Un cambio shared debe reconciliar donde aplique:

- tokens y paleta;
- tipografía;
- botones, inputs y controles;
- tarjetas/tablas/alerts/badges;
- spacing, bordes, radios y sombras;
- foco;
- temas Claro/Oscuro/Automático/Alto contraste;
- forced-colors y motion;
- selector de apariencia;
- footer y patrones comunes.

Una UX no cierra dejando drift shared conocido sin un owner bloqueante.

## 12. Salida de UX

SEC.2 R7 se habilita cuando:

- todas las UX.x obligatorias registradas están cerradas/absorbidas;
- no queda superficie material sin clasificación UX;
- no existe derivado bloqueante de sincronización;
- #189 confirma ausencia de drift shared conocido.

El número UX final no está predefinido.

## 13. Gates finales

### SEC.2 R7 — #144

Hardening final de seguridad sobre producto/deployment estabilizado.

### Rendimiento — #156

Medición reproducible y corrección de problemas materiales de rendimiento.

### A11Y.2 — #145

Auditoría final de accesibilidad sobre las superficies definitivas, incluyendo
WCAG 2.2, reflow, forced-colors y tecnologías de apoyo cuando corresponda.

### REV.1 — #146

Revisión final normativa, jurídica, privacidad y terceros.

### Settings GitHub — #153

Revalidación manual de configuración pública/security/release/deploy. No
consume Global mientras sea exclusivamente un gate de configuración.

### DOC.1 R6 — #147

Freeze documental final pre-QA. No sustituye DOC.4: DOC.4 crea el baseline;
DOC.1 R6 congela el producto beta final.

### QA.1 — #148

Validación integral del candidato beta final.

### REL.1 — #149

Empaquetado/publicación oficial `1.0.0.0`, Build reproducible, hashes, firma,
SBOM/terceros y Release oficial según el alcance final.

## 14. Cadencia DOC.3

DOC.4 crea un nuevo baseline documental y reinicia el contador.

Por defecto, una nueva DOC.3 integral ocurre después de la segunda fase
material top-level aceptada desde ese baseline, salvo que un impacto documental
alto justifique adelantarla.

No se crea ni se versiona una DOC.3 futura solo por esta regla.

## 15. Políticas transversales

- **#166:** preflight Dependabot/limpieza y posible inserción MANT.2.
- **#203:** workspace remoto, SYNC POINTS y transferencia canónica.
- **#214:** briefing + aprobación previa de fase.
- **#189:** sincronización visual multiportal.
- **DOC.3:** auditoría documental por cadencia.

## 16. Post-1.0

Fuera del alcance obligatorio actual:

- #131 — i18n;
- #150 — sesiones/accesos Developer avanzados;
- #151 — notificaciones Developer;
- #152 — Bearer granular, salvo escalamiento explícito por seguridad.

Si un bloque post-1.0 se escala y crea UI pre-1.0, entra también al programa UX.

## 17. Clasificación actual

**Obligatorio antes de 1.0:** DOC.4, #142 y derivados necesarios, PERSIST.1,
REP.1, DEPLOY.1, UX.7→UX.x, SEC.2 R7, #156, A11Y.2, REV.1, DOC.1 R6, QA.1 y
REL.1.

**Transversal:** #166, #203, #214, #189, #153 y DOC.3.

**Post-1.0:** #131, #150, #151 y #152 por defecto.

**Absorbido:** #176 por DOC.4/Lote C.

No existe actualmente un bloque “opcional 1.0” sin owner identificado.

## 18. Autoridades sincronizadas

- [Roadmap](roadmap.md);
- [Matriz maestra de pendientes](pre-1-0-pending-matrix.md);
- [Ledger pre-1.0](pre-1-0-revision-ledger.md);
- [Política de versionado](../../VERSIONING.md);
- [Gobierno](../../GOVERNANCE.md);
- `data/governance/pre-1-0-revision-ledger.json`;
- `data/governance/work-block-registry.json`;
- `data/governance/release-publication-manifest.json`;
- Issues propietarias.

## 19. Continuidad

DOC.4 es la fase material activa. Su siguiente paso ordinario es #142 una vez
DOC.4 quede cerrado/publicado y un preflight #166 fresco lo habilite.

G130 permanece disponible pero no pertenece a DOC.4 ni a #142 hasta que exista
un candidato material que cumpla el contrato revision-aware.
