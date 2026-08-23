"""Catálogo legible de metodología y fuentes oficiales de la aplicación.

La vista de metodología reutiliza las URLs versionadas de ``regulations/*.json``. Este
módulo añade únicamente etiquetas, agrupación y alcance humano para la interfaz;
no incorpora reglas de cálculo ni sustituye los motores previsionales.
"""

from app.core.normativa import (
    cargar_parametros_generales,
    cargar_parametros_mixto,
    cargar_parametros_sebd,
    cargar_parametros_sucgs,
)


def _fuente(
    identificador: str,
    titulo: str,
    referencia: str,
    url: str,
    alcance: str,
    tipo: str = "Normativa",
) -> dict:
    """Construye una fuente lista para renderizar en la interfaz."""

    return {
        "id": identificador,
        "titulo": titulo,
        "referencia": referencia,
        "url": url,
        "alcance": alcance,
        "tipo": tipo,
    }


def construir_catalogo_metodologia() -> dict:
    """Devuelve la metodología transversal y el catálogo oficial versionado."""

    # El catálogo se construye desde parámetros versionados para que las URLs
    # oficiales se mantengan en normativa y no dentro de plantillas HTML.
    generales = cargar_parametros_generales()
    sebd = cargar_parametros_sebd()
    mixto = cargar_parametros_mixto()
    sucgs = cargar_parametros_sucgs()

    urls_sebd = sebd["fuentes_oficiales"]
    urls_mixto = mixto["fuentes_oficiales"]
    urls_sucgs = sucgs["fuentes_oficiales"]

    # Fuentes generales: base legal y portales oficiales comunes a más de un
    # sistema previsional.
    fuentes_generales = [
        _fuente(
            "texto_unico",
            "Texto Único de la Ley 51 de 2005",
            "Gaceta Oficial 30284-B de 22/05/2025",
            generales["fuente_texto_unico_url"],
            "Fuente legal consolidada principal del proyecto.",
        ),
        _fuente(
            "ley_462",
            "Ley 462 de 18 de marzo de 2025",
            "Reforma de la Ley Orgánica de la CSS",
            urls_sucgs["ley_462_2025"],
            "Reforma incorporada en el Texto Único y fuente histórica de los cambios de 2025.",
        ),
        _fuente(
            "gaceta_30284_b",
            "Gaceta Oficial 30284-B",
            "22 de mayo de 2025",
            generales["fuente_gaceta_url"],
            "Publicación oficial del Texto Único vigente utilizado por la aplicación.",
            "Gaceta Oficial",
        ),
        _fuente(
            "normativa_ley_organica",
            "Normativa de la Ley Orgánica — CSS",
            "Portal institucional",
            generales["fuente_url"],
            "Página oficial para consultar el Texto Único y las leyes incorporadas.",
            "Portal oficial",
        ),
        _fuente(
            "prestaciones_economicas",
            "Normativa de Prestaciones Económicas — CSS",
            "Reglamentos y resoluciones",
            generales["fuente_prestaciones_economicas_url"],
            "Portal oficial que agrupa reglamentos y resoluciones de prestaciones económicas.",
            "Portal oficial",
        ),
    ]

    # Los grupos separan sistemas para que la vista explique alcance, artículos
    # y fuentes sin mezclar motores ni sugerir equivalencias jurídicas.
    grupos = [
        {
            "id": "sebd",
            "titulo": "SEBD — Subsistema Exclusivamente de Beneficio Definido",
            "descripcion": "Reglas de vejez normal, anticipada, proporcional, indemnización y límites del componente definido.",
            "articulos": ["178", "179", "180", "181", "186", "192", "193"],
            "fuentes": [
                _fuente(
                    "reglamento_calculo",
                    "Reglamento para el Cálculo de Prestaciones Económicas",
                    "Resolución 39,302-2007-J.D. y modificaciones",
                    urls_sebd["resolucion_39302_2007_jd"],
                    "Desarrolla reglas operativas de cálculo, incluida la indemnización y factores reglamentarios.",
                ),
                _fuente(
                    "pension_vejez",
                    "Pensión por Vejez — CSS",
                    "Orientación institucional",
                    urls_sebd["pension_vejez_css"],
                    "Página oficial de orientación sobre la pensión por vejez.",
                    "Orientación",
                ),
                _fuente(
                    "pension_anticipada",
                    "Pensión por Vejez Anticipada — CSS",
                    "Orientación institucional",
                    urls_sebd["pension_vejez_anticipada_css"],
                    "Página oficial de orientación sobre retiro anticipado.",
                    "Orientación",
                ),
                _fuente(
                    "pension_proporcional",
                    "Pensión por Vejez Proporcional — CSS",
                    "Orientación institucional",
                    urls_sebd["pension_vejez_proporcional_css"],
                    "Página oficial de orientación sobre la modalidad proporcional.",
                    "Orientación",
                ),
                _fuente(
                    "pension_proporcional_anticipada",
                    "Pensión por Vejez Proporcional Anticipada — CSS",
                    "Orientación institucional",
                    urls_sebd["pension_vejez_proporcional_anticipada_css"],
                    "Página oficial de orientación sobre la modalidad proporcional anticipada.",
                    "Orientación",
                ),
            ],
        },
        {
            "id": "mixto",
            "titulo": "Subsistema Mixto",
            "descripcion": "Componente de Beneficio Definido, CAP, bono, renta vitalicia, devolución e incorporación al nuevo componente solidario.",
            "articulos": ["155", "178–188", "192", "193"],
            "fuentes": [
                _fuente(
                    "reglamento_mixto",
                    "Reglamento de Incorporación al Subsistema Mixto",
                    "Reglamento oficial CSS",
                    urls_mixto["reglamento_incorporacion_mixto"],
                    "Incorporación y reglas concordantes del Subsistema Mixto.",
                ),
                _fuente(
                    "res_39470",
                    "Resolución 39,470-2007-J.D.",
                    "Subsistema Mixto",
                    urls_mixto["resolucion_39470_2007_jd"],
                    "Resolución relacionada con la incorporación al Subsistema Mixto.",
                ),
                _fuente(
                    "res_41055",
                    "Resolución 41,055-2009-J.D.",
                    "Subsistema Mixto",
                    urls_mixto["resolucion_41055_2009_jd"],
                    "Resolución relacionada con el Subsistema Mixto y sus seguros colectivos.",
                ),
                _fuente(
                    "seguros_cap",
                    "Reglamento de Seguros Colectivos del CAP",
                    "Componente de Ahorro Personal del Subsistema Mixto",
                    urls_mixto["reglamento_seguros_colectivos_cap"],
                    "Regula, entre otros aspectos, el Seguro Colectivo de Renta Vitalicia.",
                ),
                _fuente(
                    "ley_58_2008",
                    "Ley 58 de 2008",
                    "Norma consultada para seguros colectivos",
                    urls_mixto["ley_58_2008"],
                    "Norma listada por la CSS entre las consultadas para el reglamento de seguros colectivos.",
                ),
                _fuente(
                    "reglamento_cccs_mixto",
                    "Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria",
                    "Resolución 57,805-2025-J.D.",
                    urls_mixto["reglamento_incorporacion_cccs"],
                    "Regula la incorporación y la frontera operativa de transición del Subsistema Mixto.",
                ),
            ],
        },
        {
            "id": "sucgs",
            "titulo": "SUCGS — Sistema Único de Capitalización con Garantía Solidaria",
            "descripcion": "Componente contributivo, capa solidaria, factores actuariales y garantía de reemplazo.",
            "articulos": ["Art. 1, num. 41", "152", "153", "194", "195", "196", "197", "198"],
            "fuentes": [
                _fuente(
                    "reglamento_cccs",
                    "Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria",
                    "Resolución 57,805-2025-J.D.",
                    urls_sucgs["reglamento_incorporacion_cccs"],
                    "Reglamento de incorporación y transición hacia el componente contributivo solidario.",
                ),
            ],
        },
    ]

    # Recursos complementarios: enlaces útiles para el usuario, pero no fuentes
    # que habiliten cálculos automáticos adicionales.
    recursos = [
        {
            "titulo": "Mi Caja Digital",
            "descripcion": "Consulta individual de información del Asegurado(a). No sustituye la normativa aplicada por los motores.",
            "url": "https://micajadigital.css.gob.pa/Auth/SignIn",
        },
        {
            "titulo": "Pensión para trabajadores estacionales agrícolas y de la construcción",
            "descripcion": "Régimen especial identificado y todavía fuera del motor general actual.",
            "url": "https://www.css.gob.pa/pension-por-vejez-para-los-trabajadores-estacionales-agricolas-y-de-la-construccion/",
        },
    ]

    # La salida usa listas simples y textos finales porque se consume como
    # contenido metodológico, no como parámetros de cálculo.
    return {
        "version": "1.0",
        "fuentes_generales": fuentes_generales,
        "grupos": grupos,
        "recursos": recursos,
        "principios": [
            "La aplicación prioriza el Texto Único vigente y después reglamentos y resoluciones oficiales.",
            "Las páginas informativas de la CSS apoyan la interpretación operativa, pero no reemplazan la Ley o el reglamento.",
            "Los importes indexables, saldos individuales y parámetros actuariales que no puedan reconstruirse con seguridad deben confirmarse o mostrarse como pendientes.",
            "SEBD, Mixto y SUCGS conservan motores separados; la trazabilidad y el comparador explican resultados sin recalcular las fórmulas jurídicas.",
            "La herramienta es independiente de la CSS y está dirigida a Asegurados(as); la determinación oficial corresponde a la Caja de Seguro Social de Panamá.",
        ],
        "limitaciones": [
            "El historial principal es anual; algunas reglas legales operan con granularidad mensual y se identifican como aproximaciones cuando corresponde.",
            "El Mixto conserva documentada la diferencia temporal 2032/2036 entre disposiciones consultadas; el motor usa la regla específica de transición versionada y muestra advertencias.",
            "La estabilidad salarial del artículo 197 del SUCGS requiere confirmación explícita mientras no exista una regla operativa pública inequívoca para reproducirla automáticamente.",
            "Los regímenes especiales no deben interpretarse mediante el motor general hasta que dispongan de implementación y validación propias.",
        ],
    }
