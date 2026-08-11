"use strict";


/* ============================================================
   Paso 5 — Condiciones y escenarios de retiro
   ============================================================ */

/*
 * Este módulo conecta los datos personales y de cuotas con el
 * endpoint /api/simulacion/retiro. Mantiene separadas la fecha
 * de evaluación y la fecha hasta la cual las cuotas reales están
 * acreditadas.
 */


// ============================================================
// Utilidades de fecha
// ============================================================

/**
 * Devuelve la fecha local actual con formato YYYY-MM-DD.
 *
 * @returns {string} Fecha local del navegador.
 */
function obtenerFechaLocalActual() {
  const ahora = new Date();

  const anio = ahora.getFullYear();
  const mes = String(
    ahora.getMonth() + 1,
  ).padStart(2, "0");
  const dia = String(
    ahora.getDate(),
  ).padStart(2, "0");

  return `${anio}-${mes}-${dia}`;
}


/**
 * Convierte una fecha ISO YYYY-MM-DD a DD/MM/YYYY sin aplicar
 * conversiones de zona horaria.
 *
 * @param {string} fechaIso Fecha recibida desde la API.
 * @returns {string} Fecha preparada para la interfaz.
 */
function formatearFechaRetiro(fechaIso) {
  if (!fechaIso) {
    return "—";
  }

  const partes = fechaIso.split("-");

  if (partes.length !== 3) {
    return fechaIso;
  }

  return `${partes[2]}/${partes[1]}/${partes[0]}`;
}


// ============================================================
// Preparación y restauración
// ============================================================

/**
 * Sincroniza el Paso 5 con los datos ya validados en los pasos
 * anteriores y completa valores predeterminados cuando es necesario.
 */
function prepararPasoRetiro() {
  const simulacion = obtenerSimulacion();

  const cuotas = simulacion.cuotas || {};
  const persona = simulacion.persona || {};

  document.getElementById(
    "retiro-fecha-nacimiento",
  ).textContent = formatearFechaRetiro(
    persona.fecha_nacimiento,
  );

  document.getElementById(
    "retiro-sexo",
  ).textContent = (
    persona.sexo === "FEMENINO"
      ? "Femenino"
      : persona.sexo === "MASCULINO"
        ? "Masculino"
        : persona.sexo || "—"
  );

  document.getElementById(
    "retiro-cuotas-reales",
  ).textContent = cuotas.cuotas_totales ?? 0;

  document.getElementById(
    "retiro-cuotas-cierre",
  ).textContent = (
    cuotas.cuotas_esperadas_cierre_anio
    ?? cuotas.cuotas_anio_actual
    ?? 0
  );

  document.getElementById(
    "retiro-continua-cotizando",
  ).textContent = (
    cuotas.continua_cotizando
      ? "Sí"
      : "No"
  );

  document.getElementById(
    "retiro-cuotas-anuales",
  ).textContent = cuotas.cuotas_esperadas_por_anio ?? 0;

  const fechaEvaluacion = document.getElementById(
    "fecha_corte_retiro",
  );

  const fechaCuotas = document.getElementById(
    "fecha_corte_cuotas",
  );

  const hoy = obtenerFechaLocalActual();

  if (!fechaEvaluacion.value) {
    fechaEvaluacion.value = (
      simulacion.retiro?.fecha_corte
      || hoy
    );
  }

  if (!fechaCuotas.value) {
    fechaCuotas.value = (
      simulacion.retiro?.fecha_corte_cuotas
      || fechaEvaluacion.value
      || hoy
    );
  }

  actualizarLimiteFechaCuotas();
}


/**
 * Restaura las opciones específicas del Paso 5 desde sessionStorage.
 */
function restaurarDatosRetiro() {
  const simulacion = obtenerSimulacion();
  const retiro = simulacion.retiro || {};

  prepararPasoRetiro();

  if (retiro.fecha_corte) {
    document.getElementById(
      "fecha_corte_retiro",
    ).value = retiro.fecha_corte;
  }

  if (retiro.fecha_corte_cuotas) {
    document.getElementById(
      "fecha_corte_cuotas",
    ).value = retiro.fecha_corte_cuotas;
  }

  if (Array.isArray(retiro.anios_adicionales)) {
    const adicionales = new Set(
      retiro.anios_adicionales.map(Number),
    );

    document.getElementById(
      "btn-ajustar-proyeccion-retiro",
    ).addEventListener(
      "click",
      ajustarHorizonteProyeccionDesdeRetiro,
    );

    document
      .querySelectorAll(".retiro-adicional")
      .forEach((elemento) => {
        elemento.checked = adicionales.has(
          Number(elemento.value),
        );
      });
  }

  const usaPersonalizada = Boolean(
    retiro.fecha_retiro_personalizada,
  );

  document.getElementById(
    "usar_fecha_retiro_personalizada",
  ).checked = usaPersonalizada;

  document.getElementById(
    "fecha_retiro_personalizada",
  ).value = retiro.fecha_retiro_personalizada || "";

  actualizarEstadoFechaPersonalizada();
  actualizarLimiteFechaCuotas();

  if (simulacion.resumen_retiro) {
    mostrarResumenRetiro(
      simulacion.resumen_retiro,
    );
  }
}


// ============================================================
// Estado del formulario
// ============================================================

/**
 * Impide que la fecha de actualización de cuotas quede después
 * de la fecha utilizada para evaluar la simulación.
 */
function actualizarLimiteFechaCuotas() {
  const fechaEvaluacion = document.getElementById(
    "fecha_corte_retiro",
  ).value;

  const fechaCuotas = document.getElementById(
    "fecha_corte_cuotas",
  );

  fechaCuotas.max = fechaEvaluacion || "";

  if (
    fechaEvaluacion
    && fechaCuotas.value
    && fechaCuotas.value > fechaEvaluacion
  ) {
    fechaCuotas.value = fechaEvaluacion;
  }
}


/**
 * Muestra u oculta el campo de fecha de retiro personalizada.
 */
function actualizarEstadoFechaPersonalizada() {
  const activada = document.getElementById(
    "usar_fecha_retiro_personalizada",
  ).checked;

  const contenedor = document.getElementById(
    "contenedor-fecha-retiro-personalizada",
  );

  const campo = document.getElementById(
    "fecha_retiro_personalizada",
  );

  contenedor.classList.toggle(
    "d-none",
    !activada,
  );

  campo.required = activada;

  if (!activada) {
    campo.value = "";
  }
}


/**
 * Invalida el resultado del Paso 5 cuando cambia un dato que
 * participa en el análisis.
 */
function invalidarResumenRetiro() {
  const simulacion = obtenerSimulacion();

  simulacion.resumen_retiro = null;

  guardarSimulacion(simulacion);

  document.getElementById(
    "resultado-retiro",
  ).classList.add("d-none");

  document.getElementById(
    "retiro-advertencias",
  ).classList.add("d-none");

  ocultarErrorRetiro();
}


// ============================================================
// Construcción de la solicitud
// ============================================================

/**
 * Obtiene los años adicionales seleccionados por el usuario.
 * La edad de referencia siempre se envía como escenario base 0.
 *
 * @returns {number[]} Años adicionales ordenados.
 */
function obtenerAniosAdicionalesRetiro() {
  const adicionales = [0];

  document
    .querySelectorAll(".retiro-adicional:checked")
    .forEach((elemento) => {
      adicionales.push(
        Number(elemento.value),
      );
    });

  return adicionales.sort(
    (a, b) => a - b,
  );
}


/**
 * Construye los datos enviados al endpoint de retiro.
 *
 * @returns {Object} Solicitud preparada para FastAPI.
 */
function construirDatosRetiro() {
  const simulacion = obtenerSimulacion();

  const persona = simulacion.persona || {};
  const cuotas = simulacion.cuotas || {};

  if (
    !persona.fecha_nacimiento
    || !persona.sexo
  ) {
    throw new Error(
      "Faltan la fecha de nacimiento o el sexo del Paso 1.",
    );
  }

  if (
    cuotas.cuotas_totales === undefined
    || cuotas.cuotas_anio_actual === undefined
    || cuotas.cuotas_esperadas_cierre_anio === undefined
    || cuotas.continua_cotizando === undefined
    || cuotas.cuotas_esperadas_por_anio === undefined
  ) {
    throw new Error(
      "Faltan datos de cuotas del Paso 2.",
    );
  }

  const fechaEvaluacion = document.getElementById(
    "fecha_corte_retiro",
  ).value;

  const fechaCuotas = document.getElementById(
    "fecha_corte_cuotas",
  ).value;

  if (!fechaEvaluacion || !fechaCuotas) {
    throw new Error(
      "Debes indicar la fecha de evaluación y la fecha de actualización de cuotas.",
    );
  }

  if (fechaCuotas > fechaEvaluacion) {
    throw new Error(
      "La fecha de actualización de cuotas no puede ser posterior a la fecha de evaluación.",
    );
  }

  const usarPersonalizada = document.getElementById(
    "usar_fecha_retiro_personalizada",
  ).checked;

  const fechaPersonalizada = usarPersonalizada
    ? document.getElementById(
      "fecha_retiro_personalizada",
    ).value
    : null;

  if (usarPersonalizada && !fechaPersonalizada) {
    throw new Error(
      "Debes indicar la fecha personalizada de retiro.",
    );
  }

  return {
    fecha_nacimiento: persona.fecha_nacimiento,
    sexo: persona.sexo,
    fecha_corte: fechaEvaluacion,
    fecha_corte_cuotas: fechaCuotas,
    cuotas_reales: Number(
      cuotas.cuotas_totales,
    ),
    cuotas_anio_actual: Number(
      cuotas.cuotas_anio_actual,
    ),
    cuotas_esperadas_cierre_anio: Number(
      cuotas.cuotas_esperadas_cierre_anio,
    ),
    continua_cotizando: Boolean(
      cuotas.continua_cotizando,
    ),
    cuotas_esperadas_por_anio: Number(
      cuotas.cuotas_esperadas_por_anio,
    ),
    anio_fin_proyeccion_salarial:
      simulacion.resumen_proyeccion?.anio_fin
      ?? simulacion.proyeccion?.anio_fin
      ?? null,
    anios_adicionales: obtenerAniosAdicionalesRetiro(),
    fecha_retiro_personalizada: fechaPersonalizada,
  };
}


// ============================================================
// Comunicación con la API
// ============================================================

/**
 * Ejecuta el análisis del Paso 5 y conserva el resultado.
 *
 * @param {SubmitEvent} evento Evento submit del formulario.
 */
async function analizarRetiro(evento) {
  evento.preventDefault();

  const formulario = document.getElementById(
    "form-retiro",
  );

  ocultarErrorRetiro();

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return;
  }

  let datos;

  try {
    datos = construirDatosRetiro();
  } catch (error) {
    mostrarErrorRetiro(
      error.message,
    );
    return;
  }

  try {
    const respuesta = await fetch(
      "/api/simulacion/retiro",
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
      mostrarErrorRetiro(
        obtenerMensajeError(
          contenido,
          "No fue posible analizar los escenarios de retiro.",
        ),
      );
      return;
    }

    const simulacion = obtenerSimulacion();

    simulacion.retiro = datos;
    simulacion.resumen_retiro = contenido;

    guardarSimulacion(simulacion);

    mostrarResumenRetiro(contenido);

  } catch {
    mostrarErrorRetiro(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


// ============================================================
// Presentación de resultados
// ============================================================

/**
 * Muestra el resumen y la tabla de escenarios calculados.
 *
 * @param {Object} resumen Resultado recibido desde FastAPI.
 */
function mostrarResumenRetiro(resumen) {
  document.getElementById(
    "retiro-edad-actual",
  ).textContent = `${resumen.edad_actual_anios} años`;

  document.getElementById(
    "retiro-edad-referencia",
  ).textContent = `${resumen.edad_referencia} años`;

  document.getElementById(
    "retiro-fecha-referencia",
  ).textContent = formatearFechaRetiro(
    resumen.fecha_referencia,
  );

  document.getElementById(
    "retiro-situacion-referencia",
  ).textContent = obtenerTextoSituacionReferencia(
    resumen,
  );

  const contenedorAdvertencias = document.getElementById(
    "retiro-advertencias",
  );

  const textoAdvertencias = document.getElementById(
    "retiro-advertencias-texto",
  );

  const botonAjustar = document.getElementById(
    "btn-ajustar-proyeccion-retiro",
  );

  if (
    Array.isArray(resumen.advertencias)
    && resumen.advertencias.length > 0
  ) {
    textoAdvertencias.replaceChildren();

    resumen.advertencias.forEach(
      (mensaje) => {
        const parrafo = document.createElement("p");
        parrafo.className = "mb-1";
        parrafo.textContent = mensaje;
        textoAdvertencias.appendChild(parrafo);
      },
    );

    contenedorAdvertencias.classList.remove("d-none");

    botonAjustar.classList.toggle(
      "d-none",
      resumen.proyeccion_salarial_cubre_escenarios,
    );

  } else {
    contenedorAdvertencias.classList.add("d-none");
    botonAjustar.classList.add("d-none");
  }

  const cuerpo = document.getElementById(
    "retiro-tabla-body",
  );

  cuerpo.replaceChildren();

  resumen.escenarios.forEach(
    (escenario) => {
      cuerpo.appendChild(
        crearFilaEscenarioRetiro(
          escenario,
        ),
      );
    },
  );

  document.getElementById(
    "retiro-metodo-estimacion",
  ).textContent = resumen.metodo_estimacion_cuotas;

  const resultado = document.getElementById(
    "resultado-retiro",
  );

  resultado.classList.remove("d-none");

  resultado.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}


/**
 * Explica la posición de la persona respecto a la edad de referencia.
 *
 * @param {Object} resumen Resumen devuelto por el backend.
 * @returns {string} Mensaje breve para una tarjeta de resultados.
 */
function obtenerTextoSituacionReferencia(resumen) {
  if (resumen.alcanzo_edad_referencia) {
    const dias = Math.abs(
      Number(resumen.dias_hasta_referencia),
    );

    if (dias === 0) {
      return "Se alcanza hoy";
    }

    return `Alcanzada hace ${dias} días`;
  }

  return `Faltan ${resumen.dias_hasta_referencia} días`;
}


/**
 * Crea una fila de la tabla de escenarios sin utilizar innerHTML.
 *
 * @param {Object} escenario Escenario recibido desde FastAPI.
 * @returns {HTMLTableRowElement} Fila preparada.
 */
function crearFilaEscenarioRetiro(escenario) {
  const fila = document.createElement("tr");

  agregarCeldaRetiro(
    fila,
    escenario.nombre,
    "fw-semibold",
  );

  agregarCeldaRetiro(
    fila,
    formatearFechaRetiro(
      escenario.fecha_retiro,
    ),
  );

  agregarCeldaRetiro(
    fila,
    `${escenario.edad_retiro_anios} años`,
  );

  agregarCeldaRetiro(
    fila,
    escenario.meses_desde_corte_cuotas,
  );

  agregarCeldaRetiro(
    fila,
    escenario.cuotas_estimadas_adicionales,
  );

  agregarCeldaRetiro(
    fila,
    escenario.cuotas_estimadas_totales,
    "fw-bold",
  );

  const estado = document.createElement("td");
  const badge = document.createElement("span");

  badge.className = escenario.fecha_ya_transcurrida
    ? "retirement-status retirement-status-past"
    : "retirement-status retirement-status-future";

  badge.textContent = escenario.fecha_ya_transcurrida
    ? "Fecha transcurrida"
    : "Fecha futura";

  estado.appendChild(badge);
  fila.appendChild(estado);

  return fila;
}


/**
 * Agrega una celda simple a una fila de resultados.
 *
 * @param {HTMLTableRowElement} fila Fila de destino.
 * @param {string|number} valor Contenido visible.
 * @param {string} clase Clase CSS opcional.
 */
function agregarCeldaRetiro(
  fila,
  valor,
  clase = "",
) {
  const celda = document.createElement("td");

  celda.textContent = valor;

  if (clase) {
    celda.className = clase;
  }

  fila.appendChild(celda);
}


/**
 * Amplía el horizonte del Paso 4 hasta el escenario de retiro más lejano.
 *
 * La modificación solo actualiza el año final editable; el usuario debe
 * volver a generar la proyección para confirmar los nuevos resultados.
 */
function ajustarHorizonteProyeccionDesdeRetiro() {
  const simulacion = obtenerSimulacion();

  if (!simulacion.resumen_retiro) {
    return;
  }

  const anioMaximo = Math.max(
    ...simulacion.resumen_retiro.escenarios.map(
      (escenario) => Number(
        escenario.fecha_retiro.slice(0, 4),
      ),
    ),
  );

  const campoAnioFin = document.getElementById(
    "proyeccion_anio_fin",
  );

  campoAnioFin.value = anioMaximo;

  invalidarResumenProyeccion();
  actualizarLimitesSalarioFuturo();
  mostrarPaso(4);

  campoAnioFin.scrollIntoView({
    behavior: "smooth",
    block: "center",
  });
}


// ============================================================
// Errores
// ============================================================

/**
 * Muestra un error del Paso 5.
 *
 * @param {string} mensaje Texto que se presentará al usuario.
 */
function mostrarErrorRetiro(mensaje) {
  const error = document.getElementById(
    "error-retiro",
  );

  error.textContent = mensaje;
  error.classList.remove("d-none");

  error.scrollIntoView({
    behavior: "smooth",
    block: "center",
  });
}


/**
 * Oculta el mensaje de error del Paso 5.
 */
function ocultarErrorRetiro() {
  document.getElementById(
    "error-retiro",
  ).classList.add("d-none");
}


// ============================================================
// Inicialización
// ============================================================

document.addEventListener(
  "DOMContentLoaded",
  () => {
    restaurarDatosRetiro();

    document.getElementById(
      "btn-continuar-paso-5",
    ).addEventListener(
      "click",
      () => {
        const simulacion = obtenerSimulacion();

        if (!simulacion.resumen_proyeccion) {
          mostrarErrorProyeccion(
            "Primero debes generar la proyección salarial.",
          );
          return;
        }

        prepararPasoRetiro();
        mostrarPaso(5);
      },
    );

    document.getElementById(
      "btn-volver-paso-4",
    ).addEventListener(
      "click",
      () => {
        mostrarPaso(4);
      },
    );

    document.getElementById(
      "form-retiro",
    ).addEventListener(
      "submit",
      analizarRetiro,
    );

    document.getElementById(
      "fecha_corte_retiro",
    ).addEventListener(
      "change",
      () => {
        actualizarLimiteFechaCuotas();
        invalidarResumenRetiro();
      },
    );

    document.getElementById(
      "fecha_corte_cuotas",
    ).addEventListener(
      "change",
      invalidarResumenRetiro,
    );

    document.getElementById(
      "usar_fecha_retiro_personalizada",
    ).addEventListener(
      "change",
      () => {
        actualizarEstadoFechaPersonalizada();
        invalidarResumenRetiro();
      },
    );

    document.getElementById(
      "fecha_retiro_personalizada",
    ).addEventListener(
      "change",
      invalidarResumenRetiro,
    );

    document
      .querySelectorAll(".retiro-adicional")
      .forEach((elemento) => {
        elemento.addEventListener(
          "change",
          invalidarResumenRetiro,
        );
      });
  },
);
