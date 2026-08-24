# VER.2 R4 — Promoción controlada G071/E01

- Fecha local de generación: 2026-08-23T23:52:45
- Versión anterior en `VERSION`: `0.0.26-beta`
- Versión promovida en `VERSION`: `0.0.71.01-beta`
- Último tag formal legacy antes del cierre: `v0.0.26-beta`
- Tag formal pendiente post-merge: `v0.0.71.01-beta`

## 1. Decisión

VER.2 R4 promueve `VERSION` a `0.0.71.01-beta` como G071/E01.

Esta promoción consume el candidato documentado en VER.2 R1, R2 y R3, pero no crea el tag formal dentro del PR. El tag `v0.0.71.01-beta` queda pendiente para el cierre firmado post-merge, después de revalidar `main`.

## 2. Alcance

- Actualiza `VERSION`.
- Sincroniza documentación viva que declaraba el estado vigente de la aplicación.
- Mantiene referencias históricas a `0.0.26-beta` cuando documentan cierres anteriores.
- No mueve ni recrea `v0.0.26-beta`.
- No crea tags revision-aware retrospectivos para G001–G070.
- No modifica motores previsionales, normativa, datos protegidos ni `_entregas/`.

## 3. Estado de tags

- `v0.0.26-beta` permanece como último tag formal legacy antes de cerrar G071/E01.
- `v0.0.71.01-beta` no se crea dentro de esta rama.
- `v0.0.71.01-beta` solo debe crearse después de merge, revalidación post-merge y verificación de firma.

## 4. Criterio de aceptación

G071/E01 queda listo para aceptación si:

1. `VERSION` contiene exactamente `0.0.71.01-beta`.
2. `APP_VERSION` expone el mismo valor.
3. La documentación viva declara la promoción sin falsear historia.
4. La suite completa pasa.
5. GitHub Actions pasa en el PR.
6. `main` se revalida después del merge.
