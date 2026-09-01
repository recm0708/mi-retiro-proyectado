# Fuentes oficiales preservadas

**Estado:** colección de preservación documental
**Alcance:** normativa, publicaciones oficiales y referencias institucionales utilizadas por Mi Retiro Proyectado
**Uso en runtime:** no
**Autoridad canónica:** la publicación oficial de origen

Esta carpeta conserva copias binarias de fuentes oficiales relevantes para la trazabilidad normativa, la reproducibilidad documental y la consulta offline del proyecto.

Las copias locales **no sustituyen** a la fuente oficial ni convierten una nota, hoja de cálculo o publicación institucional en norma jurídica. Cuando existe diferencia entre una copia preservada y una publicación oficial vigente, prevalece la fuente oficial verificada.

## Organización

```text
official/
├── pensions/
│   ├── normative/
│   └── reference/
└── privacy/
    └── normative/
```

- `pensions/normative/` conserva leyes, textos únicos, gacetas, reglamentos y resoluciones vinculados con los sistemas previsionales modelados.
- `pensions/reference/` conserva referencias institucionales útiles para contraste técnico que no constituyen por sí mismas una norma; aquí se encuentra el cuadro comparativo de pensiones publicado por la CSS.
- `privacy/normative/` conserva el marco legal oficial de protección de datos personales citado por la documentación del proyecto.

## Manifiesto

`manifest.json` es el inventario machine-readable de la colección. Cada entrada conserva:

- identificador estable;
- dominio y clasificación;
- título descriptivo;
- emisor;
- rol documental;
- nombre canónico local;
- nombre original servido por la URL;
- URL oficial;
- página institucional de procedencia;
- tamaño;
- SHA-256;
- fecha de captura;
- tipo de medio.

El auditor `scripts/audit_official_sources.py` comprueba localmente que los binarios existan, tengan el tamaño y SHA-256 declarados, conserven una firma coherente con PDF/XLSX y no existan archivos huérfanos.

## Nombres

Los binarios siguen `docs/standards/naming-conventions.md`: ASCII, minúsculas, `kebab-case`, sin espacios ni sufijos informales. Los números de ley, resolución, gaceta y otros identificadores regulatorios se preservan en el nombre cuando aportan trazabilidad.

## Actualización

Para incorporar o sustituir una fuente:

1. verificar que la URL y la página de procedencia sean oficiales;
2. descargar a un área temporal fuera del repositorio;
3. comprobar tipo de archivo y calcular SHA-256;
4. asignar nombre canónico;
5. conservar el nombre original servido por el origen;
6. actualizar `manifest.json`;
7. ejecutar `python scripts/audit_official_sources.py`;
8. actualizar `docs/regulatory/regulatory-sources.md` cuando cambie la fuente utilizada o su interpretación;
9. ejecutar los gates documentales y de integridad antes del commit.

Una actualización de la copia local no debe alterar silenciosamente la lógica de cálculo. Los cambios normativos que afecten motores, tablas o decisiones de producto siguen el proceso normal de revisión normativa y pruebas.

## Derechos de terceros

Estos documentos son materiales oficiales de terceros y **no son relicenciados** por la licencia propietaria de Mi Retiro Proyectado. Su presencia en el repositorio tiene fines de preservación, trazabilidad, revisión y consulta. Consulta `LICENSE` y `THIRD_PARTY_NOTICES.md`.
