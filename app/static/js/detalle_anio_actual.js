"use strict";


/* ============================================================
   Mi Retiro Proyectado
   Detalle salarial del año actual
   ============================================================ */

/*
 * Este módulo permite registrar información mensual o quincenal
 * disponible en la Ficha Digital sin confundir salario visible,
 * cuota acreditada y períodos todavía parciales.
 */


const MESES_DETALLE_ANIO = [
  "Enero",
  "Febrero",
  "Marzo",
  "Abril",
  "Mayo",
  "Junio",
  "Julio",
  "Agosto",
  "Septiembre",
  "Octubre",
  "Noviembre",
  "Diciembre",
];


// ============================================================
// Estado y utilidades
// ============================================================

function estaHabilitadoDetalleAnioActual() {
  return document.getElementById(
    "usar_detalle_anio_actual",
  ).value === "true";
}


function obtenerModoDetalleAnioActual() {
  return document.getElementById(
    "modo_detalle_anio_actual",
  ).value;
}


function obtenerCantidadMesesDisponibles() {
  return new Date().getMonth() + 1;
}


function formatearMesIsoLegible(valor) {
  if (!/^\d{4}-\d{2}$/.test(valor || "")) {
    return "—";
  }

  const mes = Number(valor.slice(5, 7));
  const anio = valor.slice(0, 4);

  return `${MESES_DETALLE_ANIO[mes - 1]} ${anio}`;
}


function valorMonetarioOpcional(campo) {
  const texto = campo.value.trim();

  if (!texto) {
    return null;
  }

  const valor = obtenerValorMonetario(texto);

  if (!Number.isFinite(valor) || valor < 0) {
    throw new Error(
      `El valor de ${campo.getAttribute("aria-label")} no es válido.`,
    );
  }

  return valor;
}


function origenCampoDetalle(mes, campo) {
  const simulacion = obtenerSimulacion();
  return simulacion.origen_campos_detalle_anio_actual?.[String(mes)]?.[campo] || null;
}


function marcarCampoDetalleImportado(control, mes, campo) {
  if (!control) return;

  const origenMes = obtenerSimulacion()
    .origen_campos_detalle_anio_actual?.[String(mes)] || {};
  const origenDirecto = origenCampoDetalle(mes, campo);
  const cuotaDeMesImportado = (
    control.type === "checkbox"
    && Boolean(origenMes.salario_mensual || origenMes.estado || origenDirecto)
  );

  if (!origenDirecto && !cuotaDeMesImportado) return;

  if (control.type === "checkbox") {
    // Si el mes fue importado con salario/estado utilizable, su cuota forma
    // parte del registro documental confirmado aunque una sesión antigua no
    // hubiera guardado metadata específica para la casilla.
    control.checked = true;
    control.defaultChecked = true;
    control.setAttribute("checked", "checked");
    control.setAttribute("aria-checked", "true");
    control.disabled = true;
    control.dataset.importedLocked = "true";
  } else if (control.tagName === "SELECT") {
    control.disabled = true;
  } else {
    control.readOnly = true;
  }

  control.classList.add("detail-field-imported");
  control.setAttribute("aria-readonly", "true");
  control.title = "Dato confirmado desde Ficha Digital. Usa Revisar importación si necesitas corregirlo.";
}


function filaDetalleTieneDatosImportados(mes) {
  const simulacion = obtenerSimulacion();
  const origen = simulacion.origen_campos_detalle_anio_actual?.[String(mes)] || {};
  return Object.values(origen).some(Boolean);
}


function actualizarProcedenciaFilaDetalle(fila) {
  if (!fila) return;
  const mes = Number(fila.dataset.mes || 0);
  const etiqueta = fila.querySelector(".detail-row-provenance");
  if (!etiqueta || !mes) return;

  const origenMes = obtenerSimulacion()
    .origen_campos_detalle_anio_actual?.[String(mes)] || {};
  const origenes = Object.values(origenMes).filter(Boolean);
  const tieneImportado = origenes.some((origen) => String(origen).startsWith("FICHA_DIGITAL"));
  const tieneEditado = origenes.some((origen) => String(origen).includes("EDITADO"));

  let codigo = "NO_DETECTADO";
  if (tieneEditado) {
    codigo = "EDITADO_USUARIO";
  } else if (tieneImportado) {
    codigo = "DETECTADO";
  } else {
    const check = fila.querySelector(".detalle-cuota-acreditada");
    const mensual = fila.querySelector(".detalle-col-mensual .detalle-salario-input");
    const primera = fila.querySelectorAll(".detalle-col-quincenal .detalle-salario-input")[0];
    const segunda = fila.querySelectorAll(".detalle-col-quincenal .detalle-salario-input")[1];
    const estado = fila.querySelector(".detalle-estado-salario");
    const tieneDatoManual = Boolean(
      check?.checked
      || mensual?.value.trim()
      || primera?.value.trim()
      || segunda?.value.trim()
      || (estado?.value && estado.value !== "SIN_INFORMACION")
    );
    if (tieneDatoManual) codigo = "COMPLETADO_MANUAL";
  }

  etiqueta.textContent = typeof textoProcedenciaDato === "function"
    ? textoProcedenciaDato(codigo)
    : codigo;
  etiqueta.className = `data-provenance-badge detail-row-provenance ${
    typeof claseProcedenciaDato === "function" ? claseProcedenciaDato(codigo) : ""
  }`;
  fila.dataset.provenance = codigo;
}


// ============================================================
// Tabla de captura
// ============================================================

function crearCampoDineroDetalle(etiqueta) {
  const grupo = document.createElement("div");
  grupo.className = "input-group input-group-sm";

  const prefijo = document.createElement("span");
  prefijo.className = "input-group-text";
  prefijo.textContent = "B/.";

  const campo = document.createElement("input");
  campo.type = "text";
  campo.inputMode = "decimal";
  campo.className = "form-control money-input detalle-salario-input";
  campo.setAttribute("aria-label", etiqueta);

  configurarCampoMonetario(campo);

  grupo.append(prefijo, campo);

  return { grupo, campo };
}


function crearFilaDetalleAnioActual(mes, datosGuardados) {
  const fila = document.createElement("tr");
  fila.dataset.mes = String(mes);

  if (filaDetalleTieneDatosImportados(mes)) {
    fila.classList.add("data-row-imported");
    fila.dataset.dataOrigin = "imported";
  } else {
    fila.classList.add("data-row-manual");
    fila.dataset.dataOrigin = "manual";
  }

  const celdaMes = document.createElement("th");
  celdaMes.scope = "row";
  celdaMes.className = "current-year-detail-month";
  const nombreMes = document.createElement("span");
  nombreMes.textContent = MESES_DETALLE_ANIO[mes - 1];
  const procedenciaMes = document.createElement("small");
  procedenciaMes.className = "data-provenance-badge detail-row-provenance";
  procedenciaMes.setAttribute("aria-label", `Procedencia de los datos de ${MESES_DETALLE_ANIO[mes - 1]}`);
  celdaMes.append(nombreMes, procedenciaMes);

  const celdaCuota = document.createElement("td");
  const check = document.createElement("input");
  check.type = "checkbox";
  check.className = "form-check-input detalle-cuota-acreditada";
  check.setAttribute(
    "aria-label",
    `Cuota acreditada de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
  celdaCuota.appendChild(check);

  const celdaMensual = document.createElement("td");
  celdaMensual.className = "detalle-col-mensual";
  const mensual = crearCampoDineroDetalle(
    `Salario reportado de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
  mensual.campo.placeholder = "Ej.: 1,500.00";
  celdaMensual.appendChild(mensual.grupo);

  const celdaPrimera = document.createElement("td");
  celdaPrimera.className = "detalle-col-quincenal d-none";
  const primera = crearCampoDineroDetalle(
    `Primera quincena de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
  primera.campo.placeholder = "Ej.: 750.00";
  celdaPrimera.appendChild(primera.grupo);

  const celdaSegunda = document.createElement("td");
  celdaSegunda.className = "detalle-col-quincenal d-none";
  const segunda = crearCampoDineroDetalle(
    `Segunda quincena de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
  segunda.campo.placeholder = "Ej.: 750.00";
  celdaSegunda.appendChild(segunda.grupo);

  const celdaEstado = document.createElement("td");
  const selectorEstado = document.createElement("select");
  selectorEstado.className = "form-select form-select-sm detalle-estado-salario";
  selectorEstado.setAttribute(
    "aria-label",
    `Estado salarial de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
  selectorEstado.innerHTML = `
    <option value="SIN_INFORMACION">Sin información</option>
    <option value="PARCIAL">Parcial</option>
    <option value="COMPLETO">Completo</option>
  `;
  celdaEstado.appendChild(selectorEstado);

  const celdaTotal = document.createElement("td");
  const total = document.createElement("strong");
  total.className = "detalle-total-mes";
  total.textContent = "B/.0.00";
  celdaTotal.appendChild(total);

  fila.append(
    celdaMes,
    celdaCuota,
    celdaMensual,
    celdaPrimera,
    celdaSegunda,
    celdaEstado,
    celdaTotal,
  );

  if (datosGuardados) {
    check.checked = Boolean(datosGuardados.cuota_acreditada);
    selectorEstado.value = datosGuardados.estado || "SIN_INFORMACION";

    if (datosGuardados.salario_mensual !== null
        && datosGuardados.salario_mensual !== undefined) {
      mensual.campo.value = formatearNumeroMonetario(
        datosGuardados.salario_mensual,
      );
    }

    if (datosGuardados.primera_quincena !== null
        && datosGuardados.primera_quincena !== undefined) {
      primera.campo.value = formatearNumeroMonetario(
        datosGuardados.primera_quincena,
      );
    }

    if (datosGuardados.segunda_quincena !== null
        && datosGuardados.segunda_quincena !== undefined) {
      segunda.campo.value = formatearNumeroMonetario(
        datosGuardados.segunda_quincena,
      );
    }
  }

  marcarCampoDetalleImportado(check, mes, "cuota_acreditada");
  marcarCampoDetalleImportado(mensual.campo, mes, "salario_mensual");
  marcarCampoDetalleImportado(selectorEstado, mes, "estado");

  [
    check,
    mensual.campo,
    primera.campo,
    segunda.campo,
    selectorEstado,
  ].forEach((control) => {
    control.addEventListener("input", () => {
      actualizarEstadoFilaDetalle(fila);
      actualizarProcedenciaFilaDetalle(fila);
      guardarBorradorDetalleAnioActual();
      invalidarDetalleAnioActual();
    });

    control.addEventListener("change", () => {
      actualizarEstadoFilaDetalle(fila);
      actualizarProcedenciaFilaDetalle(fila);
      guardarBorradorDetalleAnioActual();

      if (
        control === check
        && control.dataset.importedLocked !== "true"
      ) {
        sincronizarCuotasPaso2DesdeDetalle();
      }

      invalidarDetalleAnioActual();
    });
  });

  actualizarEstadoFilaDetalle(fila);
  actualizarProcedenciaFilaDetalle(fila);

  return fila;
}


function generarTablaDetalleAnioActual() {
  const cuerpo = document.getElementById(
    "detalle-anio-actual-body",
  );

  const simulacion = obtenerSimulacion();
  const detalle = simulacion.detalle_anio_actual || {};
  const guardados = {};

  (detalle.registros || []).forEach((registro) => {
    guardados[registro.mes] = registro;
  });

  cuerpo.replaceChildren();

  const cantidadMeses = obtenerCantidadMesesDisponibles();

  for (let mes = 1; mes <= cantidadMeses; mes += 1) {
    cuerpo.appendChild(
      crearFilaDetalleAnioActual(
        mes,
        guardados[mes] || null,
      ),
    );
  }

  actualizarColumnasModoDetalle();
  sincronizarFilaAnualDesdeDetalleLocal();
}


function actualizarColumnasModoDetalle() {
  const modo = obtenerModoDetalleAnioActual();
  const esQuincenal = modo === "QUINCENAL";

  document
    .querySelectorAll(".detalle-col-mensual")
    .forEach((elemento) => {
      elemento.classList.toggle("d-none", esQuincenal);
    });

  document
    .querySelectorAll(".detalle-col-quincenal")
    .forEach((elemento) => {
      elemento.classList.toggle("d-none", !esQuincenal);
    });

  document
    .querySelectorAll(".detalle-estado-salario")
    .forEach((selector) => {
      const fila = selector.closest("tr");
      const mes = Number(fila?.dataset.mes || 0);
      selector.disabled = esQuincenal || Boolean(origenCampoDetalle(mes, "estado"));
    });

  document
    .querySelectorAll("#detalle-anio-actual-body tr")
    .forEach(actualizarEstadoFilaDetalle);
}


function actualizarEstadoFilaDetalle(fila) {
  const modo = obtenerModoDetalleAnioActual();
  const mensual = fila.querySelector(".detalle-col-mensual input");
  const quincenas = fila.querySelectorAll(".detalle-col-quincenal input");
  const estado = fila.querySelector(".detalle-estado-salario");
  const total = fila.querySelector(".detalle-total-mes");

  let valorTotal = 0;

  if (modo === "MENSUAL") {
    const valor = obtenerValorMonetario(mensual.value || "0");
    valorTotal = Number.isFinite(valor) ? valor : 0;

    if (valorTotal > 0 && estado.value === "SIN_INFORMACION") {
      estado.value = "COMPLETO";
    }

    if (valorTotal === 0 && estado.value !== "SIN_INFORMACION") {
      estado.value = "SIN_INFORMACION";
    }
  } else {
    const primera = obtenerValorMonetario(quincenas[0].value || "0");
    const segunda = obtenerValorMonetario(quincenas[1].value || "0");
    const tienePrimera = Number.isFinite(primera) && primera > 0;
    const tieneSegunda = Number.isFinite(segunda) && segunda > 0;

    valorTotal = (tienePrimera ? primera : 0) + (tieneSegunda ? segunda : 0);

    estado.value = (
      tienePrimera && tieneSegunda
        ? "COMPLETO"
        : (tienePrimera || tieneSegunda)
          ? "PARCIAL"
          : "SIN_INFORMACION"
    );
  }

  total.textContent = formatearMoneda(valorTotal);

  fila.classList.toggle(
    "current-year-detail-partial",
    estado.value === "PARCIAL",
  );

  fila.classList.toggle(
    "current-year-detail-complete",
    estado.value === "COMPLETO",
  );
}


// ============================================================
// Lectura, persistencia y validación
// ============================================================

function leerDetalleAnioActual() {
  const modo = obtenerModoDetalleAnioActual();
  const registros = [];

  document
    .querySelectorAll("#detalle-anio-actual-body tr")
    .forEach((fila) => {
      const mes = Number(fila.dataset.mes);
      const campoCuota = fila.querySelector(".detalle-cuota-acreditada");
      const cuota = (
        campoCuota.dataset.importedLocked === "true"
        || campoCuota.checked
      );
      const estado = fila.querySelector(".detalle-estado-salario").value;
      const mensual = fila.querySelector(".detalle-col-mensual input");
      const quincenas = fila.querySelectorAll(".detalle-col-quincenal input");

      registros.push({
        mes,
        cuota_acreditada: cuota,
        estado,
        salario_mensual: (
          modo === "MENSUAL"
            ? valorMonetarioOpcional(mensual)
            : null
        ),
        primera_quincena: (
          modo === "QUINCENAL"
            ? valorMonetarioOpcional(quincenas[0])
            : null
        ),
        segunda_quincena: (
          modo === "QUINCENAL"
            ? valorMonetarioOpcional(quincenas[1])
            : null
        ),
      });
    });

  const simulacion = obtenerSimulacion();

  return {
    anio: ANIO_ACTUAL,
    modo_captura: modo,
    cuotas_anio_actual_referencia: Number(
      simulacion.cuotas?.cuotas_anio_actual || 0,
    ),
    registros,
  };
}


function resumenLocalDetalleParaHistorial() {
  const detalle = leerDetalleAnioActual();
  let cuotas = 0;
  let salarioAcreditado = 0;
  let cuotasSinSalario = 0;

  detalle.registros.forEach((registro) => {
    if (!registro.cuota_acreditada) return;

    cuotas += 1;

    if (detalle.modo_captura === "MENSUAL") {
      const salario = Number(registro.salario_mensual || 0);
      salarioAcreditado += salario;
      if (salario <= 0) cuotasSinSalario += 1;
      return;
    }

    const salarioQuincenal = (
      Number(registro.primera_quincena || 0)
      + Number(registro.segunda_quincena || 0)
    );
    salarioAcreditado += salarioQuincenal;
    if (salarioQuincenal <= 0) cuotasSinSalario += 1;
  });

  return {
    cuotas,
    salario_acreditado: salarioAcreditado,
    cuotas_sin_salario: cuotasSinSalario,
  };
}


function sincronizarFilaAnualDesdeDetalleLocal() {
  if (!estaHabilitadoDetalleAnioActual()) return;

  let resumen;
  try {
    resumen = resumenLocalDetalleParaHistorial();
  } catch {
    return;
  }

  const filaActual = document.querySelector(
    `#historial-tabla-body tr[data-anio="${ANIO_ACTUAL}"]`,
  );
  if (!filaActual) return;

  const cuotas = filaActual.querySelector(".history-input-cuotas");
  const salario = filaActual.querySelector(".history-input-salario");
  if (!cuotas || !salario) return;

  cuotas.value = String(resumen.cuotas);
  cuotas.readOnly = true;
  cuotas.dataset.sincronizadoDetalle = "true";
  cuotas.setAttribute(
    "title",
    "Sincronizado desde las cuotas confirmadas en el detalle del año actual.",
  );

  salario.value = (
    resumen.salario_acreditado > 0
    && resumen.cuotas_sin_salario === 0
  )
    ? formatearNumeroMonetario(resumen.salario_acreditado)
    : "";
  salario.readOnly = true;
  salario.dataset.sincronizadoDetalle = "true";
  salario.setAttribute(
    "title",
    "Sincronizado desde los salarios de los meses con cuota acreditada.",
  );

  if (typeof actualizarEstadoFila === "function") {
    actualizarEstadoFila(filaActual);
  }
}


function sincronizarCuotasPaso2DesdeDetalle(opciones = {}) {
  if (!estaHabilitadoDetalleAnioActual()) return false;

  let resumen;
  try {
    resumen = resumenLocalDetalleParaHistorial();
  } catch {
    return false;
  }

  const simulacion = obtenerSimulacion();
  if (!simulacion.cuotas) return false;

  const fuente = opciones.fuente || "DETALLE_MANUAL";
  const cuotasAnteriores = Number(simulacion.cuotas.cuotas_anio_actual || 0);
  if (resumen.cuotas === cuotasAnteriores) return false;

  // R23: una Ficha Digital confirmada puede aportar una fotografía más
  // reciente del año actual que Mi Retiro Seguro. Solo la usamos para
  // ampliar automáticamente la cantidad acreditada; una ficha con menos
  // meses nunca reduce silenciosamente una referencia superior del Paso 2.
  if (fuente === "FICHA_DIGITAL" && resumen.cuotas < cuotasAnteriores) {
    return false;
  }

  const totalAnterior = Number(simulacion.cuotas.cuotas_totales || 0);
  const cuotasPreviasAlAnioActual = Math.max(0, totalAnterior - cuotasAnteriores);
  const nuevoTotal = cuotasPreviasAlAnioActual + resumen.cuotas;
  const origenActualizado = fuente === "FICHA_DIGITAL"
    ? "FICHA_DIGITAL_ACTUALIZADO"
    : "DETALLE_ANIO_ACTUAL_EDITADO";

  simulacion.cuotas = {
    ...simulacion.cuotas,
    cuotas_totales: nuevoTotal,
    cuotas_anio_actual: resumen.cuotas,
  };
  if (simulacion.detalle_anio_actual) {
    simulacion.detalle_anio_actual.cuotas_anio_actual_referencia = resumen.cuotas;
  }
  simulacion.origen_campos_cuotas = {
    ...(simulacion.origen_campos_cuotas || {}),
    cuotas_totales: origenActualizado,
    cuotas_anio_actual: origenActualizado,
  };
  simulacion.resumen_cuotas = null;
  simulacion.resumen_historial = null;
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_sucgs = null;

  const campoTotal = document.getElementById("cuotas_totales");
  const campoActual = document.getElementById("cuotas_anio_actual");
  if (campoTotal) campoTotal.value = String(nuevoTotal);
  if (campoActual) campoActual.value = String(resumen.cuotas);

  guardarSimulacion(simulacion);

  const aviso = document.getElementById("detalle-cuotas-sincronizadas");
  if (aviso) {
    aviso.textContent = fuente === "FICHA_DIGITAL"
      ? (
        `La Ficha Digital confirmada identifica ${resumen.cuotas} cuota(s) acreditada(s) en el año actual. `
        + `El Paso 2 se actualizó de ${cuotasAnteriores} a ${resumen.cuotas} y ahora registra ${nuevoTotal} cuota(s) acumuladas.`
      )
      : (
        `Actualizaste las cuotas acreditadas del año actual a ${resumen.cuotas}. `
        + `El Paso 2 se ajustó automáticamente a ${nuevoTotal} cuota(s) acumuladas usando este detalle más reciente.`
      );
    aviso.classList.remove("d-none");
  }

  return true;
}


function guardarBorradorDetalleAnioActual() {
  if (!estaHabilitadoDetalleAnioActual()) {
    return;
  }

  try {
    const simulacion = obtenerSimulacion();
    simulacion.detalle_anio_actual_habilitado = true;
    simulacion.detalle_anio_actual = leerDetalleAnioActual();
    guardarSimulacion(simulacion);
    sincronizarFilaAnualDesdeDetalleLocal();
  } catch {
    // La validación visible se realiza al pulsar el botón principal.
  }
}


function invalidarDetalleAnioActual() {
  const simulacion = obtenerSimulacion();
  simulacion.resumen_detalle_anio_actual = null;
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_mixto = null;
  simulacion.resultado_sucgs = null;
  guardarSimulacion(simulacion);

  document.getElementById("resultado-detalle-anio-actual")?.classList.add("d-none");
  document.getElementById("detalle-estado-coherencia")?.classList.add("d-none");
  document.getElementById("detalle-resumen-visible")?.classList.add("d-none");
  document.getElementById("resultado-paso3")?.classList.add("d-none");

  actualizarOpcionesBaseSalarial(false);
}


function fuenteReconciliacionCuotasPaso2() {
  const simulacion = obtenerSimulacion();
  const origenes = simulacion.origen_campos_cuotas || {};
  const referenciaYaDerivadaDelDetalle = (
    origenes.cuotas_anio_actual === "DETALLE_ANIO_ACTUAL_EDITADO"
    || origenes.cuotas_totales === "DETALLE_ANIO_ACTUAL_EDITADO"
    || origenes.cuotas_anio_actual === "FICHA_DIGITAL_ACTUALIZADO"
    || origenes.cuotas_totales === "FICHA_DIGITAL_ACTUALIZADO"
  );

  const controles = Array.from(
    document.querySelectorAll("#detalle-anio-actual-body .detalle-cuota-acreditada"),
  );
  const hayCuotaManualConfirmada = controles.some((control) => (
    control.dataset.importedLocked !== "true"
    && control.checked
  ));

  if (hayCuotaManualConfirmada || referenciaYaDerivadaDelDetalle) {
    return "DETALLE_MANUAL";
  }

  const fichaConfirmada = Boolean(
    simulacion.importacion_ficha_digital_confirmada
    && simulacion.ficha_digital_importada,
  );

  if (fichaConfirmada) {
    let resumen;
    try {
      resumen = resumenLocalDetalleParaHistorial();
    } catch {
      return null;
    }
    const cuotasPaso2 = Number(simulacion.cuotas?.cuotas_anio_actual || 0);
    if (resumen.cuotas > cuotasPaso2) {
      return "FICHA_DIGITAL";
    }
  }

  return null;
}


function detallePuedeReconciliarCuotasPaso2() {
  return Boolean(fuenteReconciliacionCuotasPaso2());
}


async function validarDetalleAnioActual() {
  ocultarMensajesDetalleAnioActual();

  // R22: una cuota confirmada manualmente en este detalle es información
  // más reciente que la fotografía importada en el Paso 2. Reconciliamos
  // la referencia antes de construir el payload para que una restauración,
  // F5 o evento perdido no deje 6 meses frente a una referencia obsoleta de 5.
  const fuenteReconciliacion = fuenteReconciliacionCuotasPaso2();
  if (fuenteReconciliacion) {
    const cuotasSincronizadas = sincronizarCuotasPaso2DesdeDetalle({
      fuente: fuenteReconciliacion,
    });

    if (cuotasSincronizadas && typeof analizarCuotas === "function") {
      const cuotasRevalidadas = await analizarCuotas(
        null,
        { mostrarMensajes: false, reportarValidez: false },
      );

      if (!cuotasRevalidadas) {
        mostrarErrorDetalleAnioActual(
          "Las cuotas del año actual se actualizaron desde este detalle, pero no fue posible revalidar el Paso 2. Revisa los datos de cotización futura antes de continuar.",
        );
        return false;
      }
    }
  }

  let datos;

  try {
    datos = leerDetalleAnioActual();
  } catch (error) {
    mostrarErrorDetalleAnioActual(error.message);
    return false;
  }

  try {
    const respuesta = await fetch(
      "/api/simulacion/detalle-anio-actual",
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
      mostrarErrorDetalleAnioActual(
        obtenerMensajeError(
          contenido,
          "No fue posible validar el detalle del año actual.",
        ),
      );
      return false;
    }

    const simulacion = obtenerSimulacion();
    simulacion.detalle_anio_actual_habilitado = true;
    simulacion.detalle_anio_actual = datos;
    simulacion.resumen_detalle_anio_actual = contenido;

    if (
      contenido.cuotas_coinciden
      && contenido.ultimo_mes_cuota_acreditada
    ) {
      simulacion.ultimo_mes_cuotas_derivado = (
        contenido.ultimo_mes_cuota_acreditada
      );
    } else {
      simulacion.ultimo_mes_cuotas_derivado = null;
    }

    guardarSimulacion(simulacion);

    mostrarResumenDetalleAnioActual(contenido);

    await sincronizarDetalleConHistorial(contenido);

    actualizarOpcionesBaseSalarial(true);

    if (typeof actualizarResumenPaso3 === "function") {
      actualizarResumenPaso3();
    }

    if (!contenido.cuotas_coinciden) {
      const cuotasPaso2 = Number(
        obtenerSimulacion().cuotas?.cuotas_anio_actual || 0,
      );
      mostrarErrorDetalleAnioActual(
        `El detalle identifica ${contenido.cuotas_acreditadas_identificadas} cuota(s) acreditada(s), `
        + `pero el Paso 2 registra ${cuotasPaso2} para el año actual. `
        + "Revisa únicamente las casillas de Cuota acreditada; los salarios conocidos pueden conservarse aunque su cuota todavía no figure acreditada.",
      );
      return false;
    }

    return true;
  } catch {
    mostrarErrorDetalleAnioActual(
      "No fue posible comunicarse con el servidor.",
    );
    return false;
  }
}


function sincronizarDetalleConHistorial(resumen) {
  const filaActual = document.querySelector(
    `#historial-tabla-body tr[data-anio="${ANIO_ACTUAL}"]`,
  );

  if (!filaActual) {
    return;
  }

  const cuotas = filaActual.querySelector(".history-input-cuotas");
  const salario = filaActual.querySelector(".history-input-salario");

  cuotas.value = String(resumen.cuotas_acreditadas_identificadas || 0);
  cuotas.readOnly = true;
  cuotas.dataset.sincronizadoDetalle = "true";
  cuotas.setAttribute(
    "title",
    "Sincronizado desde las cuotas confirmadas en el detalle del año actual.",
  );

  salario.value = formatearNumeroMonetario(
    resumen.total_salario_acreditado,
  );
  salario.readOnly = true;
  salario.dataset.sincronizadoDetalle = "true";
  salario.setAttribute(
    "title",
    "Sincronizado desde los salarios de los meses con cuota acreditada.",
  );

  actualizarEstadoFila(filaActual);

  // La acción principal del Paso 3 valida el historial después de sincronizar
  // este total, evitando análisis duplicados dentro de una misma operación.
}


function liberarSalarioAnualActual() {
  const filaActual = document.querySelector(
    `#historial-tabla-body tr[data-anio="${ANIO_ACTUAL}"]`,
  );

  if (!filaActual) {
    return;
  }

  const cuotas = filaActual.querySelector(".history-input-cuotas");
  const salario = filaActual.querySelector(".history-input-salario");

  if (cuotas?.dataset.sincronizadoDetalle === "true") {
    delete cuotas.dataset.sincronizadoDetalle;
    cuotas.removeAttribute("title");
    // Fuera del detalle, las cuotas del año actual vuelven a depender del Paso 2.
    cuotas.readOnly = Boolean(obtenerSimulacion().cuotas?.cuotas_anio_actual !== undefined);
  }

  if (salario?.dataset.sincronizadoDetalle === "true") {
    salario.readOnly = false;
    delete salario.dataset.sincronizadoDetalle;
    salario.removeAttribute("title");
  }
}


// ============================================================
// Resumen y base salarial sugerida
// ============================================================

function valorResumenMoneda(valor) {
  if (valor === null || valor === undefined || valor === "") return "—";
  return Number(valor) >= 0 ? formatearMoneda(valor) : "—";
}


function valorResumenMes(valor) {
  return valor ? formatearMesIsoLegible(valor) : "—";
}


function actualizarResumenVisibleDetalleAnioActual(resumen) {
  const seccion = document.getElementById("detalle-resumen-visible");
  if (!seccion || !resumen) return;

  const valores = {
    "detalle-resumen-cuotas": resumen.cuotas_acreditadas_identificadas ?? "—",
    "detalle-resumen-salario-disponible": valorResumenMoneda(resumen.total_salario_disponible),
    "detalle-resumen-salario-acreditado": valorResumenMoneda(resumen.total_salario_acreditado),
    "detalle-resumen-meses-info": resumen.meses_con_informacion ?? "—",
    "detalle-resumen-meses-completos": resumen.meses_completos ?? "—",
    "detalle-resumen-ultimo-mes-completo": valorResumenMes(resumen.ultimo_mes_con_salario_completo),
    "detalle-resumen-ultimo-mes-cuota": valorResumenMes(resumen.ultimo_mes_cuota_acreditada),
    "detalle-resumen-ultimo-salario": valorResumenMoneda(resumen.salario_ultimo_mes_completo),
    "detalle-resumen-promedio-completos": valorResumenMoneda(resumen.promedio_meses_completos),
    "detalle-resumen-promedio-tres": valorResumenMoneda(resumen.promedio_ultimos_3_meses_completos),
    "detalle-resumen-promedio-cuota": valorResumenMoneda(resumen.promedio_por_cuota_acreditada),
  };

  Object.entries(valores).forEach(([id, valor]) => {
    const elemento = document.getElementById(id);
    if (elemento) elemento.textContent = String(valor);
  });

  seccion.classList.remove("d-none");
}


function mostrarResumenDetalleAnioActual(resumen) {
  const estado = document.getElementById("detalle-estado-coherencia");
  if (!estado) return;

  actualizarResumenVisibleDetalleAnioActual(resumen);
  estado.classList.remove("d-none");

  if (resumen.cuotas_coinciden) {
    estado.className = "alert alert-success mt-4 mb-0";
    estado.textContent = (
      "Las cuotas acreditadas del detalle coinciden con el total del año actual informado en el Paso 2."
    );
  } else {
    const simulacion = obtenerSimulacion();
    const cuotasPaso2 = Number(simulacion.cuotas?.cuotas_anio_actual || 0);
    estado.className = "alert alert-warning mt-4 mb-0";
    estado.textContent = (
      `Marcaste ${resumen.cuotas_acreditadas_identificadas} cuota(s), pero el Paso 2 registra ${cuotasPaso2} para el año actual. `
      + "Si un mes tiene salario pero la cuota todavía no aparece acreditada por la CSS, conserva el salario y deja su casilla sin marcar. "
      + "Si la cuota ya está acreditada, revisa el dato del Paso 2 antes de continuar."
    );
  }

  if (typeof actualizarResumenPaso3 === "function") {
    actualizarResumenPaso3();
  }
}


function obtenerValorBaseSalarial(origen, resumen) {
  if (!resumen) {
    return null;
  }

  if (origen === "ULTIMO_MES_COMPLETO") {
    return resumen.salario_ultimo_mes_completo;
  }

  if (origen === "PROMEDIO_ANIO_ACTUAL") {
    return resumen.promedio_meses_completos;
  }

  if (origen === "PROMEDIO_3_MESES") {
    return resumen.promedio_ultimos_3_meses_completos;
  }

  if (origen === "PROMEDIO_CUOTA_ACREDITADA") {
    return resumen.promedio_por_cuota_acreditada;
  }

  return null;
}


function descripcionOrigenBaseSalarial(origen, resumen) {
  if (origen === "ULTIMO_MES_COMPLETO") {
    return (
      "Último mes completo disponible"
      + (resumen?.ultimo_mes_con_salario_completo
        ? ` (${formatearMesIsoLegible(resumen.ultimo_mes_con_salario_completo)})`
        : "")
    );
  }

  if (origen === "PROMEDIO_ANIO_ACTUAL") {
    return "Promedio de meses completos del año actual";
  }

  if (origen === "PROMEDIO_3_MESES") {
    return "Promedio de los últimos 3 meses completos";
  }

  if (origen === "PROMEDIO_CUOTA_ACREDITADA") {
    return "Promedio del salario acreditado por cuota del año actual";
  }

  if (origen === "MANUAL") {
    return "Salario indicado manualmente";
  }

  return "Base salarial definida en el Paso 3";
}


function actualizarOpcionesBaseSalarial(aplicarSugerencia) {
  const selector = document.getElementById(
    "origen_salario_proyeccion",
  );

  const simulacion = obtenerSimulacion();
  const resumen = simulacion.resumen_detalle_anio_actual;

  const opciones = {
    ULTIMO_MES_COMPLETO: resumen?.salario_ultimo_mes_completo,
    PROMEDIO_ANIO_ACTUAL: resumen?.promedio_meses_completos,
    PROMEDIO_3_MESES: resumen?.promedio_ultimos_3_meses_completos,
    PROMEDIO_CUOTA_ACREDITADA: resumen?.promedio_por_cuota_acreditada,
  };

  Object.entries(opciones).forEach(([valor, disponible]) => {
    selector.querySelector(
      `option[value="${valor}"]`,
    ).disabled = !(Number(disponible) > 0);
  });

  const origenGuardado = simulacion.origen_salario_proyeccion || "";
  const opcionGuardada = origenGuardado
    ? selector.querySelector(`option[value="${origenGuardado}"]`)
    : null;

  selector.value = (
    opcionGuardada && !opcionGuardada.disabled
      ? origenGuardado
      : ""
  );

  aplicarOrigenBaseSalarial(false);

  if (
    aplicarSugerencia
    && !selector.value
    && Number(resumen?.salario_ultimo_mes_completo) > 0
  ) {
    document.getElementById(
      "origen-salario-proyeccion-ayuda",
    ).textContent = (
      "Hay bases automáticas disponibles a partir del detalle validado. "
      + "Selecciona la que represente mejor tu situación; ninguna se aplicará sin tu decisión."
    );
  }
}


function aplicarOrigenBaseSalarial(invalidar = true) {
  const selector = document.getElementById(
    "origen_salario_proyeccion",
  );
  const origen = selector.value;

  const monto = document.getElementById("monto_salario");
  const periodicidad = document.getElementById("periodicidad_salario");
  const ayuda = document.getElementById("origen-salario-proyeccion-ayuda");

  const simulacion = obtenerSimulacion();
  const resumen = simulacion.resumen_detalle_anio_actual;

  const requiredMonto = document.getElementById("required-monto-salario");
  const requiredPeriodicidad = document.getElementById("required-periodicidad-salario");
  const requiredNote = document.getElementById("base-salarial-required-note");
  const origenMonto = document.getElementById("origen-monto-salario");
  const origenPeriodicidad = document.getElementById("origen-periodicidad-salario");

  if (!origen) {
    monto.disabled = true;
    monto.readOnly = false;
    monto.required = false;
    periodicidad.disabled = true;
    periodicidad.required = false;
    requiredMonto?.classList.add("d-none");
    requiredPeriodicidad?.classList.add("d-none");
    requiredNote?.classList.remove("d-none");
    origenMonto?.classList.add("d-none");
    origenPeriodicidad?.classList.add("d-none");
    const hayBaseAutomatica = Boolean(
      Number(resumen?.salario_ultimo_mes_completo) > 0
      || Number(resumen?.promedio_meses_completos) > 0
      || Number(resumen?.promedio_ultimos_3_meses_completos) > 0
      || Number(resumen?.promedio_por_cuota_acreditada) > 0
    );
    ayuda.textContent = hayBaseAutomatica
      ? "Selecciona primero la base salarial. La aplicación no elegirá una opción por ti."
      : (
        "Las bases automáticas se habilitan después de analizar y validar el detalle salarial del año actual. "
        + "Mientras tanto, puedes indicar el salario manualmente."
      );
  } else if (origen === "MANUAL") {
    monto.disabled = false;
    monto.readOnly = false;
    periodicidad.disabled = false;
    monto.required = true;
    periodicidad.required = true;
    requiredMonto?.classList.remove("d-none");
    requiredPeriodicidad?.classList.remove("d-none");
    requiredNote?.classList.remove("d-none");
    origenMonto?.classList.add("d-none");
    origenPeriodicidad?.classList.add("d-none");
    ayuda.textContent = "Indica el monto y la periodicidad que deseas usar como base.";
  } else {
    const valor = obtenerValorBaseSalarial(origen, resumen);

    if (!(Number(valor) > 0)) {
      selector.value = "";
      aplicarOrigenBaseSalarial(invalidar);
      return;
    }

    monto.disabled = false;
    monto.value = formatearNumeroMonetario(valor);
    monto.readOnly = true;
    monto.required = false;
    periodicidad.value = "MENSUAL";
    periodicidad.disabled = true;
    periodicidad.required = false;
    requiredMonto?.classList.add("d-none");
    requiredPeriodicidad?.classList.add("d-none");
    requiredNote?.classList.add("d-none");
    ayuda.textContent = `${descripcionOrigenBaseSalarial(origen, resumen)}: ${formatearMoneda(valor)}.`;
    if (origenMonto) {
      origenMonto.textContent = "Calculado automáticamente a partir del detalle validado.";
      origenMonto.className = "field-origin-note automatic";
    }
    if (origenPeriodicidad) {
      origenPeriodicidad.textContent = "Calculado automáticamente: periodicidad mensual.";
      origenPeriodicidad.className = "field-origin-note automatic";
    }
  }

  simulacion.origen_salario_proyeccion = origen;
  guardarSimulacion(simulacion);

  if (invalidar && typeof invalidarResumenSalario === "function") {
    invalidarResumenSalario();
  }
}


// ============================================================
// Activación y restauración
// ============================================================

function actualizarEstadoDetalleAnioActual() {
  const selectorDecision = document.getElementById("usar_detalle_anio_actual");
  const decision = selectorDecision.value;
  const decisionTomada = decision === "true" || decision === "false";
  const habilitado = decision === "true";
  const simulacion = obtenerSimulacion();
  const importado = Boolean(
    simulacion.importacion_ficha_digital_confirmada
    && simulacion.ficha_digital_importada,
  );

  if (importado && Array.isArray(simulacion.detalle_anio_actual?.registros)) {
    simulacion.detalle_anio_actual.registros.forEach((registro) => {
      const origenMes = simulacion.origen_campos_detalle_anio_actual?.[String(registro.mes)] || {};
      const salarioImportado = Boolean(origenMes.salario_mensual || origenMes.estado);
      if (salarioImportado) {
        registro.cuota_acreditada = true;
        simulacion.origen_campos_detalle_anio_actual[String(registro.mes)] = {
          ...origenMes,
          cuota_acreditada: origenMes.cuota_acreditada || origenMes.salario_mensual || origenMes.estado,
        };
      }
    });
  }

  const modo = document.getElementById("modo_detalle_anio_actual");
  if (importado && habilitado) {
    modo.value = "MENSUAL";
  } else if (!habilitado) {
    modo.value = "";
  }
  modo.disabled = !habilitado || importado;

  const modoSeleccionado = (
    importado
    || ["MENSUAL", "QUINCENAL"].includes(modo.value)
  );
  const mostrarContenido = habilitado && modoSeleccionado;

  document.getElementById(
    "detalle-anio-actual-contenido",
  ).classList.toggle("d-none", !mostrarContenido);

  const origenModo = document.getElementById("origen-modo-detalle");
  if (origenModo) {
    const mostrarOrigen = importado && habilitado;
    origenModo.textContent = mostrarOrigen
      ? "Calculado automáticamente: la Ficha Digital utiliza captura mensual."
      : "";
    origenModo.className = mostrarOrigen
      ? "field-origin-note automatic"
      : "field-origin-note d-none";
  }

  document.getElementById("detalle-importado-estado")?.classList.toggle(
    "d-none",
    !importado || !mostrarContenido,
  );
  document.getElementById("detalle-importado-inactivo")?.classList.toggle(
    "d-none",
    !importado || decision !== "false",
  );

  simulacion.detalle_anio_actual_habilitado = (
    decisionTomada ? habilitado : null
  );

  if (!mostrarContenido) {
    document.getElementById("detalle-cuotas-sincronizadas")?.classList.add("d-none");
    document.getElementById("detalle-resumen-visible")?.classList.add("d-none");
    simulacion.resumen_detalle_anio_actual = null;
    simulacion.ultimo_mes_cuotas_derivado = null;
    guardarSimulacion(simulacion);
    liberarSalarioAnualActual();
    actualizarOpcionesBaseSalarial(false);
    return;
  }

  guardarSimulacion(simulacion);
  generarTablaDetalleAnioActual();
}


function restaurarDetalleAnioActual() {
  const simulacion = obtenerSimulacion();
  const importado = Boolean(
    simulacion.importacion_ficha_digital_confirmada
    && simulacion.ficha_digital_importada,
  );
  const decisionGuardada = simulacion.detalle_anio_actual_habilitado;
  const valorDecision = importado
    ? "true"
    : (typeof decisionGuardada === "boolean" ? String(decisionGuardada) : "");

  document.getElementById(
    "usar_detalle_anio_actual",
  ).value = valorDecision;

  if (
    valorDecision === "true"
    && simulacion.detalle_anio_actual?.modo_captura
  ) {
    document.getElementById(
      "modo_detalle_anio_actual",
    ).value = simulacion.detalle_anio_actual.modo_captura;
  }

  actualizarEstadoDetalleAnioActual();

  if (
    valorDecision === "true"
    && simulacion.resumen_detalle_anio_actual
  ) {
    mostrarResumenDetalleAnioActual(
      simulacion.resumen_detalle_anio_actual,
    );

    sincronizarDetalleConHistorial(
      simulacion.resumen_detalle_anio_actual,
    );
  }

  actualizarOpcionesBaseSalarial(false);
}


function mostrarErrorDetalleAnioActual(mensaje) {
  const error = document.getElementById("error-detalle-anio-actual");
  error.textContent = mensaje;
  error.classList.remove("d-none");
}


function ocultarMensajesDetalleAnioActual() {
  document.getElementById("error-detalle-anio-actual").classList.add("d-none");
  document.getElementById("advertencia-detalle-anio-actual").classList.add("d-none");
  document.getElementById("detalle-resumen-visible")?.classList.add("d-none");
}


// ============================================================
// Eventos
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  restaurarDetalleAnioActual();

  document.getElementById(
    "usar_detalle_anio_actual",
  ).addEventListener("change", actualizarEstadoDetalleAnioActual);

  document.getElementById(
    "modo_detalle_anio_actual",
  ).addEventListener("change", () => {
    const simulacion = obtenerSimulacion();
    simulacion.detalle_anio_actual = {
      anio: ANIO_ACTUAL,
      modo_captura: obtenerModoDetalleAnioActual(),
      cuotas_anio_actual_referencia: Number(
        simulacion.cuotas?.cuotas_anio_actual || 0,
      ),
      registros: [],
    };
    simulacion.resumen_detalle_anio_actual = null;
    guardarSimulacion(simulacion);
    generarTablaDetalleAnioActual();
    invalidarDetalleAnioActual();
  });

  document.getElementById("btn-revisar-detalle-importado")?.addEventListener(
    "click",
    () => {
      if (typeof revisarFichaDigitalImportada === "function") {
        revisarFichaDigitalImportada();
      }
    },
  );

  document.getElementById(
    "origen_salario_proyeccion",
  ).addEventListener("change", () => aplicarOrigenBaseSalarial(true));
});
