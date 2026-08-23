# Auditoría integral del repositorio — 2026-08-18

**Estado:** completada
**Versión de aplicación auditada:** `0.0.24-beta`
**Commit base auditado:** `653900cebd84019fbbaa3ff3cfd91536ccab76eb`
**Tag de cierre:** `v0.0.24-beta`
**Alcance:** repositorio, Git/GitHub, documentación, configuración, gobierno y metadatos; excluye auditoría de lógica funcional de `app/` salvo referencias administrativas del repositorio.

## 1. Fuentes utilizadas

La revisión cruzó:

- snapshot de archivos versionados fuera de la lógica de aplicación;
- reporte Git local generado desde el clon principal;
- inventario local de archivos;
- estado remoto del repositorio y Pull Requests;
- documentación y configuración versionadas;
- comprobaciones de formato, JSON/YAML y enlaces Markdown internos vigentes.

No se recopilaron ni solicitaron claves privadas, tokens, credenciales ni documentos personales.

## 2. Resultado general

No se detectó corrupción del repositorio ni evidencia de secretos o documentos personales versionados en el alcance revisado. La estructura base de gobierno, CI, seguridad, versionado, licencia y documentación es consistente.

Se identificaron deudas documentales post-merge y de metadatos del repositorio. El saneamiento asociado corrige esas deudas sin modificar `VERSION`, sin mover tags y sin reescribir commits históricos.

## 3. Integridad Git

La auditoría local registró:

- **101 commits** alcanzables en el historial principal al momento de la revisión;
- `main` sincronizada con `origin/main`;
- una rama local ya integrada, `fix/gov17-saltos-linea-licencia`, cuyo upstream remoto había sido eliminado;
- una carpeta temporal `_auditoria_repo_20260818_144449/` no rastreada;
- `git fsck --full` sin corrupción de objetos;
- objetos `dangling` residuales de operaciones históricas/migración, sin `garbage` reportado.

Los objetos `dangling` no justifican reescritura ni limpieza agresiva. Puede utilizarse mantenimiento Git ordinario posteriormente, pero no forma parte del saneamiento funcional/documental.

## 4. Firmas de commits y tags

La política adoptada durante la migración criptográfica se mantiene:

- los commits históricos anteriores a la frontera de firma **no se reescriben** para obtener un badge `Verified`;
- los commits nuevos continúan firmándose;
- los tags publicados permanecen inmutables.

Resultado de tags:

- **24/24 tags** `v0.0.1-beta` a `v0.0.24-beta` verificaron localmente con firma SSH válida;
- `v0.0.24-beta` corresponde al objeto tag `3cdf6f84804c1bb4bdda9e449eb0932528557aa3`;
- ese tag apunta al commit `653900cebd84019fbbaa3ff3cfd91536ccab76eb`.

El estado `N` de commits históricos no firmados describe una etapa anterior a la política; no constituye una razón para alterar el DAG. Los commits/squash generados por GitHub se interpretan conforme al mecanismo de verificación de GitHub y no se equiparan automáticamente a firmas SSH locales.

## 5. Higiene de archivos

Sobre los archivos actuales incluidos en la auditoría se verificó:

- 0 archivos con BOM UTF-8 detectado;
- 0 archivos CRLF detectados en el snapshot auditado;
- 0 archivos de texto no UTF-8 detectados;
- 0 caracteres de control prohibidos;
- 0 líneas con whitespace final;
- JSON normativo válido;
- YAML de GitHub válido;
- ausencia de ZIP, `.bak`, bases locales, logs, PDFs personales o secretos rastreados en el conjunto revisado.

`.gitignore`, `.gitattributes` y `.editorconfig` están bien estructurados. Se añade `_auditoria_repo_*/` a `.gitignore` para impedir que futuras auditorías locales vuelvan a ensuciar `git status`.

## 6. Documentación

La navegación Markdown vigente revisada no presentó enlaces internos rotos en el conjunto activo.

Se detectaron estados transitorios ya superados en:

- `CIERRE_GOV1.md`;
- `VALIDACION.md`;
- `AUDITORIA_GITHUB.md`;
- `ROADMAP.md`;
- `REGISTRO_CAMBIOS_HISTORICO.md`;
- `TRANSPARENCIA.md`;
- `SEGURIDAD_PRIVACIDAD.md`;
- `MODELO_AMENAZAS.md`;
- `EVALUACION_TERCEROS_DESPLIEGUE.md`;
- `THIRD_PARTY_NOTICES.md`;
- `CHANGELOG.md` y `RELEASES.md`.

El saneamiento reemplaza formulaciones de “candidato”, “pendiente” o “debe promoverse” que ya no describen el estado real.

## 7. Archivo histórico

`docs/archive/` se conserva como snapshot. No se corrigen masivamente sus rutas antiguas ni nombres de repositorio, porque hacerlo falsearía el contexto en que fueron capturados. `docs/archive/README.md` aclara esta regla.

También se conserva el nombre histórico del bundle `calculadora-pension-css_pre_firma_2026-08-17.bundle` mencionado en la documentación de migración, porque identifica un artefacto real de aquella operación.

## 8. Cambio de nombre del repositorio

Se adopta como nombre objetivo:

```text
mi-retiro-proyectado
```

Razones:

- coincide con la identidad real del producto;
- evita reducir el proyecto a una “calculadora”;
- no limita nominalmente el alcance a un único subsistema;
- alinea repositorio, README y enlaces públicos.

Después del rename debe actualizarse `origin` en cada clon local. Las URLs vigentes del repositorio se actualizan; las referencias históricas se preservan.

## 9. About y funciones de GitHub

Descripción adoptada:

> Aplicación web independiente y no oficial para estimar, explicar y comparar escenarios de retiro de la CSS de Panamá (SEBD, Mixto y SUCGS).

Configuración recomendada para la etapa privada actual:

- Issues: habilitado;
- Wiki: deshabilitado;
- Projects: deshabilitado mientras no se utilice un tablero;
- Discussions: deshabilitado;
- topics: ninguno por ahora;
- flujo de integración ordinario: Pull Request + checks requeridos + squash.

## 10. Salud comunitaria y soporte

Se incorporan:

- `CODE_OF_CONDUCT.md`;
- `SUPPORT.md`;
- `.github/ISSUE_TEMPLATE/question.yml`.

No se añaden `FUNDING.yml` ni `CITATION.cff`: no responden a una necesidad actual del proyecto.

## 11. Cambios que no se realizan

Esta auditoría no:

- reescribe commits históricos para alterar badges de verificación;
- mueve ni recrea `v0.0.24-beta`;
- incrementa `VERSION`;
- modifica fórmulas, motores o comportamiento previsional;
- declara completada la revisión jurídica externa;
- convierte el repositorio en público;
- declara lista la primera beta pública.

## 12. Limpieza local recomendada

Después de conservar el ZIP de auditoría fuera del repositorio:

```powershell
Remove-Item -Recurse -Force .\_auditoria_repo_20260818_144449
git branch -d fix/gov17-saltos-linea-licencia
git status
```

La eliminación de la rama local solo debe ejecutarse si Git confirma que está integrada; usar `-d`, no `-D`, preserva esa protección.

## 13. Estado de salida

El saneamiento post-GOV.1 es mantenimiento de repositorio y documentación. Debe integrarse mediante un nuevo commit firmado y Pull Request. Se registra en `[Unreleased]` porque ocurre **después** del tag `v0.0.24-beta`.

Una vez integrado y validado, el trabajo funcional puede continuar en **UX.4.6e — Paso 4 · Proyección salarial/laboral**.

> **Nota posterior — UX.4.6e R7:** la recomendación final de esta auditoría conserva la numeración prospectiva vigente en el momento en que se emitió. La secuencia actual reserva **UX.4.6e** para la estandarización transversal y desplaza **Paso 4 / Paso 5 / Paso 6** a **UX.4.6f / UX.4.6g / UX.4.6h**. El texto original se preserva como evidencia histórica y no se reescribe retroactivamente.
