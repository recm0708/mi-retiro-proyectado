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

  const celdaMes = document.createElement("th");
  celdaMes.scope = "row";
  celdaMes.textContent = MESES_DETALLE_ANIO[mes - 1];
  celdaMes.className = "current-year-detail-month";

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
  celdaMensual.appendChild(mensual.grupo);

  const celdaPrimera = document.createElement("td");
  celdaPrimera.className = "detalle-col-quincenal d-none";
  const primera = crearCampoDineroDetalle(
    `Primera quincena de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
  celdaPrimera.appendChild(primera.grupo);

  const celdaSegunda = document.createElement("td");
  celdaSegunda.className = "detalle-col-quincenal d-none";
  const segunda = crearCampoDineroDetalle(
    `Segunda quincena de ${MESES_DETALLE_ANIO[mes - 1]}`,
  );
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

  [
    check,
    mensual.campo,
    primera.campo,
    segunda.campo,
    selectorEstado,
  ].forEach((control) => {
    control.addEventListener("input", () => {
      actualizarEstadoFilaDetalle(fila);
      guardarBorradorDetalleAnioActual();
      invalidarDetalleAnioActual();
    });

    control.addEventListener("change", () => {
      actualizarEstadoFilaDetalle(fila);
      guardarBorradorDetalleAnioActual();
      invalidarDetalleAnioActual();
    });
  });

  actualizarEstadoFilaDetalle(fila);

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
      selector.disabled = esQuincenal;
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
      const cuota = fila.querySelector(".detalle-cuota-acreditada").checked;
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


function guardarBorradorDetalleAnioActual() {
  if (!estaHabilitadoDetalleAnioActual()) {
    return;
  }

  try {
    const simulacion = obtenerSimulacion();
    simulacion.detalle_anio_actual_habilitado = true;
    simulacion.detalle_anio_actual = leerDetalleAnioActual();
    guardarSimulacion(simulacion);
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

  document.getElementById(
    "resultado-detalle-anio-actual",
  ).classList.add("d-none");

  actualizarOpcionesBaseSalarial(false);
}


async function validarDetalleAnioActual() {
  ocultarMensajesDetalleAnioActual();

  let datos;

  try {
    datos = leerDetalleAnioActual();
  } catch (error) {
    mostrarErrorDetalleAnioActual(error.message);
    return;
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
      return;
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

    if (contenido.cuotas_coinciden) {
      await sincronizarDetalleConHistorial(contenido);
    }

    actualizarOpcionesBaseSalarial(true);

  } catch {
    mostrarErrorDetalleAnioActual(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


async function sincronizarDetalleConHistorial(resumen) {
  const filaActual = document.querySelector(
    `#historial-tabla-body tr[data-anio="${ANIO_ACTUAL}"]`,
  );

  if (!filaActual) {
    return;
  }

  const salario = filaActual.querySelector(
    ".history-input-salario",
  );

  salario.value = formatearNumeroMonetario(
    resumen.total_salario_acreditado,
  );
  salario.readOnly = true;
  salario.dataset.sincronizadoDetalle = "true";
  salario.setAttribute(
    "title",
    "Sincronizado desde el detalle salarial del año actual.",
  );

  actualizarEstadoFila(filaActual);

  // Se vuelve a validar el historial para que el resumen anual y los motores
  // posteriores consuman el total acreditado recién sincronizado.
  await analizarHistorialSalarial();
}


function liberarSalarioAnualActual() {
  const filaActual = document.querySelector(
    `#historial-tabla-body tr[data-anio="${ANIO_ACTUAL}"]`,
  );

  if (!filaActual) {
    return;
  }

  const salario = filaActual.querySelector(
    ".history-input-salario",
  );

  if (salario.dataset.sincronizadoDetalle === "true") {
    salario.readOnly = false;
    delete salario.dataset.sincronizadoDetalle;
    salario.removeAttribute("title");
  }
}


// ============================================================
// Resumen y base salarial sugerida
// ============================================================

function mostrarResumenDetalleAnioActual(resumen) {
  document.getElementById(
    "resultado-detalle-anio-actual",
  ).classList.remove("d-none");

  document.getElementById(
    "detalle-cuotas-identificadas",
  ).textContent = resumen.cuotas_acreditadas_identificadas;

  document.getElementById(
    "detalle-salario-acreditado",
  ).textContent = formatearMoneda(
    resumen.total_salario_acreditado,
  );

  document.getElementById(
    "detalle-salario-disponible",
  ).textContent = formatearMoneda(
    resumen.total_salario_disponible,
  );

  document.getElementById(
    "detalle-ultimo-mes-acreditado",
  ).textContent = formatearMesIsoLegible(
    resumen.ultimo_mes_cuota_acreditada,
  );

  const baseCuota = document.getElementById(
    "detalle-base-cuota-acreditada",
  );
  if (baseCuota) {
    baseCuota.textContent = (
      "Promedio del salario acreditado por cuota del año actual: "
      + (resumen.promedio_por_cuota_acreditada == null
        ? "—"
        : formatearMoneda(resumen.promedio_por_cuota_acreditada))
    );
  }

  const estado = document.getElementById(
    "detalle-estado-coherencia",
  );

  if (resumen.cuotas_coinciden) {
    estado.className = "alert alert-success mt-4 mb-0";
    estado.textContent = (
      "Las cuotas acreditadas marcadas coinciden con el total del año actual "
      + "informado en el Paso 2. El total salarial acreditado se sincronizó "
      + "con la fila anual correspondiente."
    );
  } else {
    estado.className = "alert alert-warning mt-4 mb-0";
    estado.textContent = (
      `Marcaste ${resumen.cuotas_acreditadas_identificadas} cuota(s), pero el `
      + "Paso 2 contiene un total diferente para el año actual. Corrige esa "
      + "diferencia antes de usar este detalle para los cálculos posteriores."
    );
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

  return "Salario indicado manualmente";
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

  if (
    simulacion.origen_salario_proyeccion
    && !selector.querySelector(
      `option[value="${simulacion.origen_salario_proyeccion}"]`,
    )?.disabled
  ) {
    selector.value = simulacion.origen_salario_proyeccion;
  } else if (
    aplicarSugerencia
    && Number(resumen?.salario_ultimo_mes_completo) > 0
  ) {
    selector.value = "ULTIMO_MES_COMPLETO";
  } else if (selector.selectedOptions[0]?.disabled) {
    selector.value = "MANUAL";
  }

  aplicarOrigenBaseSalarial(false);
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

  if (origen === "MANUAL") {
    monto.readOnly = false;
    periodicidad.disabled = false;
    ayuda.textContent = "Indica el monto y la periodicidad que deseas usar como base.";
  } else {
    const valor = obtenerValorBaseSalarial(origen, resumen);

    if (!(Number(valor) > 0)) {
      selector.value = "MANUAL";
      aplicarOrigenBaseSalarial(invalidar);
      return;
    }

    monto.value = formatearNumeroMonetario(valor);
    monto.readOnly = true;
    periodicidad.value = "MENSUAL";
    periodicidad.disabled = true;
    ayuda.textContent = (
      `${descripcionOrigenBaseSalarial(origen, resumen)}: ${formatearMoneda(valor)}. `
      + "Puedes volver a ingreso manual en cualquier momento."
    );
  }

  simulacion.origen_salario_proyeccion = selector.value;
  guardarSimulacion(simulacion);

  if (invalidar && typeof invalidarResumenSalario === "function") {
    invalidarResumenSalario();
  }
}


// ============================================================
// Activación y restauración
// ============================================================

function actualizarEstadoDetalleAnioActual() {
  const habilitado = estaHabilitadoDetalleAnioActual();

  document.getElementById(
    "detalle-anio-actual-contenido",
  ).classList.toggle("d-none", !habilitado);

  document.getElementById(
    "modo_detalle_anio_actual",
  ).disabled = !habilitado;

  const simulacion = obtenerSimulacion();
  simulacion.detalle_anio_actual_habilitado = habilitado;

  if (!habilitado) {
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
  const habilitado = Boolean(simulacion.detalle_anio_actual_habilitado);

  document.getElementById(
    "usar_detalle_anio_actual",
  ).value = String(habilitado);

  if (simulacion.detalle_anio_actual?.modo_captura) {
    document.getElementById(
      "modo_detalle_anio_actual",
    ).value = simulacion.detalle_anio_actual.modo_captura;
  }

  actualizarEstadoDetalleAnioActual();

  if (habilitado && simulacion.resumen_detalle_anio_actual) {
    mostrarResumenDetalleAnioActual(
      simulacion.resumen_detalle_anio_actual,
    );

    if (simulacion.resumen_detalle_anio_actual.cuotas_coinciden) {
      const filaActual = document.querySelector(
        `#historial-tabla-body tr[data-anio="${ANIO_ACTUAL}"]`,
      );

      if (filaActual) {
        const salario = filaActual.querySelector(".history-input-salario");
        salario.value = formatearNumeroMonetario(
          simulacion.resumen_detalle_anio_actual.total_salario_acreditado,
        );
        salario.readOnly = true;
        salario.dataset.sincronizadoDetalle = "true";
      }
    }
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

  document.getElementById(
    "btn-validar-detalle-anio-actual",
  ).addEventListener("click", validarDetalleAnioActual);

  document.getElementById(
    "origen_salario_proyeccion",
  ).addEventListener("change", () => aplicarOrigenBaseSalarial(true));
});
