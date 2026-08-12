# Subsistema Mixto — diseño y alcance del motor

El Subsistema Mixto combina un **Componente de Beneficio Definido (BD)** y un **Componente de Ahorro Personal (CAP)**. La aplicación conserva ambos componentes separados y solo suma resultados cuando su naturaleza y datos permiten hacerlo.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

Fuentes y enlaces completos: [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md).

## 1. Estructura general

```text
Subsistema Mixto
├── Componente de Beneficio Definido
│   └── prestación mensual o indemnización según modalidad
└── Componente de Ahorro Personal
    ├── pensión programada; o
    └── devolución total cuando corresponda
```

El resultado puede contener:

- pensión mensual total;
- pago único BD;
- pago único CAP;
- total de pagos únicos;
- garantía futura del CAP.

## 2. Componente de Beneficio Definido

### 2.1. Salario participante

La participación salarial se limita a **B/.500.00 mensuales**.

Como el historial actual es anual, la aplicación aproxima el máximo del año como:

```text
B/.500 × cuotas registradas en el año
```

La interfaz muestra una advertencia porque un historial mensual oficial puede producir un resultado distinto en años irregulares.

### 2.2. Modalidad

El componente BD reutiliza la clasificación general de edad/cuotas del SEBD:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- Indemnización por Vejez cuando corresponde.

Los parámetros monetarios del componente siguen siendo propios del Mixto.

## 3. Componente de Ahorro Personal

### 3.1. Saldo

El motor exige un saldo CAP informado o validado. No reconstruye la cuenta sumando porcentajes sobre salarios anuales porque la cuenta real depende de movimientos, rendimientos y reglas que no se reproducen con suficiente fidelidad desde un resumen anual.

### 3.2. Bono de reconocimiento

El artículo 183 se modela como un monto adicional cuando corresponde.

La aplicación:

- acepta el monto ya determinado;
- registra si fue confirmado oficialmente;
- no reconstruye automáticamente el bono individual con datos insuficientes.

### 3.3. Pensión programada

Cuando se dispone del valor actuarial aplicable:

```text
pensión programada CAP
= (saldo CAP + bono aplicable) / valor actuarial de expectativa de vida
```

El valor actuarial no es un monto monetario y no se presenta con prefijo `B/.`.

## 4. Opciones del CAP

La entrada `opcion_prestacion_cap` admite:

- `AUTO`;
- `PENSION_PROGRAMADA`;
- `DEVOLUCION_TOTAL`.

Cuando la devolución está disponible y `AUTO` no permite concluir la intención del asegurado, el resultado queda pendiente hasta una decisión expresa.

## 5. Devolución total del CAP

El artículo 187 permite la devolución en los casos previstos cuando se alcanza la edad de referencia sin cumplir los requisitos de la pensión normal.

La devolución:

- se presenta como pago único;
- no se convierte en pensión mensual;
- se mantiene separada de cualquier indemnización del componente BD.

## 6. Indemnización BD + devolución CAP

Con menos de 180 cuotas puede existir una indemnización del componente BD y, de forma separada, una devolución del CAP.

La API conserva:

```text
pago único BD
+ pago único CAP
= total de pagos únicos
```

Nunca se presenta esa suma como una mensualidad.

## 7. Garantía del Seguro Colectivo de Renta Vitalicia

El artículo 184 y el reglamento de seguros colectivos se modelan como una garantía futura.

Se activa cuando:

- el pensionado sobrevive la expectativa de vida utilizada; y
- se extinguen los fondos ahorrados del CAP.

El seguro continúa el pago mensual correspondiente al CAP según las condiciones reglamentarias. No aumenta la pensión inicial.

La referencia histórica de prima 0.93 % se documenta para trazabilidad y no se vuelve a descontar de un saldo oficial ingresado.

## 8. Transición hacia SUCGS

La aplicación usa:

- hasta 29/02/2032: cálculo Mixto;
- desde 01/03/2032: cálculo bajo artículo 196 y concordantes del SUCGS.

Esta frontera se apoya en el artículo 188 y en el Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria.

El artículo 153 contiene una referencia distinta a 01/03/2036. La discrepancia se mantiene documentada en lugar de armonizarla silenciosamente.

## 9. Opción operativa de sistema en 2026

La Resolución 57,805-2025-J.D. contiene originalmente 17/03/2026. Comunicaciones oficiales posteriores de la CSS señalan **18/08/2026** como fecha límite operativa para quienes cumplen los requisitos de la opción.

Esta información es temporal y debe verificarse antes de usarse en una decisión individual.

## 10. Fuentes principales

- [Texto Único de la Ley 51 — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Reglamento de Incorporación al Subsistema Mixto](https://w3.css.gob.pa/wp-content/wdocs/REGLAMENTO%20DE%20INCORPORACION%20AL%20SUBSISTEMA%20MIXTO.pdf)
- [Reglamento de Seguros Colectivos del CAP](https://www.css.gob.pa/wp-content/uploads/2023/10/REGLAMENTO-DE-SEGUROS-COLECTIVOS-DEL-COMPONENTE-DE-AHORRO-PERSONAL-DEL-SUBSISTEMA-MIXTO-actualizado.pdf)
- [Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria](https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf)
- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)
