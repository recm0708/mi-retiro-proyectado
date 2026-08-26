# Identidad visual de Mi Retiro Proyectado

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.10.01-beta`
**Versión base histórica:** `0.0.24-beta`
**Fecha:** 2026-08-19
**Clasificación:** Producto / UX / Marca / GitHub

## 1. Objetivo

Este documento define la identidad gráfica canónica de Mi Retiro Proyectado, separa los archivos maestros de sus derivados y establece qué activos utiliza el runtime de la aplicación y cuáles pertenecen a presentación del repositorio.

La identidad es propia del proyecto y **no representa afiliación, patrocinio ni identidad oficial de la Caja de Seguro Social de Panamá**.

## 2. Logo oficial

El logo mark oficial es el símbolo circular que representa a una pareja adulta mayor, un calendario con marca de verificación y la referencia monetaria `B/.`.

El símbolo se utiliza como:

- marca de la barra superior de la aplicación;
- base de favicon;
- Apple Touch icon;
- iconos de aplicación preparados para usos futuros;
- identidad del README;
- elemento principal del Social Preview de GitHub.

No se utiliza un logotipo oficial de la CSS ni se debe añadir uno como parte de la marca del producto.

## 3. Fuente canónica

La fuente original conservada es:

`assets/brand/source/icono-simple-master-1254.png`

Dimensiones reales:

`1254 × 1254 px`

La copia normalizada para derivación es:

`assets/brand/source/icono-simple-1024.png`

Dimensiones:

`1024 × 1024 px`

Ambos archivos conservan canal alfa. El fondo transparente forma parte del contrato del activo.

## 4. Familia canónica de iconos

Los derivados oficiales se mantienen en `assets/brand/icons/`:

- `icon-16.png`
- `icon-32.png`
- `icon-48.png`
- `icon-64.png`
- `icon-128.png`
- `icon-180.png`
- `icon-192.png`
- `icon-256.png`
- `icon-512.png`
- `icon-1024.png`

No se añaden resoluciones adicionales salvo que exista un consumidor real que las requiera.

## 5. Logo marks para presentación

`assets/brand/logos/` contiene:

- `logo-mark-512.png`
- `logo-mark-1024.png`

Estos archivos se destinan a documentación, GitHub y otras superficies de presentación que necesiten una resolución mayor que la usada en la barra de navegación.

## 6. Activos del runtime

La aplicación consume únicamente derivados necesarios bajo:

`app/static/img/brand/`

Inventario:

- `logo-mark-128.png` — barra de navegación;
- `favicon.ico` — contenedor ICO multicapa;
- `favicon-16x16.png`;
- `favicon-32x32.png`;
- `favicon-48x48.png`;
- `apple-touch-icon.png` — 180 × 180;
- `app-icon-192.png`;
- `app-icon-512.png`.

El ICO vigente contiene 16 × 16, 32 × 32, 48 × 48 y 256 × 256.

La plantilla global declara explícitamente favicon PNG/ICO y Apple Touch icon. La capa `app/static/css/brand.css` controla únicamente presentación de marca y se mantiene separada del sistema visual transversal.

## 7. Temas y accesibilidad

El logo oficial conserva sus colores originales en:

- Claro;
- Oscuro;
- Automático;
- Alto contraste.

No se recolorea el contenido raster para simular una variante temática. En Alto contraste se permite una señal externa de contorno para mantener separación perceptible respecto al fondo.

El `<img>` de la navbar utiliza `alt=""` porque el enlace contenedor ya tiene un nombre accesible mediante `aria-label` y el texto visible de marca aparece inmediatamente al lado. Esto evita anunciar dos veces la misma identidad.

## 8. Social Preview de GitHub

Archivo versionado:

`assets/social/github-social-preview.png`

Contrato:

- 1280 × 640 px;
- PNG;
- menos de 1 MiB;
- logo oficial;
- nombre `Mi Retiro Proyectado`;
- texto de planificación previsional en Panamá;
- declaración visible `Herramienta independiente · No oficial`.

La misma pieza se configura manualmente como Social Preview del repositorio de GitHub.

## 9. README

El README utiliza:

`assets/brand/logos/logo-mark-512.png`

La imagen es presentación documental y no altera el runtime.

## 10. Regeneración con ImageMagick

La fuente normalizada se genera desde el maestro:

```powershell
magick `
    ".\assets\brand\source\icono-simple-master-1254.png" `
    -resize 1024x1024 `
    -strip `
    ".\assets\brand\source\icono-simple-1024.png"
```

La familia canónica se deriva así:

```powershell
$sizes = 16, 32, 48, 64, 128, 180, 192, 256, 512, 1024

foreach ($size in $sizes) {
    magick `
        ".\assets\brand\source\icono-simple-1024.png" `
        -resize "${size}x${size}" `
        -strip `
        ".\assets\brand\icons\icon-$size.png"
}
```

Después de regenerar, deben ejecutarse las regresiones de identidad visual antes de reemplazar un activo ya aprobado.

## 11. Control de cambios

Un cambio sustancial del símbolo, composición o significado visual exige:

1. conservar o documentar la fuente anterior si tuvo uso oficial;
2. regenerar derivados desde una única fuente aprobada;
3. revisar navbar, favicon, temas, README y Social Preview;
4. actualizar este documento;
5. ejecutar pruebas automatizadas y validación visual.

Una simple optimización sin cambio perceptible debe conservar las dimensiones y el contrato de transparencia aplicable.
