# VER.2 R6 — Decisión del modelo revision-aware

**Issue propietaria:** #164
**Base:** CP1 `69cc6b4ce2e59e7da7aba1c4dc764923cc8cca81`
**Fecha:** 2026-09-20
**Estado:** decisión arquitectónica aprobada para implementación

## 1. Propósito

VER.2 R6 debe eliminar ambigüedades acumuladas entre Global, revisión
funcional, ordinal aceptado, correcciones materiales, mantenimiento de
dependencias y publicación.

Este checkpoint fija la semántica antes de modificar parsers, ledger,
registry, manifest o `VERSION`.

No materializa candidato revision-aware y no reserva G128.

## 2. Familias preservadas

La historia publicada permanece inmutable.

Se reconocen tres familias:

1. legacy histórica: `0.0.N-beta`;
2. revision-aware v1 histórica: `0.<G_HI>.<G_LO>.<EE>-beta`;
3. revision-aware v2 prospectiva:
   `0.<G_HI>.<G_LO>.<EE>.<CCC>.<DDD>-beta`.

La tercera forma es equivalente a la extensión evaluada como
`0.GG.RR.EE.CCC.DDD-beta`, pero usa los nombres internos `G_HI` y `G_LO`
para evitar confundir el segundo fragmento del Global con una revisión
funcional `R#`.

Ningún tag o Release histórico se renombra, mueve, recrea o normaliza.

## 3. Global

`G` continúa siendo el contador monotónico de estados materialmente distintos
y aceptados.

Su codificación beta permanece:

- `G_HI = Global // 100`;
- `G_LO = Global % 100`, representado con dos dígitos.

Por ejemplo, un Global sintético G234 se codifica como `2.34`.

El número global no representa la revisión funcional.

Un checkpoint de trabajo, commit, PR, squash, tag o intento fallido no consume
por sí mismo un Global.

## 4. Revisión funcional y Edition

La revisión funcional, por ejemplo `R6`, `R1.1` o `R3B2`, continúa como
metadata semántica del bloque.

`EE` representa exclusivamente el ordinal de estados aceptados dentro del
bloque y conserva dos dígitos.

Por tanto, revisión funcional y Edition pueden divergir.

Una subrevisión consume Global y Edition solamente cuando existe evidencia
de aceptación material independiente.

Una iteración que permanece como checkpoint interno no incrementa ninguno.

## 5. Corrección material — CCC

`CCC` usa tres dígitos.

`000` significa que el estado no es una corrección material de un estado
previamente aceptado dentro de la misma línea funcional.

`001`–`999` identifican correcciones materiales aceptadas posteriores.

Reglas:

- una corrección realizada antes de que el candidato sea aceptado no aumenta
  `CCC`;
- un intento fallido no aumenta `CCC`;
- un hotfix posterior a un estado aceptado utiliza un nuevo Global y Edition
  y aumenta `CCC`;
- una corrección parcial puede usar `CCC > 000` si constituye por sí misma un
  estado aceptado, aunque la revisión funcional continúe abierta;
- una nueva revisión funcional reinicia `CCC` a `000`;
- si fueran necesarias más de 999 correcciones dentro de una misma línea
  funcional, la política debe revisarse antes de continuar.

Ejemplo sintético:

`0.2.34.07.000.000-beta`

puede representar un estado ordinario G234/E07.

Una corrección material aceptada posterior podría producir, en otro Global:

`0.2.35.08.001.000-beta`.

Estos ejemplos no corresponden al roadmap vigente.

## 6. Mantenimiento de dependencias — DDD

`DDD` usa tres dígitos y distingue los ciclos materiales de MANT.2.

Reglas:

- `000` para estados que no pertenecen a MANT.2;
- `001`–`999` para ciclos MANT.2 aceptados;
- el contador es monotónico a través del proyecto;
- no se incrementa por cada PR Dependabot;
- solo aumenta cuando un nuevo ciclo MANT.2 constituye un estado material
  aceptado;
- correcciones aceptadas dentro del mismo ciclo MANT.2 conservan `DDD` y
  utilizan `CCC` cuando corresponda;
- un nuevo ciclo MANT.2 reinicia `CCC` a `000`;
- múltiples lotes de dependencias solo reciben valores distintos cuando se
  gobiernan como ciclos materiales independientes.

MANT.2 R1/G123 y MANT.2 R2/G127 se preservan con sus versiones históricas
originales. El ledger v2 podrá registrar respectivamente sus ordinales de
mantenimiento 1 y 2 como metadata, sin alterar sus strings, tags o Releases.

Un ejemplo sintético de un ciclo MANT.2 posterior sería:

`0.2.36.05.000.012-beta`.

El ejemplo es ilustrativo y no reserva ningún estado futuro real.

## 7. Intentos, checkpoints y subrevisiones

Un intento fallido o revertido:

- no consume Global;
- no incrementa Edition;
- no incrementa `CCC`;
- no incrementa `DDD`;
- permanece trazable mediante Git, PR, Issue o auditoría.

Un checkpoint firmado de una fase en curso tampoco consume esos contadores
salvo que la Issue propietaria declare y demuestre su aceptación independiente.

Una subrevisión aceptada de forma independiente sí consume Global y Edition,
pero usa `CCC = 000` cuando es evolución funcional y no una corrección de un
estado previamente aceptado.

## 8. Fases insertadas dinámicamente

Una fase intermedia descubierta mediante #166 u otro control de gobierno no
recibe un Global al ser planificada.

Primero se incorpora al árbol canónico y a sus Issues.

Solo cuando existe un candidato material validado puede utilizar el siguiente
Global disponible.

Esto impide que fases futuras reserven números por anticipado y evita
renumeraciones del roadmap.

## 9. Candidato, integración y publicación

VER.2 R6 separa tres planos que no deben confundirse:

1. snapshot versionado del candidato;
2. estado operacional de PR/integración;
3. estado real de publicación mediante Git/tag/GitHub Release.

Un artefacto versionado no puede describir de forma fiable un hecho que solo
ocurrirá después de que ese mismo snapshot sea integrado o etiquetado.

Por tanto:

- manifest y registry no deben usar frases transitorias como
  `accepted_pending_publication` como verdad viva de publicación;
- el manifest debe ser un snapshot estable de entrada al proceso de release;
- la existencia de tag/Release se deriva durante la ejecución desde Git y
  GitHub;
- las notas de Release combinan el snapshot estable con hechos de publicación
  resueltos en runtime;
- un Release histórico no se reescribe para aparentar un estado posterior;
- documentación viva y datos versionados deben distinguir explícitamente
  snapshot, planificación y evidencia externa.

## 10. Dirección del ledger v2

La implementación deberá evolucionar el ledger sin alterar la identidad
histórica de G001–G127.

El modelo objetivo debe poder representar explícitamente:

- esquema/formato usado por cada entrada;
- Global;
- bloque;
- Edition;
- revisión funcional;
- ordinal de corrección;
- ordinal de mantenimiento MANT.2;
- evidencia;
- candidato actual como entidad separada o `null`;
- siguiente Global aritméticamente disponible.

`next_global` será el nombre canónico del siguiente número disponible.

La semántica específica
`next_global_if_ver2_accepted`
deberá retirarse porque acopla una regla general a una fase concreta.

## 11. Compatibilidad de parsers

La implementación no puede invalidar versiones ya publicadas.

Los parsers deberán aceptar:

- `0.0.N-beta`;
- revision-aware v1 `0.<G_HI>.<G_LO>.<EE>-beta`;
- revision-aware v2
  `0.<G_HI>.<G_LO>.<EE>.<CCC>.<DDD>-beta`;
- versiones oficiales de cuatro componentes.

Solo los estados nuevos posteriores a la adopción efectiva de R6 utilizarán
la familia revision-aware v2.

La versión exacta del futuro candidato de VER.2 no se fija en este checkpoint.

## 12. Transición a 1.0

La primera versión oficial continúa prevista como:

`1.0.0.0`

Los componentes `G`, `EE`, `CCC` y `DDD` son coordenadas de gobierno
pre-1.0 y de auditoría.

Después de 1.0 pueden seguir registrándose como metadata interna del ledger,
pero no se añaden como componentes públicos adicionales de la versión estable.

La familia estable conserva:

`MAYOR.MENOR.PARCHE.REVISIÓN`

El Build sigue siendo independiente y será responsabilidad de REL.1.

## 13. Casos que la implementación debe demostrar

La suite de VER.2 R6 deberá cubrir, como mínimo:

- varias revisiones sin correcciones;
- revisión funcional y Edition divergentes;
- subrevisiones aceptadas A/B/C;
- checkpoint no aceptado;
- intento fallido y revertido;
- corrección material aceptada;
- corrección parcial que no cierra la revisión;
- hotfix posterior a publicación;
- MANT.2 ordinario;
- corrección dentro de MANT.2;
- múltiples ciclos MANT.2;
- fase intermedia insertada dinámicamente;
- fase documental o de planificación transversal;
- snapshot candidato frente a estado publicado;
- compatibilidad con todos los identificadores históricos;
- transición a `1.0.0.0`.

## 14. Fronteras de este checkpoint

Este checkpoint únicamente fija el modelo.

No modifica:

- `VERSION`;
- ledger JSON;
- registry;
- manifest;
- parsers;
- release tooling;
- workflows;
- roadmap;
- fases posteriores.

G128 continúa siendo solo el siguiente Global aritméticamente disponible y
permanece sin candidato, bloque ni versión asignados.
