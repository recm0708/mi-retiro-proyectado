"use strict";

/*
 * Mi Retiro Proyectado — Importación revisable de documentos oficiales.
 *
 * Propósito: Coordina Mi Retiro Seguro y Ficha Digital desde la selección del archivo hasta la confirmación explícita.
 * Alcance: El navegador conserva datos confirmados y metadata de procedencia; el archivo original se procesa en memoria por el backend.
 */

let borradorImportacionComprobante = null;
let edicionPreviewComprobanteHabilitada = false;
let previewComprobanteFueEditado = false;
let camposEditadosPreviewComprobante = new Set();
let pasoVistaPreviewComprobante = 1;
let borradorImportacionFichaDigital = null;
let edicionPreviewFichaHabilitada = false;
let previewFichaFueEditado = false;
let camposEditadosPreviewFicha = new Set();
let borradorFichaPendienteVigencia = null;

const MESES_IMPORTACION = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
];


function textoPeriodoFicha(anio, mes) {
  const nombreMes = MESES_IMPORTACION[Number(mes) - 1];
  if (!nombreMes || !Number(anio)) return "período no identificado";
  return `${nombreMes.toLowerCase()} de ${anio}`;
}


function descomponerFechaReferenciaFicha(resumen) {
  if (!resumen?.fecha_referencia_confiable || !resumen?.fecha_referencia) return null;
  const coincidencia = String(resumen.fecha_referencia).match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (!coincidencia) return null;
  return {
    anio: Number(coincidencia[1]),
    mes: Number(coincidencia[2]),
    dia: Number(coincidencia[3]),
  };
}


function anioFichaDigital(resumen) {
  const anio = Number(resumen?.anio_mas_reciente);
  if (anio) return anio;
  const registros = Array.isArray(resumen?.registros) ? resumen.registros : [];
  return registros.reduce((maximo, registro) => Math.max(maximo, Number(registro.anio || 0)), 0);
}


function evaluarVigenciaFichaDigital(resumen) {
  // La vigencia compara el período más reciente del documento contra la fecha
  // de referencia extraída; si falta una pieza, se exige decisión explícita.
  const anio = Number(resumen?.anio_mas_reciente);
  const mes = Number(resumen?.mes_mas_reciente);
  const referencia = descomponerFechaReferenciaFicha(resumen);

  if (!anio || !mes) {
    return {
      estado: "NO_IDENTIFICADA",
      diferenciaMeses: null,
      requiereDecision: true,
      periodo: "período no identificado",
      periodoReferencia: referencia ? textoPeriodoFicha(referencia.anio, referencia.mes) : null,
    };
  }

  if (!referencia) {
    return {
      estado: "FECHA_NO_VERIFICADA",
      diferenciaMeses: null,
      requiereDecision: true,
      periodo: textoPeriodoFicha(anio, mes),
      periodoReferencia: null,
    };
  }

  const indiceDocumento = (anio * 12) + (mes - 1);
  const indiceActual = (referencia.anio * 12) + (referencia.mes - 1);
  const diferenciaMeses = indiceActual - indiceDocumento;

  let estado = "RECIENTE";
  if (diferenciaMeses > 0) {
    estado = "DESACTUALIZADA";
  } else if (diferenciaMeses < 0) {
    estado = "PERIODO_FUTURO";
  }

  return {
    estado,
    diferenciaMeses,
    requiereDecision: estado !== "RECIENTE",
    periodo: textoPeriodoFicha(anio, mes),
    periodoReferencia: textoPeriodoFicha(referencia.anio, referencia.mes),
  };
}


function mensajeVigenciaFichaDigital(resumen) {
  const vigencia = evaluarVigenciaFichaDigital(resumen);

  if (vigencia.estado === "DESACTUALIZADA") {
    return (
      `El último salario detectado corresponde a ${vigencia.periodo}. `
      + `La fecha actual verificada corresponde a ${vigencia.periodoReferencia}. `
      + "Si tienes una Ficha Digital del mes actual, conviene utilizarla; también puedes continuar con esta y completar manualmente la información faltante."
    );
  }

  if (vigencia.estado === "PERIODO_FUTURO") {
    return (
      `La Ficha Digital contiene como período más reciente ${vigencia.periodo}, `
      + `posterior a la fecha actual verificada (${vigencia.periodoReferencia}). Revisa el documento antes de continuar.`
    );
  }

  if (vigencia.estado === "FECHA_NO_VERIFICADA") {
    return (
      `El último salario detectado corresponde a ${vigencia.periodo}. `
      + "No fue posible verificar en línea la fecha actual con una fuente oficial de la CSS. "
      + "Por seguridad, revisa si dispones de una Ficha Digital más reciente o continúa con esta de forma consciente."
    );
  }

  if (vigencia.estado === "NO_IDENTIFICADA") {
    return (
      "No fue posible determinar el último período salarial de la Ficha Digital. "
      + "Puedes seleccionar otra ficha o continuar y revisar cuidadosamente la vista previa."
    );
  }

  return `Último período detectado: ${vigencia.periodo}. Coincide con el mes actual verificado.`;
}


function mostrarDecisionVigenciaFichaDigital(resumen) {
  borradorFichaPendienteVigencia = structuredClone(resumen);
  const mensaje = document.getElementById("mensaje-vigencia-ficha-digital");
  if (mensaje) mensaje.textContent = mensajeVigenciaFichaDigital(resumen);
  obtenerModalBootstrap("modal-vigencia-ficha-digital")?.show();
}


function continuarConFichaPendienteVigencia() {
  if (!borradorFichaPendienteVigencia) return;
  const resumen = structuredClone(borradorFichaPendienteVigencia);
  borradorFichaPendienteVigencia = null;

  const modalElemento = document.getElementById("modal-vigencia-ficha-digital");
  const modal = obtenerModalBootstrap("modal-vigencia-ficha-digital");
  if (!modalElemento || !modal) {
    renderizarPreviewFichaDigital(resumen, []);
    return;
  }

  modalElemento.addEventListener(
    "hidden.bs.modal",
    () => renderizarPreviewFichaDigital(resumen, []),
    { once: true },
  );
  modal.hide();
}


function seleccionarOtraFichaPorVigencia() {
  borradorFichaPendienteVigencia = null;
  const modalElemento = document.getElementById("modal-vigencia-ficha-digital");
  const modal = obtenerModalBootstrap("modal-vigencia-ficha-digital");
  const input = document.getElementById("import-ficha-digital-pdf");

  const prepararSelector = () => {
    if (!input) return;
    input.value = "";
    actualizarEstadoBotonAnalizarFichaDigital();
    input.focus();
    mostrarEstadoImportacion(
      "estado-ficha-digital-importacion",
      "Selecciona una Ficha Digital más reciente y vuelve a analizar el documento.",
      "info",
    );
  };

  if (!modalElemento || !modal) {
    prepararSelector();
    return;
  }

  modalElemento.addEventListener("hidden.bs.modal", prepararSelector, { once: true });
  modal.hide();
}


function obtenerModalBootstrap(id) {
  const elemento = document.getElementById(id);

  if (!elemento) {
    return null;
  }

  // Los modales deben vivir fuera de los paneles del wizard. Si el
  // componente fue renderizado dentro de un paso que luego queda oculto,
  // Bootstrap puede mostrar únicamente el backdrop. Se mueve una sola vez
  // al body para que pueda revisarse desde Cuotas y pasos posteriores.
  if (elemento.parentElement !== document.body) {
    document.body.appendChild(elemento);
  }

  return bootstrap.Modal.getOrCreateInstance(elemento);
}


function mostrarEstadoImportacion(id, mensaje, tipo = "info") {
  const elemento = document.getElementById(id);
  elemento.className = `official-import-status mt-3 alert alert-${tipo}`;
  elemento.textContent = mensaje;
}


function ocultarEstadoImportacion(id) {
  const elemento = document.getElementById(id);
  elemento.classList.add("d-none");
  elemento.textContent = "";
}


function mensajeErrorImportacion(contenido, predeterminado) {
  if (!contenido) return predeterminado;
  if (typeof contenido.detail === "string") return contenido.detail;
  if (Array.isArray(contenido.detail)) {
    return contenido.detail.map((item) => item.msg || String(item)).join(" ");
  }
  return predeterminado;
}


function textoSistemaImportado(sistema) {
  const nombres = {
    SEBD: "SEBD — Beneficio Definido",
    MIXTO: "Subsistema Mixto",
    SUCGS: "SUCGS — Capitalización con Garantía Solidaria",
    NO_IDENTIFICADO: "Sistema no identificado",
  };
  return nombres[sistema] || "Sistema no identificado";
}


function naturalezaPrestacionImportada(texto) {
  const normalizado = (texto || "").toUpperCase();
  if (normalizado.includes("PENSIÓN") || normalizado.includes("PENSION")) {
    return "PENSION_MENSUAL";
  }
  if (normalizado.includes("INDEMNIZ") || normalizado.includes("PAGO ÚNICO") || normalizado.includes("PAGO UNICO")) {
    return "PAGO_UNICO";
  }
  return "NO_IDENTIFICADA";
}


function invalidarResultadosPorImportacion(simulacion) {
  // Confirmar datos importados invalida resultados descendientes porque cambia
  // la procedencia o el contenido base de los pasos iniciales.
  simulacion.resumen_cuotas = null;
  simulacion.resumen_historial = null;
  simulacion.resumen_detalle_anio_actual = null;
  simulacion.resumen_salario = null;
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.configuracion_mixto_resultados = {};
  simulacion.resultado_mixto = null;
  simulacion.configuracion_sucgs_resultados = {};
  simulacion.resultado_sucgs = null;
}



// ============================================================
// Modalidad y procedencia de datos personales
// ============================================================

function actualizarApellidoCasada() {
  const sexo = document.getElementById("sexo")?.value;
  const contenedor = document.getElementById("apellido-casada-wrapper");
  if (!contenedor) return;
  const mostrar = sexo === "F";
  contenedor.classList.toggle("d-none", !mostrar);
  if (!mostrar) {
    const campo = document.getElementById("apellido_casada");
    if (campo) campo.value = "";
  }
}

function bloquearFormularioPersonal(bloqueado, simulacion = obtenerSimulacion()) {
  // Los campos detectados se bloquean hasta que el usuario habilita edición;
  // los campos manuales conservan su comportamiento normal.
  let origenes = simulacion.origen_campos_persona || {};
  if (bloqueado && Object.keys(origenes).length === 0 && typeof actualizarProcedenciaDatosPersonales === "function") {
    origenes = actualizarProcedenciaDatosPersonales(simulacion) || {};
  }

  document.querySelectorAll("#bloque-datos-personales input, #bloque-datos-personales select").forEach((control) => {
    const bloquearCampo = Boolean(
      bloqueado
      && typeof origenBloqueaCampo === "function"
      && origenBloqueaCampo(origenes[control.id]),
    );
    if (control.matches("select")) {
      control.disabled = bloquearCampo;
    } else {
      control.readOnly = bloquearCampo;
    }
  });
}

function aplicarModoDatosPersonales(
  modo,
  simulacion = obtenerSimulacion(),
) {
  const formulario = document.getElementById(
    "form-datos-personales",
  );


  const importacionConfirmada = Boolean(
    simulacion.importacion_comprobante_confirmada
    && simulacion.referencia_mi_retiro_seguro
  );


  /*
   * La visibilidad de la preparación documental pertenece
   * exclusivamente a simulation_mode.js mediante
   * assisted-preparation-panel. Este importador no vuelve
   * a ocultarse de forma independiente.
   */

  /*
   * Después de la preparación documental, los campos
   * faltantes deben poder completarse manualmente.
   */
  formulario?.classList.remove(
    "d-none",
  );


  bloquearFormularioPersonal(
    importacionConfirmada,
    simulacion,
  );


  actualizarApellidoCasada();


  if (
    typeof actualizarNavegacionFlotante
    === "function"
  ) {
    actualizarNavegacionFlotante();
  }
}

function restaurarModoDatosPersonales(simulacion = obtenerSimulacion()) {
  const modo = simulacion.modo_datos_personales || (
    simulacion.importacion_comprobante_confirmada ? "MI_RETIRO_SEGURO" : "MANUAL"
  );
  const radio = document.querySelector(`input[name="modo_datos_personales"][value="${modo}"]`);
  if (radio) radio.checked = true;
  aplicarModoDatosPersonales(modo, simulacion);
}

function cambiarModoDatosPersonales(evento) {
  const modo = evento.target.value;
  const simulacion = obtenerSimulacion();
  simulacion.modo_datos_personales = modo;
  if (modo === "MANUAL") {
    simulacion.origen_persona = "MANUAL";
  }
  guardarSimulacion(simulacion);
  aplicarModoDatosPersonales(modo, simulacion);
}

function actualizarEstadoBotonAnalizarComprobante() {
  const input = document.getElementById("import-comprobante-pdf");
  const boton = document.getElementById("btn-analizar-comprobante-importacion");
  if (boton) boton.disabled = !input?.files?.length;
}

function actualizarApellidoCasadaPreview() {
  const sexo = document.getElementById("preview-comprobante-sexo")?.value;
  document.querySelectorAll(".preview-apellido-casada-wrapper").forEach((elemento) => {
    elemento.classList.toggle("d-none", sexo !== "F");
  });
}

function valorFueDetectado(valor) {
  return (
    valor !== null
    && valor !== undefined
    && String(valor).trim() !== ""
    && valor !== "NO_IDENTIFICADO"
  );
}


function marcarEstadoDeteccion(idControl, valor, editado = false, origenExplicito = null) {
  // La etiqueta de procedencia distingue dato detectado, editado o no hallado
  // sin confiar ciegamente en que el PDF contenga todos los campos.
  const estado = document.getElementById(`estado-${idControl}`);
  const control = document.getElementById(idControl);
  if (!estado) return;

  const detectado = valorFueDetectado(valor);
  if (control) control.dataset.detectedOriginally = detectado ? "true" : "false";

  if (origenExplicito && typeof codigoProcedenciaDesdeOrigen === "function") {
    const codigo = codigoProcedenciaDesdeOrigen(origenExplicito);
    if (codigo) {
      estado.textContent = textoProcedenciaDato(codigo);
      estado.className = `import-field-status ${claseProcedenciaDato(codigo)}`;
      if (control) control.dataset.provenance = codigo;
      return;
    }
  }

  if (editado) {
    estado.textContent = detectado ? "Editado por ti" : "Completado manualmente";
    estado.className = "import-field-status edited";
    return;
  }

  estado.textContent = detectado ? "Detectado" : "No detectado";
  estado.className = `import-field-status ${detectado ? "detected" : "missing"}`;
}


function registrarEdicionCampoPreviewComprobante(control) {
  if (!edicionPreviewComprobanteHabilitada || !control) return;

  const clave = control.dataset.provenanceKey || control.id;
  if (!clave) return;

  previewComprobanteFueEditado = true;
  camposEditadosPreviewComprobante.add(clave);

  const estado = control.id ? document.getElementById(`estado-${control.id}`) : null;
  if (!estado) return;

  const detectadoOriginal = control.dataset.detectedOriginally === "true";
  estado.textContent = detectadoOriginal ? "Editado por ti" : "Completado manualmente";
  estado.className = "import-field-status edited";
}


function origenDesdeControlPreviewComprobante(control, fuente = "MI_RETIRO_SEGURO") {
  if (!control) return `${fuente}_NO_DETECTADO`;
  const clave = control.dataset.provenanceKey || control.id;
  const editado = Boolean(clave && camposEditadosPreviewComprobante.has(clave));
  const detectadoOriginal = control.dataset.detectedOriginally === "true";
  const procedenciaActual = control.dataset.provenance || null;

  if (editado) {
    if (["COMPLETADO_MANUAL", "NO_DETECTADO"].includes(procedenciaActual)) {
      return `${fuente}_COMPLETADO_MANUAL`;
    }
    return detectadoOriginal
      ? `${fuente}_EDITADO`
      : `${fuente}_COMPLETADO_MANUAL`;
  }
  return detectadoOriginal
    ? `${fuente}_DETECTADO`
    : `${fuente}_NO_DETECTADO`;
}

function establecerEdicionPreviewComprobante(habilitada) {
  edicionPreviewComprobanteHabilitada = habilitada;
  const modal = document.getElementById("modal-import-comprobante");
  if (!modal) return;

  modal.querySelectorAll(".modal-body input").forEach((control) => {
    if (control.type === "checkbox") {
      control.disabled = control.dataset.importedLocked === "true" || !habilitada;
    } else {
      control.readOnly = !habilitada;
    }
  });
  modal.querySelectorAll(".modal-body select").forEach((control) => {
    control.disabled = !habilitada;
  });

  const boton = document.getElementById("btn-editar-import-comprobante");
  if (boton) boton.textContent = habilitada ? "Finalizar edición" : "Editar campos";
  const importar = document.getElementById("btn-confirmar-import-comprobante");
  if (importar) importar.disabled = habilitada;
  const estado = document.getElementById("estado-edicion-comprobante");
  if (estado) {
    estado.textContent = habilitada ? "Editando" : "Modo revisión";
    estado.className = `badge rounded-pill ${habilitada ? "text-bg-primary" : "text-bg-secondary"}`;
  }
  actualizarApellidoCasadaPreview();
}

function alternarEdicionPreviewComprobante() {
  const habilitar = !edicionPreviewComprobanteHabilitada;
  establecerEdicionPreviewComprobante(habilitar);
}

// ============================================================
// Comprobante de Mi Retiro Seguro
// ============================================================

function crearFilaPreviewComprobante(registro) {
  const fila = document.createElement("tr");
  fila.dataset.tipoOriginal = registro.tipo;
  fila.dataset.anio = String(registro.anio);

  const aplicar = document.createElement("input");
  aplicar.type = "checkbox";
  aplicar.className = "form-check-input preview-comprobante-aplicar";
  aplicar.checked = registro.tipo === "HISTORICO";
  aplicar.disabled = true;
  aplicar.dataset.importedLocked = "true";
  aplicar.setAttribute("aria-label", `Clasificación automática del año ${registro.anio} para el historial real`);
  fila.classList.add("data-row-imported");
  fila.dataset.dataOrigin = "imported";

  const anio = document.createElement("input");
  anio.type = "number";
  anio.min = "1900";
  anio.max = "2200";
  anio.step = "1";
  anio.className = "form-control form-control-sm preview-comprobante-anio";
  anio.value = registro.anio;
  anio.setAttribute("aria-label", `Año detectado ${registro.anio}`);
  anio.dataset.provenanceKey = `historial:${registro.anio}:anio`;
  anio.dataset.detectedOriginally = "true";

  const edad = document.createElement("input");
  edad.type = "number";
  edad.min = "0";
  edad.max = "150";
  edad.step = "1";
  edad.className = "form-control form-control-sm preview-comprobante-edad";
  edad.value = registro.edad;
  edad.setAttribute("aria-label", `Edad detectada para ${registro.anio}`);
  edad.dataset.provenanceKey = `historial:${registro.anio}:edad`;
  edad.dataset.detectedOriginally = "true";

  const tipo = document.createElement("select");
  tipo.className = "form-select form-select-sm preview-comprobante-tipo";
  tipo.innerHTML = `
    <option value="HISTORICO">Histórico</option>
    <option value="HISTORICO_PROYECTADO">Histórico + proyectado</option>
    <option value="PROYECTADO">Proyectado</option>
  `;
  tipo.value = registro.tipo;
  tipo.setAttribute("aria-label", `Tipo de registro ${registro.anio}`);
  tipo.dataset.provenanceKey = `historial:${registro.anio}:tipo`;
  tipo.dataset.detectedOriginally = "true";

  const salarioGrupo = document.createElement("div");
  salarioGrupo.className = "input-group input-group-sm";
  const prefijo = document.createElement("span");
  prefijo.className = "input-group-text";
  prefijo.textContent = "B/.";
  const salario = document.createElement("input");
  salario.type = "text";
  salario.className = "form-control preview-comprobante-salario money-input";
  salario.value = formatearNumeroMonetario(registro.salario_anual);
  salario.setAttribute("aria-label", `Salario anual detectado ${registro.anio}`);
  salario.dataset.provenanceKey = `historial:${registro.anio}:salario`;
  salario.dataset.detectedOriginally = "true";
  salarioGrupo.append(prefijo, salario);
  configurarCampoMonetario(salario);

  const cuotas = document.createElement("input");
  cuotas.type = "number";
  cuotas.min = "0";
  cuotas.max = "12";
  cuotas.step = "1";
  cuotas.className = "form-control form-control-sm preview-comprobante-cuotas-anio";
  cuotas.value = registro.cuotas;
  cuotas.setAttribute("aria-label", `Cuotas detectadas ${registro.anio}`);
  cuotas.dataset.provenanceKey = `historial:${registro.anio}:cuotas`;
  cuotas.dataset.detectedOriginally = "true";

  [aplicar, anio, edad, tipo, salarioGrupo, cuotas].forEach((control) => {
    const celda = document.createElement("td");
    celda.appendChild(control);
    fila.appendChild(celda);
  });

  tipo.addEventListener("change", () => {
    aplicar.checked = tipo.value === "HISTORICO";
  });

  [anio, edad, tipo, salario, cuotas].forEach((control) => {
    const clave = control.dataset.provenanceKey;
    if (clave && camposEditadosPreviewComprobante.has(clave)) {
      control.dataset.provenance = "EDITADO_USUARIO";
      control.title = "Editado por ti durante la revisión de la importación.";
    } else {
      control.dataset.provenance = "DETECTADO";
    }
  });

  return fila;
}


function configurarVistaPreviewComprobante(numeroPaso = 1) {
  pasoVistaPreviewComprobante = Number(numeroPaso) || 1;

  document
    .querySelectorAll("#modal-import-comprobante [data-preview-step]")
    .forEach((seccion) => {
      const pasos = (seccion.dataset.previewStep || "")
        .split(",")
        .map((valor) => Number(valor.trim()))
        .filter(Boolean);

      const visible = (
        pasoVistaPreviewComprobante === 1
        || pasos.includes(pasoVistaPreviewComprobante)
      );

      seccion.classList.toggle("d-none", !visible);
    });
}


function obtenerCuotasAnioActualReferencia(referencia) {
  if (referencia.cuotas_anio_actual !== null && referencia.cuotas_anio_actual !== undefined) {
    return referencia.cuotas_anio_actual;
  }

  const registroActual = (referencia.registros || []).find((registro) => (
    registro.anio === ANIO_ACTUAL
    && registro.tipo !== "PROYECTADO"
  ));

  return registroActual ? registroActual.cuotas : null;
}


function sincronizarCuotaAnioActualPreviewConHistorial() {
  const control = document.getElementById("preview-comprobante-cuotas-anio-actual");
  if (!control || control.value === "") return;

  const filaActual = Array.from(
    document.querySelectorAll("#preview-comprobante-registros tr"),
  ).find((fila) => (
    Number(fila.dataset.anio) === ANIO_ACTUAL
    && fila.querySelector(".preview-comprobante-tipo")?.value !== "PROYECTADO"
  ));

  const campoCuotas = filaActual?.querySelector(".preview-comprobante-cuotas-anio");
  if (campoCuotas) campoCuotas.value = control.value;
}


function leerNumeroOpcionalPreview(id) {
  const valor = document.getElementById(id)?.value ?? "";
  return valor === "" ? null : Number(valor);
}


function renderizarPreviewComprobante(
  referencia,
  numeroPaso = 1,
  camposEditados = [],
  origenesPersona = {},
  origenesCuotas = {},
) {
  borradorImportacionComprobante = structuredClone(referencia);
  camposEditadosPreviewComprobante = new Set(camposEditados || []);
  previewComprobanteFueEditado = camposEditadosPreviewComprobante.size > 0;

  const campos = {
    "preview-comprobante-primer-nombre": [referencia.primer_nombre, "primer_nombre"],
    "preview-comprobante-segundo-nombre": [referencia.segundo_nombre, "segundo_nombre"],
    "preview-comprobante-primer-apellido": [referencia.primer_apellido, "primer_apellido"],
    "preview-comprobante-segundo-apellido": [referencia.segundo_apellido, "segundo_apellido"],
    "preview-comprobante-apellido-casada": [referencia.apellido_casada, "apellido_casada"],
    "preview-comprobante-cedula": [referencia.cedula, "cedula"],
    "preview-comprobante-seguro-social": [referencia.numero_seguro_social, "numero_seguro_social"],
    "preview-comprobante-fecha-nacimiento": [referencia.fecha_nacimiento, "fecha_nacimiento"],
    "preview-comprobante-sexo": [referencia.sexo, "sexo"],
    "preview-comprobante-fecha-ingreso": [referencia.fecha_ingreso_css, "fecha_ingreso_css"],
    "preview-comprobante-sistema": [referencia.sistema_elegido || "NO_IDENTIFICADO", "sistema"],
  };

  Object.entries(campos).forEach(([id, [valor, campoPersona]]) => {
    const control = document.getElementById(id);
    if (control) control.value = valor || (id === "preview-comprobante-sistema" ? "NO_IDENTIFICADO" : "");
    marcarEstadoDeteccion(
      id,
      valor,
      camposEditadosPreviewComprobante.has(id),
      origenesPersona?.[campoPersona] || null,
    );
  });


  const cuotasAnioActual = obtenerCuotasAnioActualReferencia(referencia);
  document.getElementById("preview-comprobante-cuotas").value = referencia.cuotas_historicas ?? "";
  document.getElementById("preview-comprobante-cuotas-anio-actual").value = cuotasAnioActual ?? "";
  marcarEstadoDeteccion(
    "preview-comprobante-cuotas",
    referencia.cuotas_historicas,
    camposEditadosPreviewComprobante.has("preview-comprobante-cuotas"),
    origenesCuotas?.cuotas_totales || null,
  );
  marcarEstadoDeteccion(
    "preview-comprobante-cuotas-anio-actual",
    cuotasAnioActual,
    camposEditadosPreviewComprobante.has("preview-comprobante-cuotas-anio-actual"),
    origenesCuotas?.cuotas_anio_actual || null,
  );

  const contextoCuotas = document.getElementById("preview-comprobante-cuotas-contexto");
  if (contextoCuotas) {
    const acreditadas = Number(referencia.cuotas_historicas || 0);
    const acumuladas = Number(referencia.total_cuotas_acumuladas || 0);
    const hayProyectadas = acumuladas > acreditadas;
    contextoCuotas.textContent = hayProyectadas
      ? `El comprobante también muestra ${acumuladas} cuotas acumuladas al incluir períodos proyectados. Para el Paso 2 se conservan ${acreditadas} cuotas ya acreditadas.`
      : "";
    contextoCuotas.classList.toggle("d-none", !hayProyectadas);
  }
  document.getElementById("preview-comprobante-edad-retiro").value = referencia.edad_retiro_elegida ?? "";
  const campoMontoReferencia = document.getElementById("preview-comprobante-monto");
  campoMontoReferencia.value = formatearNumeroMonetario(referencia.monto_estimado_prestacion ?? 0);
  configurarCampoMonetario(campoMontoReferencia);
  document.getElementById("preview-comprobante-fecha").value = referencia.fecha_comprobante || "";
  document.getElementById("preview-comprobante-prestacion").value = referencia.prestacion_esperada || "";

  const cuerpo = document.getElementById("preview-comprobante-registros");
  cuerpo.replaceChildren();
  (referencia.registros || []).forEach((registro) => cuerpo.appendChild(crearFilaPreviewComprobante(registro)));
  document.getElementById("preview-comprobante-registros-contador").textContent = `${(referencia.registros || []).length} registros`;

  const advertencias = document.getElementById("advertencias-import-comprobante");
  const mensajes = Array.isArray(referencia.advertencias) ? referencia.advertencias : [];
  advertencias.textContent = mensajes.join(" ");
  advertencias.classList.toggle("d-none", mensajes.length === 0);

  actualizarApellidoCasadaPreview();
  configurarVistaPreviewComprobante(numeroPaso);
  establecerEdicionPreviewComprobante(false);
  obtenerModalBootstrap("modal-import-comprobante")?.show();
}

async function analizarComprobanteImportacion() {
  // El análisis produce un borrador revisable; nada se confirma en la simulación
  // hasta que el usuario acepte explícitamente la vista previa.
  ocultarEstadoImportacion("estado-comprobante-importacion");
  const input = document.getElementById("import-comprobante-pdf");
  const archivo = input.files?.[0];

  if (!archivo) {
    mostrarEstadoImportacion("estado-comprobante-importacion", "Selecciona primero el comprobante que deseas analizar.", "danger");
    return;
  }

  const boton = document.getElementById("btn-analizar-comprobante-importacion");
  const procesamiento = window.ProcesamientoAdjuntos.iniciar({
    boton,
    input,
    estado: document.getElementById("estado-comprobante-importacion"),
  });
  if (!procesamiento) return;

  try {
    const datos = new FormData();
    datos.append("archivo", archivo);
    const respuesta = await fetch("/api/simulacion/referencia-mi-retiro-seguro", { method: "POST", body: datos });
    let contenido = null;
    try { contenido = await respuesta.json(); } catch { contenido = null; }

    if (!respuesta.ok) {
      mostrarEstadoImportacion(
        "estado-comprobante-importacion",
        mensajeErrorImportacion(contenido, "No fue posible analizar el comprobante."),
        "danger",
      );
      return;
    }

    contenido.nombre_archivo_origen = archivo.name;
    renderizarPreviewComprobante(contenido, 1, []);
  } catch {
    mostrarEstadoImportacion("estado-comprobante-importacion", "No fue posible comunicarse con el servidor.", "danger");
  } finally {
    window.ProcesamientoAdjuntos.finalizar(procesamiento);
  }
}


function leerRegistrosPreviewComprobante() {
  return Array.from(document.querySelectorAll("#preview-comprobante-registros tr")).map((fila) => ({
    aplicar_historial: fila.querySelector(".preview-comprobante-aplicar").checked,
    anio_origen: Number(fila.dataset.anio),
    anio: Number(fila.querySelector(".preview-comprobante-anio").value),
    edad: Number(fila.querySelector(".preview-comprobante-edad").value),
    tipo: fila.querySelector(".preview-comprobante-tipo").value,
    salario_anual: obtenerValorMonetario(
      fila.querySelector(".preview-comprobante-salario").value || 0,
    ),
    cuotas: Number(fila.querySelector(".preview-comprobante-cuotas-anio").value || 0),
  }));
}


function confirmarComprobanteImportacion() {
  if (!borradorImportacionComprobante) return;

  sincronizarCuotaAnioActualPreviewConHistorial();
  const registrosPreview = leerRegistrosPreviewComprobante();
  const sistema = document.getElementById("preview-comprobante-sistema").value;
  const prestacion = document.getElementById("preview-comprobante-prestacion").value.trim();
  const texto = (id) => document.getElementById(id)?.value.trim() || null;

  const referencia = {
    ...borradorImportacionComprobante,
    primer_nombre: texto("preview-comprobante-primer-nombre"),
    segundo_nombre: texto("preview-comprobante-segundo-nombre"),
    primer_apellido: texto("preview-comprobante-primer-apellido"),
    segundo_apellido: texto("preview-comprobante-segundo-apellido"),
    apellido_casada: document.getElementById("preview-comprobante-sexo").value === "F" ? texto("preview-comprobante-apellido-casada") : null,
    cedula: texto("preview-comprobante-cedula"),
    numero_seguro_social: texto("preview-comprobante-seguro-social"),
    fecha_nacimiento: document.getElementById("preview-comprobante-fecha-nacimiento").value || null,
    sexo: document.getElementById("preview-comprobante-sexo").value || null,
    fecha_ingreso_css: document.getElementById("preview-comprobante-fecha-ingreso").value || null,
    sistema_elegido: sistema,
    sistema_elegido_nombre: textoSistemaImportado(sistema),
    cuotas_historicas: leerNumeroOpcionalPreview("preview-comprobante-cuotas"),
    cuotas_anio_actual: leerNumeroOpcionalPreview("preview-comprobante-cuotas-anio-actual"),
    edad_retiro_elegida: Number(document.getElementById("preview-comprobante-edad-retiro").value || 0) || null,
    monto_estimado_prestacion: obtenerValorMonetario(document.getElementById("preview-comprobante-monto").value || 0),
    fecha_comprobante: document.getElementById("preview-comprobante-fecha").value || null,
    prestacion_esperada: prestacion || null,
    naturaleza_prestacion: naturalezaPrestacionImportada(prestacion),
    registros: registrosPreview.map(({ aplicar_historial, anio_origen, ...registro }) => registro),
  };

  const simulacion = obtenerSimulacion();
  simulacion.campos_editados_importacion_comprobante = Array.from(
    camposEditadosPreviewComprobante,
  );
  simulacion.referencia_mi_retiro_seguro = referencia;
  simulacion.importacion_comprobante_confirmada = true;
  simulacion.modo_datos_personales = "MI_RETIRO_SEGURO";
  simulacion.origen_persona = previewComprobanteFueEditado
    ? "MI_RETIRO_SEGURO_EDITADO"
    : "MI_RETIRO_SEGURO";

  const origenesPersona = {
    primer_nombre: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-primer-nombre")),
    segundo_nombre: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-segundo-nombre")),
    primer_apellido: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-primer-apellido")),
    segundo_apellido: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-segundo-apellido")),
    apellido_casada: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-apellido-casada")),
    cedula: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-cedula")),
    numero_seguro_social: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-seguro-social")),
    fecha_nacimiento: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-fecha-nacimiento")),
    sexo: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-sexo")),
    fecha_ingreso_css: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-fecha-ingreso")),
    sistema: origenDesdeControlPreviewComprobante(document.getElementById("preview-comprobante-sistema")),
  };
  simulacion.origen_campos_persona = origenesPersona;

  simulacion.persona = {
    ...simulacion.persona,
    primer_nombre: referencia.primer_nombre,
    segundo_nombre: referencia.segundo_nombre,
    primer_apellido: referencia.primer_apellido,
    segundo_apellido: referencia.segundo_apellido,
    apellido_casada: referencia.apellido_casada,
    cedula: referencia.cedula,
    numero_seguro_social: referencia.numero_seguro_social,
    ...(referencia.fecha_nacimiento ? { fecha_nacimiento: referencia.fecha_nacimiento } : {}),
    ...(referencia.sexo ? { sexo: referencia.sexo } : {}),
    ...(referencia.fecha_ingreso_css ? { fecha_ingreso_css: referencia.fecha_ingreso_css } : {}),
    ...(sistema !== "NO_IDENTIFICADO" ? { sistema } : {}),
  };

  const registroActual = registrosPreview.find((registro) => registro.anio === ANIO_ACTUAL && registro.tipo !== "PROYECTADO");
  const cuotasAnioActualConfirmadas = referencia.cuotas_anio_actual ?? registroActual?.cuotas ?? null;
  simulacion.cuotas = {
    ...simulacion.cuotas,
    ...(referencia.cuotas_historicas != null ? { cuotas_totales: referencia.cuotas_historicas } : {}),
    ...(cuotasAnioActualConfirmadas != null ? { cuotas_anio_actual: cuotasAnioActualConfirmadas } : {}),
  };

  simulacion.origen_campos_cuotas = {
    ...(simulacion.origen_campos_cuotas || {}),
    cuotas_totales: origenDesdeControlPreviewComprobante(
      document.getElementById("preview-comprobante-cuotas"),
    ),
    cuotas_anio_actual: origenDesdeControlPreviewComprobante(
      document.getElementById("preview-comprobante-cuotas-anio-actual"),
    ),
  };

  const reales = registrosPreview.filter((registro) => registro.aplicar_historial);
  simulacion.origen_campos_historial = {};
  if (reales.length > 0) {
    const anioInicio = Math.min(...reales.map((registro) => registro.anio));
    // La existencia de registros importados no responde por el usuario la
    // pregunta "Disponibilidad del historial". Se conserva la información,
    // pero el selector permanece en "Seleccione una opción" hasta una
    // decisión explícita.
    simulacion.modo_historial = "";
    simulacion.modo_historial_confirmado_usuario = false;
    reales.forEach((registro) => {
      const base = `historial:${registro.anio_origen}`;
      simulacion.origen_campos_historial[String(registro.anio)] = {
        cuotas: camposEditadosPreviewComprobante.has(`${base}:cuotas`)
          ? "MI_RETIRO_SEGURO_EDITADO"
          : "MI_RETIRO_SEGURO_DETECTADO",
        salario_cotizado: camposEditadosPreviewComprobante.has(`${base}:salario`)
          ? "MI_RETIRO_SEGURO_EDITADO"
          : "MI_RETIRO_SEGURO_DETECTADO",
      };
    });
    simulacion.historial_anio_inicio_temporal = anioInicio;
    simulacion.origen_historial_anio_inicio = "CALCULADO_AUTOMATICAMENTE";
    simulacion.historial = {
      anio_inicio: anioInicio,
      anio_fin: ANIO_ACTUAL,
      cuotas_totales_referencia: referencia.cuotas_historicas || 0,
      registros: reales.map((registro) => ({ anio: registro.anio, cuotas: registro.cuotas, salario_cotizado: registro.salario_anual })),
    };
  }

  invalidarResultadosPorImportacion(simulacion);
  guardarSimulacion(simulacion);

  restaurarDatosPersonales(simulacion);
  restaurarDatosCuotas(simulacion);
  if (typeof inicializarHistorialSalarial === "function") inicializarHistorialSalarial();

  mostrarEstadoImportacion(
    "estado-comprobante-importacion",
    `Datos importados desde Mi Retiro Seguro. Revisa cualquier campo pendiente antes de continuar.`,
    "success",
  );
  document.getElementById("acciones-comprobante-importado")?.classList.remove("d-none");
  actualizarDocumentoImportadoPersistente("COMPROBANTE", simulacion);
  obtenerModalBootstrap("modal-import-comprobante").hide();
  restaurarModoDatosPersonales(simulacion);

  if (typeof prepararComparacionReferenciaMiRetiroGuardada === "function") prepararComparacionReferenciaMiRetiroGuardada();
}

function quitarComprobanteImportacion() {
  const simulacion = obtenerSimulacion();
  simulacion.referencia_mi_retiro_seguro = null;
  simulacion.importacion_comprobante_confirmada = false;
  simulacion.modo_datos_personales = "MANUAL";
  simulacion.origen_persona = "MANUAL";
  simulacion.origen_campos_persona = {};
  simulacion.origen_campos_cuotas = {};
  simulacion.origen_campos_historial = {};
  simulacion.campos_editados_importacion_comprobante = [];
  guardarSimulacion(simulacion);

  document.getElementById("import-comprobante-pdf").value = "";
  actualizarEstadoBotonAnalizarComprobante();
  ocultarEstadoImportacion("estado-comprobante-importacion");
  document.getElementById("acciones-comprobante-importado")?.classList.add("d-none");
  actualizarDocumentoImportadoPersistente("COMPROBANTE", simulacion);
  restaurarModoDatosPersonales(simulacion);
  if (typeof restaurarDatosCuotas === "function") {
    restaurarDatosCuotas(simulacion);
  }
}

function revisarComprobanteImportado(numeroPaso = 1) {
  const simulacion = obtenerSimulacion();
  if (simulacion.referencia_mi_retiro_seguro) {
    renderizarPreviewComprobante(
      simulacion.referencia_mi_retiro_seguro,
      numeroPaso,
      simulacion.campos_editados_importacion_comprobante || [],
      simulacion.origen_campos_persona || {},
      simulacion.origen_campos_cuotas || {},
    );
  }
}


function actualizarEstadoBotonAnalizarFichaDigital() {
  const input = document.getElementById("import-ficha-digital-pdf");
  const boton = document.getElementById("btn-analizar-ficha-digital-importacion");
  if (!boton) return;
  boton.disabled = !(input?.files?.length);
}


function establecerEdicionPreviewFicha(habilitada) {
  edicionPreviewFichaHabilitada = habilitada;
  const modal = document.getElementById("modal-import-ficha-digital");
  if (!modal) return;

  modal.querySelectorAll(".modal-body input").forEach((control) => {
    if (control.type === "checkbox") {
      control.disabled = control.dataset.importedLocked === "true" || !habilitada;
    } else {
      control.readOnly = !habilitada;
    }
  });

  modal.querySelectorAll(".modal-body select").forEach((control) => {
    control.disabled = !habilitada;
  });

  const boton = document.getElementById("btn-editar-import-ficha");
  if (boton) boton.textContent = habilitada ? "Finalizar edición" : "Editar campos";

  const importar = document.getElementById("btn-confirmar-import-ficha");
  if (importar) importar.disabled = habilitada;

  const estado = document.getElementById("estado-edicion-ficha");
  if (estado) {
    estado.textContent = habilitada ? "Editando" : "Modo revisión";
    estado.className = `badge rounded-pill ${habilitada ? "text-bg-primary" : "text-bg-secondary"}`;
  }
}


function alternarEdicionPreviewFicha() {
  const habilitar = !edicionPreviewFichaHabilitada;
  establecerEdicionPreviewFicha(habilitar);
}


function registrarEdicionCampoPreviewFicha(control) {
  if (!edicionPreviewFichaHabilitada || !control) return;
  const clave = control.dataset.provenanceKey;
  if (!clave) return;
  camposEditadosPreviewFicha.add(clave);
  previewFichaFueEditado = true;
  control.dataset.provenance = "EDITADO_USUARIO";
  control.title = "Editado por ti durante la revisión de la Ficha Digital.";
}


// ============================================================
// Ficha Digital
// ============================================================

function registroFichaImportadoAutomaticamente(registro) {
  return Boolean(
    registro
    && registro.estado !== "SIN_INFORMACION"
    && registro.salario !== null
    && registro.salario !== undefined
  );
}


function crearFilaPreviewFicha(registro, esMasReciente) {
  const fila = document.createElement("tr");
  fila.dataset.anio = String(registro.anio);
  fila.dataset.mes = String(registro.mes);

  const mes = document.createElement("select");
  mes.className = "form-select form-select-sm preview-ficha-mes";
  MESES_IMPORTACION.forEach((nombre, indice) => {
    const opcion = document.createElement("option");
    opcion.value = String(indice + 1);
    opcion.textContent = nombre;
    mes.appendChild(opcion);
  });
  mes.value = String(registro.mes);
  mes.setAttribute("aria-label", `Mes del salario detectado ${registro.anio}-${String(registro.mes).padStart(2, "0")}`);
  mes.dataset.provenanceKey = `ficha:${registro.anio}:${registro.mes}:mes`;
  mes.dataset.provenance = camposEditadosPreviewFicha.has(mes.dataset.provenanceKey) ? "EDITADO_USUARIO" : "DETECTADO";

  const salarioGrupo = document.createElement("div");
  salarioGrupo.className = "input-group input-group-sm";
  const prefijo = document.createElement("span");
  prefijo.className = "input-group-text";
  prefijo.textContent = "B/.";
  const salario = document.createElement("input");
  salario.type = "text";
  salario.className = "form-control preview-ficha-salario money-input";
  salario.value = formatearNumeroMonetario(registro.salario);
  salario.setAttribute("aria-label", `Salario detectado de ${MESES_IMPORTACION[registro.mes - 1]} ${registro.anio}`);
  salario.dataset.provenanceKey = `ficha:${registro.anio}:${registro.mes}:salario`;
  salario.dataset.provenance = camposEditadosPreviewFicha.has(salario.dataset.provenanceKey) ? "EDITADO_USUARIO" : "DETECTADO";
  salarioGrupo.append(prefijo, salario);
  configurarCampoMonetario(salario);

  const estado = document.createElement("select");
  estado.className = "form-select form-select-sm preview-ficha-estado";
  estado.innerHTML = `
    <option value="COMPLETO">Completo</option>
    <option value="PARCIAL">Parcial</option>
    <option value="SIN_INFORMACION">Sin información</option>
  `;
  estado.value = registro.estado || "COMPLETO";
  estado.setAttribute("aria-label", `Estado del salario de ${MESES_IMPORTACION[registro.mes - 1]} ${registro.anio}`);
  estado.dataset.provenanceKey = `ficha:${registro.anio}:${registro.mes}:estado`;
  estado.dataset.provenance = camposEditadosPreviewFicha.has(estado.dataset.provenanceKey) ? "EDITADO_USUARIO" : "DETECTADO";

  const cuota = document.createElement("input");
  cuota.type = "checkbox";
  cuota.className = "form-check-input preview-ficha-cuota";

  const registroImportadoAutomaticamente =
    registroFichaImportadoAutomaticamente(registro);

  cuota.checked = registroImportadoAutomaticamente || Boolean(registro.cuota_acreditada);
  cuota.defaultChecked = cuota.checked;
  cuota.disabled = registroImportadoAutomaticamente;
  if (registroImportadoAutomaticamente) {
    cuota.setAttribute("checked", "checked");
    cuota.setAttribute("aria-checked", "true");
    cuota.dataset.importedLocked = "true";
    fila.classList.add("data-row-imported");
    fila.dataset.dataOrigin = "imported";
  }
  cuota.setAttribute("aria-label", `Cuota acreditada de ${MESES_IMPORTACION[registro.mes - 1]} ${registro.anio}`);

  if (esMasReciente) {
    estado.title = "Revisa si el último mes detectado está completo o parcial antes de importar.";
    estado.setAttribute(
      "aria-label",
      `Estado del salario de ${MESES_IMPORTACION[registro.mes - 1]} ${registro.anio}. Revisa si el último mes detectado está completo o parcial.`,
    );
  }

  const controles = [mes, salarioGrupo, estado, cuota];

  controles.forEach((control) => {
    const celda = document.createElement("td");
    celda.appendChild(control);
    fila.appendChild(celda);
  });

  const celdaProcedencia = document.createElement("td");
  const clavesProcedencia = [mes, salario, estado]
    .map((control) => control.dataset.provenanceKey)
    .filter(Boolean);
  const fueEditado = clavesProcedencia.some((clave) => camposEditadosPreviewFicha.has(clave));
  const etiquetaProcedencia = document.createElement("span");
  etiquetaProcedencia.className = `data-provenance-badge ${fueEditado ? "edited" : "detected"}`;
  etiquetaProcedencia.textContent = fueEditado ? "Editado por ti" : "Detectado";
  celdaProcedencia.appendChild(etiquetaProcedencia);
  fila.appendChild(celdaProcedencia);

  return fila;
}


function renderizarPreviewFichaDigital(resumen, camposEditados = []) {
  borradorImportacionFichaDigital = structuredClone(resumen);
  camposEditadosPreviewFicha = new Set(camposEditados || []);
  previewFichaFueEditado = camposEditadosPreviewFicha.size > 0;
  const cuerpo = document.getElementById("preview-ficha-digital-registros");
  cuerpo.replaceChildren();

  const anioFicha = anioFichaDigital(resumen);
  const registros = (resumen.registros || []).filter(
    (registro) => Number(registro.anio) === anioFicha,
  );
  borradorImportacionFichaDigital.registros = structuredClone(registros);
  const ultimo = registros.length ? registros[registros.length - 1] : null;
  registros.forEach((registro) => {
    const esMasReciente = ultimo && registro.anio === ultimo.anio && registro.mes === ultimo.mes;
    cuerpo.appendChild(crearFilaPreviewFicha(registro, esMasReciente));
  });

  const advertencias = document.getElementById("advertencias-import-ficha");
  const mensajes = Array.isArray(resumen.advertencias) ? resumen.advertencias : [];
  advertencias.textContent = mensajes.join(" ");
  advertencias.classList.toggle("d-none", mensajes.length === 0);

  establecerEdicionPreviewFicha(false);
  obtenerModalBootstrap("modal-import-ficha-digital").show();
}


async function analizarFichaDigitalImportacion() {
  // La ficha digital sigue el mismo patrón de borrador: procesar, revisar,
  // resolver vigencia y confirmar antes de escribir en sessionStorage.
  ocultarEstadoImportacion("estado-ficha-digital-importacion");
  const input = document.getElementById("import-ficha-digital-pdf");
  const archivo = input.files?.[0];

  if (!archivo) {
    mostrarEstadoImportacion("estado-ficha-digital-importacion", "Selecciona primero el documento de Ficha Digital que deseas analizar.", "danger");
    return;
  }

  const boton = document.getElementById("btn-analizar-ficha-digital-importacion");
  const procesamiento = window.ProcesamientoAdjuntos.iniciar({
    boton,
    input,
    estado: document.getElementById("estado-ficha-digital-importacion"),
  });
  if (!procesamiento) return;

  try {
    const datos = new FormData();
    datos.append("archivo", archivo);
    const respuesta = await fetch("/api/simulacion/ficha-digital", { method: "POST", body: datos });
    let contenido = null;
    try { contenido = await respuesta.json(); } catch { contenido = null; }

    if (!respuesta.ok) {
      mostrarEstadoImportacion(
        "estado-ficha-digital-importacion",
        mensajeErrorImportacion(contenido, "No fue posible analizar la Ficha Digital."),
        "danger",
      );
      return;
    }

    contenido.nombre_archivo_origen = archivo.name;
    const vigencia = evaluarVigenciaFichaDigital(contenido);
    if (vigencia.requiereDecision) {
      mostrarDecisionVigenciaFichaDigital(contenido);
      return;
    }
    renderizarPreviewFichaDigital(contenido, []);
  } catch {
    mostrarEstadoImportacion("estado-ficha-digital-importacion", "No fue posible comunicarse con el servidor.", "danger");
  } finally {
    window.ProcesamientoAdjuntos.finalizar(procesamiento);
  }
}


function leerRegistrosPreviewFicha() {
  return Array.from(document.querySelectorAll("#preview-ficha-digital-registros tr")).map((fila) => {
    const cuota = fila.querySelector(".preview-ficha-cuota");

    return {
      anio: Number(fila.dataset.anio || anioFichaDigital(borradorImportacionFichaDigital) || ANIO_ACTUAL),
      mes: Number(fila.querySelector(".preview-ficha-mes").value),
      salario: obtenerValorMonetario(
        fila.querySelector(".preview-ficha-salario").value || 0,
      ),
      estado: fila.querySelector(".preview-ficha-estado").value,
      cuota_acreditada: cuota.dataset.importedLocked === "true" || cuota.checked,
    };
  });
}


async function confirmarFichaDigitalImportacion() {
  if (!borradorImportacionFichaDigital) return;

  const anioFicha = anioFichaDigital(borradorImportacionFichaDigital);
  const registros = leerRegistrosPreviewFicha().filter(
    (registro) => Number(registro.anio) === anioFicha,
  );
  const actuales = registros;
  const simulacion = obtenerSimulacion();

  simulacion.ficha_digital_importada = {
    registros,
    anio_mas_reciente: borradorImportacionFichaDigital.anio_mas_reciente,
    mes_mas_reciente: borradorImportacionFichaDigital.mes_mas_reciente,
    advertencias: borradorImportacionFichaDigital.advertencias || [],
    nombre_archivo_origen: borradorImportacionFichaDigital.nombre_archivo_origen || null,
    fecha_referencia: borradorImportacionFichaDigital.fecha_referencia || null,
    fecha_referencia_confiable: Boolean(borradorImportacionFichaDigital.fecha_referencia_confiable),
    fuente_fecha_referencia: borradorImportacionFichaDigital.fuente_fecha_referencia || null,
  };
  simulacion.importacion_ficha_digital_confirmada = true;
  simulacion.campos_editados_importacion_ficha = Array.from(camposEditadosPreviewFicha);
  simulacion.origen_campos_detalle_anio_actual = {};

  if (actuales.length > 0) {
    // La Ficha Digital aporta el detalle mensual y puede ampliar la
    // referencia del Paso 2 cuando confirma más cuotas del año actual.
    // Una referencia superior se conserva hasta una corrección explícita.
    const cuotasReferenciaPaso2 = Number(
      simulacion.cuotas?.cuotas_anio_actual || 0,
    );

    simulacion.detalle_anio_actual_habilitado = true;
    simulacion.detalle_anio_actual = {
      anio: anioFicha,
      modo_captura: "MENSUAL",
      cuotas_anio_actual_referencia: cuotasReferenciaPaso2,
      registros: actuales.map((registro) => ({
        mes: registro.mes,
        cuota_acreditada: registro.cuota_acreditada,
        estado: registro.estado,
        salario_mensual: registro.estado === "SIN_INFORMACION" ? null : registro.salario,
        primera_quincena: null,
        segunda_quincena: null,
      })),
    };

    actuales.forEach((registro) => {
      const base = `ficha:${registro.anio}:${registro.mes}`;
      const origenEstado = camposEditadosPreviewFicha.has(`${base}:estado`)
        ? "FICHA_DIGITAL_EDITADO"
        : "FICHA_DIGITAL_DETECTADO";
      const origenSalario = camposEditadosPreviewFicha.has(`${base}:salario`)
        ? "FICHA_DIGITAL_EDITADO"
        : "FICHA_DIGITAL_DETECTADO";
      simulacion.origen_campos_detalle_anio_actual[String(registro.mes)] = {
        cuota_acreditada: "FICHA_DIGITAL_DETECTADO",
        estado: origenEstado,
        ...(registro.estado !== "SIN_INFORMACION" && Number(registro.salario) >= 0
          ? { salario_mensual: origenSalario }
          : {}),
      };
    });
  }

  invalidarResultadosPorImportacion(simulacion);
  guardarSimulacion(simulacion);

  if (typeof restaurarDetalleAnioActual === "function") restaurarDetalleAnioActual();

  const cuotasMarcadas = actuales.filter((registro) => registro.cuota_acreditada).length;
  const cuotasReferenciaAntes = Number(
    obtenerSimulacion().cuotas?.cuotas_anio_actual || 0,
  );
  let cuotasActualizadasDesdeFicha = false;

  if (
    cuotasMarcadas > cuotasReferenciaAntes
    && typeof sincronizarCuotasPaso2DesdeDetalle === "function"
  ) {
    cuotasActualizadasDesdeFicha = sincronizarCuotasPaso2DesdeDetalle({
      fuente: "FICHA_DIGITAL",
    });

    if (
      cuotasActualizadasDesdeFicha
      && typeof analizarCuotas === "function"
    ) {
      await analizarCuotas(
        null,
        { mostrarMensajes: false, reportarValidez: false },
      );
    }
  }

  const simulacionActualizada = obtenerSimulacion();
  const cuotasReferenciaPaso2 = Number(
    simulacionActualizada.cuotas?.cuotas_anio_actual || 0,
  );
  const totalActualizadoPaso2 = Number(
    simulacionActualizada.cuotas?.cuotas_totales || 0,
  );
  const coincidenCuotas = cuotasMarcadas === cuotasReferenciaPaso2;
  let mensajeCuotas;

  if (cuotasActualizadasDesdeFicha) {
    mensajeCuotas = (
      `La ficha confirma ${cuotasMarcadas} cuota(s) del año actual. `
      + `El Paso 2 se actualizó automáticamente de ${cuotasReferenciaAntes} a ${cuotasReferenciaPaso2} cuota(s) este año y ahora registra ${totalActualizadoPaso2} acumuladas.`
    );
  } else if (coincidenCuotas) {
    mensajeCuotas = `Las ${cuotasMarcadas} cuota(s) mensuales importadas coinciden con el Paso 2.`;
  } else if (cuotasMarcadas < cuotasReferenciaPaso2) {
    mensajeCuotas = (
      `La Ficha Digital aporta ${cuotasMarcadas} cuota(s) confirmadas, pero el Paso 2 registra ${cuotasReferenciaPaso2}. `
      + "Se conserva la referencia superior del Paso 2; completa o revisa los meses faltantes antes de analizar el historial."
    );
  } else {
    mensajeCuotas = `La Ficha Digital aporta ${cuotasMarcadas} cuota(s) confirmadas y el Paso 2 registra ${cuotasReferenciaPaso2}. Revisa ambos valores antes de continuar.`;
  }

  mostrarEstadoImportacion(
    "estado-ficha-digital-importacion",
    `Ficha Digital importada: ${actuales.length} registro(s) del año ${anioFicha}. ${mensajeCuotas}`,
    (coincidenCuotas || cuotasActualizadasDesdeFicha) ? "success" : "warning",
  );
  document.getElementById("acciones-ficha-digital-importada")?.classList.remove("d-none");
  document.getElementById("btn-quitar-ficha-digital-importacion")?.classList.remove("d-none");
  actualizarDocumentoImportadoPersistente("FICHA", simulacion);
  obtenerModalBootstrap("modal-import-ficha-digital").hide();
  if (typeof inicializarHistorialSalarial === "function") inicializarHistorialSalarial();
}


function quitarFichaDigitalImportacion() {
  const simulacion = obtenerSimulacion();
  simulacion.ficha_digital_importada = null;
  simulacion.importacion_ficha_digital_confirmada = false;
  simulacion.detalle_anio_actual_habilitado = null;
  simulacion.detalle_anio_actual = null;
  simulacion.resumen_detalle_anio_actual = null;
  simulacion.origen_campos_detalle_anio_actual = {};
  simulacion.campos_editados_importacion_ficha = [];
  guardarSimulacion(simulacion);

  document.getElementById("import-ficha-digital-pdf").value = "";
  ocultarEstadoImportacion("estado-ficha-digital-importacion");
  document.getElementById("acciones-ficha-digital-importada")?.classList.add("d-none");
  document.getElementById("btn-quitar-ficha-digital-importacion")?.classList.add("d-none");
  actualizarDocumentoImportadoPersistente("FICHA", simulacion);
  actualizarEstadoBotonAnalizarFichaDigital();
  if (typeof restaurarDetalleAnioActual === "function") restaurarDetalleAnioActual();
}


function revisarFichaDigitalImportada() {
  const simulacion = obtenerSimulacion();
  if (simulacion.ficha_digital_importada) {
    renderizarPreviewFichaDigital(
      simulacion.ficha_digital_importada,
      simulacion.campos_editados_importacion_ficha || [],
    );
  }
}


function actualizarDocumentoImportadoPersistente(tipo, simulacion = obtenerSimulacion()) {
  const esComprobante = tipo === "COMPROBANTE";
  const contenedor = document.getElementById(
    esComprobante ? "documento-comprobante-importado" : "documento-ficha-importado",
  );
  if (!contenedor) return;

  const confirmado = esComprobante
    ? Boolean(simulacion.importacion_comprobante_confirmada && simulacion.referencia_mi_retiro_seguro)
    : Boolean(simulacion.importacion_ficha_digital_confirmada && simulacion.ficha_digital_importada);
  if (!confirmado) {
    contenedor.classList.add("d-none");
    contenedor.textContent = "";
    return;
  }

  const datos = esComprobante
    ? simulacion.referencia_mi_retiro_seguro
    : simulacion.ficha_digital_importada;
  const nombre = datos?.nombre_archivo_origen || "Documento importado anteriormente";
  contenedor.replaceChildren();

  const titulo = document.createElement("strong");
  titulo.textContent = `Importación vigente: ${nombre}`;
  const ayuda = document.createElement("span");
  ayuda.textContent = "El navegador vacía el selector de archivos al recargar por seguridad; los datos confirmados siguen disponibles y no necesitas volver a adjuntar el documento para revisarlos o utilizarlos.";
  contenedor.append(titulo, ayuda);

  if (!esComprobante) {
    const vigencia = evaluarVigenciaFichaDigital(datos);
    const periodo = document.createElement("span");
    periodo.textContent = `Último período detectado: ${vigencia.periodo}.`;
    periodo.className = "official-import-persisted-recency";
    if (vigencia.estado !== "RECIENTE") {
      periodo.classList.add("warning");
      periodo.textContent += " Considera utilizar una Ficha Digital más reciente si está disponible.";
    }
    contenedor.appendChild(periodo);
  }

  contenedor.classList.remove("d-none");
}


async function refrescarFechaReferenciaFichaPersistida() {
  const simulacion = obtenerSimulacion();
  const ficha = simulacion.ficha_digital_importada;
  if (!ficha || !simulacion.importacion_ficha_digital_confirmada) return;

  try {
    const respuesta = await fetch("/api/sistema/fecha-referencia", {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });
    if (!respuesta.ok) throw new Error("fecha no disponible");
    const referencia = await respuesta.json();
    ficha.fecha_referencia = referencia.fecha || null;
    ficha.fecha_referencia_confiable = Boolean(referencia.confiable && referencia.fecha);
    ficha.fuente_fecha_referencia = referencia.fuente || "NO_DISPONIBLE";
  } catch {
    ficha.fecha_referencia = null;
    ficha.fecha_referencia_confiable = false;
    ficha.fuente_fecha_referencia = "NO_DISPONIBLE";
  }

  guardarSimulacion(simulacion);
  actualizarDocumentoImportadoPersistente("FICHA", simulacion);
}


function restaurarResumenImportaciones() {
  const simulacion = obtenerSimulacion();
  actualizarDocumentoImportadoPersistente("COMPROBANTE", simulacion);
  actualizarDocumentoImportadoPersistente("FICHA", simulacion);

  if (simulacion.referencia_mi_retiro_seguro && simulacion.importacion_comprobante_confirmada) {
    const ref = simulacion.referencia_mi_retiro_seguro;
    mostrarEstadoImportacion(
      "estado-comprobante-importacion",
      `Comprobante confirmado: ${textoSistemaImportado(ref.sistema_elegido)} · ${ref.cuotas_historicas ?? "—"} cuotas · referencia ${formatearMoneda(ref.monto_estimado_prestacion)}.`,
      "success",
    );
    document.getElementById("acciones-comprobante-importado")?.classList.remove("d-none");
  }

  if (simulacion.ficha_digital_importada && simulacion.importacion_ficha_digital_confirmada) {
    const registros = simulacion.ficha_digital_importada.registros || [];
    const anioFicha = anioFichaDigital(simulacion.ficha_digital_importada);
    const actuales = registros.filter((registro) => Number(registro.anio) === anioFicha);
    let normalizado = false;
    actuales.forEach((registro) => {
      if (registroFichaImportadoAutomaticamente(registro) && !registro.cuota_acreditada) {
        registro.cuota_acreditada = true;
        normalizado = true;
      }
    });
    if (normalizado) guardarSimulacion(simulacion);

    const cuotasMarcadas = actuales.filter((registro) => registro.cuota_acreditada).length;
    const cuotasReferenciaPaso2 = Number(simulacion.cuotas?.cuotas_anio_actual || 0);
    const coincidenCuotas = cuotasMarcadas === cuotasReferenciaPaso2;
    const mensajeCuotas = coincidenCuotas
      ? `Las ${cuotasMarcadas} cuota(s) mensuales importadas coinciden con el Paso 2.`
      : `La Ficha Digital aporta ${cuotasMarcadas} mes(es) con datos confirmados y el Paso 2 registra ${cuotasReferenciaPaso2} cuota(s) acreditadas.`;
    mostrarEstadoImportacion(
      "estado-ficha-digital-importacion",
      `Ficha Digital importada: ${actuales.length} registro(s) del año ${anioFicha}. ${mensajeCuotas}`,
      coincidenCuotas ? "success" : "warning",
    );
    document.getElementById("acciones-ficha-digital-importada")?.classList.remove("d-none");
    document.getElementById("btn-quitar-ficha-digital-importacion")?.classList.remove("d-none");
  }
}


document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("import-comprobante-pdf")?.addEventListener("change", actualizarEstadoBotonAnalizarComprobante);
  document.getElementById("btn-analizar-comprobante-importacion")?.addEventListener("click", analizarComprobanteImportacion);
  document.getElementById("btn-editar-import-comprobante")?.addEventListener("click", alternarEdicionPreviewComprobante);
  document.getElementById("btn-confirmar-import-comprobante")?.addEventListener("click", confirmarComprobanteImportacion);
  document.getElementById("btn-revisar-comprobante-importacion")?.addEventListener("click", () => revisarComprobanteImportado(1));
  document.getElementById("btn-quitar-comprobante-importacion")?.addEventListener("click", quitarComprobanteImportacion);
  document.querySelectorAll('input[name="modo_datos_personales"]').forEach((control) => control.addEventListener("change", cambiarModoDatosPersonales));
  document.getElementById("sexo")?.addEventListener("change", actualizarApellidoCasada);
  document.getElementById("preview-comprobante-sexo")?.addEventListener("change", actualizarApellidoCasadaPreview);
  const modalComprobante = document.getElementById("modal-import-comprobante");
  ["input", "change"].forEach((tipoEvento) => {
    modalComprobante?.addEventListener(tipoEvento, (evento) => {
      const control = evento.target.closest("input, select");
      if (!control || control.type === "checkbox") return;
      registrarEdicionCampoPreviewComprobante(control);
    });
  });

  const modalFicha = document.getElementById("modal-import-ficha-digital");
  ["input", "change"].forEach((tipoEvento) => {
    modalFicha?.addEventListener(tipoEvento, (evento) => {
      const control = evento.target.closest("input, select");
      if (!control || control.type === "checkbox") return;
      registrarEdicionCampoPreviewFicha(control);
    });
  });

  document.getElementById("import-ficha-digital-pdf")?.addEventListener("change", actualizarEstadoBotonAnalizarFichaDigital);
  document.getElementById("btn-analizar-ficha-digital-importacion")?.addEventListener("click", analizarFichaDigitalImportacion);
  document.getElementById("btn-continuar-ficha-vigencia")?.addEventListener("click", continuarConFichaPendienteVigencia);
  document.getElementById("btn-seleccionar-otra-ficha-vigencia")?.addEventListener("click", seleccionarOtraFichaPorVigencia);
  document.getElementById("btn-editar-import-ficha")?.addEventListener("click", alternarEdicionPreviewFicha);
  document.getElementById("btn-confirmar-import-ficha")?.addEventListener("click", confirmarFichaDigitalImportacion);
  document.getElementById("btn-revisar-ficha-digital-importacion")?.addEventListener("click", revisarFichaDigitalImportada);
  document.getElementById("btn-quitar-ficha-digital-importacion")?.addEventListener("click", quitarFichaDigitalImportacion);

  actualizarEstadoBotonAnalizarComprobante();
  actualizarEstadoBotonAnalizarFichaDigital();
  restaurarModoDatosPersonales();
  actualizarApellidoCasada();
  restaurarResumenImportaciones();
  refrescarFechaReferenciaFichaPersistida();
});
