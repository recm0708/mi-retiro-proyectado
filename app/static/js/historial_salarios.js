"use strict";


/* ============================================================
   Calculadora de Pensión CSS
   Gestión del historial salarial
   ============================================================ */

/*
 * Este archivo administra la tabla histórica del Paso 3.
 * La lógica previsional permanece en Python; JavaScript se
 * limita a recopilar, presentar y conservar los datos.
 */


// ============================================================
// Configuración
// ============================================================

const ANIO_HISTORIAL_ACTUAL =
  new Date().getFullYear();


// ============================================================
// Inicialización
// ============================================================

/**
 * Inicializa el historial utilizando la información almacenada
 * en los pasos anteriores.
 */
function inicializarHistorialSalarial() {
  const simulacion = obtenerSimulacion();

  const selectorModo = document.getElementById(
    "modo_historial",
  );

  if (simulacion.modo_historial) {
    selectorModo.value =
      simulacion.modo_historial;
  }

  actualizarModoHistorial();
  sincronizarHistorialConDatosActuales();

  if (
    selectorModo.value === "MANUAL"
    && simulacion.resumen_historial
  ) {
    mostrarResumenHistorial(
      simulacion.resumen_historial,
    );
  }
}


/**
 * Sincroniza el período histórico con los datos actuales del
 * Paso 1 y del Paso 2 antes de mostrar o regenerar la tabla.
 */
function sincronizarHistorialConDatosActuales() {
  const simulacion = obtenerSimulacion();

  const campoFin = document.getElementById(
    "historial_anio_fin",
  );

  const campoInicio = document.getElementById(
    "historial_anio_inicio",
  );

  campoFin.value =
    ANIO_HISTORIAL_ACTUAL;

  let anioInicio = null;

  if (
    simulacion.historial
    && simulacion.historial.anio_inicio
  ) {
    anioInicio =
      simulacion.historial.anio_inicio;

  } else if (
    simulacion.historial_anio_inicio_temporal
  ) {
    anioInicio =
      simulacion.historial_anio_inicio_temporal;

  } else if (
    simulacion.persona
    && simulacion.persona.fecha_ingreso_css
  ) {
    anioInicio = Number(
      simulacion.persona
        .fecha_ingreso_css
        .substring(0, 4),
    );
  }

  if (
    !Number.isInteger(anioInicio)
    || anioInicio < 1900
    || anioInicio > ANIO_HISTORIAL_ACTUAL
  ) {
    anioInicio =
      ANIO_HISTORIAL_ACTUAL;
  }

  campoInicio.value =
    anioInicio;

  if (
    document.getElementById(
      "modo_historial",
    ).value === "MANUAL"
  ) {
    generarTablaHistorial();
  }
}



// ============================================================
// Modos de captura
// ============================================================

/**
 * Muestra la interfaz correspondiente al método seleccionado
 * por el usuario.
 */
function actualizarModoHistorial() {
  const modo = document.getElementById(
    "modo_historial",
  ).value;

  const manual = document.getElementById(
    "historial-modo-manual",
  );

  const soloActual = document.getElementById(
    "historial-modo-solo-actual",
  );

  manual.classList.toggle(
    "d-none",
    modo !== "MANUAL",
  );

  soloActual.classList.toggle(
    "d-none",
    modo !== "SOLO_ACTUAL",
  );

  const simulacion = obtenerSimulacion();

  simulacion.modo_historial = modo;

  guardarSimulacion(simulacion);
}


/**
 * Confirma que el usuario desea continuar sin proporcionar
 * el historial anual completo.
 */
function confirmarModoSoloActual() {
  const simulacion = obtenerSimulacion();

  simulacion.modo_historial =
    "SOLO_ACTUAL";

  simulacion.historial = null;
  simulacion.resumen_historial = null;

  guardarSimulacion(simulacion);

  document.getElementById(
    "monto_salario",
  ).focus();
}


// ============================================================
// Generación de la tabla
// ============================================================

/**
 * Obtiene los registros ya introducidos en la tabla actual.
 *
 * @returns {Object} Registros indexados por año.
 */
function obtenerValoresTablaActual() {
  const valores = {};

  document
    .querySelectorAll(
      "#historial-tabla-body tr",
    )
    .forEach((fila) => {
      const anio = Number(
        fila.dataset.anio,
      );

      const cuotas = fila.querySelector(
        ".history-input-cuotas",
      );

      const salario = fila.querySelector(
        ".history-input-salario",
      );

      valores[anio] = {
        cuotas: cuotas.value,
        salario_cotizado: salario.value,
      };
    });

  return valores;
}


/**
 * Genera una fila editable del historial.
 *
 * @param {number} anio Año correspondiente a la fila.
 * @param {Object|null} datos Datos previamente almacenados.
 * @returns {HTMLTableRowElement} Fila creada.
 */
function crearFilaHistorial(
  anio,
  datos,
) {
  const fila = document.createElement(
    "tr",
  );

  fila.dataset.anio = anio;


  // ----------------------------------------------------------
  // Año
  // ----------------------------------------------------------

  const celdaAnio =
    document.createElement("td");

  celdaAnio.className =
    "history-year-cell";

  celdaAnio.textContent = anio;


  // ----------------------------------------------------------
  // Cuotas
  // ----------------------------------------------------------

  const celdaCuotas =
    document.createElement("td");

  const inputCuotas =
    document.createElement("input");

  inputCuotas.type = "number";
  inputCuotas.min = "0";
  inputCuotas.max = "12";
  inputCuotas.step = "1";

  inputCuotas.className =
    "form-control history-input-cuotas";

  inputCuotas.setAttribute(
    "aria-label",
    `Cuotas ${anio}`,
  );


  // ----------------------------------------------------------
  // Salario cotizado
  // ----------------------------------------------------------

  const celdaSalario =
    document.createElement("td");

  const grupoSalario =
    document.createElement("div");

  grupoSalario.className =
    "input-group";

  const prefijo =
    document.createElement("span");

  prefijo.className =
    "input-group-text";

  prefijo.textContent = "B/.";

  const inputSalario =
    document.createElement("input");

  inputSalario.type = "text";
  inputSalario.inputMode = "decimal";

  inputSalario.className =
    "form-control history-input-salario money-input";

  inputSalario.setAttribute(
    "aria-label",
    `Salario cotizado ${anio}`,
  );

  grupoSalario.append(
    prefijo,
    inputSalario,
  );


  // ----------------------------------------------------------
  // Estado
  // ----------------------------------------------------------

  const celdaEstado =
    document.createElement("td");

  const estado =
    document.createElement("span");

  estado.className =
    "history-status";

  celdaEstado.appendChild(
    estado,
  );


  // ----------------------------------------------------------
  // Restaurar datos existentes
  // ----------------------------------------------------------

  if (datos) {
    if (
      datos.cuotas !== undefined
      && datos.cuotas !== null
      && datos.cuotas !== ""
    ) {
      inputCuotas.value =
        datos.cuotas;
    }

    if (
      datos.salario_cotizado !== undefined
      && datos.salario_cotizado !== null
      && datos.salario_cotizado !== ""
    ) {
      inputSalario.value =
        datos.salario_cotizado;
    }
  }


  // ----------------------------------------------------------
  // Año actual
  // ----------------------------------------------------------

  if (
    anio === ANIO_HISTORIAL_ACTUAL
  ) {
    const simulacion =
      obtenerSimulacion();

    if (
      simulacion.cuotas
      && simulacion.cuotas
        .cuotas_anio_actual !== undefined
    ) {
      inputCuotas.value =
        simulacion.cuotas
          .cuotas_anio_actual;

      // Las cuotas del año actual deben coincidir con
      // las informadas previamente en el Paso 2.
      inputCuotas.readOnly = true;
    }
  }


  configurarCampoMonetario(
    inputSalario,
  );


  // ----------------------------------------------------------
  // Eventos
  // ----------------------------------------------------------

  inputCuotas.addEventListener(
    "input",
    () => {
      actualizarEstadoFila(
        fila,
      );

      invalidarHistorial();
    },
  );

  inputSalario.addEventListener(
    "input",
    invalidarHistorial,
  );


  // ----------------------------------------------------------
  // Ensamblar fila
  // ----------------------------------------------------------

  celdaCuotas.appendChild(
    inputCuotas,
  );

  celdaSalario.appendChild(
    grupoSalario,
  );

  fila.append(
    celdaAnio,
    celdaCuotas,
    celdaSalario,
    celdaEstado,
  );

  actualizarEstadoFila(
    fila,
  );

  return fila;
}


/**
 * Genera todos los años comprendidos entre el año inicial
 * y el año actual.
 */
function generarTablaHistorial() {
  ocultarErrorHistorial();
  ocultarAdvertenciaHistorial();

  const inicio = Number(
    document.getElementById(
      "historial_anio_inicio",
    ).value,
  );

  if (
    !Number.isInteger(inicio)
    || inicio < 1900
    || inicio > ANIO_HISTORIAL_ACTUAL
  ) {
    mostrarErrorHistorial(
      "El año inicial del historial no es válido.",
    );

    return;
  }

  const cuerpo = document.getElementById(
    "historial-tabla-body",
  );

  // Conserva los valores actualmente escritos antes
  // de volver a generar la tabla.
  const valoresActuales =
    obtenerValoresTablaActual();

  const simulacion =
    obtenerSimulacion();

  const valoresGuardados = {};

  if (
    simulacion.historial
    && Array.isArray(
      simulacion.historial.registros,
    )
  ) {
    simulacion.historial.registros.forEach(
      (registro) => {
        valoresGuardados[registro.anio] =
          registro;
      },
    );
  }

  cuerpo.replaceChildren();

  for (
    let anio = inicio;
    anio <= ANIO_HISTORIAL_ACTUAL;
    anio += 1
  ) {
    const datos =
      valoresActuales[anio]
      || valoresGuardados[anio]
      || null;

    cuerpo.appendChild(
      crearFilaHistorial(
        anio,
        datos,
      ),
    );
  }
}


/**
 * Actualiza la etiqueta visual de una fila según las cuotas
 * introducidas.
 *
 * @param {HTMLTableRowElement} fila Fila que debe actualizarse.
 */
function actualizarEstadoFila(fila) {
  const input = fila.querySelector(
    ".history-input-cuotas",
  );

  const etiqueta = fila.querySelector(
    ".history-status",
  );

  if (input.value === "") {
    etiqueta.className =
      "history-status history-status-pending";

    etiqueta.textContent =
      "Pendiente";

    return;
  }

  const cuotas = Number(
    input.value,
  );

  if (cuotas === 0) {
    etiqueta.className =
      "history-status history-status-none";

    etiqueta.textContent =
      "Sin cotización";

  } else if (cuotas < 12) {
    etiqueta.className =
      "history-status history-status-partial";

    etiqueta.textContent =
      "Parcial";

  } else {
    etiqueta.className =
      "history-status history-status-complete";

    etiqueta.textContent =
      "Completo";
  }
}


/**
 * Completa con doce cuotas los años que todavía no tienen
 * un valor introducido.
 */
function completarCuotasVacias() {
  document
    .querySelectorAll(
      "#historial-tabla-body tr",
    )
    .forEach((fila) => {
      const anio = Number(
        fila.dataset.anio,
      );

      const input = fila.querySelector(
        ".history-input-cuotas",
      );

      // El año actual ya está vinculado al Paso 2.
      if (
        anio !== ANIO_HISTORIAL_ACTUAL
        && input.value === ""
      ) {
        input.value = 12;

        actualizarEstadoFila(
          fila,
        );
      }
    });

  invalidarHistorial();
}


// ============================================================
// Lectura y validación
// ============================================================

/**
 * Convierte la tabla visible en registros para la API.
 *
 * Una fila completamente vacía se omite para que el backend
 * pueda identificarla como año sin registro.
 *
 * @returns {Array<Object>} Registros históricos.
 */
function leerRegistrosHistorial() {
  const registros = [];

  const filas = document.querySelectorAll(
    "#historial-tabla-body tr",
  );

  for (const fila of filas) {
    const anio = Number(
      fila.dataset.anio,
    );

    const cuotasTexto = fila.querySelector(
      ".history-input-cuotas",
    ).value.trim();

    const salarioTexto = fila.querySelector(
      ".history-input-salario",
    ).value.trim();


    // Una fila totalmente vacía representa un año pendiente.
    if (
      cuotasTexto === ""
      && salarioTexto === ""
    ) {
      continue;
    }


    if (
      cuotasTexto === ""
      || salarioTexto === ""
    ) {
      throw new Error(
        `Completa tanto las cuotas como el salario del año ${anio}.`,
      );
    }

    const cuotas = Number(
      cuotasTexto,
    );

    const salario = obtenerValorMonetario(
      salarioTexto,
    );

    if (
      !Number.isInteger(cuotas)
      || cuotas < 0
      || cuotas > 12
    ) {
      throw new Error(
        `Las cuotas del año ${anio} deben estar entre 0 y 12.`,
      );
    }

    if (
      !Number.isFinite(salario)
      || salario < 0
    ) {
      throw new Error(
        `El salario del año ${anio} no es válido. Usa como máximo dos decimales.`,
      );
    }

    registros.push({
      anio: anio,
      cuotas: cuotas,
      salario_cotizado: salario,
    });
  }

  return registros;
}


/**
 * Envía el historial salarial al backend para su validación.
 */
async function analizarHistorialSalarial() {
  ocultarErrorHistorial();
  ocultarAdvertenciaHistorial();

  const simulacion =
    obtenerSimulacion();

  if (
    !simulacion.resumen_cuotas
  ) {
    mostrarErrorHistorial(
      "Primero debes analizar las cuotas en el Paso 2.",
    );

    return;
  }

  let registros;

  try {
    registros =
      leerRegistrosHistorial();

  } catch (error) {
    mostrarErrorHistorial(
      error.message,
    );

    return;
  }

  const anioInicio = Number(
    document.getElementById(
      "historial_anio_inicio",
    ).value,
  );

  const datos = {
    anio_inicio:
      anioInicio,

    anio_fin:
      ANIO_HISTORIAL_ACTUAL,

    cuotas_totales_referencia:
      simulacion.resumen_cuotas
        .cuotas_reales,

    registros:
      registros,
  };

  try {
    const respuesta = await fetch(
      "/api/simulacion/historial-salarial",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(
          datos,
        ),
      },
    );

    const contenido =
      await respuesta.json();

    if (!respuesta.ok) {
      mostrarErrorHistorial(
        obtenerMensajeError(
          contenido,
          "No fue posible analizar el historial salarial.",
        ),
      );

      return;
    }

    simulacion.modo_historial =
      "MANUAL";

    simulacion.historial =
      datos;

    simulacion.historial_anio_inicio_temporal =
      datos.anio_inicio;

    simulacion.resumen_historial =
      contenido;

    // Los cálculos previsionales posteriores deberán
    // regenerarse después de modificar el historial.
    simulacion.resultado_retiro = null;
    simulacion.resultados = null;

    guardarSimulacion(
      simulacion,
    );

    mostrarResumenHistorial(
      contenido,
    );

  } catch {
    mostrarErrorHistorial(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


// ============================================================
// Presentación del resultado
// ============================================================

/**
 * Muestra el resumen devuelto por el backend.
 *
 * @param {Object} resumen Resultado del historial salarial.
 */
function mostrarResumenHistorial(resumen) {
  document.getElementById(
    "resultado-historial",
  ).classList.remove("d-none");

  document.getElementById(
    "historial-cuotas-referencia",
  ).textContent =
    resumen.cuotas_totales_referencia;

  document.getElementById(
    "historial-cuotas-sumadas",
  ).textContent =
    resumen.cuotas_sumadas;

  document.getElementById(
    "historial-diferencia-cuotas",
  ).textContent =
    resumen.diferencia_cuotas;

  document.getElementById(
    "historial-total-salarios",
  ).textContent = formatearMoneda(
    resumen.total_salarios_reportados,
  );

  const estado = document.getElementById(
    "historial-estado-general",
  );

  if (
    resumen.cuotas_coinciden
    && resumen.historial_completo
  ) {
    estado.className =
      "alert alert-success mt-4 mb-0";

    estado.textContent =
      "El historial introducido explica el total de cuotas "
      + "acreditadas informado en el Paso 2.";

  } else {
    estado.className =
      "alert alert-warning mt-4 mb-0";

    const mensajes = [];

    if (
      !resumen.historial_completo
    ) {
      mensajes.push(
        `Faltan registros para ${resumen.anios_sin_registro.length} año(s).`,
      );
    }

    if (
      resumen.diferencia_cuotas !== 0
    ) {
      mensajes.push(
        `Existe una diferencia de ${resumen.diferencia_cuotas} cuota(s) `
        + "respecto del total informado en el Paso 2.",
      );
    }

    estado.textContent =
      mensajes.join(" ");
  }
}


/**
 * Invalida el análisis histórico después de una modificación.
 */
function invalidarHistorial() {
  const simulacion =
    obtenerSimulacion();

  simulacion.resumen_historial =
    null;

  simulacion.resultado_retiro =
    null;

  simulacion.resultados =
    null;

  guardarSimulacion(
    simulacion,
  );

  document.getElementById(
    "resultado-historial",
  ).classList.add("d-none");
}


// ============================================================
// Mensajes
// ============================================================

function mostrarErrorHistorial(mensaje) {
  const elemento = document.getElementById(
    "error-historial",
  );

  elemento.textContent =
    mensaje;

  elemento.classList.remove(
    "d-none",
  );
}


function ocultarErrorHistorial() {
  document.getElementById(
    "error-historial",
  ).classList.add("d-none");
}


function ocultarAdvertenciaHistorial() {
  document.getElementById(
    "advertencia-historial",
  ).classList.add("d-none");
}


// ============================================================
// Eventos
// ============================================================

document.addEventListener(
  "DOMContentLoaded",
  () => {
    inicializarHistorialSalarial();

    document.getElementById(
      "modo_historial",
    ).addEventListener(
      "change",
      () => {
        actualizarModoHistorial();

        if (
          document.getElementById(
            "modo_historial",
          ).value === "MANUAL"
        ) {
          generarTablaHistorial();
        }
      },
    );


    document.getElementById(
      "btn-generar-historial",
    ).addEventListener(
      "click",
      () => {
        generarTablaHistorial();
        invalidarHistorial();
      },
    );


    document.getElementById(
      "historial_anio_inicio",
    ).addEventListener(
      "change",
      () => {
        const simulacion = obtenerSimulacion();

        simulacion.historial_anio_inicio_temporal = Number(
          document.getElementById(
            "historial_anio_inicio",
          ).value,
        );

        guardarSimulacion(simulacion);

        generarTablaHistorial();
        invalidarHistorial();
      },
    );


    document.getElementById(
      "btn-completar-cuotas",
    ).addEventListener(
      "click",
      completarCuotasVacias,
    );


    document.getElementById(
      "btn-analizar-historial",
    ).addEventListener(
      "click",
      analizarHistorialSalarial,
    );


    document.getElementById(
      "btn-confirmar-solo-actual",
    ).addEventListener(
      "click",
      confirmarModoSoloActual,
    );
  },
);
