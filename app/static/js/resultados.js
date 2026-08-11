"use strict";


/* ============================================================
   Calculadora de Pensión CSS
   Paso 6 — Resultados
   ============================================================ */

/*
 * Este módulo conecta los datos validados en los Pasos 1–5 con
 * los motores legales. La integración SEBD clasifica automáticamente
 * la modalidad normal, anticipada, proporcional, proporcional anticipada
 * o la Indemnización por Vejez de pago único.
 */


// ============================================================
// Preparación del paso
// ============================================================

/**
 * Devuelve una etiqueta legible para el sistema previsional.
 *
 * @param {string} sistema Código almacenado en el Paso 1.
 * @returns {string} Nombre visible.
 */
function obtenerNombreSistemaResultados(sistema) {
  const nombres = {
    SEBD: "SEBD — Beneficio Definido",
    MIXTO: "Subsistema Mixto",
    SUCGS: "SUCGS",
    NO_SE: "Sistema no identificado",
  };

  return nombres[sistema] || sistema || "—";
}


/**
 * Prepara el contexto visible y las opciones salariales del Paso 6.
 */
function prepararPasoResultados() {
  const simulacion = obtenerSimulacion();
  const persona = simulacion.persona || {};
  const seleccionado = simulacion.escenario_retiro_seleccionado;

  ocultarErrorResultados();

  document.getElementById(
    "resultado-sistema",
  ).textContent = obtenerNombreSistemaResultados(
    persona.sistema,
  );

  if (!seleccionado) {
    mostrarErrorResultados(
      "Primero debes seleccionar un escenario de retiro en el Paso 5.",
    );
    return false;
  }

  document.getElementById(
    "resultado-escenario-retiro",
  ).textContent = seleccionado.nombre;

  document.getElementById(
    "resultado-fecha-edad",
  ).textContent = (
    `${formatearFechaRetiro(seleccionado.fecha_retiro)} · `
    + `${seleccionado.edad_retiro_anios} años`
  );

  document.getElementById(
    "resultado-pension-cuotas",
  ).textContent = (
    `${seleccionado.cuotas_estimadas_totales}`
  );

  const contenedorSEBD = document.getElementById(
    "resultado-config-sebd",
  );

  const pendiente = document.getElementById(
    "resultado-motor-pendiente",
  );

  pendiente.classList.add("d-none");

  if (persona.sistema !== "SEBD") {
    contenedorSEBD.classList.add("d-none");
    document.getElementById(
      "resultado-sebd",
    ).classList.add("d-none");

    pendiente.classList.remove("d-none");

    if (persona.sistema === "MIXTO") {
      pendiente.textContent = (
        "El motor del Subsistema Mixto todavía no está habilitado "
        + "en esta subfase. Los datos de los Pasos 1–5 se conservarán "
        + "para integrarlo posteriormente."
      );

    } else if (persona.sistema === "SUCGS") {
      pendiente.textContent = (
        "El motor SUCGS todavía no está habilitado en esta subfase. "
        + "Los escenarios construidos se conservarán para su integración."
      );

    } else {
      pendiente.textContent = (
        "Para calcular una pensión debes identificar primero el "
        + "sistema previsional aplicable en el Paso 1."
      );
    }

    return true;
  }

  contenedorSEBD.classList.remove("d-none");

  return prepararEscenariosSalarialesResultados(
    simulacion,
  );
}


/**
 * Llena el selector de escenarios salariales disponibles.
 *
 * @param {Object} simulacion Estado actual del asistente.
 * @returns {boolean} true cuando existe al menos un escenario.
 */
function prepararEscenariosSalarialesResultados(simulacion) {
  const select = document.getElementById(
    "resultado-escenario-salarial",
  );

  select.replaceChildren();

  const linea = simulacion.resumen_linea_tiempo;

  if (
    !linea
    || !Array.isArray(linea.escenarios)
    || linea.escenarios.length === 0
  ) {
    mostrarErrorResultados(
      "No existe una línea temporal salarial completa. "
      + "Vuelve al Paso 4 y genera la proyección con historial.",
    );

    return false;
  }

  linea.escenarios.forEach(
    (escenario) => {
      const opcion = document.createElement("option");
      opcion.value = escenario.nombre;
      opcion.textContent = escenario.nombre;
      select.appendChild(opcion);
    },
  );

  const guardado = simulacion.escenario_salarial_seleccionado;

  const existeGuardado = linea.escenarios.some(
    (escenario) => escenario.nombre === guardado,
  );

  select.value = existeGuardado
    ? guardado
    : linea.escenarios[0].nombre;

  return true;
}


// ============================================================
// Solicitud al backend
// ============================================================

/**
 * Construye la entrada integrada para el motor general SEBD.
 *
 * @returns {Object} Solicitud lista para FastAPI.
 */
function construirSolicitudResultadoSEBD() {
  const simulacion = obtenerSimulacion();
  const persona = simulacion.persona || {};
  const seleccionado = simulacion.escenario_retiro_seleccionado;

  if (persona.sistema !== "SEBD") {
    throw new Error(
      "El cálculo SEBD solo puede ejecutarse cuando el sistema "
      + "seleccionado en el Paso 1 es SEBD.",
    );
  }

  if (!simulacion.historial || !simulacion.resumen_historial) {
    throw new Error(
      "El cálculo SEBD requiere un historial salarial anual "
      + "analizado en el Paso 3.",
    );
  }

  if (!simulacion.resumen_linea_tiempo) {
    throw new Error(
      "Falta la línea temporal salarial del Paso 4.",
    );
  }

  if (!simulacion.resumen_retiro || !seleccionado) {
    throw new Error(
      "Falta analizar y seleccionar un escenario de retiro en el Paso 5.",
    );
  }

  const escenarioSalarial = document.getElementById(
    "resultado-escenario-salarial",
  ).value;

  if (!escenarioSalarial) {
    throw new Error(
      "Selecciona un escenario salarial para realizar el cálculo.",
    );
  }

  return {
    fecha_nacimiento: persona.fecha_nacimiento,
    sexo: persona.sexo,
    historial: simulacion.historial,
    linea_tiempo: simulacion.resumen_linea_tiempo,
    resumen_retiro: simulacion.resumen_retiro,
    fecha_retiro_seleccionada: seleccionado.fecha_retiro,
    escenario_salarial_nombre: escenarioSalarial,
  };
}


/**
 * Solicita la clasificación y cálculo integrado de la prestación SEBD.
 */
async function calcularResultadoSEBD() {
  ocultarErrorResultados();

  let datos;

  try {
    datos = construirSolicitudResultadoSEBD();
  } catch (error) {
    mostrarErrorResultados(
      error.message,
    );
    return;
  }

  const boton = document.getElementById(
    "btn-calcular-resultado-sebd",
  );

  boton.disabled = true;
  boton.textContent = "Calculando…";

  try {
    const respuesta = await fetch(
      "/api/simulacion/resultados/sebd",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datos),
      },
    );

    let contenido = null;

    try {
      contenido = await respuesta.json();
    } catch {
      contenido = null;
    }

    if (!respuesta.ok) {
      mostrarErrorResultados(
        obtenerMensajeError(
          contenido,
          "No fue posible calcular la prestación SEBD.",
        ),
      );
      return;
    }

    const simulacion = obtenerSimulacion();

    simulacion.escenario_salarial_seleccionado = (
      datos.escenario_salarial_nombre
    );
    simulacion.resultado_sebd_normal = contenido;

    guardarSimulacion(
      simulacion,
    );

    mostrarResultadoSEBD(
      contenido,
    );

  } catch {
    mostrarErrorResultados(
      "No fue posible comunicarse con el servidor.",
    );

  } finally {
    boton.disabled = false;
    boton.textContent = "Recalcular prestación SEBD";
  }
}


// ============================================================
// Presentación del resultado
// ============================================================

/**
 * Presenta la modalidad SEBD detectada y su trazabilidad.
 *
 * @param {Object} resultado Respuesta integrada del backend.
 */
function mostrarResultadoSEBD(resultado) {
  const calculo = resultado.calculo;
  const esIndemnizacion = (
    calculo.modalidad === "INDEMNIZACION"
    && calculo.calculo_disponible
  );

  configurarVistaPrestacionSEBD(
    calculo,
    esIndemnizacion,
  );

  document.getElementById(
    "resultado-sebd-modalidad",
  ).textContent = calculo.modalidad_nombre || calculo.modalidad || "—";

  document.getElementById(
    "resultado-sebd-modalidad-nota",
  ).textContent = obtenerNotaModalidadSEBD(calculo);

  mostrarElegibilidadSEBD(
    calculo,
  );

  document.getElementById(
    "resultado-sebd-pension",
  ).textContent = esIndemnizacion
    ? formatearMoneda(calculo.indemnizacion_pago_unico_estimado)
    : (
      calculo.pension_mensual_estimada == null
        ? "—"
        : formatearMoneda(calculo.pension_mensual_estimada)
    );

  document.getElementById(
    "resultado-sebd-salario-base",
  ).textContent = formatearMoneda(
    calculo.salario_base_mensual,
  );

  document.getElementById(
    "resultado-sebd-base-nota",
  ).textContent = (
    `${calculo.mejores_anios_requeridos} mejores años seleccionados`
  );

  document.getElementById(
    "resultado-sebd-tasa-total",
  ).textContent = formatearPorcentaje(
    calculo.tasa_reemplazo_total_pct,
  );

  document.getElementById(
    "resultado-sebd-cuotas",
  ).textContent = calculo.cuotas_totales;

  document.getElementById(
    "resultado-sebd-cuotas-nota",
  ).textContent = esIndemnizacion
    ? (
      `${calculo.cuotas_totales} meses acreditados · divisor `
      + `${calculo.indemnizacion_divisor_cuotas}`
    )
    : (
      `${calculo.cuotas_exceso_total} sobre las `
      + `${calculo.cuotas_referencia} de referencia`
    );

  document.getElementById(
    "resultado-sebd-anios-requeridos",
  ).textContent = calculo.mejores_anios_requeridos;

  document.getElementById(
    "resultado-sebd-total-salarios",
  ).textContent = formatearMoneda(
    calculo.total_salarios_seleccionados,
  );

  document.getElementById(
    "resultado-sebd-promedio",
  ).textContent = formatearMoneda(
    calculo.salario_base_mensual,
  );

  mostrarAniosSeleccionadosSEBD(
    calculo.anios_seleccionados,
    resultado.anios_proyectados_incluidos || [],
  );

  document.getElementById(
    "resultado-sebd-cuotas-referencia",
  ).textContent = (
    `${calculo.cuotas_referencia} cuotas`
  );

  document.getElementById(
    "resultado-sebd-tasa-base",
  ).textContent = (
    formatearPorcentaje(
      calculo.tasa_base_pct,
    )
  );

  document.getElementById(
    "resultado-sebd-exceso-antes",
  ).textContent = (
    `${calculo.cuotas_exceso_antes_referencia} cuotas · `
    + `${calculo.bloques_12_antes_referencia} bloques`
  );

  document.getElementById(
    "resultado-sebd-incremento-antes",
  ).textContent = (
    `+${formatearPorcentaje(
      calculo.incremento_antes_referencia_pct,
    )}`
  );

  document.getElementById(
    "resultado-sebd-exceso-despues",
  ).textContent = (
    `${calculo.cuotas_exceso_despues_referencia} cuotas · `
    + `${calculo.bloques_12_despues_referencia} bloques`
  );

  document.getElementById(
    "resultado-sebd-incremento-despues",
  ).textContent = (
    `+${formatearPorcentaje(
      calculo.incremento_despues_referencia_pct,
    )}`
  );

  document.getElementById(
    "resultado-sebd-tasa-final-tabla",
  ).textContent = formatearPorcentaje(
    calculo.tasa_reemplazo_total_pct,
  );

  document.getElementById(
    "resultado-sebd-factor-cuotas",
  ).textContent = formatearFactorSEBD(
    calculo.factor_proporcional_cuotas,
  );

  document.getElementById(
    "resultado-sebd-factor-edad",
  ).textContent = formatearFactorSEBD(
    calculo.factor_reduccion_edad,
  );

  document.getElementById(
    "resultado-sebd-meses-anticipacion",
  ).textContent = calculo.meses_anticipacion_referencia > 0
    ? `${calculo.meses_anticipacion_referencia} meses`
    : "No aplica";

  document.getElementById(
    "resultado-sebd-monto-previo",
  ).textContent = formatearMoneda(
    calculo.monto_antes_limite_maximo,
  );

  document.getElementById(
    "resultado-sebd-maximo",
  ).textContent = formatearMoneda(
    calculo.monto_maximo_aplicable,
  );

  document.getElementById(
    "resultado-sebd-monto-final",
  ).textContent = calculo.pension_mensual_estimada == null
    ? "—"
    : formatearMoneda(calculo.pension_mensual_estimada);

  if (esIndemnizacion) {
    mostrarDetalleIndemnizacionSEBD(
      calculo,
    );
  }

  mostrarAdvertenciasResultadoSEBD(
    resultado,
  );

  document.getElementById(
    "resultado-sebd-fuente",
  ).textContent = calculo.fuente_normativa;

  const contenedor = document.getElementById(
    "resultado-sebd",
  );

  contenedor.classList.remove("d-none");

  contenedor.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}



/**
 * Ajusta etiquetas y secciones según se trate de una pensión o indemnización.
 *
 * @param {Object} calculo Resultado del motor.
 * @param {boolean} esIndemnizacion Indica si es una prestación de pago único.
 */
function configurarVistaPrestacionSEBD(
  calculo,
  esIndemnizacion,
) {
  const etiquetaPrestacion = document.getElementById(
    "resultado-sebd-prestacion-label",
  );
  const notaPrestacion = document.getElementById(
    "resultado-sebd-prestacion-nota",
  );
  const etiquetaTasa = document.getElementById(
    "resultado-sebd-tasa-label",
  );
  const notaTasa = document.getElementById(
    "resultado-sebd-tasa-nota",
  );
  const factores = document.getElementById(
    "resultado-sebd-factores",
  );
  const limites = document.getElementById(
    "resultado-sebd-limites",
  );
  const indemnizacion = document.getElementById(
    "resultado-sebd-indemnizacion",
  );

  if (esIndemnizacion) {
    etiquetaPrestacion.textContent = "Pago único estimado";
    notaPrestacion.textContent = (
      "Indemnización por Vejez; no es una pensión mensual vitalicia."
    );
    etiquetaTasa.textContent = "Tasa hipotética";
    notaTasa.textContent = (
      "Tasa utilizada para obtener la mensualidad de pensión normal hipotética."
    );
    factores.classList.add("d-none");
    limites.classList.add("d-none");
    indemnizacion.classList.remove("d-none");
    return;
  }

  etiquetaPrestacion.textContent = "Pensión mensual estimada";
  notaPrestacion.textContent = (
    "Antes de asignaciones familiares u otros conceptos."
  );
  etiquetaTasa.textContent = "Tasa de reemplazo";
  notaTasa.textContent = (
    "Base legal + incrementos completos aplicables."
  );
  factores.classList.remove("d-none");
  limites.classList.remove("d-none");
  indemnizacion.classList.add("d-none");
}


/**
 * Muestra la fórmula específica de la Indemnización por Vejez.
 *
 * @param {Object} calculo Resultado del motor.
 */
function mostrarDetalleIndemnizacionSEBD(calculo) {
  const mensualidad = Number(
    calculo.indemnizacion_mensualidad_hipotetica,
  );
  const factor = Number(
    calculo.indemnizacion_factor_cuotas,
  );
  const divisor = Number(
    calculo.indemnizacion_divisor_cuotas,
  );
  const pago = Number(
    calculo.indemnizacion_pago_unico_estimado,
  );

  document.getElementById(
    "resultado-sebd-indem-mensualidad",
  ).textContent = formatearMoneda(mensualidad);

  document.getElementById(
    "resultado-sebd-indem-factor",
  ).textContent = Number.isFinite(factor)
    ? factor.toFixed(4)
    : "—";

  document.getElementById(
    "resultado-sebd-indem-pago",
  ).textContent = formatearMoneda(pago);

  document.getElementById(
    "resultado-sebd-indem-formula",
  ).textContent = (
    `${formatearMoneda(mensualidad)} × `
    + `(${calculo.cuotas_totales} ÷ ${divisor}) = `
    + `${formatearMoneda(pago)}`
  );
}


/**
 * Muestra si la modalidad normal SEBD es elegible en el escenario.
 *
 * @param {Object} calculo Resultado jurídico del motor.
 */
function mostrarElegibilidadSEBD(calculo) {
  const alerta = document.getElementById(
    "resultado-sebd-elegibilidad",
  );

  alerta.replaceChildren();

  const titulo = document.createElement("strong");

  if (
    calculo.modalidad === "INDEMNIZACION"
    && calculo.elegible
    && calculo.calculo_disponible
  ) {
    alerta.className = "alert alert-info";
    titulo.textContent = (
      "Modalidad aplicable: Indemnización por Vejez de pago único."
    );
    alerta.appendChild(titulo);
    return;
  }

  if (calculo.elegible && calculo.calculo_disponible) {
    alerta.className = "alert alert-success";
    titulo.textContent = (
      `Modalidad aplicable: ${calculo.modalidad_nombre}.`
    );
    alerta.appendChild(titulo);
    return;
  }

  if (calculo.modalidad === "INDEMNIZACION") {
    alerta.className = "alert alert-info";
    titulo.textContent = (
      "El escenario corresponde a una posible Indemnización por Vejez."
    );
    alerta.appendChild(titulo);
    return;
  }

  alerta.className = "alert alert-warning";
  titulo.textContent = (
    "Este escenario no cumple todavía una modalidad de pensión SEBD calculable."
  );
  alerta.appendChild(titulo);

  if (
    Array.isArray(calculo.motivos_no_elegible)
    && calculo.motivos_no_elegible.length > 0
  ) {
    const lista = document.createElement("ul");
    lista.className = "mb-0 mt-2";

    calculo.motivos_no_elegible.forEach(
      (motivo) => {
        const item = document.createElement("li");
        item.textContent = motivo;
        lista.appendChild(item);
      },
    );

    alerta.appendChild(lista);
  }
}


/**
 * Explica brevemente cómo se construye la modalidad detectada.
 *
 * @param {Object} calculo Resultado del motor jurídico.
 * @returns {string} Nota visible.
 */
function obtenerNotaModalidadSEBD(calculo) {
  const notas = {
    NORMAL: "Edad de referencia o superior y 240 cuotas o más.",
    ANTICIPADA: "Hasta dos años antes de la edad de referencia, con 240 cuotas o más y factor de reducción por edad.",
    PROPORCIONAL: "Edad de referencia o superior, con entre 180 y 239 cuotas.",
    PROPORCIONAL_ANTICIPADA: "Dentro de la banda anticipada, con entre 180 y 239 cuotas; combina factor por cuotas y factor por edad.",
    INDEMNIZACION: "Con menos de 180 cuotas y la edad de referencia cumplida, corresponde una prestación de pago único antes de la transición legal de 2036.",
    NO_ELEGIBLE: "La edad y/o las cuotas del escenario todavía no permiten una prestación SEBD calculable.",
  };

  return notas[calculo.modalidad] || (
    "La modalidad se determina automáticamente según edad, fecha y cuotas."
  );
}


/**
 * Formatea un factor decimal con cuatro posiciones.
 *
 * @param {number} valor Factor recibido del backend.
 * @returns {string} Valor visible.
 */
function formatearFactorSEBD(valor) {
  const numero = Number(valor);

  if (!Number.isFinite(numero)) {
    return "—";
  }

  return numero.toFixed(4);
}


/**
 * Muestra los años que formaron el salario base.
 *
 * @param {Array<Object>} registros Años seleccionados por el motor.
 * @param {number[]} aniosProyectados Años de origen proyectado.
 */
function mostrarAniosSeleccionadosSEBD(
  registros,
  aniosProyectados,
) {
  const cuerpo = document.getElementById(
    "resultado-sebd-anios-body",
  );

  cuerpo.replaceChildren();

  const proyectados = new Set(
    aniosProyectados.map(Number),
  );

  registros.forEach(
    (registro) => {
      const fila = document.createElement("tr");

      agregarCeldaResultado(
        fila,
        registro.anio,
      );

      agregarCeldaResultado(
        fila,
        registro.cuotas,
      );

      agregarCeldaResultado(
        fila,
        formatearMoneda(
          registro.salario_cotizado,
        ),
      );

      const origen = document.createElement("td");
      const badge = document.createElement("span");

      if (proyectados.has(Number(registro.anio))) {
        badge.className = "results-origin results-origin-projected";
        badge.textContent = "Proyectado";

      } else {
        badge.className = "results-origin results-origin-historic";
        badge.textContent = "Histórico";
      }

      origen.appendChild(badge);
      fila.appendChild(origen);

      cuerpo.appendChild(fila);
    },
  );
}


/**
 * Agrega una celda de texto a una fila del Paso 6.
 *
 * @param {HTMLTableRowElement} fila Fila de destino.
 * @param {string|number} valor Valor visible.
 */
function agregarCeldaResultado(
  fila,
  valor,
) {
  const celda = document.createElement("td");
  celda.textContent = valor;
  fila.appendChild(celda);
}


/**
 * Consolida advertencias de integración y del motor legal.
 *
 * @param {Object} resultado Respuesta completa integrada.
 */
function mostrarAdvertenciasResultadoSEBD(resultado) {
  const mensajes = [
    ...(resultado.advertencias_integracion || []),
    ...(resultado.calculo.advertencias || []),
  ];

  const alerta = document.getElementById(
    "resultado-sebd-advertencias",
  );

  alerta.replaceChildren();

  if (mensajes.length === 0) {
    alerta.classList.add("d-none");
    return;
  }

  const titulo = document.createElement("strong");
  titulo.textContent = "Advertencias del cálculo";
  alerta.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "mb-0 mt-2";

  mensajes.forEach(
    (mensaje) => {
      const item = document.createElement("li");
      item.textContent = mensaje;
      lista.appendChild(item);
    },
  );

  alerta.appendChild(lista);
  alerta.classList.remove("d-none");
}


// ============================================================
// Estado e invalidación
// ============================================================

/**
 * Invalida el cálculo al cambiar el escenario salarial.
 */
function invalidarResultadoSEBD() {
  const simulacion = obtenerSimulacion();

  simulacion.escenario_salarial_seleccionado = (
    document.getElementById(
      "resultado-escenario-salarial",
    ).value || null
  );
  simulacion.resultado_sebd_normal = null;

  guardarSimulacion(simulacion);

  document.getElementById(
    "resultado-sebd",
  ).classList.add("d-none");
}


/**
 * Restaura un resultado compatible guardado en sessionStorage.
 */
function restaurarResultadoSEBDGuardado() {
  const simulacion = obtenerSimulacion();

  if (
    simulacion.resultado_sebd_normal
    && simulacion.persona?.sistema === "SEBD"
  ) {
    mostrarResultadoSEBD(
      simulacion.resultado_sebd_normal,
    );
  }
}


// ============================================================
// Errores
// ============================================================

/**
 * Muestra un error del Paso 6.
 *
 * @param {string} mensaje Texto visible.
 */
function mostrarErrorResultados(mensaje) {
  const alerta = document.getElementById(
    "error-resultados",
  );

  alerta.textContent = mensaje;
  alerta.classList.remove("d-none");
}


/**
 * Oculta errores previos del Paso 6.
 */
function ocultarErrorResultados() {
  document.getElementById(
    "error-resultados",
  ).classList.add("d-none");
}


// ============================================================
// Inicialización
// ============================================================

document.addEventListener(
  "DOMContentLoaded",
  () => {
    document.getElementById(
      "btn-continuar-paso-6",
    ).addEventListener(
      "click",
      () => {
        const simulacion = obtenerSimulacion();

        if (!simulacion.resumen_retiro) {
          mostrarErrorRetiro(
            "Primero debes analizar los escenarios de retiro.",
          );
          return;
        }

        if (!simulacion.escenario_retiro_seleccionado) {
          mostrarErrorRetiro(
            "Selecciona un escenario de retiro para continuar.",
          );
          return;
        }

        if (
          simulacion.resumen_retiro
            .proyeccion_salarial_cubre_escenarios
          === false
        ) {
          mostrarErrorRetiro(
            "Amplía primero el horizonte salarial del Paso 4.",
          );
          return;
        }

        mostrarPaso(6);
        prepararPasoResultados();
        restaurarResultadoSEBDGuardado();
      },
    );

    document.getElementById(
      "btn-volver-paso-5",
    ).addEventListener(
      "click",
      () => {
        mostrarPaso(5);
      },
    );

    document.getElementById(
      "btn-calcular-resultado-sebd",
    ).addEventListener(
      "click",
      calcularResultadoSEBD,
    );

    document.getElementById(
      "resultado-escenario-salarial",
    ).addEventListener(
      "change",
      invalidarResultadoSEBD,
    );

    const simulacion = obtenerSimulacion();

    if (Number(simulacion.paso_actual) === 6) {
      prepararPasoResultados();
      restaurarResultadoSEBDGuardado();
    }
  },
);
