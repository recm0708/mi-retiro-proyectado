"use strict";


/* ============================================================
   Mi Retiro Proyectado
   Línea temporal histórica y proyectada
   ============================================================ */

/*
 * Este archivo presenta una vista integrada del historial real,
 * el año actual parcialmente cotizado y los escenarios futuros.
 * La construcción matemática se realiza en el backend.
 */


// ============================================================
// Construcción y recuperación
// ============================================================

/**
 * Genera la línea temporal integrada a partir de la proyección
 * salarial y de los datos ya validados en pasos anteriores.
 *
 * @param {Object} datosProyeccion Parámetros enviados al motor salarial.
 * @param {Object} resumenProyeccion Respuesta del motor salarial.
 */
async function generarLineaTiempo(
  datosProyeccion,
  resumenProyeccion,
) {
  const simulacion = obtenerSimulacion();

  // Si el Asegurado(a) decidió continuar sin historial completo,
  // se conserva la visualización de proyección futura únicamente.
  if (
    simulacion.modo_historial !== "MANUAL"
    || !simulacion.historial
    || !simulacion.resumen_historial
  ) {
    simulacion.resumen_linea_tiempo = null;
    guardarSimulacion(simulacion);

    mostrarProyeccionConHistorialLimitado(
      resumenProyeccion,
    );

    return;
  }

  const datos = {
    historial: simulacion.historial,
    cuotas: simulacion.cuotas,
    salario_actual: simulacion.salario,
    proyeccion: datosProyeccion,
  };

  try {
    const respuesta = await fetch(
      "/api/simulacion/linea-tiempo",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(datos),
      },
    );

    const contenido = await respuesta.json();

    if (!respuesta.ok) {
      mostrarErrorProyeccion(
        obtenerMensajeError(
          contenido,
          "No fue posible construir la línea temporal.",
        ),
      );

      return;
    }

    simulacion.resumen_linea_tiempo = contenido;
    guardarSimulacion(simulacion);

    mostrarLineaTiempo(contenido);

  } catch {
    mostrarErrorProyeccion(
      "No fue posible comunicarse con el servidor para construir la línea temporal.",
    );
  }
}


/**
 * Restaura la línea temporal guardada al recargar la pestaña.
 */
function restaurarLineaTiempoGuardada() {
  const simulacion = obtenerSimulacion();

  if (
    simulacion.modo_historial === "MANUAL"
    && simulacion.resumen_linea_tiempo
  ) {
    mostrarLineaTiempo(
      simulacion.resumen_linea_tiempo,
    );
  }
}


// ============================================================
// Presentación principal
// ============================================================

/**
 * Muestra una línea temporal sin repetir el historial real en cada
 * escenario futuro.
 *
 * @param {Object} resumen Resultado del endpoint de línea temporal.
 */
function mostrarLineaTiempo(resumen) {
  const resultado = document.getElementById(
    "resultado-proyeccion",
  );

  const contenedor = document.getElementById(
    "contenedor-escenarios",
  );

  contenedor.replaceChildren();

  if (!resumen.escenarios.length) {
    return;
  }

  const escenarioBase = resumen.escenarios[0];

  const historicos = escenarioBase.registros.filter(
    (registro) => registro.anio < resumen.anio_actual,
  );

  const registroActual = escenarioBase.registros.find(
    (registro) => registro.anio === resumen.anio_actual,
  );

  contenedor.appendChild(
    crearEncabezadoLineaTiempo(resumen),
  );

  if (historicos.length > 0) {
    contenedor.appendChild(
      crearTablaHistorialLineaTiempo(historicos),
    );
  }

  if (registroActual) {
    contenedor.appendChild(
      crearResumenAnioActual(registroActual),
    );
  }

  const tituloFuturo = document.createElement("div");
  tituloFuturo.className = "timeline-section-heading";

  const titulo = document.createElement("h4");
  titulo.className = "h5 fw-bold mb-1";
  titulo.textContent = "Proyección futura";

  const descripcion = document.createElement("p");
  descripcion.className = "text-secondary mb-0";
  descripcion.textContent = (
    resumen.escenarios.length > 1
      ? "Cada escenario aplica una hipótesis salarial distinta sin modificar el historial real."
      : "Los años siguientes corresponden exclusivamente a estimaciones futuras."
  );

  tituloFuturo.append(
    titulo,
    descripcion,
  );

  contenedor.appendChild(tituloFuturo);

  resumen.escenarios.forEach((escenario) => {
    const futuros = escenario.registros.filter(
      (registro) => registro.anio > resumen.anio_actual,
    );

    if (futuros.length > 0) {
      contenedor.appendChild(
        crearTablaProyeccionLineaTiempo(
          escenario,
          futuros,
        ),
      );
    }
  });

  resultado.classList.remove("d-none");
}


/**
 * Crea un resumen superior que explica el alcance de la línea temporal.
 *
 * @param {Object} resumen Resultado completo de la línea temporal.
 * @returns {HTMLElement} Bloque informativo.
 */
function crearEncabezadoLineaTiempo(resumen) {
  const bloque = document.createElement("div");
  bloque.className = "timeline-overview";

  const titulo = document.createElement("strong");
  titulo.textContent = "Historial real + proyección futura";

  const texto = document.createElement("p");
  texto.className = "mb-0 mt-1";
  texto.textContent = (
    `Período mostrado: ${resumen.anio_inicio_historico}–${resumen.anio_fin_proyeccion}. `
    + "Los datos históricos y los valores proyectados permanecen separados."
  );

  bloque.append(
    titulo,
    texto,
  );

  return bloque;
}


// ============================================================
// Edad por año calendario
// ============================================================

/**
 * Calcula la edad que el Asegurado(a) cumple durante un año calendario.
 * Esta convención coincide con los comprobantes de Mi Retiro Seguro:
 * edad = año mostrado - año de nacimiento.
 *
 * @param {number} anio Año calendario de la fila.
 * @returns {number|string} Edad cumplida durante ese año o raya si no hay dato válido.
 */
function obtenerEdadEnAnio(anio) {
  const simulacion = obtenerSimulacion();
  const fechaNacimiento = simulacion.persona?.fecha_nacimiento;

  if (!fechaNacimiento) {
    return "—";
  }

  const anioNacimiento = Number.parseInt(
    fechaNacimiento.slice(0, 4),
    10,
  );

  const anioFila = Number(anio);

  if (
    !Number.isInteger(anioNacimiento)
    || !Number.isInteger(anioFila)
    || anioFila < anioNacimiento
  ) {
    return "—";
  }

  return anioFila - anioNacimiento;
}


// ============================================================
// Historial real
// ============================================================

/**
 * Crea la tabla del período completamente histórico.
 *
 * @param {Array<Object>} registros Registros previos al año actual.
 * @returns {HTMLElement} Sección del historial.
 */
function crearTablaHistorialLineaTiempo(registros) {
  const seccion = document.createElement("section");
  seccion.className = "timeline-section";

  const encabezado = document.createElement("div");
  encabezado.className = "timeline-section-heading";

  const titulo = document.createElement("h4");
  titulo.className = "h5 fw-bold mb-1";
  titulo.textContent = "Historial salarial real";

  const descripcion = document.createElement("p");
  descripcion.className = "text-secondary mb-0";
  descripcion.textContent = (
    "Información ya reportada como histórica. No contiene proyecciones."
  );

  encabezado.append(
    titulo,
    descripcion,
  );

  const envoltura = document.createElement("div");
  envoltura.className = "timeline-history-wrapper app-table-shell";

  const tabla = crearTablaBaseLineaTiempo([
    "Año",
    "Edad",
    "Cuotas",
    "Salario cotizado/reportado",
    "Estado",
  ]);

  const tbody = tabla.querySelector("tbody");

  registros.forEach((registro) => {
    const fila = document.createElement("tr");

    agregarCelda(fila, registro.anio);
    agregarCelda(fila, obtenerEdadEnAnio(registro.anio));
    agregarCelda(fila, registro.cuotas_historicas);
    agregarCelda(
      fila,
      formatearMoneda(registro.salario_historico),
    );
    agregarCeldaEstado(fila, registro.estado);

    tbody.appendChild(fila);
  });

  envoltura.appendChild(tabla);

  seccion.append(
    encabezado,
    envoltura,
  );

  return seccion;
}


// ============================================================
// Año actual
// ============================================================

/**
 * Muestra por separado la parte real y la parte todavía proyectada
 * del año calendario actual.
 *
 * @param {Object} registro Registro correspondiente al año actual.
 * @returns {HTMLElement} Sección del año actual.
 */
function crearResumenAnioActual(registro) {
  const seccion = document.createElement("section");
  seccion.className = "timeline-section timeline-current-year";

  const encabezado = document.createElement("div");
  encabezado.className = "timeline-section-heading";

  const titulo = document.createElement("h4");
  titulo.className = "h5 fw-bold mb-1";
  titulo.textContent = `Año actual — ${registro.anio}`;

  const descripcion = document.createElement("p");
  descripcion.className = "text-secondary mb-0";
  descripcion.textContent = (
    registro.estado === "MIXTO"
      ? "Este año contiene una parte ya cotizada y otra parte todavía estimada."
      : "Estado del año actual según las cuotas disponibles."
  );

  encabezado.append(
    titulo,
    descripcion,
  );

  const tarjetas = document.createElement("div");
  tarjetas.className = "row g-3";

  tarjetas.append(
    crearTarjetaActual(
      "Histórico real",
      registro.cuotas_historicas,
      registro.salario_historico,
      "Ya acreditado/reportado",
    ),
    crearTarjetaActual(
      "Proyección restante",
      registro.cuotas_proyectadas,
      registro.salario_proyectado,
      "Todavía estimado",
    ),
    crearTarjetaActual(
      "Cierre estimado",
      registro.cuotas_cierre,
      registro.salario_cierre,
      "Real + proyectado",
    ),
  );

  seccion.append(
    encabezado,
    tarjetas,
  );

  return seccion;
}


/**
 * Construye una tarjeta del resumen del año actual.
 *
 * @param {string} titulo Título de la tarjeta.
 * @param {number} cuotas Cuotas asociadas.
 * @param {number} salario Salario asociado.
 * @param {string} nota Descripción breve.
 * @returns {HTMLElement} Columna Bootstrap con tarjeta.
 */
function crearTarjetaActual(
  titulo,
  cuotas,
  salario,
  nota,
) {
  const columna = document.createElement("div");
  columna.className = "col-md-4";

  const tarjeta = document.createElement("div");
  tarjeta.className = "timeline-current-card";

  const etiqueta = document.createElement("span");
  etiqueta.className = "timeline-current-label";
  etiqueta.textContent = titulo;

  const valorCuotas = document.createElement("strong");
  valorCuotas.className = "timeline-current-quotas";
  valorCuotas.textContent = `${cuotas} cuota${cuotas === 1 ? "" : "s"}`;

  const valorSalario = document.createElement("span");
  valorSalario.className = "timeline-current-salary";
  valorSalario.textContent = formatearMoneda(salario);

  const textoNota = document.createElement("small");
  textoNota.className = "text-secondary";
  textoNota.textContent = nota;

  tarjeta.append(
    etiqueta,
    valorCuotas,
    valorSalario,
    textoNota,
  );

  columna.appendChild(tarjeta);

  return columna;
}


// ============================================================
// Futuro por escenario
// ============================================================

/**
 * Crea una tabla exclusivamente futura para un escenario salarial.
 *
 * @param {Object} escenario Escenario completo.
 * @param {Array<Object>} registros Registros posteriores al año actual.
 * @returns {HTMLElement} Sección de proyección.
 */
function crearTablaProyeccionLineaTiempo(
  escenario,
  registros,
) {
  const seccion = document.createElement("section");
  seccion.className = "projection-scenario timeline-future-scenario";

  const encabezado = document.createElement("div");
  encabezado.className = "projection-scenario-header";

  const titulo = document.createElement("h4");
  titulo.className = "projection-scenario-title";
  titulo.textContent = escenario.nombre;

  const tasa = document.createElement("span");
  tasa.className = "projection-rate";
  tasa.textContent = `Tasa anual: ${formatearPorcentaje(escenario.tasa_anual_pct)}`;

  encabezado.append(
    titulo,
    tasa,
  );

  const envoltura = document.createElement("div");
  envoltura.className = "table-responsive app-table-shell";

  const tabla = crearTablaBaseLineaTiempo([
    "Año",
    "Edad",
    "Cuotas proyectadas",
    "Salario mensual estimado",
    "Salario cotizado proyectado",
    "Estado",
  ]);

  const tbody = tabla.querySelector("tbody");

  registros.forEach((registro) => {
    const fila = document.createElement("tr");

    const salarioMensual = (
      registro.cuotas_proyectadas > 0
        ? registro.salario_proyectado / registro.cuotas_proyectadas
        : 0
    );

    agregarCelda(fila, registro.anio);
    agregarCelda(fila, obtenerEdadEnAnio(registro.anio));
    agregarCelda(fila, registro.cuotas_proyectadas);
    agregarCelda(
      fila,
      formatearMoneda(salarioMensual),
    );
    agregarCelda(
      fila,
      formatearMoneda(registro.salario_proyectado),
    );
    agregarCeldaEstado(fila, registro.estado);

    tbody.appendChild(fila);
  });

  envoltura.appendChild(tabla);

  seccion.append(
    encabezado,
    envoltura,
  );

  return seccion;
}


// ============================================================
// Modo con historial limitado
// ============================================================

/**
 * Mantiene la salida salarial anterior cuando no existe historial
 * suficiente para construir una línea temporal completa.
 *
 * @param {Object} resumenProyeccion Resultado del motor salarial.
 */
function mostrarProyeccionConHistorialLimitado(
  resumenProyeccion,
) {
  mostrarResumenProyeccion(
    resumenProyeccion,
  );

  const contenedor = document.getElementById(
    "contenedor-escenarios",
  );

  const aviso = document.createElement("div");
  aviso.className = "alert alert-warning mb-4";
  aviso.textContent = (
    "No se proporcionó un historial salarial completo. "
    + "Por ello se muestra únicamente la proyección futura."
  );

  contenedor.prepend(aviso);
}


// ============================================================
// Utilidades de DOM
// ============================================================

/**
 * Crea una tabla con encabezados y cuerpo vacío.
 *
 * @param {string[]} encabezados Nombres de columnas.
 * @returns {HTMLTableElement} Tabla preparada.
 */
function crearTablaBaseLineaTiempo(encabezados) {
  const tabla = document.createElement("table");
  tabla.className = "table table-hover align-middle timeline-table";

  const thead = document.createElement("thead");
  const tr = document.createElement("tr");

  encabezados.forEach((texto) => {
    const th = document.createElement("th");
    th.scope = "col";
    th.textContent = texto;
    tr.appendChild(th);
  });

  thead.appendChild(tr);

  const tbody = document.createElement("tbody");

  tabla.append(
    thead,
    tbody,
  );

  return tabla;
}


/**
 * Agrega una celda de texto a una fila.
 *
 * @param {HTMLTableRowElement} fila Fila de destino.
 * @param {string|number} valor Contenido de la celda.
 */
function agregarCelda(fila, valor) {
  const td = document.createElement("td");
  td.textContent = valor;
  fila.appendChild(td);
}


/**
 * Agrega una etiqueta visual de estado.
 *
 * @param {HTMLTableRowElement} fila Fila de destino.
 * @param {string} estado Estado técnico del registro.
 */
function agregarCeldaEstado(fila, estado) {
  const td = document.createElement("td");
  const badge = document.createElement("span");

  const configuracion = {
    SIN_COTIZACION: ["Sin cotización", "timeline-status-none"],
    HISTORICO: ["Histórico", "timeline-status-historic"],
    HISTORICO_PARCIAL: ["Histórico parcial", "timeline-status-partial"],
    MIXTO: ["Real + proyectado", "timeline-status-mixed"],
    PROYECTADO: ["Proyectado", "timeline-status-projected"],
    PENDIENTE: ["Pendiente", "timeline-status-pending"],
  };

  const [texto, clase] = (
    configuracion[estado]
    || [estado, "timeline-status-pending"]
  );

  badge.className = `timeline-status ${clase}`;
  badge.textContent = texto;

  td.appendChild(badge);
  fila.appendChild(td);
}


// ============================================================
// Restauración al cargar la página
// ============================================================

document.addEventListener(
  "DOMContentLoaded",
  restaurarLineaTiempoGuardada,
);
