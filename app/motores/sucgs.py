"""Motor del Sistema Único de Capitalización con Garantía Solidaria.

Este módulo contendrá las reglas de cálculo correspondientes al
Sistema Único de Capitalización con Garantía Solidaria (SUCGS).

Entre sus responsabilidades futuras estarán:

- acumular aportes destinados a capitalización;
- aplicar rendimientos según los parámetros correspondientes;
- procesar el capital acumulado;
- utilizar factores actuariales versionados;
- evaluar condiciones para garantías solidarias;
- aplicar mínimos o garantías cuando legalmente correspondan;
- distinguir capital propio de componentes solidarios;
- generar un desglose explicable de la prestación estimada.

Ningún factor actuarial, porcentaje de aporte o garantía deberá
quedar disperso directamente dentro del código. Estos parámetros
serán obtenidos de los archivos versionados en ``normativa/``.
"""