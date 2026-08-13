"use strict";


/* ============================================================
   Mi Retiro Proyectado
   Asistente de simulación
   ============================================================ */

/*
 * Este archivo controla la navegación entre los pasos del
 * asistente, el almacenamiento temporal en sessionStorage,
 * la comunicación con la API y la presentación de resultados.
 */


// ============================================================
// Configuración general
// ============================================================

const CLAVE_SIMULACION = "calculadoraPensionCSS.simulacion";

// El año se obtiene dinámicamente del equipo del Asegurado(a).
const ANIO_ACTUAL = new Date().getFullYear();

// Si todavía no existe una proyección guardada, se muestran
// inicialmente cinco años futuros además del año actual.
const ANIOS_PROYECCION_PREDETERMINADOS = 5;

let pasoActual = 1;


// ============================================================
// Almacenamiento temporal
// ============================================================

/**
 * Crea la estructura inicial utilizada para una nueva simulación.
 *
 * @returns {Object} Estado vacío del asistente.
 */
function crearSimulacionVacia() {
  return {
    paso_actual: 1,

    persona: {},
    modo_datos_personales: "MANUAL",
    origen_persona: "MANUAL",

    cuotas: {},
    resumen_cuotas: null,

    modo_historial: "MANUAL",
    historial: null,
    resumen_historial: null,

    referencia_mi_retiro_seguro: null,
    importacion_comprobante_confirmada: false,
    ficha_digital_importada: null,
    importacion_ficha_digital_confirmada: false,

    detalle_anio_actual_habilitado: false,
    detalle_anio_actual: null,
    resumen_detalle_anio_actual: null,
    ultimo_mes_cuotas_derivado: null,

    origen_salario_proyeccion: "MANUAL",
    salario: {},
    resumen_salario: null,

    proyeccion: {},
    resumen_proyeccion: null,
    resumen_linea_tiempo: null,

    retiro: {},
    resumen_retiro: null,
    escenario_retiro_seleccionado: null,

    escenario_salarial_seleccionado: null,
    resultado_sebd_normal: null,
    resultado_sebd_acreditado: null,

    configuracion_mixto_resultados: {},
    resultado_mixto: null,
    resultado_mixto_acreditado: null,

    configuracion_sucgs_resultados: {},
    resultado_sucgs: null,
    resultado_sucgs_acreditado: null,
  };
}


/**
 * Recupera la simulación almacenada temporalmente en la pestaña.
 *
 * Si no existe información válida, devuelve una estructura vacía.
 *
 * @returns {Object} Estado actual de la simulación.
 */
function obtenerSimulacion() {
  const almacenada = sessionStorage.getItem(
    CLAVE_SIMULACION,
  );

  if (!almacenada) {
    return crearSimulacionVacia();
  }

  try {
    const simulacion = JSON.parse(
      almacenada,
    );

    // Se combina la estructura actual con los datos almacenados.
    // Esto permite agregar nuevos campos en versiones posteriores
    // sin romper simulaciones creadas con una estructura anterior.
    return {
      ...crearSimulacionVacia(),
      ...simulacion,

      persona:
        simulacion.persona || {},

      modo_datos_personales:
        simulacion.modo_datos_personales || "MANUAL",

      origen_persona:
        simulacion.origen_persona || "MANUAL",

      cuotas:
        simulacion.cuotas || {},

      modo_historial:
        simulacion.modo_historial || "MANUAL",

      historial:
        simulacion.historial || null,

      detalle_anio_actual:
        simulacion.detalle_anio_actual || null,

      salario:
        simulacion.salario || {},

      proyeccion:
        simulacion.proyeccion || {},

      retiro:
        simulacion.retiro || {},
    };

  } catch {
    // Si sessionStorage contiene información corrupta o no válida,
    // se inicia una simulación nueva.
    return crearSimulacionVacia();
  }
}


/**
 * Guarda temporalmente el estado completo de la simulación.
 *
 * @param {Object} simulacion Estado que debe conservarse.
 */
function guardarSimulacion(simulacion) {
  sessionStorage.setItem(
    CLAVE_SIMULACION,
    JSON.stringify(simulacion),
  );

  if (
    typeof actualizarNavegacionFlotante
    === "function"
  ) {
    actualizarNavegacionFlotante();
  }

  if (
    typeof actualizarNavegacionDirecta
    === "function"
  ) {
    actualizarNavegacionDirecta();
  }
}


// ============================================================
// Navegación del asistente
// ============================================================

/**
 * Muestra un panel del asistente y actualiza su indicador de progreso.
 *
 * @param {number} numeroPaso Número del paso que debe mostrarse.
 */
function mostrarPaso(numeroPaso) {
  pasoActual = numeroPaso;

  // Oculta todos los paneles.
  document
    .querySelectorAll(".wizard-panel")
    .forEach((panel) => {
      panel.classList.add("d-none");
    });

  // Muestra únicamente el panel solicitado.
  const panelActivo = document.querySelector(
    `[data-panel="${numeroPaso}"]`,
  );

  if (panelActivo) {
    panelActivo.classList.remove("d-none");
  }

  // Actualiza la representación gráfica de los pasos.
  document
    .querySelectorAll(".wizard-step")
    .forEach((elemento) => {
      const numero = Number(
        elemento.dataset.step,
      );

      elemento.classList.remove(
        "active",
        "completed",
      );

      if (numero === numeroPaso) {
        elemento.classList.add(
          "active",
        );

      } else if (numero < numeroPaso) {
        elemento.classList.add(
          "completed",
        );
      }
    });

  // Conserva el paso actual para poder restaurarlo después de F5.
  const simulacion = obtenerSimulacion();

  simulacion.paso_actual = numeroPaso;

  guardarSimulacion(simulacion);

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}


// ============================================================
// Paso 1 — Datos personales
// ============================================================

/**
 * Valida y guarda los datos introducidos en el Paso 1.
 *
 * @returns {boolean} true cuando los datos pudieron guardarse.
 */
function guardarDatosPersonales() {
  const formulario = document.getElementById(
    "form-datos-personales",
  );

  const modoDatos = document.querySelector('input[name="modo_datos_personales"]:checked')?.value || "MANUAL";
  const fechaNacimiento = document.getElementById("fecha_nacimiento")?.value || "";
  const sexo = document.getElementById("sexo")?.value || "";
  const sistema = document.getElementById("sistema")?.value || "";
  const error = document.getElementById("error-datos-personales");

  if (!fechaNacimiento || !sexo || !sistema) {
    if (error) {
      error.textContent = modoDatos === "MI_RETIRO_SEGURO"
        ? "El PDF no completó toda la información previsional obligatoria. Abre Revisar datos importados, pulsa Editar campos y completa fecha de nacimiento, sexo y sistema previsional."
        : "Completa fecha de nacimiento, sexo y sistema previsional antes de continuar.";
      error.classList.remove("d-none");
    }
    if (modoDatos === "MANUAL") formulario.reportValidity();
    return false;
  }

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return false;
  }

  if (error) {
    error.classList.add("d-none");
    error.textContent = "";
  }

  const simulacion = obtenerSimulacion();

  const valor = (id) => document.getElementById(id)?.value.trim() || null;
  simulacion.persona = {
    primer_nombre: valor("primer_nombre"),
    segundo_nombre: valor("segundo_nombre"),
    primer_apellido: valor("primer_apellido"),
    segundo_apellido: valor("segundo_apellido"),
    apellido_casada: document.getElementById("sexo").value === "F" ? valor("apellido_casada") : null,
    cedula: valor("cedula"),
    numero_seguro_social: valor("numero_seguro_social"),
    fecha_nacimiento: document.getElementById("fecha_nacimiento").value,
    sexo: document.getElementById("sexo").value,
    fecha_ingreso_css: document.getElementById("fecha_ingreso_css").value || null,
    sistema: document.getElementById("sistema").value,
  };
  simulacion.modo_datos_personales = modoDatos;
  if (modoDatos === "MANUAL") {
    simulacion.origen_persona = "MANUAL";
  }

  // Las fechas de retiro dependen de nacimiento y sexo.
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_sebd_acreditado = null;
  simulacion.configuracion_mixto_resultados = {};
  simulacion.resultado_mixto = null;
  simulacion.resultado_mixto_acreditado = null;
  simulacion.configuracion_sucgs_resultados = {};
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;

  guardarSimulacion(simulacion);

  return true;
}


/**
 * Restaura los datos personales previamente guardados.
 *
 * @param {Object} simulacion Estado actual de la simulación.
 */
function restaurarDatosPersonales(simulacion) {
  const persona = simulacion.persona;

  if (!persona) {
    return;
  }

  [
    "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido",
    "apellido_casada", "cedula", "numero_seguro_social",
  ].forEach((id) => {
    if (persona[id] && document.getElementById(id)) {
      document.getElementById(id).value = persona[id];
    }
  });

  if (persona.fecha_nacimiento) {
    document.getElementById(
      "fecha_nacimiento",
    ).value = persona.fecha_nacimiento;
  }

  if (persona.sexo) {
    document.getElementById(
      "sexo",
    ).value = persona.sexo;
  }

  if (persona.fecha_ingreso_css) {
    document.getElementById(
      "fecha_ingreso_css",
    ).value = persona.fecha_ingreso_css;
  }

  if (persona.sistema) {
    document.getElementById(
      "sistema",
    ).value = persona.sistema;
  }

  if (typeof actualizarApellidoCasada === "function") {
    actualizarApellidoCasada();
  }
  if (typeof restaurarModoDatosPersonales === "function") {
    restaurarModoDatosPersonales(simulacion);
  }
}


// ============================================================
// Paso 2 — Cuotas
// ============================================================

/**
 * Activa o desactiva los campos de proyección de cuotas según
 * la decisión del Asegurado(a) de continuar o no cotizando.
 */
function actualizarEstadoContinuidad() {
  const continua = document.getElementById(
    "continua_cotizando",
  ).value;

  const cuotasActuales = Number(
    document.getElementById(
      "cuotas_anio_actual",
    ).value || 0,
  );

  const cierre = document.getElementById(
    "cuotas_esperadas_cierre_anio",
  );

  const futuras = document.getElementById(
    "cuotas_esperadas_por_anio",
  );

  if (continua === "false") {
    // Si no continuará cotizando, las cuotas futuras se anulan.
    cierre.value = cuotasActuales;
    futuras.value = 0;

    cierre.disabled = true;
    futuras.disabled = true;

  } else {
    cierre.disabled = false;
    futuras.disabled = false;

    // Si todavía no existe un valor válido, se utiliza
    // como referencia un máximo de doce cuotas por año.
    if (
      !cierre.value ||
      Number(cierre.value) < cuotasActuales
    ) {
      cierre.value = 12;
    }

    if (
      !futuras.value ||
      Number(futuras.value) === 0
    ) {
      futuras.value = 12;
    }
  }
}


/**
 * Restaura los datos y el resultado del análisis de cuotas.
 *
 * @param {Object} simulacion Estado actual de la simulación.
 */
function restaurarDatosCuotas(simulacion) {
  const cuotas = simulacion.cuotas;

  if (!cuotas) {
    return;
  }

  if (
    cuotas.cuotas_totales !== undefined
  ) {
    document.getElementById(
      "cuotas_totales",
    ).value = cuotas.cuotas_totales;
  }

  if (
    cuotas.cuotas_anio_actual !== undefined
  ) {
    document.getElementById(
      "cuotas_anio_actual",
    ).value = cuotas.cuotas_anio_actual;
  }

  if (
    cuotas.continua_cotizando !== undefined
  ) {
    document.getElementById(
      "continua_cotizando",
    ).value = String(
      cuotas.continua_cotizando,
    );
  }

  if (
    cuotas.cuotas_esperadas_cierre_anio
    !== undefined
  ) {
    document.getElementById(
      "cuotas_esperadas_cierre_anio",
    ).value =
      cuotas.cuotas_esperadas_cierre_anio;
  }

  if (
    cuotas.cuotas_esperadas_por_anio
    !== undefined
  ) {
    document.getElementById(
      "cuotas_esperadas_por_anio",
    ).value =
      cuotas.cuotas_esperadas_por_anio;
  }

  actualizarEstadoContinuidad();

  if (simulacion.resumen_cuotas) {
    mostrarResumenCuotas(
      simulacion.resumen_cuotas,
    );
  }
}


/**
 * Elimina el resultado de cuotas cuando el Asegurado(a) modifica
 * alguno de los datos que sirvieron para calcularlo.
 */
function invalidarResumenCuotas() {
  const simulacion = obtenerSimulacion();

  simulacion.resumen_cuotas = null;

  // El historial se conserva, pero debe volver a validarse porque
  // utiliza el total real de cuotas del Paso 2 como referencia.
  simulacion.resumen_historial = null;
  simulacion.resumen_detalle_anio_actual = null;
  simulacion.ultimo_mes_cuotas_derivado = null;

  // Los resultados de etapas posteriores también dejan de ser
  // completamente confiables hasta volver a analizar las cuotas.
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_sebd_acreditado = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_mixto_acreditado = null;
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;

  guardarSimulacion(simulacion);

  if (typeof liberarSalarioAnualActual === "function") {
    liberarSalarioAnualActual();
  }

  if (typeof actualizarOpcionesBaseSalarial === "function") {
    actualizarOpcionesBaseSalarial(false);
  }

  document.getElementById(
    "resultado-cuotas",
  ).classList.add("d-none");

  const resultadoHistorial = document.getElementById(
    "resultado-historial",
  );

  if (resultadoHistorial) {
    resultadoHistorial.classList.add("d-none");
  }

  document.getElementById(
    "resultado-proyeccion",
  ).classList.add("d-none");
}


/**
 * Envía las cuotas al backend, guarda el resultado y actualiza
 * el resumen mostrado al Asegurado(a).
 *
 * @param {SubmitEvent} evento Evento submit del formulario.
 */
async function analizarCuotas(evento) {
  evento.preventDefault();

  const formulario = document.getElementById(
    "form-cuotas",
  );

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return;
  }

  const continua = (
    document.getElementById(
      "continua_cotizando",
    ).value === "true"
  );

  const cuotasAnioActual = Number(
    document.getElementById(
      "cuotas_anio_actual",
    ).value,
  );

  const datos = {
    cuotas_totales: Number(
      document.getElementById(
        "cuotas_totales",
      ).value,
    ),

    cuotas_anio_actual:
      cuotasAnioActual,

    continua_cotizando:
      continua,

    cuotas_esperadas_cierre_anio:
      continua
        ? Number(
            document.getElementById(
              "cuotas_esperadas_cierre_anio",
            ).value,
          )
        : cuotasAnioActual,

    cuotas_esperadas_por_anio:
      continua
        ? Number(
            document.getElementById(
              "cuotas_esperadas_por_anio",
            ).value,
          )
        : 0,
  };

  ocultarErrorCuotas();

  try {
    const respuesta = await fetch(
      "/api/simulacion/cuotas",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(datos),
      },
    );

    const contenido =
      await respuesta.json();

    if (!respuesta.ok) {
      const mensaje = obtenerMensajeError(
        contenido,
        "No fue posible analizar las cuotas.",
      );

      mostrarErrorCuotas(mensaje);
      return;
    }

    const simulacion = obtenerSimulacion();

    simulacion.cuotas = datos;
    simulacion.resumen_cuotas = contenido;

    if (simulacion.detalle_anio_actual_habilitado) {
      simulacion.resumen_detalle_anio_actual = null;
      simulacion.ultimo_mes_cuotas_derivado = null;
    }

    guardarSimulacion(simulacion);

    if (simulacion.detalle_anio_actual_habilitado) {
      if (typeof liberarSalarioAnualActual === "function") {
        liberarSalarioAnualActual();
      }
      if (typeof actualizarOpcionesBaseSalarial === "function") {
        actualizarOpcionesBaseSalarial(false);
      }
    }

    mostrarResumenCuotas(
      contenido,
    );

  } catch {
    mostrarErrorCuotas(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


/**
 * Muestra en la interfaz el resultado preliminar de cuotas.
 *
 * @param {Object} resumen Respuesta obtenida desde la API.
 */
function mostrarResumenCuotas(resumen) {
  document.getElementById(
    "resultado-cuotas",
  ).classList.remove("d-none");

  document.getElementById(
    "resultado-cuotas-reales",
  ).textContent =
    resumen.cuotas_reales;

  document.getElementById(
    "resultado-cuotas-cierre",
  ).textContent =
    resumen.cuotas_proyectadas_cierre_anio;

  document.getElementById(
    "resultado-faltantes-180",
  ).textContent =
    resumen.faltantes_180;

  document.getElementById(
    "resultado-faltantes-240",
  ).textContent =
    resumen.faltantes_240;

  document.getElementById(
    "resultado-tiempo-180",
  ).textContent = formatearTiempo(
    resumen.anios_aprox_180,
  );

  document.getElementById(
    "resultado-tiempo-240",
  ).textContent = formatearTiempo(
    resumen.anios_aprox_240,
  );
}


/**
 * Muestra un mensaje de error en el Paso 2.
 *
 * @param {string} mensaje Texto que se mostrará al Asegurado(a).
 */
function mostrarErrorCuotas(mensaje) {
  const error = document.getElementById(
    "error-cuotas",
  );

  error.textContent = mensaje;
  error.classList.remove("d-none");
}


/**
 * Oculta cualquier mensaje de error existente en el Paso 2.
 */
function ocultarErrorCuotas() {
  document.getElementById(
    "error-cuotas",
  ).classList.add("d-none");
}


// ============================================================
// Paso 3 — Salario
// ============================================================

/**
 * Restaura el salario introducido y sus equivalencias calculadas.
 *
 * @param {Object} simulacion Estado actual de la simulación.
 */
function restaurarDatosSalario(simulacion) {
  const salario = simulacion.salario;

  if (!salario) {
    return;
  }

  if (salario.monto !== undefined) {
    const campoMonto = document.getElementById(
      "monto_salario",
    );

    campoMonto.value = formatearNumeroMonetario(
      salario.monto,
    );
  }

  if (salario.periodicidad) {
    document.getElementById(
      "periodicidad_salario",
    ).value = salario.periodicidad;
  }

  if (simulacion.resumen_salario) {
    mostrarResumenSalario(
      simulacion.resumen_salario,
    );
  }
}


/**
 * Elimina el resultado salarial y la proyección posterior cuando
 * el Asegurado(a) modifica el salario del Paso 3.
 */
function invalidarResumenSalario() {
  const simulacion = obtenerSimulacion();

  simulacion.resumen_salario = null;
  simulacion.proyeccion = {};
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_sebd_acreditado = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_mixto_acreditado = null;
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;

  guardarSimulacion(simulacion);

  document.getElementById(
    "resultado-salario",
  ).classList.add("d-none");

  document.getElementById(
    "resultado-proyeccion",
  ).classList.add("d-none");
}


/**
 * Normaliza el salario mediante la API y conserva el resultado
 * dentro de la simulación temporal.
 *
 * @param {SubmitEvent} evento Evento submit del formulario.
 */
async function analizarSalario(evento) {
  evento.preventDefault();

  const formulario = document.getElementById(
    "form-salario",
  );

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return;
  }

  const datos = {
    monto: obtenerValorMonetario(
      document.getElementById(
        "monto_salario",
      ).value,
    ),

    periodicidad:
      document.getElementById(
        "periodicidad_salario",
      ).value,
  };

  if (
    !Number.isFinite(datos.monto)
    || datos.monto <= 0
  ) {
    mostrarErrorSalario(
      "El salario debe ser un monto mayor que cero y admite como máximo dos decimales.",
    );
    return;
  }

  ocultarErrorSalario();

  try {
    const respuesta = await fetch(
      "/api/simulacion/salario",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(datos),
      },
    );

    const contenido =
      await respuesta.json();

    if (!respuesta.ok) {
      const mensaje = obtenerMensajeError(
        contenido,
        "No fue posible analizar el salario.",
      );

      mostrarErrorSalario(mensaje);
      return;
    }

    const simulacion = obtenerSimulacion();

    simulacion.salario = datos;
    simulacion.resumen_salario = contenido;
    simulacion.origen_salario_proyeccion = (
      document.getElementById("origen_salario_proyeccion")?.value
      || "MANUAL"
    );

    // Una nueva normalización salarial invalida cualquier
    // proyección construida con un salario anterior.
    simulacion.proyeccion = {};
    simulacion.resumen_proyeccion = null;
    simulacion.resumen_linea_tiempo = null;
    simulacion.retiro = {};
    simulacion.resumen_retiro = null;
    simulacion.escenario_retiro_seleccionado = null;
    simulacion.escenario_salarial_seleccionado = null;
    simulacion.resultado_sebd_normal = null;
    simulacion.resultado_sebd_acreditado = null;
    simulacion.resultado_mixto = null;
    simulacion.resultado_mixto_acreditado = null;
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;

    guardarSimulacion(simulacion);

    mostrarResumenSalario(
      contenido,
    );

  } catch {
    mostrarErrorSalario(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


/**
 * Muestra las equivalencias salariales devueltas por el backend.
 *
 * @param {Object} resumen Resultado de normalización salarial.
 */
function mostrarResumenSalario(resumen) {
  document.getElementById(
    "resultado-salario",
  ).classList.remove("d-none");

  document.getElementById(
    "salario-semanal",
  ).textContent = formatearMoneda(
    resumen.salario_semanal,
  );

  document.getElementById(
    "salario-quincenal",
  ).textContent = formatearMoneda(
    resumen.salario_quincenal,
  );

  document.getElementById(
    "salario-mensual",
  ).textContent = formatearMoneda(
    resumen.salario_mensual,
  );

  document.getElementById(
    "salario-anual",
  ).textContent = formatearMoneda(
    resumen.salario_anual,
  );
}


/**
 * Muestra un mensaje de error en el Paso 3.
 *
 * @param {string} mensaje Texto que se mostrará al Asegurado(a).
 */
function mostrarErrorSalario(mensaje) {
  const error = document.getElementById(
    "error-salario",
  );

  error.textContent = mensaje;
  error.classList.remove("d-none");
}


/**
 * Oculta cualquier mensaje de error existente en el Paso 3.
 */
function ocultarErrorSalario() {
  document.getElementById(
    "error-salario",
  ).classList.add("d-none");
}


// ============================================================
// Paso 4 — Proyección salarial
// ============================================================

/**
 * Configura los valores iniciales del Paso 4 utilizando el salario
 * normalizado en el Paso 3 y el año calendario actual.
 *
 * @param {Object} simulacion Estado actual de la simulación.
 */
function prepararPasoProyeccion(simulacion) {
  const resumenSalario =
    simulacion.resumen_salario;

  if (!resumenSalario) {
    return;
  }

  // El salario base del Paso 4 nunca se escribe manualmente.
  document.getElementById(
    "proyeccion-salario-base",
  ).textContent = formatearMoneda(
    resumenSalario.salario_mensual,
  );

  const notaBase = document.querySelector(
    ".projection-base-note",
  );

  if (notaBase) {
    const origen = simulacion.origen_salario_proyeccion || "MANUAL";
    const resumenDetalle = simulacion.resumen_detalle_anio_actual;

    notaBase.textContent = (
      typeof descripcionOrigenBaseSalarial === "function"
        ? descripcionOrigenBaseSalarial(origen, resumenDetalle)
        : "Obtenido automáticamente del Paso 3"
    );
  }

  const campoInicio = document.getElementById(
    "proyeccion_anio_inicio",
  );

  const campoFin = document.getElementById(
    "proyeccion_anio_fin",
  );

  campoInicio.value = ANIO_ACTUAL;

  // Impide seleccionar un año final anterior al actual.
  campoFin.min = ANIO_ACTUAL;

  // Si todavía no existe un valor, se proyectan inicialmente
  // cinco años futuros.
  if (!campoFin.value) {
    campoFin.value = (
      ANIO_ACTUAL
      + ANIOS_PROYECCION_PREDETERMINADOS
    );
  }

  actualizarLimitesSalarioFuturo();
}


/**
 * Restaura la configuración y el resultado del Paso 4.
 *
 * @param {Object} simulacion Estado actual de la simulación.
 */
function restaurarDatosProyeccion(simulacion) {
  prepararPasoProyeccion(
    simulacion,
  );

  const proyeccion =
    simulacion.proyeccion;

  if (
    !proyeccion ||
    Object.keys(proyeccion).length === 0
  ) {
    actualizarConfiguracionProyeccion();
    return;
  }

  document.getElementById(
    "proyeccion_anio_inicio",
  ).value =
    proyeccion.anio_inicio
    || ANIO_ACTUAL;

  if (
    proyeccion.anio_fin !== undefined
  ) {
    document.getElementById(
      "proyeccion_anio_fin",
    ).value =
      proyeccion.anio_fin;
  }

  if (proyeccion.modalidad) {
    document.getElementById(
      "modalidad_proyeccion",
    ).value =
      proyeccion.modalidad;
  }

  if (
    proyeccion.porcentaje_anual
    !== null
    && proyeccion.porcentaje_anual
    !== undefined
  ) {
    document.getElementById(
      "porcentaje_anual",
    ).value =
      proyeccion.porcentaje_anual;
  }

  if (
    proyeccion.salario_mensual_futuro
    !== null
    && proyeccion.salario_mensual_futuro
    !== undefined
  ) {
    document.getElementById(
      "salario_mensual_futuro",
    ).value = formatearNumeroMonetario(
      proyeccion.salario_mensual_futuro,
    );
  }

  if (
    proyeccion.anio_salario_futuro
    !== null
    && proyeccion.anio_salario_futuro
    !== undefined
  ) {
    document.getElementById(
      "anio_salario_futuro",
    ).value =
      proyeccion.anio_salario_futuro;
  }

  if (
    Array.isArray(
      proyeccion.escenarios_porcentajes,
    )
  ) {
    document.getElementById(
      "escenarios_porcentajes",
    ).value =
      proyeccion.escenarios_porcentajes.join(
        ", ",
      );
  }

  actualizarLimitesSalarioFuturo();
  actualizarConfiguracionProyeccion();

  if (simulacion.resumen_proyeccion) {
    mostrarResumenProyeccion(
      simulacion.resumen_proyeccion,
    );
  }
}


/**
 * Muestra únicamente los campos correspondientes a la modalidad
 * de proyección seleccionada.
 */
function actualizarConfiguracionProyeccion() {
  const modalidad = document.getElementById(
    "modalidad_proyeccion",
  ).value;

  const bloquePorcentaje =
    document.getElementById(
      "config-proyeccion-porcentaje",
    );

  const bloqueFuturo =
    document.getElementById(
      "config-proyeccion-futuro",
    );

  const bloqueEscenarios =
    document.getElementById(
      "config-proyeccion-escenarios",
    );

  const porcentaje =
    document.getElementById(
      "porcentaje_anual",
    );

  const salarioFuturo =
    document.getElementById(
      "salario_mensual_futuro",
    );

  const anioFuturo =
    document.getElementById(
      "anio_salario_futuro",
    );

  const escenarios =
    document.getElementById(
      "escenarios_porcentajes",
    );

  // Primero se ocultan todas las configuraciones adicionales.
  bloquePorcentaje.classList.add(
    "d-none",
  );

  bloqueFuturo.classList.add(
    "d-none",
  );

  bloqueEscenarios.classList.add(
    "d-none",
  );

  // También se eliminan requisitos HTML que no correspondan
  // a la modalidad activa.
  porcentaje.required = false;
  salarioFuturo.required = false;
  anioFuturo.required = false;
  escenarios.required = false;


  if (modalidad === "PORCENTAJE") {
    bloquePorcentaje.classList.remove(
      "d-none",
    );

    porcentaje.required = true;

  } else if (
    modalidad === "FUTURO_CONOCIDO"
  ) {
    bloqueFuturo.classList.remove(
      "d-none",
    );

    salarioFuturo.required = true;
    anioFuturo.required = true;

  } else if (
    modalidad === "ESCENARIOS"
  ) {
    bloqueEscenarios.classList.remove(
      "d-none",
    );

    escenarios.required = true;
  }
}


/**
 * Actualiza los límites permitidos para el año del salario futuro
 * en función del período general de proyección.
 */
function actualizarLimitesSalarioFuturo() {
  const inicio = Number(
    document.getElementById(
      "proyeccion_anio_inicio",
    ).value || ANIO_ACTUAL,
  );

  const fin = Number(
    document.getElementById(
      "proyeccion_anio_fin",
    ).value || (
      ANIO_ACTUAL
      + ANIOS_PROYECCION_PREDETERMINADOS
    ),
  );

  const campo = document.getElementById(
    "anio_salario_futuro",
  );

  campo.min = inicio + 1;
  campo.max = fin;
}


/**
 * Convierte el texto utilizado para comparar escenarios en una
 * lista numérica de porcentajes.
 *
 * Se admiten comas o punto y coma como separadores.
 *
 * @param {string} texto Porcentajes escritos por el Asegurado(a).
 * @returns {number[]} Lista de porcentajes.
 */
function convertirEscenariosPorcentajes(texto) {
  const partes = texto
    .split(/[,;]/)
    .map((valor) => valor.trim())
    .filter((valor) => valor !== "");

  if (partes.length === 0) {
    throw new Error(
      "Debes indicar al menos un porcentaje para comparar.",
    );
  }

  const formatoInvalido = partes.some(
    (valor) => !/^-?\d+(?:\.\d{1,2})?$/.test(
      valor,
    ),
  );

  if (formatoInvalido) {
    throw new Error(
      "Cada porcentaje admite como máximo dos decimales.",
    );
  }

  const porcentajes = partes.map(
    (valor) => Number(valor),
  );

  const contieneValorInvalido =
    porcentajes.some(
      (valor) => (
        !Number.isFinite(valor)
        || valor <= -100
        || valor > 100
      ),
    );

  if (contieneValorInvalido) {
    throw new Error(
      "Los porcentajes deben ser números mayores que -100 y "
      + "menores o iguales que 100.",
    );
  }

  return porcentajes;
}


/**
 * Elimina la proyección calculada cuando se modifica alguno de
 * los parámetros utilizados para construirla.
 */
function invalidarResumenProyeccion() {
  const simulacion =
    obtenerSimulacion();

  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_sebd_acreditado = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_mixto_acreditado = null;
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;

  guardarSimulacion(
    simulacion,
  );

  document.getElementById(
    "resultado-proyeccion",
  ).classList.add("d-none");
}


/**
 * Construye los datos del Paso 4, llama al backend y conserva
 * la proyección obtenida.
 *
 * @param {SubmitEvent} evento Evento submit del formulario.
 */
async function analizarProyeccion(evento) {
  evento.preventDefault();

  const formulario = document.getElementById(
    "form-proyeccion",
  );

  actualizarConfiguracionProyeccion();

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return;
  }

  const simulacion =
    obtenerSimulacion();

  if (!simulacion.resumen_salario) {
    mostrarErrorProyeccion(
      "Primero debes analizar el salario en el Paso 3.",
    );

    return;
  }

  const modalidad =
    document.getElementById(
      "modalidad_proyeccion",
    ).value;

  let escenariosPorcentajes = [
    0,
    1,
    2,
    3,
  ];

  if (modalidad === "ESCENARIOS") {
    try {
      escenariosPorcentajes =
        convertirEscenariosPorcentajes(
          document.getElementById(
            "escenarios_porcentajes",
          ).value,
        );

    } catch (error) {
      mostrarErrorProyeccion(
        error.message,
      );

      return;
    }
  }

  const datos = {
    salario_mensual_actual: Number(
      simulacion.resumen_salario
        .salario_mensual,
    ),

    anio_inicio: Number(
      document.getElementById(
        "proyeccion_anio_inicio",
      ).value,
    ),

    anio_fin: Number(
      document.getElementById(
        "proyeccion_anio_fin",
      ).value,
    ),

    modalidad: modalidad,

    porcentaje_anual:
      modalidad === "PORCENTAJE"
        ? Number(
            document.getElementById(
              "porcentaje_anual",
            ).value,
          )
        : null,

    salario_mensual_futuro:
      modalidad === "FUTURO_CONOCIDO"
        ? obtenerValorMonetario(
            document.getElementById(
              "salario_mensual_futuro",
            ).value,
          )
        : null,

    anio_salario_futuro:
      modalidad === "FUTURO_CONOCIDO"
        ? Number(
            document.getElementById(
              "anio_salario_futuro",
            ).value,
          )
        : null,

    escenarios_porcentajes:
      escenariosPorcentajes,
  };

  ocultarErrorProyeccion();

  try {
    const respuesta = await fetch(
      "/api/simulacion/proyeccion-salario",
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
      const mensaje = obtenerMensajeError(
        contenido,
        "No fue posible generar la proyección salarial.",
      );

      mostrarErrorProyeccion(
        mensaje,
      );

      return;
    }

    simulacion.proyeccion =
      datos;

    simulacion.resumen_proyeccion =
      contenido;

    // La línea temporal depende de esta proyección. Se elimina
    // cualquier resultado anterior antes de reconstruirla.
    simulacion.resumen_linea_tiempo = null;
    simulacion.retiro = {};
    simulacion.resumen_retiro = null;
    simulacion.escenario_retiro_seleccionado = null;
    simulacion.escenario_salarial_seleccionado = null;
    simulacion.resultado_sebd_normal = null;
    simulacion.resultado_sebd_acreditado = null;
    simulacion.resultado_mixto = null;
    simulacion.resultado_mixto_acreditado = null;
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;

    guardarSimulacion(
      simulacion,
    );

    // Cuando existe historial validado, la interfaz combina
    // información histórica y futura. En modo simplificado se
    // mantiene la tabla de proyección salarial tradicional.
    if (typeof generarLineaTiempo === "function") {
      await generarLineaTiempo(
        datos,
        contenido,
      );
    } else {
      mostrarResumenProyeccion(
        contenido,
      );
    }

  } catch {
    mostrarErrorProyeccion(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


/**
 * Muestra todos los escenarios salariales generados por el backend.
 *
 * @param {Object} resumen Resultado completo de la proyección.
 */
function mostrarResumenProyeccion(resumen) {
  const resultado =
    document.getElementById(
      "resultado-proyeccion",
    );

  const contenedor =
    document.getElementById(
      "contenedor-escenarios",
    );

  contenedor.replaceChildren();

  resumen.escenarios.forEach(
    (escenario) => {
      contenedor.appendChild(
        crearTablaEscenario(
          escenario,
        ),
      );
    },
  );

  resultado.classList.remove(
    "d-none",
  );
}


/**
 * Construye visualmente una tabla para un escenario salarial.
 *
 * Los elementos se crean mediante la API del DOM para evitar
 * insertar directamente contenido recibido mediante innerHTML.
 *
 * @param {Object} escenario Escenario devuelto por el backend.
 * @returns {HTMLElement} Contenedor completo del escenario.
 */
function crearTablaEscenario(escenario) {
  const seccion = document.createElement(
    "section",
  );

  seccion.className =
    "projection-scenario";


  // ----------------------------------------------------------
  // Encabezado del escenario
  // ----------------------------------------------------------

  const encabezado =
    document.createElement("div");

  encabezado.className =
    "projection-scenario-header";

  const titulo =
    document.createElement("h4");

  titulo.className =
    "projection-scenario-title";

  titulo.textContent =
    escenario.nombre;

  const tasa =
    document.createElement("span");

  tasa.className =
    "projection-rate";

  tasa.textContent = (
    `Tasa anual: ${
      formatearPorcentaje(
        escenario.tasa_anual_pct,
      )
    }`
  );

  encabezado.append(
    titulo,
    tasa,
  );


  // ----------------------------------------------------------
  // Contenedor adaptable de la tabla
  // ----------------------------------------------------------

  const tablaResponsive =
    document.createElement("div");

  tablaResponsive.className =
    "table-responsive";

  const tabla =
    document.createElement("table");

  tabla.className =
    "table table-hover projection-table align-middle";


  // ----------------------------------------------------------
  // Encabezados de la tabla
  // ----------------------------------------------------------

  const thead =
    document.createElement("thead");

  const filaEncabezado =
    document.createElement("tr");

  [
    "Año",
    "Salario mensual",
    "Salario anual",
    "Crecimiento desde base",
  ].forEach((texto) => {
    const th =
      document.createElement("th");

    th.scope = "col";
    th.textContent = texto;

    filaEncabezado.appendChild(
      th,
    );
  });

  thead.appendChild(
    filaEncabezado,
  );


  // ----------------------------------------------------------
  // Registros anuales
  // ----------------------------------------------------------

  const tbody =
    document.createElement("tbody");

  escenario.registros.forEach(
    (registro) => {
      const fila =
        document.createElement("tr");

      const celdaAnio =
        document.createElement("td");

      celdaAnio.textContent =
        registro.anio;


      const celdaMensual =
        document.createElement("td");

      celdaMensual.textContent =
        formatearMoneda(
          registro.salario_mensual,
        );


      const celdaAnual =
        document.createElement("td");

      celdaAnual.textContent =
        formatearMoneda(
          registro.salario_anual,
        );


      const celdaCrecimiento =
        document.createElement("td");

      celdaCrecimiento.textContent =
        formatearPorcentaje(
          registro
            .crecimiento_desde_base_pct,
        );

      fila.append(
        celdaAnio,
        celdaMensual,
        celdaAnual,
        celdaCrecimiento,
      );

      tbody.appendChild(
        fila,
      );
    },
  );


  tabla.append(
    thead,
    tbody,
  );

  tablaResponsive.appendChild(
    tabla,
  );

  seccion.append(
    encabezado,
    tablaResponsive,
  );

  return seccion;
}


/**
 * Muestra un mensaje de error en el Paso 4.
 *
 * @param {string} mensaje Texto que se mostrará al Asegurado(a).
 */
function mostrarErrorProyeccion(mensaje) {
  const error = document.getElementById(
    "error-proyeccion",
  );

  error.textContent = mensaje;
  error.classList.remove("d-none");
}


/**
 * Oculta cualquier mensaje de error existente en el Paso 4.
 */
function ocultarErrorProyeccion() {
  document.getElementById(
    "error-proyeccion",
  ).classList.add("d-none");
}


// ============================================================
// Formateadores
// ============================================================

/**
 * Convierte una cantidad decimal de años en un texto legible.
 *
 * @param {number|null} anios Cantidad aproximada de años.
 * @returns {string} Representación en años y meses.
 */
function formatearTiempo(anios) {
  if (anios === null) {
    return (
      "No alcanzable con "
      + "la proyección actual"
    );
  }

  if (anios === 0) {
    return "Requisito alcanzado";
  }

  const meses = Math.round(
    anios * 12,
  );

  const aniosCompletos =
    Math.floor(
      meses / 12,
    );

  const mesesRestantes =
    meses % 12;

  const partes = [];

  if (aniosCompletos > 0) {
    partes.push(
      `${aniosCompletos} ${
        aniosCompletos === 1
          ? "año"
          : "años"
      }`,
    );
  }

  if (mesesRestantes > 0) {
    partes.push(
      `${mesesRestantes} ${
        mesesRestantes === 1
          ? "mes"
          : "meses"
      }`,
    );
  }

  return partes.join(
    " y ",
  );
}


/**
 * Formatea un valor numérico como moneda panameña.
 *
 * @param {number} valor Monto que debe mostrarse.
 * @returns {string} Valor con prefijo B/. y dos decimales.
 */
function formatearMoneda(valor) {
  const numero = Number(
    valor,
  );

  return `B/.${numero.toLocaleString(
    "es-PA",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  )}`;
}


/**
 * Formatea un porcentaje eliminando decimales innecesarios.
 *
 * @param {number} valor Porcentaje que debe mostrarse.
 * @returns {string} Porcentaje formateado.
 */
function formatearPorcentaje(valor) {
  const numero = Number(
    valor,
  );

  return `${numero.toLocaleString(
    "es-PA",
    {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    },
  )} %`;
}


// ============================================================
// Manejo genérico de errores de la API
// ============================================================

/**
 * Extrae un mensaje legible de una respuesta de error de FastAPI.
 *
 * @param {Object} contenido Respuesta recibida desde la API.
 * @param {string} mensajePredeterminado Mensaje alternativo.
 * @returns {string} Mensaje que se mostrará al Asegurado(a).
 */
function obtenerMensajeError(
  contenido,
  mensajePredeterminado,
) {
  if (!contenido) {
    return mensajePredeterminado;
  }

  if (
    typeof contenido.detail
    === "string"
  ) {
    return contenido.detail;
  }

  if (
    Array.isArray(
      contenido.detail,
    )
  ) {
    return contenido.detail
      .map(
        (error) => error.msg,
      )
      .join(" ");
  }

  return mensajePredeterminado;
}


// ============================================================
// Inicialización del asistente
// ============================================================

document.addEventListener(
  "DOMContentLoaded",
  () => {
    configurarCampoDecimal(
      document.getElementById(
        "porcentaje_anual",
      ),
      true,
    );

    const simulacion =
      obtenerSimulacion();


    // --------------------------------------------------------
    // Restauración de información
    // --------------------------------------------------------

    restaurarDatosPersonales(
      simulacion,
    );

    restaurarDatosCuotas(
      simulacion,
    );

    restaurarDatosSalario(
      simulacion,
    );

    restaurarDatosProyeccion(
      simulacion,
    );


    // --------------------------------------------------------
    // Restaurar paso actual
    // --------------------------------------------------------

    const pasoGuardado = Number(
      simulacion.paso_actual || 1,
    );

    mostrarPaso(
      pasoGuardado >= 1
      && pasoGuardado <= 6
        ? pasoGuardado
        : 1,
    );


    // ========================================================
    // Paso 1
    // ========================================================

    document.getElementById(
      "form-datos-personales",
    ).addEventListener(
      "submit",
      (evento) => {
        evento.preventDefault();

        if (
          guardarDatosPersonales()
        ) {
          mostrarPaso(2);
        }
      },
    );


    // ========================================================
    // Paso 2
    // ========================================================

    document.getElementById(
      "form-cuotas",
    ).addEventListener(
      "submit",
      analizarCuotas,
    );


    document.getElementById(
      "btn-volver-paso-1",
    ).addEventListener(
      "click",
      () => {
        mostrarPaso(1);
      },
    );


    document.getElementById(
      "btn-continuar-paso-3",
    ).addEventListener(
      "click",
      () => {
        const simulacionActual =
          obtenerSimulacion();

        if (
          !simulacionActual
            .resumen_cuotas
        ) {
          mostrarErrorCuotas(
            "Primero debes analizar las cuotas.",
          );

          return;
        }

        // El historial se vuelve a sincronizar aquí porque la fecha
        // de ingreso y las cuotas se introducen después de cargar la página.
        if (
          typeof sincronizarHistorialConDatosActuales === "function"
        ) {
          sincronizarHistorialConDatosActuales();
        }

        mostrarPaso(3);
      },
    );


    document.getElementById(
      "continua_cotizando",
    ).addEventListener(
      "change",
      () => {
        actualizarEstadoContinuidad();
        invalidarResumenCuotas();
      },
    );


    document.getElementById(
      "cuotas_anio_actual",
    ).addEventListener(
      "input",
      () => {
        actualizarEstadoContinuidad();
        invalidarResumenCuotas();
      },
    );


    [
      "cuotas_totales",
      "cuotas_esperadas_cierre_anio",
      "cuotas_esperadas_por_anio",
    ].forEach((id) => {
      document.getElementById(
        id,
      ).addEventListener(
        "input",
        invalidarResumenCuotas,
      );
    });


    // ========================================================
    // Paso 3
    // ========================================================

    document.getElementById(
      "form-salario",
    ).addEventListener(
      "submit",
      analizarSalario,
    );


    document.getElementById(
      "btn-volver-paso-2",
    ).addEventListener(
      "click",
      () => {
        mostrarPaso(2);
      },
    );


    document.getElementById(
      "btn-continuar-paso-4",
    ).addEventListener(
      "click",
      () => {
        const simulacionActual =
          obtenerSimulacion();

        const modoHistorial =
          simulacionActual.modo_historial || "MANUAL";

        if (
          modoHistorial === "MANUAL"
          && !simulacionActual.resumen_historial
        ) {
          const errorHistorial = document.getElementById(
            "error-historial",
          );

          if (errorHistorial) {
            errorHistorial.textContent =
              "Primero debes analizar el historial salarial.";
            errorHistorial.classList.remove("d-none");
            errorHistorial.scrollIntoView({
              behavior: "smooth",
              block: "center",
            });
          }

          return;
        }

        if (
          !simulacionActual
            .resumen_salario
        ) {
          mostrarErrorSalario(
            "Primero debes analizar el salario actual.",
          );

          return;
        }

        prepararPasoProyeccion(
          simulacionActual,
        );

        mostrarPaso(4);
      },
    );


    document.getElementById(
      "monto_salario",
    ).addEventListener(
      "input",
      invalidarResumenSalario,
    );


    document.getElementById(
      "periodicidad_salario",
    ).addEventListener(
      "change",
      invalidarResumenSalario,
    );


    // ========================================================
    // Paso 4
    // ========================================================

    document.getElementById(
      "form-proyeccion",
    ).addEventListener(
      "submit",
      analizarProyeccion,
    );


    document.getElementById(
      "btn-volver-paso-3",
    ).addEventListener(
      "click",
      () => {
        mostrarPaso(3);
      },
    );


    document.getElementById(
      "modalidad_proyeccion",
    ).addEventListener(
      "change",
      () => {
        actualizarConfiguracionProyeccion();
        invalidarResumenProyeccion();
      },
    );


    document.getElementById(
      "proyeccion_anio_fin",
    ).addEventListener(
      "input",
      () => {
        actualizarLimitesSalarioFuturo();
        invalidarResumenProyeccion();
      },
    );


    [
      "porcentaje_anual",
      "salario_mensual_futuro",
      "anio_salario_futuro",
      "escenarios_porcentajes",
    ].forEach((id) => {
      document.getElementById(
        id,
      ).addEventListener(
        "input",
        invalidarResumenProyeccion,
      );
    });
  },
);
