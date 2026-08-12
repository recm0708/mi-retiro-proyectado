"""Pruebas del comparador transversal 6F.1."""

import unittest
from datetime import date

from app.modelos.comparacion import DatosComparacionEscenarios
from app.modelos.pension import (
    DatosResultadoMixto,
    DatosResultadoSEBD,
    DatosResultadoSUCGS,
)
from app.modelos.simulacion import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.servicios.comparador import comparar_escenarios


class TestComparadorEscenarios(unittest.TestCase):
    """Valida diferencias y normalización entre los tres motores."""

    def _historial_sebd(self) -> DatosHistorialSalarial:
        salarios = [
            8920.45,
            10013.23,
            10431.36,
            10910.82,
            11064.62,
            17474.59,
            17538.10,
            17719.86,
            17760.01,
            17760.67,
        ]
        registros = [
            RegistroHistorialSalarial(
                anio=2016 + indice,
                cuotas=12,
                salario_cotizado=salario,
            )
            for indice, salario in enumerate(salarios)
        ]
        registros.append(
            RegistroHistorialSalarial(
                anio=2026,
                cuotas=5,
                salario_cotizado=6659.50,
            )
        )

        return DatosHistorialSalarial(
            anio_inicio=2016,
            anio_fin=2026,
            cuotas_totales_referencia=281,
            registros=registros,
        )

    def _linea_sebd(self) -> ResumenLineaTiempo:
        return ResumenLineaTiempo(
            anio_inicio_historico=2016,
            anio_actual=2026,
            anio_fin_proyeccion=2027,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Crecimiento anual de 1 %",
                    tasa_anual_pct=1.0,
                    registros=[
                        RegistroLineaTiempo(
                            anio=2026,
                            cuotas_historicas=5,
                            salario_historico=6659.50,
                            cuotas_proyectadas=0,
                            salario_proyectado=0,
                            cuotas_cierre=5,
                            salario_cierre=6659.50,
                            estado="HISTORICO_PARCIAL",
                        ),
                        RegistroLineaTiempo(
                            anio=2027,
                            cuotas_historicas=0,
                            salario_historico=0,
                            cuotas_proyectadas=12,
                            salario_proyectado=16142.63,
                            cuotas_cierre=12,
                            salario_cierre=16142.63,
                            estado="PROYECTADO",
                        ),
                    ],
                )
            ],
        )

    def _retiro_sebd(self) -> ResumenRetiro:
        referencia = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=3,
            cuotas_estimadas_adicionales=0,
            cuotas_estimadas_totales=281,
            fecha_ya_transcurrida=False,
        )
        adicional = EscenarioRetiro(
            tipo="ADICIONAL",
            nombre="Edad de referencia + 1 año",
            fecha_retiro=date(2027, 11, 16),
            edad_retiro_anios=58,
            meses_desde_corte_cuotas=15,
            cuotas_estimadas_adicionales=10,
            cuotas_estimadas_totales=291,
            fecha_ya_transcurrida=False,
        )

        return ResumenRetiro(
            fecha_corte=date(2026, 8, 10),
            fecha_corte_cuotas=date(2026, 8, 10),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=98,
            escenarios=[referencia, adicional],
            anio_fin_proyeccion_salarial=2027,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba.",
        )

    def test_sebd_calcula_diferencia_contra_escenario_base(self):
        datos = DatosResultadoSEBD(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=self._historial_sebd(),
            linea_tiempo=self._linea_sebd(),
            resumen_retiro=self._retiro_sebd(),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Crecimiento anual de 1 %",
        )

        resultado = comparar_escenarios(
            DatosComparacionEscenarios(
                sistema="SEBD",
                datos_sebd=datos,
            )
        )

        self.assertEqual(resultado.total_combinaciones, 2)
        self.assertEqual(resultado.resultados_completos, 2)

        base = next(fila for fila in resultado.filas if fila.es_base)
        adicional = next(
            fila
            for fila in resultado.filas
            if fila.fecha_retiro == date(2027, 11, 16)
        )

        self.assertEqual(base.pension_mensual_estimada, 741.59)
        self.assertEqual(base.diferencia_mensual_absoluta, 0.0)
        self.assertEqual(adicional.pension_mensual_estimada, 765.67)
        self.assertEqual(adicional.diferencia_mensual_absoluta, 24.08)
        self.assertEqual(
            resultado.clave_mejor_pension_mensual,
            adicional.clave,
        )

    def test_mixto_normaliza_total_mensual_y_advierte_saldo_constante(self):
        historial = DatosHistorialSalarial(
            anio_inicio=2002,
            anio_fin=2026,
            cuotas_totales_referencia=300,
            registros=[
                RegistroHistorialSalarial(
                    anio=anio,
                    cuotas=12,
                    salario_cotizado=12000,
                )
                for anio in range(2002, 2027)
            ],
        )
        retiro = ResumenRetiro(
            fecha_corte=date(2026, 8, 10),
            fecha_corte_cuotas=date(2026, 8, 10),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=98,
            escenarios=[
                EscenarioRetiro(
                    tipo="REFERENCIA",
                    nombre="Edad de referencia",
                    fecha_retiro=date(2026, 11, 16),
                    edad_retiro_anios=57,
                    meses_desde_corte_cuotas=3,
                    cuotas_estimadas_adicionales=0,
                    cuotas_estimadas_totales=300,
                    fecha_ya_transcurrida=False,
                )
            ],
            anio_fin_proyeccion_salarial=2026,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba.",
        )
        linea = ResumenLineaTiempo(
            anio_inicio_historico=2002,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Escenario base",
                    tasa_anual_pct=0,
                    registros=[],
                )
            ],
        )
        datos = DatosResultadoMixto(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=historial,
            linea_tiempo=linea,
            resumen_retiro=retiro,
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Escenario base",
            saldo_ahorro_personal=100000,
            bono_reconocimiento=5000,
            bono_reconocimiento_confirmado_oficialmente=True,
            valor_actuarial_expectativa_vida=200,
            opcion_prestacion_cap="PENSION_PROGRAMADA",
        )

        resultado = comparar_escenarios(
            DatosComparacionEscenarios(
                sistema="MIXTO",
                datos_mixto=datos,
            )
        )

        self.assertEqual(resultado.filas[0].pension_mensual_estimada, 856.25)
        self.assertIsNone(resultado.filas[0].pago_unico_estimado)
        self.assertTrue(any("saldo CAP" in aviso for aviso in resultado.advertencias))

    def test_sucgs_normaliza_resultado_total_477(self):
        registros = [
            RegistroHistorialSalarial(
                anio=2001,
                cuotas=2,
                salario_cotizado=2000,
            )
        ]
        registros.extend(
            RegistroHistorialSalarial(
                anio=anio,
                cuotas=12,
                salario_cotizado=12000,
            )
            for anio in range(2002, 2026)
        )
        registros.append(
            RegistroHistorialSalarial(
                anio=2026,
                cuotas=7,
                salario_cotizado=7000,
            )
        )
        historial = DatosHistorialSalarial(
            anio_inicio=2001,
            anio_fin=2026,
            cuotas_totales_referencia=297,
            registros=registros,
        )
        linea = ResumenLineaTiempo(
            anio_inicio_historico=2001,
            anio_actual=2026,
            anio_fin_proyeccion=2031,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Salario constante",
                    tasa_anual_pct=0,
                    registros=[
                        RegistroLineaTiempo(
                            anio=2026,
                            cuotas_historicas=7,
                            salario_historico=7000,
                            cuotas_proyectadas=5,
                            salario_proyectado=5000,
                            cuotas_cierre=12,
                            salario_cierre=12000,
                            estado="MIXTO",
                        )
                    ],
                )
            ],
        )
        retiro = ResumenRetiro(
            fecha_corte=date(2026, 8, 11),
            fecha_corte_cuotas=date(2026, 8, 11),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=97,
            escenarios=[
                EscenarioRetiro(
                    tipo="REFERENCIA",
                    nombre="Edad de referencia",
                    fecha_retiro=date(2026, 11, 16),
                    edad_retiro_anios=57,
                    meses_desde_corte_cuotas=3,
                    cuotas_estimadas_adicionales=3,
                    cuotas_estimadas_totales=300,
                    fecha_ya_transcurrida=False,
                )
            ],
            anio_fin_proyeccion_salarial=2031,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba.",
        )
        datos = DatosResultadoSUCGS(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=historial,
            linea_tiempo=linea,
            resumen_retiro=retiro,
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Salario constante",
            saldo_capitalizacion_solidaria=100000,
            saldo_confirmado_oficialmente=True,
            valor_minimo_universal_vigente=144,
            pension_garantizada_solidaria_vigente=265,
            valores_solidarios_confirmados_oficialmente=True,
            historial_laboral_completo_confirmado=True,
            estabilidad_salarial_art197_confirmada=True,
        )

        resultado = comparar_escenarios(
            DatosComparacionEscenarios(
                sistema="SUCGS",
                datos_sucgs=datos,
            )
        )

        self.assertEqual(resultado.filas[0].pension_mensual_estimada, 477.0)
        self.assertTrue(resultado.filas[0].calculo_completo)
        self.assertIsNone(resultado.filas[0].pago_unico_estimado)


if __name__ == "__main__":
    unittest.main()
