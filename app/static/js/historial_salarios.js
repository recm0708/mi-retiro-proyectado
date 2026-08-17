"use strict";


/* ============================================================
   Mi Retiro Proyectado
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

let filtroHistorialActual = "TODOS";


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
  restaurarEstadoImportacionHistorial();
  actualizarFiltroHistorial();

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
 * por el Asegurado(a).
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
  const modoAnterior = simulacion.modo_historial || "MANUAL";

  simulacion.modo_historial = modo;

  if (modoAnterior !== modo) {
    simulacion.resumen_historial = null;
    simulacion.resumen_salario = null;
    simulacion.resumen_proyeccion = null;
    simulacion.resumen_linea_tiempo = null;
    simulacion.retiro = {};
    simulacion.resumen_retiro = null;
    document.getElementById("historial-estado-general")?.classList.add("d-none");
    document.getElementById("resultado-paso3")?.classList.add("d-none");
  }

  guardarSimulacion(simulacion);
}


/**
 * Confirma que el Asegurado(a) desea continuar sin proporcionar
 * el historial anual completo.
 */
function confirmarModoSoloActual() {
  const simulacion = obtenerSimulacion();

  simulacion.modo_historial = "SOLO_ACTUAL";
  simulacion.historial = null;
  simulacion.resumen_historial = null;
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_sucgs = null;

  guardarSimulacion(simulacion);

  if (typeof actualizarResumenPaso3 === "function") {
    actualizarResumenPaso3();
  }

  return true;
}


function restaurarEstadoImportacionHistorial() {
  const simulacion = obtenerSimulacion();
  const acciones = document.getElementById("historial-importado-acciones");

  if (!acciones) return;

  const hayImportacion = Boolean(
    simulacion.importacion_comprobante_confirmada
    && simulacion.referencia_mi_retiro_seguro
    && Array.isArray(simulacion.referencia_mi_retiro_seguro.registros)
    && simulacion.referencia_mi_retiro_seguro.registros.length,
  );

  acciones.classList.toggle("d-none", !hayImportacion);
}


function origenCampoHistorial(anio, campo) {
  const simulacion = obtenerSimulacion();
  return simulacion.origen_campos_historial?.[String(anio)]?.[campo] || null;
}


function aplicarOrigenCampoHistorial(control, anio, campo) {
  if (!control) return;
  const origen = origenCampoHistorial(anio, campo);
  if (!origen) {
    control.dataset.provenance = control.value.trim() ? "COMPLETADO_MANUAL" : "NO_DETECTADO";
    return;
  }

  control.readOnly = true;
  control.classList.add("history-field-imported");
  control.setAttribute("aria-readonly", "true");
  const codigo = typeof codigoProcedenciaDesdeOrigen === "function"
    ? codigoProcedenciaDesdeOrigen(origen)
    : "DETECTADO";
  control.dataset.provenance = codigo || "DETECTADO";
  const etiqueta = typeof textoProcedenciaDato === "function"
    ? textoProcedenciaDato(codigo)
    : "Detectado";
  control.title = `${etiqueta}. Usa Revisar importación si necesitas corregirlo.`;
}


function actualizarPeriodoHistorialVisible() {
  const inicio = document.getElementById("historial_anio_inicio")?.value || "—";
  const fin = document.getElementById("historial_anio_fin")?.value || String(ANIO_HISTORIAL_ACTUAL);
  const salida = document.getElementById("historial-periodo-visible");
  if (salida) salida.textContent = `${inicio}–${fin}`;
}


function evaluarEstadoFilaHistorial(fila) {
  const cuotasTexto = fila.querySelector(".history-input-cuotas")?.value.trim() || "";
  const salarioTexto = fila.querySelector(".history-input-salario")?.value.trim() || "";
  const tieneCuotas = cuotasTexto !== "";
  const tieneSalario = salarioTexto !== "";

  if (!tieneCuotas && !tieneSalario) {
    return {
      codigo: "PENDIENTE",
      etiqueta: "Pendiente",
      clase: "history-status-pending",
      pendiente: true,
    };
  }

  if (tieneCuotas && !tieneSalario) {
    return {
      codigo: "FALTA_SALARIO",
      etiqueta: "Falta salario",
      clase: "history-status-missing",
      pendiente: true,
    };
  }

  if (!tieneCuotas && tieneSalario) {
    return {
      codigo: "FALTAN_CUOTAS",
      etiqueta: "Faltan cuotas",
      clase: "history-status-missing",
      pendiente: true,
    };
  }

  const cuotas = Number(cuotasTexto);
  const salario = obtenerValorMonetario(salarioTexto || "0");

  if (
    !Number.isInteger(cuotas)
    || cuotas < 0
    || cuotas > 12
    || !Number.isFinite(salario)
    || salario < 0
  ) {
    return {
      codigo: "REVISAR",
      etiqueta: "Revisar",
      clase: "history-status-review",
      pendiente: true,
    };
  }

  if (cuotas === 0 && salario === 0) {
    return {
      codigo: "SIN_COTIZACION",
      etiqueta: "Sin cotización",
      clase: "history-status-none",
      pendiente: false,
    };
  }

  if ((cuotas === 0 && salario > 0) || (cuotas > 0 && salario <= 0)) {
    return {
      codigo: "REVISAR",
      etiqueta: "Revisar",
      clase: "history-status-review",
      pendiente: true,
    };
  }

  if (cuotas < 12) {
    return {
      codigo: "PARCIAL",
      etiqueta: "Parcial",
      clase: "history-status-partial",
      pendiente: false,
    };
  }

  return {
    codigo: "COMPLETO",
    etiqueta: "Completo",
    clase: "history-status-complete",
    pendiente: false,
  };
}


function filaHistorialPendiente(fila) {
  return evaluarEstadoFilaHistorial(fila).pendiente;
}


function actualizarFiltroHistorial() {
  const filas = Array.from(document.querySelectorAll("#historial-tabla-body tr"));
  let visibles = 0;

  filas.forEach((fila) => {
    const mostrar = filtroHistorialActual === "TODOS" || filaHistorialPendiente(fila);
    fila.classList.toggle("d-none", !mostrar);
    if (mostrar) visibles += 1;
  });

  document.querySelectorAll("[data-history-filter]").forEach((boton) => {
    const activo = boton.dataset.historyFilter === filtroHistorialActual;
    boton.classList.toggle("active", activo);
    boton.setAttribute("aria-pressed", String(activo));
  });

  const estado = document.getElementById("historial-filtro-estado");
  if (estado) {
    estado.textContent = filtroHistorialActual === "PENDIENTES"
      ? `${visibles} año(s) pendiente(s)`
      : `${filas.length} año(s) en el período`;
  }

  const contenedor = document.querySelector(".history-table-wrapper");
  const vacio = document.getElementById("historial-filtro-vacio");
  const sinPendientesVisibles = filtroHistorialActual === "PENDIENTES" && visibles === 0;

  if (contenedor) {
    const tablaCorta = visibles <= 4;
    contenedor.classList.toggle("table-scroll-compact", tablaCorta);
    contenedor.classList.toggle("d-none", sinPendientesVisibles);
    contenedor.dataset.visibleRows = String(visibles);

    if (tablaCorta) {
      contenedor.scrollTop = 0;
    }
  }

  if (vacio) {
    vacio.classList.toggle("d-none", !sinPendientesVisibles);
  }
}


/**
 * Mantiene el estado visual y el filtro sincronizados mientras el usuario
 * escribe, sin depender de listeners instalados en cada fila individual.
 */
function manejarEdicionDelegadaHistorial(evento) {
  const control = evento.target.closest(
    ".history-input-cuotas, .history-input-salario",
  );

  if (!control) return;

  const fila = control.closest("tr");
  if (!fila) return;

  if (!control.readOnly) {
    control.dataset.provenance = control.value.trim()
      ? "COMPLETADO_MANUAL"
      : "NO_DETECTADO";
  }

  actualizarEstadoFila(fila);
  invalidarHistorial();
}


function configurarEventosDelegadosHistorial() {
  const cuerpo = document.getElementById("historial-tabla-body");
  if (!cuerpo || cuerpo.dataset.historyDelegated === "true") return;

  cuerpo.dataset.historyDelegated = "true";
  cuerpo.addEventListener("input", manejarEdicionDelegadaHistorial);
  cuerpo.addEventListener("change", manejarEdicionDelegadaHistorial);
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

  const filaTieneImportacion = Boolean(
    origenCampoHistorial(anio, "cuotas")
    || origenCampoHistorial(anio, "salario_cotizado")
  );

  fila.classList.add(filaTieneImportacion ? "data-row-imported" : "data-row-manual");
  fila.dataset.dataOrigin = filaTieneImportacion ? "imported" : "manual";


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
  inputCuotas.placeholder = "0–12";


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
    `Salario anual reportado ${anio}`,
  );
  inputSalario.placeholder = "Ej.: 12,000.00";

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

    if (
      simulacion.resumen_detalle_anio_actual?.cuotas_coinciden
    ) {
      inputSalario.value = formatearNumeroMonetario(
        simulacion.resumen_detalle_anio_actual.total_salario_acreditado,
      );
      inputSalario.readOnly = true;
      inputSalario.dataset.sincronizadoDetalle = "true";
      inputSalario.setAttribute(
        "title",
        "Sincronizado desde el detalle salarial del año actual.",
      );
    }
  }


  aplicarOrigenCampoHistorial(inputCuotas, anio, "cuotas");
  aplicarOrigenCampoHistorial(inputSalario, anio, "salario_cotizado");

  // Un cero no confirmado no debe parecer un salario válido cuando el
  // año actual ya tiene cuotas. Se muestra como pendiente para que el
  // usuario pueda completarlo o derivarlo desde el detalle del año actual.
  if (
    anio === ANIO_HISTORIAL_ACTUAL
    && Number(inputCuotas.value || 0) > 0
    && obtenerValorMonetario(inputSalario.value || 0) <= 0
    && !origenCampoHistorial(anio, "salario_cotizado")
    && inputSalario.dataset.sincronizadoDetalle !== "true"
  ) {
    inputSalario.value = "";
  }

  configurarCampoMonetario(
    inputSalario,
  );


  // ----------------------------------------------------------
  // Eventos
  // ----------------------------------------------------------

  // La actualización reactiva de la fila se gestiona mediante
  // delegación sobre el tbody. Así continúa funcionando aunque
  // la tabla se regenere, cambie el filtro o se restauren datos.


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
  actualizarPeriodoHistorialVisible();

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

  actualizarFiltroHistorial();

  if (
    simulacion.detalle_anio_actual_habilitado
    && typeof sincronizarFilaAnualDesdeDetalleLocal === "function"
  ) {
    sincronizarFilaAnualDesdeDetalleLocal();
  }
}


/**
 * Actualiza la etiqueta visual de una fila según las cuotas
 * introducidas.
 *
 * @param {HTMLTableRowElement} fila Fila que debe actualizarse.
 */
function actualizarEstadoFila(fila) {
  const etiqueta = fila.querySelector(".history-status");
  if (!etiqueta) return;

  const estado = evaluarEstadoFilaHistorial(fila);
  etiqueta.className = `history-status ${estado.clase}`;
  etiqueta.textContent = estado.etiqueta;
  etiqueta.dataset.historyState = estado.codigo;

  actualizarFiltroHistorial();
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
      if (
        anio === ANIO_HISTORIAL_ACTUAL
        && cuotasTexto !== ""
        && Number(cuotasTexto) > 0
        && salarioTexto === ""
      ) {
        throw new Error(
          `Completa el salario anual reportado de ${anio}. `
          + "Si prefieres construirlo con salarios mensuales o quincenales, activa el detalle del año actual.",
        );
      }

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

    if (cuotas > 0 && salario <= 0) {
      const orientacion = anio === ANIO_HISTORIAL_ACTUAL
        ? " Completa el total anual reportado o activa el detalle del año actual para construirlo con salarios mensuales o quincenales."
        : "";
      throw new Error(
        `El año ${anio} tiene cuotas acreditadas pero falta un salario anual válido.${orientacion}`,
      );
    }

    if (cuotas === 0 && salario > 0) {
      throw new Error(
        `El año ${anio} tiene salario reportado pero registra cero cuotas. Revisa ambos valores.`,
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

  let simulacion =
    obtenerSimulacion();

  if (!simulacion.resumen_cuotas) {
    const puedeRevalidar = (
      typeof asegurarCuotasAnalizadasParaPaso3 === "function"
      && await asegurarCuotasAnalizadasParaPaso3()
    );

    if (!puedeRevalidar) {
      return false;
    }

    simulacion = obtenerSimulacion();
  }

  let registros;

  try {
    registros =
      leerRegistrosHistorial();

  } catch (error) {
    mostrarErrorHistorial(
      error.message,
    );

    return false;
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

      return false;
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
    simulacion.resumen_proyeccion = null;
    simulacion.resumen_linea_tiempo = null;
    simulacion.retiro = {};
    simulacion.resumen_retiro = null;
    simulacion.escenario_retiro_seleccionado = null;
    simulacion.escenario_salarial_seleccionado = null;
    simulacion.resultado_sebd_normal = null;
    simulacion.resultado_mixto = null;
  simulacion.resultado_sucgs = null;

    guardarSimulacion(
      simulacion,
    );

    mostrarResumenHistorial(
      contenido,
    );

    return true;
  } catch {
    mostrarErrorHistorial(
      "No fue posible comunicarse con el servidor.",
    );
    return false;
  }
}


// ============================================================
// Presentación del resultado
// ============================================================

function ocultarResumenHistorialAnalizado() {
  const contenedor = document.getElementById("historial-resumen-analizado");
  contenedor?.classList.add("d-none");
}


function mostrarResumenHistorialAnalizado(resumen) {
  const contenedor = document.getElementById("historial-resumen-analizado");
  if (!contenedor || !resumen) return;

  const asignar = (id, valor) => {
    const elemento = document.getElementById(id);
    if (elemento) elemento.textContent = valor;
  };

  asignar("historial-resumen-cuotas-referencia", resumen.cuotas_totales_referencia ?? "—");
  asignar("historial-resumen-cuotas-identificadas", resumen.cuotas_sumadas ?? "—");
  asignar("historial-resumen-diferencia", resumen.diferencia_cuotas ?? "—");
  asignar(
    "historial-resumen-total-salarios",
    typeof formatearMoneda === "function"
      ? formatearMoneda(resumen.total_salarios_reportados)
      : resumen.total_salarios_reportados,
  );

  contenedor.classList.remove("d-none");
}

/**
 * Muestra el resumen devuelto por el backend.
 *
 * @param {Object} resumen Resultado del historial salarial.
 */
function mostrarResumenHistorial(resumen) {
  mostrarResumenHistorialAnalizado(resumen);

  const estado = document.getElementById("historial-estado-general");

  if (estado) {
    estado.classList.remove("d-none");

    if (resumen.cuotas_coinciden && resumen.historial_completo) {
      estado.className = "alert alert-success mt-4 mb-0";
      estado.textContent = "El historial registrado coincide con el total de cuotas acreditadas informado en el Paso 2.";
    } else {
      estado.className = "alert alert-warning mt-4 mb-0";
      const mensajes = [];

      if (!resumen.historial_completo) {
        mensajes.push(`Faltan registros para ${resumen.anios_sin_registro.length} año(s).`);
      }

      if (resumen.diferencia_cuotas !== 0) {
        mensajes.push(
          `Existe una diferencia de ${resumen.diferencia_cuotas} cuota(s) respecto del total informado en el Paso 2.`,
        );
      }

      estado.textContent = mensajes.join(" ");
    }
  }

  if (typeof actualizarResumenPaso3 === "function") {
    actualizarResumenPaso3();
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

  ocultarResumenHistorialAnalizado();

  simulacion.resumen_proyeccion =
    null;

  simulacion.resumen_linea_tiempo =
    null;

  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_sucgs = null;

  guardarSimulacion(
    simulacion,
  );

  document.getElementById("historial-estado-general")?.classList.add("d-none");
  document.getElementById("resultado-paso3")?.classList.add("d-none");
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
    configurarEventosDelegadosHistorial();
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


    document.querySelectorAll("[data-history-filter]").forEach((boton) => {
      boton.addEventListener("click", () => {
        filtroHistorialActual = boton.dataset.historyFilter || "TODOS";
        actualizarFiltroHistorial();
      });
    });

    document.getElementById("btn-revisar-historial-importado")?.addEventListener(
      "click",
      () => {
        if (typeof revisarComprobanteImportado === "function") {
          revisarComprobanteImportado(3);
        }
      },
    );
  },
);
