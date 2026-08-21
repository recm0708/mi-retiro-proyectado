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

const CLAVE_SIMULACION = "miRetiroProyectado.simulacion";

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
    origen_campos_persona: {},

    cuotas: {},
    origen_campos_cuotas: {},
    resumen_cuotas: null,

    modo_historial: "",
    modo_historial_confirmado_usuario: false,
    historial: null,
    origen_historial_anio_inicio: null,
    origen_campos_historial: {},
    resumen_historial: null,

    referencia_mi_retiro_seguro: null,
    importacion_comprobante_confirmada: false,
    ficha_digital_importada: null,
    importacion_ficha_digital_confirmada: false,
    campos_editados_importacion_ficha: [],

    detalle_anio_actual_habilitado: null,
    detalle_anio_actual: null,
    origen_campos_detalle_anio_actual: {},
    resumen_detalle_anio_actual: null,
    ultimo_mes_cuotas_derivado: null,

    origen_salario_proyeccion: "",
    salario: {},
    resumen_salario: null,

    proyeccion: {},
    origen_proyeccion_anio_fin: null,
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

      origen_campos_persona:
        simulacion.origen_campos_persona || {},

      cuotas:
        simulacion.cuotas || {},

      origen_campos_cuotas:
        simulacion.origen_campos_cuotas || {},

      modo_historial:
        simulacion.modo_historial ?? "",

      historial:
        simulacion.historial || null,

      origen_campos_historial:
        simulacion.origen_campos_historial || {},

      detalle_anio_actual:
        simulacion.detalle_anio_actual || null,

      origen_campos_detalle_anio_actual:
        simulacion.origen_campos_detalle_anio_actual || {},

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

  if (
    typeof actualizarDisponibilidadGestionDatos
    === "function"
  ) {
    actualizarDisponibilidadGestionDatos();
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
// Procedencia visible de datos importados y editados
// ============================================================

function codigoProcedenciaDesdeOrigen(origen) {
  const valor = String(origen || "").toUpperCase();
  if (!valor) return null;
  if (valor.includes("NO_DETECTADO")) return "NO_DETECTADO";
  if (valor.includes("COMPLETADO_MANUAL")) return "COMPLETADO_MANUAL";
  if (valor.includes("EDITADO")) return "EDITADO_USUARIO";
  if (valor.includes("MI_RETIRO_SEGURO") || valor.includes("FICHA_DIGITAL")) {
    return "DETECTADO";
  }
  if (valor === "MANUAL") return "COMPLETADO_MANUAL";
  return null;
}


function textoProcedenciaDato(codigo) {
  const textos = {
    DETECTADO: "Detectado",
    EDITADO_USUARIO: "Editado por ti",
    COMPLETADO_MANUAL: "Completado manualmente",
    NO_DETECTADO: "No detectado",
  };
  return textos[codigo] || "";
}


function claseProcedenciaDato(codigo) {
  const clases = {
    DETECTADO: "detected",
    EDITADO_USUARIO: "edited",
    COMPLETADO_MANUAL: "manual",
    NO_DETECTADO: "missing",
  };
  return clases[codigo] || "";
}


function origenBloqueaCampo(origen) {
  const codigo = codigoProcedenciaDesdeOrigen(origen);
  return ["DETECTADO", "EDITADO_USUARIO", "COMPLETADO_MANUAL"].includes(codigo)
    && String(origen || "").toUpperCase() !== "MANUAL";
}


function asegurarNotaProcedencia(control, idPreferido = null) {
  if (!control) return null;
  const id = idPreferido || `procedencia-${control.id}`;
  let nota = document.getElementById(id);
  if (nota) return nota;

  nota = document.createElement("div");
  nota.id = id;
  nota.className = "field-origin-note data-provenance-note d-none";

  const grupo = control.closest(".input-group");
  if (grupo) {
    grupo.insertAdjacentElement("afterend", nota);
  } else {
    control.insertAdjacentElement("afterend", nota);
  }
  return nota;
}


function mostrarProcedenciaCampo(control, origen, opciones = {}) {
  if (!control) return;
  const codigo = codigoProcedenciaDesdeOrigen(origen);
  const nota = asegurarNotaProcedencia(control, opciones.notaId || null);
  if (!nota) return;

  if (!codigo || (origen === "MANUAL" && !opciones.mostrarManual)) {
    nota.textContent = "";
    nota.className = "field-origin-note data-provenance-note d-none";
    control.removeAttribute("data-provenance");
    return;
  }

  nota.textContent = opciones.texto || textoProcedenciaDato(codigo);
  nota.className = `field-origin-note data-provenance-note ${claseProcedenciaDato(codigo)}`;
  control.dataset.provenance = codigo;
}


function actualizarProcedenciaDatosPersonales(simulacion = obtenerSimulacion()) {
  const importacionConfirmada = Boolean(
    simulacion.importacion_comprobante_confirmada
    && simulacion.referencia_mi_retiro_seguro,
  );
  const origenes = { ...(simulacion.origen_campos_persona || {}) };

  if (importacionConfirmada && Object.keys(origenes).length === 0) {
    const referencia = simulacion.referencia_mi_retiro_seguro || {};
    const editados = new Set(simulacion.campos_editados_importacion_comprobante || []);
    const mapeo = {
      primer_nombre: ["preview-comprobante-primer-nombre", referencia.primer_nombre],
      segundo_nombre: ["preview-comprobante-segundo-nombre", referencia.segundo_nombre],
      primer_apellido: ["preview-comprobante-primer-apellido", referencia.primer_apellido],
      segundo_apellido: ["preview-comprobante-segundo-apellido", referencia.segundo_apellido],
      apellido_casada: ["preview-comprobante-apellido-casada", referencia.apellido_casada],
      cedula: ["preview-comprobante-cedula", referencia.cedula],
      numero_seguro_social: ["preview-comprobante-seguro-social", referencia.numero_seguro_social],
      fecha_nacimiento: ["preview-comprobante-fecha-nacimiento", referencia.fecha_nacimiento],
      sexo: ["preview-comprobante-sexo", referencia.sexo],
      fecha_ingreso_css: ["preview-comprobante-fecha-ingreso", referencia.fecha_ingreso_css],
      sistema: ["preview-comprobante-sistema", referencia.sistema_elegido],
    };
    Object.entries(mapeo).forEach(([campo, [previewId, valor]]) => {
      if (editados.has(previewId)) {
        origenes[campo] = "MI_RETIRO_SEGURO_EDITADO";
      } else if (valor !== null && valor !== undefined && String(valor).trim() !== "" && valor !== "NO_IDENTIFICADO") {
        origenes[campo] = "MI_RETIRO_SEGURO_DETECTADO";
      } else {
        origenes[campo] = "MI_RETIRO_SEGURO_NO_DETECTADO";
      }
    });
  }

  const campos = [
    "primer_nombre", "segundo_nombre", "primer_apellido", "segundo_apellido",
    "apellido_casada", "cedula", "numero_seguro_social", "fecha_nacimiento",
    "sexo", "fecha_ingreso_css", "sistema",
  ];

  campos.forEach((id) => {
    const control = document.getElementById(id);
    if (!control) return;
    if (!importacionConfirmada) {
      mostrarProcedenciaCampo(control, null);
      return;
    }
    mostrarProcedenciaCampo(control, origenes[id] || "MI_RETIRO_SEGURO_NO_DETECTADO");
  });

  return origenes;
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
        ? "La importación no completó toda la información previsional obligatoria. Abre Revisar importación, pulsa Editar campos y completa fecha de nacimiento, sexo y sistema previsional."
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
  actualizarProcedenciaDatosPersonales(simulacion);
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

  const marcadorCierre = document.getElementById(
    "required-cierre-anio",
  );
  const marcadorFuturas = document.getElementById(
    "required-cuotas-futuras",
  );
  const notaSinContinuidad = document.getElementById(
    "cuotas-sin-continuidad",
  );
  const notaSugerencia = document.getElementById(
    "cuotas-sugerencia-continuidad",
  );

  if (continua === "false") {
    cierre.value = cuotasActuales;
    futuras.value = 0;

    cierre.disabled = true;
    futuras.disabled = true;
    cierre.required = false;
    futuras.required = false;
    marcadorCierre?.classList.add("d-none");
    marcadorFuturas?.classList.add("d-none");
    notaSinContinuidad?.classList.remove("d-none");
    notaSugerencia?.classList.add("d-none");

  } else if (continua === "true") {
    cierre.disabled = false;
    futuras.disabled = false;
    cierre.required = true;
    futuras.required = true;
    marcadorCierre?.classList.remove("d-none");
    marcadorFuturas?.classList.remove("d-none");
    notaSinContinuidad?.classList.add("d-none");
    notaSugerencia?.classList.remove("d-none");

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
  } else {
    // Estado limpio/nuevo: ninguna decisión de cotización futura se presume.
    // Los dos supuestos permanecen vacíos hasta que el usuario elija Sí/No.
    cierre.value = "";
    futuras.value = "";
    cierre.disabled = true;
    futuras.disabled = true;
    cierre.required = false;
    futuras.required = false;
    marcadorCierre?.classList.add("d-none");
    marcadorFuturas?.classList.add("d-none");
    notaSinContinuidad?.classList.add("d-none");
    notaSugerencia?.classList.add("d-none");
  }
}


/**
 * Refleja en el Paso 2 qué valores fueron confirmados desde un PDF.
 *
 * Los campos detectados quedan de solo lectura. Los campos que el documento
 * no aportó permanecen editables para que el Asegurado(a) los complete.
 *
 * @param {Object} simulacion Estado actual de la simulación.
 */
function actualizarOrigenCamposCuotas(simulacion) {
  const importacionConfirmada = Boolean(
    simulacion.importacion_comprobante_confirmada,
  );
  const origenes = {
    ...(simulacion.origen_campos_cuotas || {}),
  };

  // Si el estado serializado no incluye procedencia por campo pero sí una
  // referencia confirmada, reconstruye esa metadata desde los datos que
  // el propio comprobante aportó.
  if (importacionConfirmada && simulacion.referencia_mi_retiro_seguro) {
    const referencia = simulacion.referencia_mi_retiro_seguro;

    if (
      referencia.cuotas_historicas != null
      && simulacion.cuotas?.cuotas_totales != null
      && !origenes.cuotas_totales
    ) {
      origenes.cuotas_totales = "MI_RETIRO_SEGURO";
    }

    const registroActual = (referencia.registros || []).find(
      (registro) => (
        Number(registro.anio) === ANIO_ACTUAL
        && registro.tipo !== "PROYECTADO"
      ),
    );

    if (
      registroActual
      && simulacion.cuotas?.cuotas_anio_actual != null
      && !origenes.cuotas_anio_actual
    ) {
      origenes.cuotas_anio_actual = "MI_RETIRO_SEGURO";
    }
  }

  const campos = [
    {
      id: "cuotas_totales",
      notaId: "origen-cuotas-totales",
    },
    {
      id: "cuotas_anio_actual",
      notaId: "origen-cuotas-anio-actual",
    },
  ];

  let hayImportados = false;

  campos.forEach(({ id, notaId }) => {
    const control = document.getElementById(id);
    const nota = document.getElementById(notaId);
    const origen = origenes[id] || null;
    const importado = origenBloqueaCampo(origen);

    if (!control || !nota) {
      return;
    }

    control.readOnly = importado;
    control.classList.toggle("field-imported-readonly", importado);

    if (importado) {
      hayImportados = true;
      nota.textContent = textoProcedenciaDato(codigoProcedenciaDesdeOrigen(origen));
      nota.className = `field-origin-note data-provenance-note ${claseProcedenciaDato(codigoProcedenciaDesdeOrigen(origen))}`;
    } else if (importacionConfirmada) {
      nota.textContent = "No detectado";
      nota.className = "field-origin-note data-provenance-note missing";
    } else {
      nota.textContent = "";
      nota.className = "field-origin-note d-none";
    }
  });

  const acciones = document.getElementById(
    "cuotas-importadas-acciones",
  );

  if (acciones) {
    acciones.classList.toggle(
      "d-none",
      !importacionConfirmada,
    );
    acciones.classList.toggle(
      "has-locked-fields",
      hayImportados,
    );

    const estado = document.getElementById(
      "cuotas-importadas-estado",
    );

    if (estado) {
      estado.textContent = hayImportados
        ? "Los datos confirmados desde la importación se mantienen sin cambios en este paso."
        : "La importación no aportó estas cuotas. Completa manualmente los campos pendientes.";
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
  actualizarOrigenCamposCuotas(simulacion);

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
async function analizarCuotas(evento = null, opciones = {}) {
  evento?.preventDefault();

  const mostrarMensajes = opciones.mostrarMensajes !== false;
  const reportarValidez = opciones.reportarValidez !== false;

  const formulario = document.getElementById(
    "form-cuotas",
  );

  if (!formulario.checkValidity()) {
    if (mostrarMensajes && reportarValidez) {
      formulario.reportValidity();
    }
    return false;
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

      if (mostrarMensajes) {
        mostrarErrorCuotas(mensaje);
      }
      return false;
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

    return true;
  } catch {
    if (mostrarMensajes) {
      mostrarErrorCuotas(
        "No fue posible comunicarse con el servidor.",
      );
    }
    return false;
  }
}


/**
 * Continúa al historial cuando el análisis de cuotas ya está disponible.
 */
function continuarDesdePasoCuotas() {
  const simulacionActual = obtenerSimulacion();

  if (!simulacionActual.resumen_cuotas) {
    mostrarErrorCuotas(
      "Primero debes analizar las cuotas.",
    );
    return;
  }

  if (
    typeof sincronizarHistorialConDatosActuales === "function"
  ) {
    sincronizarHistorialConDatosActuales();
  }

  mostrarPaso(3);
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

  document.getElementById("resultado-salario")?.classList.add("d-none");
  document.getElementById("resultado-paso3")?.classList.add("d-none");
  document.getElementById("resultado-proyeccion")?.classList.add("d-none");
}


/**
 * Normaliza el salario mediante la API y conserva el resultado
 * dentro de la simulación temporal.
 *
 * @param {SubmitEvent} evento Evento submit del formulario.
 */
async function analizarSalario(evento = null) {
  evento?.preventDefault();

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
    return false;
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
      return false;
    }

    const simulacion = obtenerSimulacion();

    simulacion.salario = datos;
    simulacion.resumen_salario = contenido;
    simulacion.origen_salario_proyeccion = (
      document.getElementById("origen_salario_proyeccion")?.value
      || ""
    );

    // Una nueva normalización salarial invalida cualquier
    // proyección construida con un salario anterior.
    simulacion.proyeccion = {};
    simulacion.origen_proyeccion_anio_fin = null;
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

    return true;
  } catch {
    mostrarErrorSalario(
      "No fue posible comunicarse con el servidor.",
    );
    return false;
  }
}


/**
 * Muestra las equivalencias salariales devueltas por el backend.
 *
 * @param {Object} resumen Resultado de normalización salarial.
 */
function mostrarResumenSalario(resumen) {
  if (!resumen) return;

  if (typeof actualizarResumenPaso3 === "function") {
    actualizarResumenPaso3();
  }
}


function paso3EstaCompleto(simulacion = obtenerSimulacion()) {
  const modo = simulacion.modo_historial || "";
  const modoHistorialValido = ["MANUAL", "SOLO_ACTUAL"].includes(modo);
  const decisionDetalleValida = (
    typeof simulacion.detalle_anio_actual_habilitado === "boolean"
  );
  const historial = simulacion.resumen_historial;
  const historialListo = (
    modo === "SOLO_ACTUAL"
    || Boolean(
      historial
      && historial.cuotas_coinciden
      && historial.historial_completo,
    )
  );

  const detalleListo = (
    !simulacion.detalle_anio_actual_habilitado
    || Boolean(
      simulacion.resumen_detalle_anio_actual
      && simulacion.resumen_detalle_anio_actual.cuotas_coinciden,
    )
  );

  return Boolean(
    modoHistorialValido
    && decisionDetalleValida
    && historialListo
    && detalleListo
    && simulacion.resumen_salario,
  );
}


function actualizarResumenPaso3() {
  const simulacion = obtenerSimulacion();
  const historial = simulacion.resumen_historial;
  const salario = simulacion.resumen_salario;
  const contenedor = document.getElementById("resultado-paso3");

  if (!contenedor) return;

  const referencia = historial?.cuotas_totales_referencia
    ?? simulacion.resumen_cuotas?.cuotas_reales
    ?? "—";
  const identificadas = historial?.cuotas_sumadas ?? "No detallado";
  const diferencia = historial?.diferencia_cuotas ?? "—";
  const totalSalarios = historial
    ? formatearMoneda(historial.total_salarios_reportados)
    : "No detallado";
  const baseMensual = salario
    ? formatearMoneda(salario.salario_mensual)
    : "—";

  const asignar = (id, valor) => {
    const elemento = document.getElementById(id);
    if (elemento) elemento.textContent = valor;
  };

  asignar("paso3-cuotas-referencia", referencia);
  asignar("paso3-cuotas-identificadas", identificadas);
  asignar("paso3-diferencia-cuotas", diferencia);
  asignar("paso3-total-salarios", totalSalarios);
  asignar("paso3-base-mensual", baseMensual);

  const listo = paso3EstaCompleto(simulacion);
  contenedor.classList.toggle("d-none", !listo);

  const estado = document.getElementById("paso3-estado-general");
  if (estado && listo) {
    estado.className = "alert alert-success mt-4 mb-0";
    estado.textContent = (
      (simulacion.modo_historial || "") === "SOLO_ACTUAL"
        ? "Base salarial lista. La simulación continuará con información histórica limitada."
        : "Historial y base salarial listos para continuar."
    );
  }
}


function enfocarSeccionPaso3(id) {
  const seccion = document.getElementById(id);
  seccion?.scrollIntoView({ behavior: "smooth", block: "start" });
}


/**
 * Garantiza la dependencia del Paso 2 sin obligar al usuario a retroceder
 * cuando las cuotas ya están completas pero su resumen quedó invalidado.
 *
 * Si el formulario de cuotas aún está incompleto, Paso 3 permanece visible
 * y explica qué dependencia falta; nunca navega hacia atrás por sorpresa.
 *
 * @returns {Promise<boolean>} true si existe un resumen de cuotas vigente.
 */
async function asegurarCuotasAnalizadasParaPaso3() {
  const simulacion = obtenerSimulacion();

  if (simulacion.resumen_cuotas) {
    return true;
  }

  const formularioCuotas = document.getElementById("form-cuotas");

  if (!formularioCuotas || !formularioCuotas.checkValidity()) {
    if (typeof mostrarErrorHistorial === "function") {
      mostrarErrorHistorial(
        "Antes de analizar el historial, completa la información de cuotas del Paso 2. "
        + "El Paso 3 conservará tus datos; revisa Cuotas únicamente si todavía falta información.",
      );
    }
    return false;
  }

  const analizadas = await analizarCuotas(
    null,
    { mostrarMensajes: false, reportarValidez: false },
  );

  if (!analizadas && typeof mostrarErrorHistorial === "function") {
    mostrarErrorHistorial(
      "No fue posible revalidar automáticamente las cuotas. Revisa los datos del Paso 2 antes de continuar.",
    );
  }

  return analizadas;
}


function validarDecisionesPaso3() {
  const modoHistorial = document.getElementById("modo_historial");
  const usarDetalle = document.getElementById("usar_detalle_anio_actual");
  const modoDetalle = document.getElementById("modo_detalle_anio_actual");

  for (const control of [modoHistorial, usarDetalle]) {
    if (!control?.value) {
      control?.reportValidity();
      control?.focus();
      return false;
    }
  }

  if (usarDetalle.value === "true" && !modoDetalle?.value) {
    modoDetalle?.reportValidity();
    modoDetalle?.focus();
    return false;
  }

  return true;
}


async function analizarPasoHistorialCompleto() {
  const cuotasListas = await asegurarCuotasAnalizadasParaPaso3();
  if (!cuotasListas) {
    enfocarSeccionPaso3("seccion-historial-salarial");
    return false;
  }

  if (!validarDecisionesPaso3()) {
    enfocarSeccionPaso3("seccion-historial-salarial");
    return false;
  }

  const simulacionInicial = obtenerSimulacion();
  const modo = simulacionInicial.modo_historial || "";

  if (simulacionInicial.detalle_anio_actual_habilitado) {
    if (typeof validarDetalleAnioActual !== "function") return false;
    const detalleValido = await validarDetalleAnioActual();
    if (!detalleValido) {
      enfocarSeccionPaso3("seccion-detalle-anio-actual");
      return false;
    }
  }

  if (modo === "MANUAL") {
    if (typeof analizarHistorialSalarial !== "function") return false;
    const historialAnalizado = await analizarHistorialSalarial();
    const simulacionHistorial = obtenerSimulacion();
    const resumenHistorial = simulacionHistorial.resumen_historial;

    if (
      !historialAnalizado
      || !resumenHistorial?.cuotas_coinciden
      || !resumenHistorial?.historial_completo
    ) {
      enfocarSeccionPaso3("seccion-historial-salarial");
      return false;
    }
  } else if (typeof confirmarModoSoloActual === "function") {
    confirmarModoSoloActual();
  }

  const salarioAnalizado = await analizarSalario();
  if (!salarioAnalizado) {
    enfocarSeccionPaso3("base-salarial-titulo");
    return false;
  }

  actualizarResumenPaso3();
  return paso3EstaCompleto();
}


function continuarDesdePasoHistorial() {
  const simulacion = obtenerSimulacion();
  if (!paso3EstaCompleto(simulacion)) {
    analizarPasoHistorialCompleto();
    return;
  }

  prepararPasoProyeccion(simulacion);
  mostrarPaso(4);
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
function actualizarProcedenciaHorizonteProyeccion(origen) {
  const nota = document.getElementById("origen-proyeccion-anio-fin");
  if (!nota) return;

  if (origen === "EDITADO_USUARIO") {
    nota.className = "field-origin-note edited";
    nota.textContent = (
      "Editado por ti. Este horizonte sustituye la sugerencia automática inicial."
    );
    return;
  }

  nota.className = "field-origin-note automatic";
  nota.textContent = (
    origen === "AJUSTADO_DESDE_RETIRO"
      ? "Calculado automáticamente para cubrir el escenario de retiro más lejano que seleccionaste en el Paso 5. Puedes modificarlo."
      : `Calculado automáticamente: horizonte inicial sugerido de ${ANIOS_PROYECCION_PREDETERMINADOS} años. Puedes modificarlo según la edad de retiro que quieras comparar.`
  );
}


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
    const origen = simulacion.origen_salario_proyeccion || "";
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

  const anioPredeterminado = (
    ANIO_ACTUAL
    + ANIOS_PROYECCION_PREDETERMINADOS
  );
  const anioGuardado = Number(simulacion.proyeccion?.anio_fin || 0);

  if (!campoFin.value) {
    campoFin.value = (
      Number.isInteger(anioGuardado)
      && anioGuardado >= ANIO_ACTUAL
        ? anioGuardado
        : anioPredeterminado
    );
  }

  if (!simulacion.origen_proyeccion_anio_fin) {
    simulacion.origen_proyeccion_anio_fin = (
      Number(campoFin.value) === anioPredeterminado
        ? "CALCULADO_AUTOMATICAMENTE"
        : "EDITADO_USUARIO"
    );
    guardarSimulacion(simulacion);
  }

  actualizarProcedenciaHorizonteProyeccion(
    simulacion.origen_proyeccion_anio_fin,
  );
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

  let escenariosPorcentajes = [];

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

  const tasaEsObjetivo = escenario.nombre.startsWith(
    "Proyección hasta salario conocido",
  );
  tasa.textContent = (
    `${tasaEsObjetivo ? "Tasa equivalente al objetivo" : "Tasa anual"}: ${
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
    "table-responsive app-table-shell";

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

    let pasoRestaurado = (
      pasoGuardado >= 1
      && pasoGuardado <= 6
        ? pasoGuardado
        : 1
    );

    // Nunca restaura una etapa posterior si una dependencia previa fue
    // limpiada o invalidada. Retrocede solo hasta el último paso seguro.
    if (typeof puedeAccederDirectamenteAPaso === "function") {
      while (
        pasoRestaurado > 1
        && !puedeAccederDirectamenteAPaso(
          pasoRestaurado,
          simulacion,
        )
      ) {
        pasoRestaurado -= 1;
      }
    }

    mostrarPaso(pasoRestaurado);


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
      "btn-revisar-cuotas-importadas",
    )?.addEventListener(
      "click",
      () => {
        if (typeof revisarComprobanteImportado === "function") {
          revisarComprobanteImportado(2);
        }
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
      (evento) => {
        evento.preventDefault();
        analizarPasoHistorialCompleto();
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
        const simulacion = obtenerSimulacion();
        const anioFin = Number(
          document.getElementById("proyeccion_anio_fin").value,
        );

        simulacion.origen_proyeccion_anio_fin = "EDITADO_USUARIO";
        if (Number.isInteger(anioFin)) {
          simulacion.proyeccion = {
            ...(simulacion.proyeccion || {}),
            anio_inicio: ANIO_ACTUAL,
            anio_fin: anioFin,
          };
        }
        guardarSimulacion(simulacion);
        actualizarProcedenciaHorizonteProyeccion("EDITADO_USUARIO");
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
