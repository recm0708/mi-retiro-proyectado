"use strict";


/* ============================================================
   Mi Retiro Proyectado
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
    SUCGS: "SUCGS — Sistema Único de Capitalización con Garantía Solidaria",
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
  ocultarTrazabilidadResultado();

  const resumenUnificado = document.getElementById(
    "resultado-resumen-unificado",
  );
  if (resumenUnificado) {
    resumenUnificado.classList.add("d-none");
  }

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
  const contenedorMixto = document.getElementById(
    "resultado-config-mixto",
  );
  const contenedorSUCGS = document.getElementById(
    "resultado-config-sucgs",
  );
  const pendiente = document.getElementById(
    "resultado-motor-pendiente",
  );

  pendiente.classList.add("d-none");
  contenedorSEBD.classList.add("d-none");
  contenedorMixto.classList.add("d-none");
  contenedorSUCGS.classList.add("d-none");

  if (persona.sistema === "SEBD") {
    document.getElementById(
      "resultado-mixto",
    ).classList.add("d-none");
    document.getElementById(
      "resultado-sucgs",
    ).classList.add("d-none");
    contenedorSEBD.classList.remove("d-none");

    return prepararEscenariosSalarialesResultados(
      simulacion,
    );
  }

  if (persona.sistema === "MIXTO") {
    document.getElementById(
      "resultado-sebd",
    ).classList.add("d-none");
    document.getElementById(
      "resultado-sucgs",
    ).classList.add("d-none");
    contenedorMixto.classList.remove("d-none");

    return prepararConfiguracionMixto(
      simulacion,
    );
  }

  document.getElementById(
    "resultado-sebd",
  ).classList.add("d-none");
  document.getElementById(
    "resultado-mixto",
  ).classList.add("d-none");
  document.getElementById(
    "resultado-sucgs",
  ).classList.add("d-none");

  if (persona.sistema === "SUCGS") {
    contenedorSUCGS.classList.remove("d-none");
    return prepararConfiguracionSUCGS(simulacion);
  }

  pendiente.classList.remove("d-none");
  pendiente.textContent = (
    "Para calcular una pensión debes identificar primero el "
    + "sistema previsional aplicable en el Paso 1."
  );

  return true;
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



/**
 * Prepara los campos específicos del Subsistema Mixto.
 *
 * @param {Object} simulacion Estado actual del asistente.
 * @returns {boolean} true cuando existe al menos un escenario salarial.
 */
function prepararConfiguracionMixto(simulacion) {
  const select = document.getElementById(
    "resultado-mixto-escenario-salarial",
  );
  const linea = simulacion.resumen_linea_tiempo;

  select.replaceChildren();

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

  const configuracion = (
    simulacion.configuracion_mixto_resultados || {}
  );
  const escenarioGuardado = (
    configuracion.escenario_salarial_nombre
    || simulacion.escenario_salarial_seleccionado
  );
  const existeGuardado = linea.escenarios.some(
    (escenario) => escenario.nombre === escenarioGuardado,
  );

  select.value = existeGuardado
    ? escenarioGuardado
    : linea.escenarios[0].nombre;

  document.getElementById(
    "resultado-mixto-saldo-cap",
  ).value = (
    configuracion.saldo_ahorro_personal == null
      ? ""
      : formatearNumeroMonetario(
        configuracion.saldo_ahorro_personal,
      )
  );

  document.getElementById(
    "resultado-mixto-bono",
  ).value = formatearNumeroMonetario(
    configuracion.bono_reconocimiento ?? 0,
  );

  document.getElementById(
    "resultado-mixto-bono-confirmado",
  ).checked = Boolean(
    configuracion.bono_reconocimiento_confirmado_oficialmente,
  );

  document.getElementById(
    "resultado-mixto-valor-actuarial",
  ).value = configuracion.valor_actuarial_expectativa_vida ?? "";

  document.getElementById(
    "resultado-mixto-opcion-cap",
  ).value = configuracion.opcion_prestacion_cap || "AUTO";

  return true;
}


/**
 * Prepara los datos específicos del SUCGS y restaura la configuración previa.
 *
 * @param {Object} simulacion Estado actual del asistente.
 * @returns {boolean} true cuando existe al menos un escenario salarial.
 */
function prepararConfiguracionSUCGS(simulacion) {
  const select = document.getElementById(
    "resultado-sucgs-escenario-salarial",
  );
  const linea = simulacion.resumen_linea_tiempo;

  select.replaceChildren();

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

  const configuracion = (
    simulacion.configuracion_sucgs_resultados || {}
  );
  const escenarioGuardado = (
    configuracion.escenario_salarial_nombre
    || simulacion.escenario_salarial_seleccionado
  );
  const existeGuardado = linea.escenarios.some(
    (escenario) => escenario.nombre === escenarioGuardado,
  );

  select.value = existeGuardado
    ? escenarioGuardado
    : linea.escenarios[0].nombre;

  document.getElementById(
    "resultado-sucgs-saldo",
  ).value = configuracion.saldo_capitalizacion_solidaria == null
    ? ""
    : formatearNumeroMonetario(
      configuracion.saldo_capitalizacion_solidaria,
    );

  document.getElementById(
    "resultado-sucgs-saldo-confirmado",
  ).checked = Boolean(
    configuracion.saldo_confirmado_oficialmente,
  );

  document.getElementById(
    "resultado-sucgs-minimo-universal",
  ).value = formatearNumeroMonetario(
    configuracion.valor_minimo_universal_vigente ?? 144,
  );

  document.getElementById(
    "resultado-sucgs-pgs",
  ).value = formatearNumeroMonetario(
    configuracion.pension_garantizada_solidaria_vigente ?? 265,
  );

  document.getElementById(
    "resultado-sucgs-valores-confirmados",
  ).checked = Boolean(
    configuracion.valores_solidarios_confirmados_oficialmente,
  );

  document.getElementById(
    "resultado-sucgs-historial-completo",
  ).checked = Boolean(
    configuracion.historial_laboral_completo_confirmado,
  );

  const estabilidad = configuracion.estabilidad_salarial_art197_confirmada;
  document.getElementById(
    "resultado-sucgs-estabilidad",
  ).value = estabilidad === true
    ? "SI"
    : (estabilidad === false ? "NO" : "");

  document.getElementById(
    "resultado-sucgs-anio-inicio",
  ).textContent = simulacion.historial?.anio_inicio ?? "—";

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



/**
 * Lee un campo numérico opcional sin convertir una cadena vacía en cero.
 *
 * @param {string} id Identificador del campo.
 * @returns {number|null} Número válido o null cuando está vacío.
 */
function leerNumeroOpcionalResultados(id) {
  const valor = document.getElementById(id).value.trim();

  if (valor === "") {
    return null;
  }

  const numero = Number(valor);

  if (!Number.isFinite(numero)) {
    throw new Error(
      "Revisa los valores numéricos introducidos en el Paso 6.",
    );
  }

  return numero;
}


/**
 * Lee un campo monetario opcional con separadores de miles.
 *
 * @param {string} id Identificador del campo monetario.
 * @returns {number|null} Número válido o null cuando está vacío.
 */
function leerMontoOpcionalResultados(id) {
  const valor = document.getElementById(id).value.trim();

  if (valor === "") {
    return null;
  }

  const numero = obtenerValorMonetario(valor);

  if (!Number.isFinite(numero)) {
    throw new Error(
      "Revisa los montos introducidos en el Paso 6.",
    );
  }

  return numero;
}


/**
 * Construye la entrada integrada para el motor del Subsistema Mixto.
 *
 * @returns {Object} Solicitud lista para FastAPI.
 */
function construirSolicitudResultadoMixto() {
  const simulacion = obtenerSimulacion();
  const persona = simulacion.persona || {};
  const seleccionado = simulacion.escenario_retiro_seleccionado;

  if (persona.sistema !== "MIXTO") {
    throw new Error(
      "El cálculo Mixto solo puede ejecutarse cuando el sistema "
      + "seleccionado en el Paso 1 es Subsistema Mixto.",
    );
  }

  if (!simulacion.historial || !simulacion.resumen_historial) {
    throw new Error(
      "El cálculo Mixto requiere un historial salarial anual "
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
    "resultado-mixto-escenario-salarial",
  ).value;

  if (!escenarioSalarial) {
    throw new Error(
      "Selecciona un escenario salarial para realizar el cálculo Mixto.",
    );
  }

  const bono = leerMontoOpcionalResultados(
    "resultado-mixto-bono",
  ) ?? 0;

  return {
    fecha_nacimiento: persona.fecha_nacimiento,
    sexo: persona.sexo,
    historial: simulacion.historial,
    linea_tiempo: simulacion.resumen_linea_tiempo,
    resumen_retiro: simulacion.resumen_retiro,
    fecha_retiro_seleccionada: seleccionado.fecha_retiro,
    escenario_salarial_nombre: escenarioSalarial,
    saldo_ahorro_personal: leerMontoOpcionalResultados(
      "resultado-mixto-saldo-cap",
    ),
    bono_reconocimiento: bono,
    bono_reconocimiento_confirmado_oficialmente: (
      document.getElementById(
        "resultado-mixto-bono-confirmado",
      ).checked
    ),
    valor_actuarial_expectativa_vida: leerNumeroOpcionalResultados(
      "resultado-mixto-valor-actuarial",
    ),
    opcion_prestacion_cap: document.getElementById(
      "resultado-mixto-opcion-cap",
    ).value,
  };
}


/**
 * Guarda la configuración Mixto usada por el Paso 6.
 *
 * @param {Object} simulacion Estado del asistente.
 * @param {Object} datos Solicitud enviada al backend.
 */
function guardarConfiguracionResultadoMixto(
  simulacion,
  datos,
) {
  simulacion.escenario_salarial_seleccionado = (
    datos.escenario_salarial_nombre
  );
  simulacion.configuracion_mixto_resultados = {
    escenario_salarial_nombre: datos.escenario_salarial_nombre,
    saldo_ahorro_personal: datos.saldo_ahorro_personal,
    bono_reconocimiento: datos.bono_reconocimiento,
    bono_reconocimiento_confirmado_oficialmente: (
      datos.bono_reconocimiento_confirmado_oficialmente
    ),
    valor_actuarial_expectativa_vida: (
      datos.valor_actuarial_expectativa_vida
    ),
    opcion_prestacion_cap: datos.opcion_prestacion_cap,
  };
}


/**
 * Solicita el cálculo Mixto integrado con los Pasos 1–5.
 */
async function calcularResultadoMixto() {
  ocultarErrorResultados();

  let datos;

  try {
    datos = construirSolicitudResultadoMixto();
  } catch (error) {
    mostrarErrorResultados(error.message);
    return;
  }

  const boton = document.getElementById(
    "btn-calcular-resultado-mixto",
  );

  boton.disabled = true;
  boton.textContent = "Calculando…";

  try {
    const respuesta = await fetch(
      "/api/simulacion/resultados/mixto",
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
          "No fue posible calcular la prestación del Subsistema Mixto.",
        ),
      );
      return;
    }

    const simulacion = obtenerSimulacion();

    guardarConfiguracionResultadoMixto(
      simulacion,
      datos,
    );
    simulacion.resultado_mixto = contenido;

    guardarSimulacion(simulacion);

    mostrarResultadoMixto(contenido);

  } catch {
    mostrarErrorResultados(
      "No fue posible comunicarse con el servidor.",
    );

  } finally {
    boton.disabled = false;
    boton.textContent = "Recalcular prestación Mixto";
  }
}


/**
 * Convierte el selector de estabilidad del artículo 197 a un valor triestado.
 *
 * @returns {boolean|null} true, false o null si permanece pendiente.
 */
function leerEstabilidadSUCGS() {
  const valor = document.getElementById(
    "resultado-sucgs-estabilidad",
  ).value;

  if (valor === "SI") {
    return true;
  }

  if (valor === "NO") {
    return false;
  }

  return null;
}


/**
 * Construye la solicitud integrada del SUCGS a partir de los Pasos 1–5.
 *
 * @returns {Object} Solicitud lista para FastAPI.
 */
function construirSolicitudResultadoSUCGS() {
  const simulacion = obtenerSimulacion();
  const persona = simulacion.persona || {};
  const seleccionado = simulacion.escenario_retiro_seleccionado;

  if (persona.sistema !== "SUCGS") {
    throw new Error(
      "El cálculo SUCGS solo puede ejecutarse cuando el sistema "
      + "seleccionado en el Paso 1 es SUCGS.",
    );
  }

  if (!simulacion.historial || !simulacion.resumen_historial) {
    throw new Error(
      "El cálculo SUCGS requiere un historial salarial anual "
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
    "resultado-sucgs-escenario-salarial",
  ).value;

  if (!escenarioSalarial) {
    throw new Error(
      "Selecciona un escenario salarial para realizar el cálculo SUCGS.",
    );
  }

  const saldo = leerMontoOpcionalResultados(
    "resultado-sucgs-saldo",
  );

  if (saldo == null) {
    throw new Error(
      "Introduce el saldo de Capitalización Solidaria para calcular SUCGS.",
    );
  }

  const minimoUniversal = leerMontoOpcionalResultados(
    "resultado-sucgs-minimo-universal",
  );
  const pgs = leerMontoOpcionalResultados(
    "resultado-sucgs-pgs",
  );

  if (minimoUniversal == null || minimoUniversal <= 0) {
    throw new Error(
      "El valor mínimo universal debe ser mayor que cero.",
    );
  }

  if (pgs == null || pgs <= 0) {
    throw new Error(
      "La Pensión Garantizada Solidaria debe ser mayor que cero.",
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
    saldo_capitalizacion_solidaria: saldo,
    saldo_confirmado_oficialmente: document.getElementById(
      "resultado-sucgs-saldo-confirmado",
    ).checked,
    valor_minimo_universal_vigente: minimoUniversal,
    pension_garantizada_solidaria_vigente: pgs,
    valores_solidarios_confirmados_oficialmente: document.getElementById(
      "resultado-sucgs-valores-confirmados",
    ).checked,
    historial_laboral_completo_confirmado: document.getElementById(
      "resultado-sucgs-historial-completo",
    ).checked,
    estabilidad_salarial_art197_confirmada: leerEstabilidadSUCGS(),
  };
}


/**
 * Conserva la configuración específica usada por el cálculo SUCGS.
 *
 * @param {Object} simulacion Estado actual del asistente.
 * @param {Object} datos Solicitud enviada al backend.
 */
function guardarConfiguracionResultadoSUCGS(simulacion, datos) {
  simulacion.escenario_salarial_seleccionado = (
    datos.escenario_salarial_nombre
  );
  simulacion.configuracion_sucgs_resultados = {
    escenario_salarial_nombre: datos.escenario_salarial_nombre,
    saldo_capitalizacion_solidaria: datos.saldo_capitalizacion_solidaria,
    saldo_confirmado_oficialmente: datos.saldo_confirmado_oficialmente,
    valor_minimo_universal_vigente: datos.valor_minimo_universal_vigente,
    pension_garantizada_solidaria_vigente: (
      datos.pension_garantizada_solidaria_vigente
    ),
    valores_solidarios_confirmados_oficialmente: (
      datos.valores_solidarios_confirmados_oficialmente
    ),
    historial_laboral_completo_confirmado: (
      datos.historial_laboral_completo_confirmado
    ),
    estabilidad_salarial_art197_confirmada: (
      datos.estabilidad_salarial_art197_confirmada
    ),
  };
}


/**
 * Solicita el cálculo SUCGS integrado con los Pasos 1–5.
 */
async function calcularResultadoSUCGS() {
  ocultarErrorResultados();

  let datos;

  try {
    datos = construirSolicitudResultadoSUCGS();
  } catch (error) {
    mostrarErrorResultados(error.message);
    return;
  }

  const boton = document.getElementById(
    "btn-calcular-resultado-sucgs",
  );

  boton.disabled = true;
  boton.textContent = "Calculando…";

  try {
    const respuesta = await fetch(
      "/api/simulacion/resultados/sucgs",
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
          "No fue posible calcular la prestación SUCGS.",
        ),
      );
      return;
    }

    const simulacion = obtenerSimulacion();

    guardarConfiguracionResultadoSUCGS(simulacion, datos);
    simulacion.resultado_sucgs = contenido;
    guardarSimulacion(simulacion);

    mostrarResultadoSUCGS(contenido);

  } catch {
    mostrarErrorResultados(
      "No fue posible comunicarse con el servidor.",
    );

  } finally {
    boton.disabled = false;
    boton.textContent = "Recalcular prestación SUCGS";
  }
}


// ============================================================
// Trazabilidad transversal
// ============================================================

/**
 * Oculta la explicación de cálculo cuando todavía no existe un resultado.
 */
function ocultarTrazabilidadResultado() {
  const contenedor = document.getElementById(
    "resultado-trazabilidad-calculo",
  );

  if (contenedor) {
    contenedor.classList.add("d-none");
  }
}


/**
 * Agrega un texto etiquetado a un bloque de trazabilidad.
 *
 * @param {HTMLElement} padre Contenedor del elemento.
 * @param {string} etiqueta Etiqueta visible.
 * @param {string|null} valor Valor que se mostrará.
 */
function agregarLineaTrazabilidad(padre, etiqueta, valor) {
  if (!valor) {
    return;
  }

  const linea = document.createElement("div");
  linea.className = "trace-line";

  const titulo = document.createElement("span");
  titulo.className = "trace-line-label";
  titulo.textContent = etiqueta;

  const contenido = document.createElement("span");
  contenido.className = "trace-line-value";
  contenido.textContent = valor;

  linea.append(titulo, contenido);
  padre.appendChild(linea);
}


/**
 * Presenta la cadena auditable enviada por el backend.
 *
 * @param {Object|null} trazabilidad Explicación transversal del cálculo.
 */
function mostrarTrazabilidadCalculo(trazabilidad) {
  const contenedor = document.getElementById(
    "resultado-trazabilidad-calculo",
  );

  if (!contenedor || !trazabilidad) {
    ocultarTrazabilidadResultado();
    return;
  }

  const datosContenedor = document.getElementById(
    "resultado-trazabilidad-datos",
  );
  const pasosContenedor = document.getElementById(
    "resultado-trazabilidad-pasos",
  );
  const fuentesContenedor = document.getElementById(
    "resultado-trazabilidad-fuentes",
  );

  datosContenedor.replaceChildren();
  pasosContenedor.replaceChildren();
  fuentesContenedor.replaceChildren();

  (trazabilidad.datos_utilizados || []).forEach((dato) => {
    const columna = document.createElement("div");
    columna.className = "col-md-6 col-xl-4";

    const tarjeta = document.createElement("div");
    tarjeta.className = "trace-data-card";

    const etiqueta = document.createElement("span");
    etiqueta.textContent = dato.etiqueta || dato.clave || "Dato";

    const valor = document.createElement("strong");
    valor.textContent = dato.valor ?? "—";

    const origen = document.createElement("small");
    origen.textContent = dato.origen || "Origen no indicado";

    tarjeta.append(etiqueta, valor, origen);

    if (dato.confirmado != null) {
      const estado = document.createElement("span");
      estado.className = dato.confirmado
        ? "trace-confirmed"
        : "trace-unconfirmed";
      estado.textContent = dato.confirmado
        ? "Confirmado"
        : "No confirmado";
      tarjeta.appendChild(estado);
    }

    columna.appendChild(tarjeta);
    datosContenedor.appendChild(columna);
  });

  (trazabilidad.pasos || []).forEach((paso) => {
    const tarjeta = document.createElement("article");
    tarjeta.className = "trace-step";

    const cabecera = document.createElement("div");
    cabecera.className = "trace-step-header";

    const numero = document.createElement("span");
    numero.className = "trace-step-number";
    numero.textContent = String(paso.orden ?? "");

    const titulo = document.createElement("strong");
    titulo.textContent = paso.titulo || "Paso de cálculo";

    cabecera.append(numero, titulo);
    tarjeta.appendChild(cabecera);

    agregarLineaTrazabilidad(tarjeta, "Regla", paso.regla);
    agregarLineaTrazabilidad(tarjeta, "Fórmula", paso.formula);
    agregarLineaTrazabilidad(tarjeta, "Sustitución", paso.sustitucion);
    agregarLineaTrazabilidad(tarjeta, "Resultado", paso.resultado);
    agregarLineaTrazabilidad(tarjeta, "Redondeo", paso.redondeo);

    if ((paso.fuentes || []).length) {
      const fuentesDisponibles = new Map(
        (trazabilidad.fuentes || []).map((fuente) => [fuente.id, fuente]),
      );

      const bloqueFuentes = document.createElement("div");
      bloqueFuentes.className = "trace-step-sources";

      const etiquetaFuentes = document.createElement("span");
      etiquetaFuentes.className = "trace-step-sources-label";
      etiquetaFuentes.textContent = "Fuentes: ";
      bloqueFuentes.appendChild(etiquetaFuentes);

      paso.fuentes.forEach((fuenteId, indice) => {
        const fuente = fuentesDisponibles.get(fuenteId);

        if (indice > 0) {
          bloqueFuentes.appendChild(document.createTextNode(" · "));
        }

        if (fuente?.url) {
          const enlaceFuente = document.createElement("a");
          enlaceFuente.href = fuente.url;
          enlaceFuente.target = "_blank";
          enlaceFuente.rel = "noopener noreferrer";
          enlaceFuente.textContent = fuente.titulo || fuenteId;
          bloqueFuentes.appendChild(enlaceFuente);
        } else {
          const textoFuente = document.createElement("span");
          textoFuente.textContent = fuente?.titulo || fuenteId;
          bloqueFuentes.appendChild(textoFuente);
        }
      });

      tarjeta.appendChild(bloqueFuentes);
    }

    pasosContenedor.appendChild(tarjeta);
  });

  document.getElementById(
    "resultado-trazabilidad-final-label",
  ).textContent = trazabilidad.resultado_final_etiqueta || "Resultado final";

  document.getElementById(
    "resultado-trazabilidad-final",
  ).textContent = trazabilidad.resultado_final || "—";

  const nombresTipo = {
    MENSUAL: "Prestación mensual",
    PAGO_UNICO: "Pago único",
    MENSUAL_Y_PAGO_UNICO: "Prestación mensual + pago único",
    PENDIENTE: "Resultado pendiente",
  };

  document.getElementById(
    "resultado-trazabilidad-final-tipo",
  ).textContent = nombresTipo[
    trazabilidad.resultado_final_tipo
  ] || trazabilidad.resultado_final_tipo || "—";

  const advertencias = document.getElementById(
    "resultado-trazabilidad-advertencias",
  );
  const mensajes = Array.from(
    new Set((trazabilidad.advertencias || []).filter(Boolean)),
  );

  if (mensajes.length) {
    advertencias.replaceChildren();
    const lista = document.createElement("ul");
    lista.className = "mb-0";

    mensajes.forEach((mensaje) => {
      const item = document.createElement("li");
      item.textContent = mensaje;
      lista.appendChild(item);
    });

    advertencias.appendChild(lista);
    advertencias.classList.remove("d-none");
  } else {
    advertencias.classList.add("d-none");
    advertencias.replaceChildren();
  }

  (trazabilidad.fuentes || []).forEach((fuente) => {
    const tarjeta = document.createElement("div");
    tarjeta.className = "trace-source-card";

    const titulo = document.createElement("strong");
    titulo.textContent = fuente.titulo || fuente.id || "Fuente oficial";

    const referencia = document.createElement("span");
    referencia.textContent = fuente.referencia || "";

    const articulos = document.createElement("small");
    articulos.textContent = (fuente.articulos || []).length
      ? `Artículos / alcance: ${fuente.articulos.join(", ")}`
      : "Fuente general";

    const enlace = document.createElement("a");
    enlace.className = "btn btn-sm btn-outline-primary mt-2 align-self-start btn-center-content";
    enlace.href = fuente.url;
    enlace.target = "_blank";
    enlace.rel = "noopener noreferrer";
    enlace.textContent = "Abrir fuente oficial";

    tarjeta.append(titulo, referencia, articulos, enlace);

    if (fuente.nota) {
      const nota = document.createElement("small");
      nota.className = "text-secondary";
      nota.textContent = fuente.nota;
      tarjeta.appendChild(nota);
    }

    fuentesContenedor.appendChild(tarjeta);
  });

  const detalle = document.getElementById(
    "resultado-trazabilidad-detalle",
  );
  detalle.classList.remove("show");

  const boton = document.getElementById(
    "btn-ver-calculo-completo",
  );
  boton.setAttribute("aria-expanded", "false");
  boton.textContent = "Ver cálculo completo";

  contenedor.classList.remove("d-none");
}


/**
 * Mantiene sincronizado el texto del botón de la sección colapsable.
 */
function configurarBotonTrazabilidad() {
  const detalle = document.getElementById(
    "resultado-trazabilidad-detalle",
  );
  const boton = document.getElementById(
    "btn-ver-calculo-completo",
  );

  if (!detalle || !boton || detalle.dataset.listenerTrazabilidad === "1") {
    return;
  }

  detalle.addEventListener("shown.bs.collapse", () => {
    boton.textContent = "Ocultar cálculo completo";
  });
  detalle.addEventListener("hidden.bs.collapse", () => {
    boton.textContent = "Ver cálculo completo";
  });
  detalle.dataset.listenerTrazabilidad = "1";
}


// ============================================================
// Resumen transversal
// ============================================================

/**
 * Traduce el estado normalizado a una etiqueta visible.
 *
 * @param {string} estado Estado devuelto por el backend.
 * @returns {string} Etiqueta legible.
 */
function nombreEstadoResultadoUnificado(estado) {
  const nombres = {
    COMPLETO: "Completo",
    INCOMPLETO: "Incompleto",
    DECISION_REQUERIDA: "Decisión requerida",
    NO_ELEGIBLE: "No elegible",
    TRANSICION: "Transición de sistema",
  };

  return nombres[estado] || estado || "—";
}


/**
 * Traduce la naturaleza económica sin mezclar pagos mensuales y únicos.
 *
 * @param {string} naturaleza Código normalizado.
 * @returns {string} Etiqueta visible.
 */
function nombreNaturalezaResultadoUnificado(naturaleza) {
  const nombres = {
    PENSION_MENSUAL: "Pensión mensual",
    PAGO_UNICO: "Pago único",
    PENSION_MAS_PAGO_UNICO: "Pensión mensual + pago único",
    SIN_MONTO: "Sin monto calculable",
    TRANSICION: "Transición a otro sistema",
  };

  return nombres[naturaleza] || naturaleza || "—";
}


/**
 * Presenta el contrato común de salida de SEBD, Mixto y SUCGS.
 *
 * @param {Object|null} resumen Resumen normalizado del backend.
 */
function mostrarResumenResultadoUnificado(resumen) {
  const contenedor = document.getElementById(
    "resultado-resumen-unificado",
  );

  if (!contenedor || !resumen) {
    if (contenedor) {
      contenedor.classList.add("d-none");
    }
    return;
  }

  document.getElementById(
    "resultado-unificado-estado",
  ).textContent = nombreEstadoResultadoUnificado(
    resumen.estado_resultado,
  );

  document.getElementById(
    "resultado-unificado-estado-nota",
  ).textContent = resumen.requiere_decision_usuario
    ? "Debes elegir una alternativa antes de cerrar el resultado."
    : (
      resumen.calculo_completo
        ? "El motor cerró las reglas evaluables con los datos disponibles."
        : "El resultado conserva una condición o dato pendiente."
    );

  document.getElementById(
    "resultado-unificado-mensual",
  ).textContent = resumen.pension_mensual_estimada == null
    ? "—"
    : formatearMoneda(resumen.pension_mensual_estimada);

  document.getElementById(
    "resultado-unificado-pago-unico",
  ).textContent = resumen.pago_unico_estimado == null
    ? "—"
    : formatearMoneda(resumen.pago_unico_estimado);

  document.getElementById(
    "resultado-unificado-naturaleza",
  ).textContent = nombreNaturalezaResultadoUnificado(
    resumen.naturaleza_prestacion,
  );

  document.getElementById(
    "resultado-unificado-modalidad",
  ).textContent = resumen.modalidad_nombre
    || resumen.modalidad_codigo
    || resumen.nombre_sistema
    || "—";

  const alerta = document.getElementById(
    "resultado-unificado-no-confirmados",
  );
  const noConfirmados = Array.isArray(resumen.datos_no_confirmados)
    ? resumen.datos_no_confirmados
    : [];

  if (noConfirmados.length > 0) {
    alerta.textContent = (
      "Datos aún no confirmados oficialmente: "
      + noConfirmados.join(", ")
      + "."
    );
    alerta.classList.remove("d-none");
  } else {
    alerta.textContent = "";
    alerta.classList.add("d-none");
  }

  contenedor.classList.remove("d-none");
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
  mostrarResumenResultadoUnificado(resultado.resumen_unificado);
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

  mostrarTrazabilidadCalculo(resultado.trazabilidad);
  configurarBotonTrazabilidad();

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



/**
 * Formatea un monto opcional para el resumen Mixto.
 *
 * @param {number|null} valor Monto recibido del backend.
 * @param {string} vacio Texto cuando el dato no aplica.
 * @returns {string} Monto formateado o texto alternativo.
 */
function formatearMontoOpcionalMixto(
  valor,
  vacio = "—",
) {
  if (valor == null) {
    return vacio;
  }

  return formatearMoneda(valor);
}


/**
 * Devuelve una etiqueta visible para la opción del CAP.
 *
 * @param {string} opcion Código devuelto por el motor.
 * @returns {string} Etiqueta legible.
 */
function obtenerNombreOpcionCAP(opcion) {
  const nombres = {
    AUTO: "Automático",
    PENSION_PROGRAMADA: "Pensión programada",
    DEVOLUCION_TOTAL: "Devolución total",
  };

  return nombres[opcion] || opcion || "—";
}


/**
 * Presenta el resultado integrado del Subsistema Mixto.
 *
 * @param {Object} resultado Respuesta integrada del backend.
 */
function mostrarResultadoMixto(resultado) {
  const calculo = resultado.calculo;
  mostrarResumenResultadoUnificado(resultado.resumen_unificado);
  const bd = calculo.componente_beneficio_definido;
  const cap = calculo.componente_ahorro_personal;

  mostrarEstadoMixto(calculo);

  document.getElementById(
    "resultado-mixto-modalidad",
  ).textContent = calculo.modalidad_nombre
    || calculo.estado_sistema
    || "—";

  document.getElementById(
    "resultado-mixto-modalidad-nota",
  ).textContent = obtenerNotaModalidadMixto(calculo);

  const decisionPendiente = Boolean(
    cap?.decision_requerida,
  );

  document.getElementById(
    "resultado-mixto-pension-total",
  ).textContent = calculo.pension_mensual_total_estimada == null
    ? (decisionPendiente ? "Pendiente" : "—")
    : formatearMoneda(calculo.pension_mensual_total_estimada);

  document.getElementById(
    "resultado-mixto-pago-unico-total",
  ).textContent = calculo.pago_unico_total_estimado == null
    ? "—"
    : formatearMoneda(calculo.pago_unico_total_estimado);

  const seccionBD = document.getElementById(
    "resultado-mixto-seccion-bd",
  );
  const seccionCAP = document.getElementById(
    "resultado-mixto-seccion-cap",
  );

  if (!bd || !cap) {
    seccionBD.classList.add("d-none");
    seccionCAP.classList.add("d-none");

    document.getElementById(
      "resultado-mixto-pension-bd",
    ).textContent = "—";
    document.getElementById(
      "resultado-mixto-pension-cap",
    ).textContent = "—";

  } else {
    seccionBD.classList.remove("d-none");
    seccionCAP.classList.remove("d-none");

    mostrarComponenteBDMixto(
      bd,
      resultado.anios_proyectados_incluidos || [],
    );
    mostrarComponenteCAPMixto(cap);
  }

  mostrarGarantiaMixto(cap);
  mostrarAdvertenciasResultadoMixto(resultado);

  document.getElementById(
    "resultado-mixto-fuente",
  ).textContent = calculo.fuente_normativa || "—";

  mostrarTrazabilidadCalculo(resultado.trazabilidad);
  configurarBotonTrazabilidad();

  const contenedor = document.getElementById(
    "resultado-mixto",
  );

  contenedor.classList.remove("d-none");
  contenedor.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}


/**
 * Muestra el estado global del cálculo Mixto.
 *
 * @param {Object} calculo Resultado jurídico del motor.
 */
function mostrarEstadoMixto(calculo) {
  const alerta = document.getElementById(
    "resultado-mixto-estado",
  );

  if (!calculo.calculo_mixto_aplicable) {
    alerta.className = "alert alert-warning";
    alerta.textContent = (
      calculo.estado_sistema === "TRANSICION_SUCGS"
        ? "Este escenario debe resolverse bajo SUCGS; no se calcula como Mixto."
        : "El escenario no se calcula bajo las reglas del Subsistema Mixto."
    );
    return;
  }

  if (calculo.componente_ahorro_personal?.decision_requerida) {
    alerta.className = "alert alert-info";
    alerta.textContent = (
      "El componente definido ya fue calculado, pero debes escoger "
      + "expresamente el tratamiento del CAP para completar el resultado."
    );
    return;
  }

  if (calculo.calculo_completo) {
    alerta.className = "alert alert-success";
    alerta.textContent = (
      "El escenario Mixto dispone de un cálculo completo con los datos ingresados."
    );
    return;
  }

  alerta.className = "alert alert-warning";
  alerta.textContent = (
    "El escenario Mixto es evaluable, pero faltan datos oficiales o "
    + "parámetros necesarios para completar el resultado."
  );
}


/**
 * Explica la modalidad o transición identificada en Mixto.
 *
 * @param {Object} calculo Resultado del motor.
 * @returns {string} Nota visible.
 */
function obtenerNotaModalidadMixto(calculo) {
  if (calculo.estado_sistema === "TRANSICION_SUCGS") {
    return (
      `Desde ${formatearFechaRetiro(calculo.fecha_inicio_calculo_sucgs)} `
      + "la prestación de este caso se deriva al cálculo SUCGS."
    );
  }

  const notas = {
    NORMAL: "El componente definido cumple la modalidad normal.",
    ANTICIPADA: "El componente definido aplica modalidad anticipada.",
    PROPORCIONAL: "El componente definido aplica modalidad proporcional.",
    PROPORCIONAL_ANTICIPADA: (
      "El componente definido combina proporcionalidad y reducción por edad."
    ),
    INDEMNIZACION: (
      "El componente definido genera una indemnización de pago único."
    ),
  };

  return notas[calculo.modalidad] || (
    "El motor mantiene separados el componente definido y el CAP."
  );
}


/**
 * Presenta el Componente de Beneficio Definido del Mixto.
 *
 * @param {Object} bd Resultado del componente definido.
 * @param {number[]} aniosProyectados Años originados por proyección.
 */
function mostrarComponenteBDMixto(
  bd,
  aniosProyectados,
) {
  document.getElementById(
    "resultado-mixto-pension-bd",
  ).textContent = bd.pension_mensual_estimada == null
    ? "No aplica"
    : formatearMoneda(bd.pension_mensual_estimada);

  document.getElementById(
    "resultado-mixto-bd-prestacion-nota",
  ).textContent = bd.indemnizacion_pago_unico_estimado != null
    ? "El componente BD genera un pago único."
    : "Resultado mensual del componente definido.";

  document.getElementById(
    "resultado-mixto-bd-salario-base",
  ).textContent = formatearMoneda(bd.salario_base_mensual);

  document.getElementById(
    "resultado-mixto-bd-tasa",
  ).textContent = formatearPorcentaje(
    bd.tasa_reemplazo_total_pct,
  );

  document.getElementById(
    "resultado-mixto-bd-maximo",
  ).textContent = formatearMoneda(
    bd.monto_maximo_componente,
  );

  document.getElementById(
    "resultado-mixto-bd-pago-unico",
  ).textContent = formatearMontoOpcionalMixto(
    bd.indemnizacion_pago_unico_estimado,
  );

  const cuerpo = document.getElementById(
    "resultado-mixto-bd-anios-body",
  );
  cuerpo.replaceChildren();

  const proyectados = new Set(
    aniosProyectados.map(Number),
  );

  (bd.anios_seleccionados || []).forEach(
    (registro) => {
      const fila = document.createElement("tr");

      agregarCeldaResultado(fila, registro.anio);
      agregarCeldaResultado(fila, registro.cuotas);
      agregarCeldaResultado(
        fila,
        formatearMoneda(registro.salario_cotizado_original),
      );
      agregarCeldaResultado(
        fila,
        formatearMoneda(registro.salario_considerado_bd),
      );

      const celdaOrigen = document.createElement("td");
      const badge = document.createElement("span");
      const esProyectado = proyectados.has(Number(registro.anio));

      badge.className = esProyectado
        ? "results-origin results-origin-projected"
        : "results-origin results-origin-historic";
      badge.textContent = esProyectado ? "Proyectado" : "Histórico";

      celdaOrigen.appendChild(badge);
      fila.appendChild(celdaOrigen);
      cuerpo.appendChild(fila);
    },
  );
}


/**
 * Presenta el Componente de Ahorro Personal del Mixto.
 *
 * @param {Object} cap Resultado del CAP.
 */
function mostrarComponenteCAPMixto(cap) {
  document.getElementById(
    "resultado-mixto-pension-cap",
  ).textContent = cap.pension_programada_mensual == null
    ? (cap.decision_requerida ? "Pendiente" : "No aplica")
    : formatearMoneda(cap.pension_programada_mensual);

  document.getElementById(
    "resultado-mixto-cap-prestacion-nota",
  ).textContent = cap.devolucion_pago_unico_estimado != null
    ? "El CAP se devuelve como pago único."
    : (
      cap.decision_requerida
        ? "Debes escoger el tratamiento del CAP."
        : "Pensión programada del CAP, cuando procede."
    );

  document.getElementById(
    "resultado-mixto-cap-saldo",
  ).textContent = formatearMontoOpcionalMixto(
    cap.saldo_ahorro_personal,
  );

  document.getElementById(
    "resultado-mixto-cap-bono",
  ).textContent = formatearMoneda(
    cap.bono_reconocimiento || 0,
  );

  document.getElementById(
    "resultado-mixto-cap-bono-estado",
  ).textContent = Number(cap.bono_reconocimiento || 0) === 0
    ? "Sin bono informado"
    : (
      cap.bono_reconocimiento_confirmado_oficialmente
        ? "Monto confirmado"
        : "Monto no confirmado"
    );

  document.getElementById(
    "resultado-mixto-cap-capital",
  ).textContent = formatearMontoOpcionalMixto(
    cap.capital_total_considerado,
  );

  const actuarial = (
    cap.valor_actuarial_expectativa_vida == null
      ? null
      : Number(cap.valor_actuarial_expectativa_vida)
  );
  document.getElementById(
    "resultado-mixto-cap-actuarial",
  ).textContent = (
    actuarial != null && Number.isFinite(actuarial)
      ? actuarial.toFixed(4).replace(/\.0+$/, "")
      : "No informado"
  );

  document.getElementById(
    "resultado-mixto-cap-opcion",
  ).textContent = obtenerNombreOpcionCAP(
    cap.opcion_solicitada,
  );

  document.getElementById(
    "resultado-mixto-cap-decision",
  ).textContent = cap.decision_requerida ? "Sí" : "No";

  document.getElementById(
    "resultado-mixto-cap-devolucion-disponible",
  ).textContent = cap.devolucion_total_disponible ? "Sí" : "No";

  document.getElementById(
    "resultado-mixto-cap-pago-unico",
  ).textContent = formatearMontoOpcionalMixto(
    cap.devolucion_pago_unico_estimado,
  );

  document.getElementById(
    "resultado-mixto-decision-ayuda",
  ).classList.toggle(
    "d-none",
    !cap.decision_requerida,
  );
}


/**
 * Muestra la garantía futura del CAP cuando la salida la incluye.
 *
 * @param {Object|null} cap Resultado del CAP.
 */
function mostrarGarantiaMixto(cap) {
  const seccion = document.getElementById(
    "resultado-mixto-garantia",
  );

  if (!cap || !cap.garantia_renta_vitalicia_aplica) {
    seccion.classList.add("d-none");
    return;
  }

  document.getElementById(
    "resultado-mixto-garantia-monto",
  ).textContent = formatearMontoOpcionalMixto(
    cap.garantia_monto_mensual,
  );

  document.getElementById(
    "resultado-mixto-garantia-condicion",
  ).textContent = cap.garantia_condicion_activacion || "—";

  const prima = Number(
    cap.prima_renta_vitalicia_pct_referencia,
  );
  document.getElementById(
    "resultado-mixto-garantia-prima",
  ).textContent = Number.isFinite(prima)
    ? (
      `Referencia histórica de prima: ${prima.toFixed(2)} %. `
      + "No se descuenta nuevamente del saldo CAP ingresado."
    )
    : "";

  seccion.classList.remove("d-none");
}


/**
 * Consolida advertencias de integración y de ambos componentes Mixto.
 *
 * @param {Object} resultado Respuesta completa integrada.
 */
function mostrarAdvertenciasResultadoMixto(resultado) {
  const calculo = resultado.calculo;
  const mensajes = [
    ...(resultado.advertencias_integracion || []),
    ...(calculo.componente_beneficio_definido?.advertencias || []),
    ...(calculo.componente_ahorro_personal?.advertencias || []),
    ...(calculo.advertencias || []),
  ];
  const unicos = [...new Set(mensajes.filter(Boolean))];
  const alerta = document.getElementById(
    "resultado-mixto-advertencias",
  );

  alerta.replaceChildren();

  if (unicos.length === 0) {
    alerta.classList.add("d-none");
    return;
  }

  const titulo = document.createElement("strong");
  titulo.textContent = "Advertencias del cálculo Mixto";
  alerta.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "mb-0 mt-2";

  unicos.forEach(
    (mensaje) => {
      const item = document.createElement("li");
      item.textContent = mensaje;
      lista.appendChild(item);
    },
  );

  alerta.appendChild(lista);
  alerta.classList.remove("d-none");
}


/**
 * Traduce el código de la capa solidaria del SUCGS a texto visible.
 *
 * @param {string|null} tipo Código devuelto por el motor.
 * @returns {string} Etiqueta legible.
 */
function obtenerNombrePrestacionSolidariaSUCGS(tipo) {
  const nombres = {
    PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO: "Contributiva sin complemento",
    PENSION_BENEFICIO_SOLIDARIO: "Pensión Garantizada Solidaria",
    PENSION_BENEFICIO_MINIMO: "Pensión de Beneficio Mínimo",
    PENSION_CONTRIBUTIVA_MENOR_MINIMO: "Contributiva inferior al mínimo",
  };

  return nombres[tipo] || tipo || "No aplica";
}


/**
 * Presenta un booleano auditable como Sí, No o Pendiente.
 *
 * @param {boolean|null|undefined} valor Valor a mostrar.
 * @returns {string} Texto visible.
 */
function formatearCondicionSUCGS(valor) {
  if (valor === true) {
    return "Sí";
  }
  if (valor === false) {
    return "No";
  }
  return "Pendiente";
}


/**
 * Presenta el resultado SUCGS completo hasta el artículo 197.
 *
 * @param {Object} resultado Respuesta integrada del backend.
 */
function mostrarResultadoSUCGS(resultado) {
  const calculo = resultado.calculo;
  mostrarResumenResultadoUnificado(resultado.resumen_unificado);

  mostrarEstadoSUCGS(calculo);

  document.getElementById(
    "resultado-sucgs-pension-total",
  ).textContent = calculo.pension_mensual_total_estimada == null
    ? "Pendiente"
    : formatearMoneda(calculo.pension_mensual_total_estimada);

  document.getElementById(
    "resultado-sucgs-pension-total-nota",
  ).textContent = calculo.calculo_total_disponible
    ? "Resultado después de las capas evaluadas hasta el artículo 197."
    : "Falta confirmar o completar una condición necesaria.";

  document.getElementById(
    "resultado-sucgs-contributiva",
  ).textContent = calculo.pension_contributiva_mensual == null
    ? "—"
    : formatearMoneda(calculo.pension_contributiva_mensual);

  document.getElementById(
    "resultado-sucgs-despues-solidaria",
  ).textContent = calculo.pension_despues_componente_solidario == null
    ? "—"
    : formatearMoneda(calculo.pension_despues_componente_solidario);

  document.getElementById(
    "resultado-sucgs-tipo-solidaria",
  ).textContent = obtenerNombrePrestacionSolidariaSUCGS(
    calculo.tipo_prestacion_solidaria,
  );

  document.getElementById(
    "resultado-sucgs-complemento-197",
  ).textContent = calculo.garantia_reemplazo_complemento_mensual == null
    ? "—"
    : formatearMoneda(calculo.garantia_reemplazo_complemento_mensual);

  document.getElementById(
    "resultado-sucgs-aplica-197",
  ).textContent = calculo.garantia_reemplazo_evaluada
    ? (calculo.garantia_reemplazo_aplica ? "Garantía aplicada" : "No aplica")
    : "Evaluación pendiente";

  document.getElementById(
    "resultado-sucgs-saldo-considerado",
  ).textContent = formatearMoneda(
    calculo.saldo_capitalizacion_solidaria,
  );

  document.getElementById(
    "resultado-sucgs-saldo-estado",
  ).textContent = calculo.saldo_confirmado_oficialmente
    ? "Saldo confirmado"
    : "Saldo no confirmado";

  const factor = calculo.factor_pensionamiento_actuarial;
  document.getElementById(
    "resultado-sucgs-factor",
  ).textContent = factor == null
    ? "No disponible"
    : `${calculo.edad_retiro_anios} años · ${Number(factor).toFixed(2)}`;

  document.getElementById(
    "resultado-sucgs-divisor",
  ).textContent = calculo.divisor_formula ?? "—";

  document.getElementById(
    "resultado-sucgs-contributiva-detalle",
  ).textContent = calculo.pension_contributiva_mensual == null
    ? "—"
    : formatearMoneda(calculo.pension_contributiva_mensual);

  document.getElementById(
    "resultado-sucgs-formula",
  ).textContent = calculo.pension_contributiva_mensual == null
    ? "No fue posible aplicar la fórmula contributiva en este escenario."
    : (
      `${formatearMoneda(calculo.saldo_capitalizacion_solidaria)} ÷ `
      + `${calculo.divisor_formula} × ${Number(factor).toFixed(2)} = `
      + `${formatearMoneda(calculo.pension_contributiva_mensual)}`
    );

  document.getElementById(
    "resultado-sucgs-solidaria-tipo",
  ).textContent = obtenerNombrePrestacionSolidariaSUCGS(
    calculo.tipo_prestacion_solidaria,
  );

  document.getElementById(
    "resultado-sucgs-vmu",
  ).textContent = formatearMoneda(
    calculo.valor_minimo_universal_utilizado,
  );

  document.getElementById(
    "resultado-sucgs-pgs-utilizada",
  ).textContent = formatearMoneda(
    calculo.pension_garantizada_solidaria_utilizada,
  );

  document.getElementById(
    "resultado-sucgs-complemento-solidario",
  ).textContent = calculo.complemento_solidario_mensual == null
    ? "—"
    : formatearMoneda(calculo.complemento_solidario_mensual);

  document.getElementById(
    "resultado-sucgs-197-evaluada",
  ).textContent = calculo.garantia_reemplazo_evaluada
    ? (calculo.garantia_reemplazo_aplica ? "Aplica" : "No aplica")
    : "Pendiente";

  document.getElementById(
    "resultado-sucgs-197-anual",
  ).textContent = formatearCondicionSUCGS(
    calculo.condicion_minimo_cuotas_anuales_cumple,
  );

  document.getElementById(
    "resultado-sucgs-197-distribucion",
  ).textContent = formatearCondicionSUCGS(
    calculo.condicion_distribucion_cuotas_cumple,
  );

  document.getElementById(
    "resultado-sucgs-197-estabilidad",
  ).textContent = formatearCondicionSUCGS(
    calculo.condicion_estabilidad_salarial_cumple,
  );

  document.getElementById(
    "resultado-sucgs-197-primeros",
  ).textContent = calculo.cuotas_primeros_20_anios ?? "—";

  document.getElementById(
    "resultado-sucgs-197-restantes",
  ).textContent = calculo.cuotas_anios_restantes ?? "—";

  document.getElementById(
    "resultado-sucgs-197-salario-base",
  ).textContent = calculo.salario_promedio_base_mensual == null
    ? "—"
    : formatearMoneda(calculo.salario_promedio_base_mensual);

  document.getElementById(
    "resultado-sucgs-197-tasa",
  ).textContent = calculo.tasa_reemplazo_minima_pct_aplicable == null
    ? "—"
    : formatearPorcentaje(calculo.tasa_reemplazo_minima_pct_aplicable);

  document.getElementById(
    "resultado-sucgs-197-objetivo",
  ).textContent = calculo.garantia_reemplazo_monto_objetivo == null
    ? "—"
    : formatearMoneda(calculo.garantia_reemplazo_monto_objetivo);

  document.getElementById(
    "resultado-sucgs-197-complemento",
  ).textContent = calculo.garantia_reemplazo_complemento_mensual == null
    ? "—"
    : formatearMoneda(calculo.garantia_reemplazo_complemento_mensual);

  mostrarDetalleArticulo197SUCGS(calculo);
  mostrarAdvertenciasResultadoSUCGS(resultado);

  document.getElementById(
    "resultado-sucgs-fuente",
  ).textContent = calculo.fuente_normativa || "—";

  mostrarTrazabilidadCalculo(resultado.trazabilidad);
  configurarBotonTrazabilidad();

  const contenedor = document.getElementById(
    "resultado-sucgs",
  );
  contenedor.classList.remove("d-none");
  contenedor.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}


/**
 * Muestra el estado general de disponibilidad del resultado SUCGS.
 *
 * @param {Object} calculo Resultado del motor.
 */
function mostrarEstadoSUCGS(calculo) {
  const alerta = document.getElementById(
    "resultado-sucgs-estado",
  );

  if (calculo.calculo_total_disponible) {
    alerta.className = "alert alert-success";
    alerta.textContent = (
      "El escenario SUCGS dispone de un resultado completo hasta las "
      + "reglas evaluadas del artículo 197."
    );
    return;
  }

  alerta.className = "alert alert-warning";
  alerta.textContent = (
    "El componente contributivo y la capa solidaria pueden estar calculados, "
    + "pero falta confirmar o completar la evaluación del artículo 197."
  );
}


/**
 * Resume las condiciones auditadas del artículo 197.
 *
 * @param {Object} calculo Resultado del motor.
 */
function mostrarDetalleArticulo197SUCGS(calculo) {
  const detalle = document.getElementById(
    "resultado-sucgs-197-detalle",
  );

  const partes = [];

  if (calculo.anios_sin_cotizacion_total != null) {
    partes.push(
      `${calculo.anios_sin_cotizacion_total} años sin cotización en total`,
    );
  }

  if (calculo.max_anios_sin_cotizacion_consecutivos != null) {
    partes.push(
      `${calculo.max_anios_sin_cotizacion_consecutivos} consecutivos como máximo`,
    );
  }

  if ((calculo.anios_con_1_a_4_cuotas || []).length > 0) {
    partes.push(
      "Años con 1 a 4 cuotas: "
      + calculo.anios_con_1_a_4_cuotas.join(", "),
    );
  }

  if (calculo.cuotas_minimas_por_tramo != null) {
    partes.push(
      `Mínimo por tramo para distribución: ${calculo.cuotas_minimas_por_tramo} cuotas`,
    );
  }

  detalle.textContent = partes.length > 0
    ? partes.join(" · ")
    : "La evaluación detallada permanece pendiente de información suficiente.";
}


/**
 * Consolida advertencias de integración y del motor SUCGS.
 *
 * @param {Object} resultado Respuesta integrada completa.
 */
function mostrarAdvertenciasResultadoSUCGS(resultado) {
  const mensajes = [
    ...(resultado.advertencias_integracion || []),
    ...(resultado.calculo?.advertencias || []),
  ];
  const unicos = [...new Set(mensajes.filter(Boolean))];
  const alerta = document.getElementById(
    "resultado-sucgs-advertencias",
  );

  alerta.replaceChildren();

  if (unicos.length === 0) {
    alerta.classList.add("d-none");
    return;
  }

  const titulo = document.createElement("strong");
  titulo.textContent = "Advertencias del cálculo SUCGS";
  alerta.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "mb-0 mt-2";

  unicos.forEach(
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


/**
 * Invalida el resultado Mixto cuando cambia uno de sus datos específicos.
 */
function invalidarResultadoMixto() {
  const simulacion = obtenerSimulacion();

  try {
    simulacion.configuracion_mixto_resultados = {
      escenario_salarial_nombre: document.getElementById(
        "resultado-mixto-escenario-salarial",
      ).value || null,
      saldo_ahorro_personal: leerMontoOpcionalResultados(
        "resultado-mixto-saldo-cap",
      ),
      bono_reconocimiento: (
        leerMontoOpcionalResultados("resultado-mixto-bono") ?? 0
      ),
      bono_reconocimiento_confirmado_oficialmente: (
        document.getElementById(
          "resultado-mixto-bono-confirmado",
        ).checked
      ),
      valor_actuarial_expectativa_vida: leerNumeroOpcionalResultados(
        "resultado-mixto-valor-actuarial",
      ),
      opcion_prestacion_cap: document.getElementById(
        "resultado-mixto-opcion-cap",
      ).value,
    };
  } catch {
    // Un valor temporalmente incompleto no debe impedir editar el formulario.
  }

  simulacion.resultado_mixto = null;
  guardarSimulacion(simulacion);

  document.getElementById(
    "resultado-mixto",
  ).classList.add("d-none");
}


/**
 * Restaura un resultado Mixto guardado y compatible con el sistema actual.
 */
function restaurarResultadoMixtoGuardado() {
  const simulacion = obtenerSimulacion();

  if (
    simulacion.resultado_mixto
    && simulacion.persona?.sistema === "MIXTO"
  ) {
    mostrarResultadoMixto(
      simulacion.resultado_mixto,
    );
  }
}


/**
 * Invalida el resultado SUCGS cuando cambia su configuración específica.
 */
function invalidarResultadoSUCGS() {
  const simulacion = obtenerSimulacion();

  try {
    simulacion.configuracion_sucgs_resultados = {
      escenario_salarial_nombre: document.getElementById(
        "resultado-sucgs-escenario-salarial",
      ).value || null,
      saldo_capitalizacion_solidaria: leerMontoOpcionalResultados(
        "resultado-sucgs-saldo",
      ),
      saldo_confirmado_oficialmente: document.getElementById(
        "resultado-sucgs-saldo-confirmado",
      ).checked,
      valor_minimo_universal_vigente: leerMontoOpcionalResultados(
        "resultado-sucgs-minimo-universal",
      ),
      pension_garantizada_solidaria_vigente: leerMontoOpcionalResultados(
        "resultado-sucgs-pgs",
      ),
      valores_solidarios_confirmados_oficialmente: document.getElementById(
        "resultado-sucgs-valores-confirmados",
      ).checked,
      historial_laboral_completo_confirmado: document.getElementById(
        "resultado-sucgs-historial-completo",
      ).checked,
      estabilidad_salarial_art197_confirmada: leerEstabilidadSUCGS(),
    };
  } catch {
    // Un valor temporalmente incompleto no debe bloquear la edición.
  }

  simulacion.resultado_sucgs = null;
  guardarSimulacion(simulacion);

  document.getElementById(
    "resultado-sucgs",
  ).classList.add("d-none");
}


/**
 * Restaura un resultado SUCGS guardado y compatible con el sistema actual.
 */
function restaurarResultadoSUCGSGuardado() {
  const simulacion = obtenerSimulacion();

  if (
    simulacion.resultado_sucgs
    && simulacion.persona?.sistema === "SUCGS"
  ) {
    mostrarResultadoSUCGS(simulacion.resultado_sucgs);
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
        restaurarResultadoMixtoGuardado();
        restaurarResultadoSUCGSGuardado();
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

    document.getElementById(
      "btn-calcular-resultado-mixto",
    ).addEventListener(
      "click",
      calcularResultadoMixto,
    );

    [
      "resultado-mixto-escenario-salarial",
      "resultado-mixto-saldo-cap",
      "resultado-mixto-bono",
      "resultado-mixto-bono-confirmado",
      "resultado-mixto-valor-actuarial",
      "resultado-mixto-opcion-cap",
    ].forEach(
      (id) => {
        document.getElementById(id).addEventListener(
          "change",
          invalidarResultadoMixto,
        );
      },
    );


    document.getElementById(
      "btn-calcular-resultado-sucgs",
    ).addEventListener(
      "click",
      calcularResultadoSUCGS,
    );

    [
      "resultado-sucgs-escenario-salarial",
      "resultado-sucgs-saldo",
      "resultado-sucgs-saldo-confirmado",
      "resultado-sucgs-minimo-universal",
      "resultado-sucgs-pgs",
      "resultado-sucgs-valores-confirmados",
      "resultado-sucgs-historial-completo",
      "resultado-sucgs-estabilidad",
    ].forEach(
      (id) => {
        document.getElementById(id).addEventListener(
          "change",
          invalidarResultadoSUCGS,
        );
      },
    );

    const simulacion = obtenerSimulacion();

    if (Number(simulacion.paso_actual) === 6) {
      prepararPasoResultados();
      restaurarResultadoSEBDGuardado();
      restaurarResultadoMixtoGuardado();
      restaurarResultadoSUCGSGuardado();
    }
  },
);
