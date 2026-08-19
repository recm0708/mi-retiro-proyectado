"use strict";


/* ============================================================
   Mi Retiro Proyectado
   Referencia opcional importada desde Mi Retiro Seguro
   ============================================================ */

/*
 * Presenta una referencia individual extraída del comprobante y permite
 * contrastarla con el resultado calculado por la aplicación. La referencia
 * nunca calibra los motores ni sustituye las entradas confirmadas del usuario.
 */

function ocultarErrorReferenciaMiRetiro() {
  const alerta = document.getElementById("error-referencia-mi-retiro");
  if (!alerta) {
    return;
  }
  alerta.textContent = "";
  alerta.classList.add("d-none");
}


function mostrarErrorReferenciaMiRetiro(mensaje) {
  const alerta = document.getElementById("error-referencia-mi-retiro");
  if (!alerta) {
    return;
  }
  alerta.textContent = mensaje;
  alerta.classList.remove("d-none");
}


function formatearFechaIsoReferencia(valor) {
  if (!valor) {
    return "—";
  }

  const partes = String(valor).split("-");
  if (partes.length !== 3) {
    return valor;
  }

  return `${partes[2]}/${partes[1]}/${partes[0]}`;
}


/**
 * Compara la referencia importada con los datos personales ya confirmados.
 *
 * @param {Object} referencia Datos extraídos del comprobante.
 * @returns {string[]} Diferencias que deben mostrarse al usuario.
 */
function obtenerInconsistenciasReferencia(referencia) {
  const simulacion = obtenerSimulacion();
  const persona = simulacion.persona || {};
  const inconsistencias = [];

  if (
    referencia.fecha_nacimiento
    && persona.fecha_nacimiento
    && referencia.fecha_nacimiento !== persona.fecha_nacimiento
  ) {
    inconsistencias.push("la fecha de nacimiento no coincide con el Paso 1");
  }

  if (
    referencia.sexo
    && persona.sexo
    && referencia.sexo !== persona.sexo
  ) {
    inconsistencias.push("el sexo no coincide con el Paso 1");
  }

  if (
    referencia.fecha_ingreso_css
    && persona.fecha_ingreso_css
    && referencia.fecha_ingreso_css !== persona.fecha_ingreso_css
  ) {
    inconsistencias.push("la fecha de ingreso a la CSS no coincide con el Paso 1");
  }

  if (
    referencia.sistema_elegido !== "NO_IDENTIFICADO"
    && persona.sistema
    && persona.sistema !== "NO_SE"
    && referencia.sistema_elegido !== persona.sistema
  ) {
    inconsistencias.push("el sistema elegido no coincide con el Paso 1");
  }

  return inconsistencias;
}


function mostrarReferenciaMiRetiro(referencia) {
  const contenedor = document.getElementById("resultado-referencia-mi-retiro");
  if (!contenedor || !referencia) {
    return;
  }

  document.getElementById(
    "referencia-mi-retiro-monto",
  ).textContent = formatearMoneda(referencia.monto_estimado_prestacion);

  document.getElementById(
    "referencia-mi-retiro-sistema",
  ).textContent = referencia.sistema_elegido_nombre || "—";

  document.getElementById(
    "referencia-mi-retiro-edad",
  ).textContent = referencia.edad_retiro_elegida == null
    ? "—"
    : `${referencia.edad_retiro_elegida} años`;

  document.getElementById(
    "referencia-mi-retiro-cuotas",
  ).textContent = referencia.cuotas_historicas == null
    ? "—"
    : referencia.cuotas_historicas;

  document.getElementById(
    "referencia-mi-retiro-fecha",
  ).textContent = (
    `Fecha del comprobante: ${formatearFechaIsoReferencia(referencia.fecha_comprobante)}`
  );

  document.getElementById(
    "referencia-mi-retiro-registros",
  ).textContent = (
    `Registros anuales detectados: ${Array.isArray(referencia.registros) ? referencia.registros.length : 0}`
  );

  const coherencia = document.getElementById(
    "referencia-mi-retiro-coherencia",
  );
  const inconsistencias = obtenerInconsistenciasReferencia(referencia);
  const advertencias = Array.isArray(referencia.advertencias)
    ? referencia.advertencias
    : [];

  if (inconsistencias.length > 0) {
    coherencia.className = "alert alert-warning mt-3 mb-0";
    coherencia.textContent = (
      "El documento fue leído, pero "
      + inconsistencias.join("; ")
      + ". La referencia se conservará, aunque la comparación del Paso 6 puede no ser directa."
    );
  } else if (advertencias.length > 0) {
    coherencia.className = "alert alert-warning mt-3 mb-0";
    coherencia.textContent = advertencias.join(" ");
  } else {
    coherencia.className = "alert alert-success mt-3 mb-0";
    coherencia.textContent = (
      "El comprobante es compatible con los datos personales disponibles. "
      + "Su monto se usará únicamente como referencia personal de comparación."
    );
  }

  contenedor.classList.remove("d-none");
  document.getElementById(
    "btn-quitar-referencia-mi-retiro",
  ).classList.remove("d-none");
}


/**
 * Envía el comprobante seleccionado al importador del backend.
 *
 * El archivo no se serializa dentro de la simulación; solo se conserva el
 * resumen confirmado que devuelve el servicio.
 */
async function analizarReferenciaMiRetiro() {
  ocultarErrorReferenciaMiRetiro();

  const input = document.getElementById("referencia-mi-retiro-pdf");
  const archivo = input.files?.[0];

  if (!archivo) {
    mostrarErrorReferenciaMiRetiro(
      "Selecciona primero el comprobante que deseas analizar.",
    );
    return;
  }

  if (!archivo.name.toLowerCase().endsWith(".pdf")) {
    mostrarErrorReferenciaMiRetiro(
      "El comprobante debe estar en formato PDF.",
    );
    return;
  }

  const boton = document.getElementById("btn-analizar-referencia-mi-retiro");
  boton.disabled = true;
  boton.textContent = "Analizando…";

  try {
    const formulario = new FormData();
    formulario.append("archivo", archivo);

    const respuesta = await fetch(
      "/api/simulacion/referencia-mi-retiro-seguro",
      {
        method: "POST",
        body: formulario,
      },
    );

    let contenido = null;
    try {
      contenido = await respuesta.json();
    } catch {
      contenido = null;
    }

    if (!respuesta.ok) {
      mostrarErrorReferenciaMiRetiro(
        obtenerMensajeError(
          contenido,
          "No fue posible analizar el comprobante.",
        ),
      );
      return;
    }

    const simulacion = obtenerSimulacion();
    simulacion.referencia_mi_retiro_seguro = contenido;
    guardarSimulacion(simulacion);

    mostrarReferenciaMiRetiro(contenido);

    if (typeof prepararComparacionReferenciaMiRetiroGuardada === "function") {
      prepararComparacionReferenciaMiRetiroGuardada();
    }

  } catch {
    mostrarErrorReferenciaMiRetiro(
      "No fue posible comunicarse con el servidor para analizar el documento.",
    );
  } finally {
    boton.disabled = false;
    boton.textContent = "Analizar comprobante";
  }
}


function quitarReferenciaMiRetiro() {
  const simulacion = obtenerSimulacion();
  simulacion.referencia_mi_retiro_seguro = null;
  guardarSimulacion(simulacion);

  const input = document.getElementById("referencia-mi-retiro-pdf");
  input.value = "";

  document.getElementById(
    "resultado-referencia-mi-retiro",
  ).classList.add("d-none");

  document.getElementById(
    "btn-quitar-referencia-mi-retiro",
  ).classList.add("d-none");

  const comparacion = document.getElementById(
    "resultado-comparacion-referencia",
  );
  if (comparacion) {
    comparacion.classList.add("d-none");
  }
}


function montoActualComparable(resumen, naturalezaReferencia) {
  if (!resumen) {
    return null;
  }

  if (naturalezaReferencia === "PENSION_MENSUAL") {
    return resumen.pension_mensual_estimada;
  }

  if (naturalezaReferencia === "PAGO_UNICO") {
    return resumen.pago_unico_estimado;
  }

  return null;
}


function formatearDiferenciaReferencia(valor) {
  if (!Number.isFinite(valor)) {
    return "—";
  }

  const prefijo = valor > 0 ? "+" : (valor < 0 ? "−" : "");
  return `${prefijo}${formatearMoneda(Math.abs(valor))}`;
}


function obtenerResumenAcreditadoReferenciaGuardado() {
  const simulacion = obtenerSimulacion();
  const sistema = simulacion.persona?.sistema;

  if (sistema === "SEBD") {
    return simulacion.resultado_sebd_acreditado?.resumen_unificado || null;
  }
  if (sistema === "MIXTO") {
    return simulacion.resultado_mixto_acreditado?.resumen_unificado || null;
  }
  if (sistema === "SUCGS") {
    return simulacion.resultado_sucgs_acreditado?.resumen_unificado || null;
  }
  return null;
}


/**
 * Presenta el contraste entre la referencia externa y el resultado actual.
 *
 * @param {Object} resumenActual Resultado calculado por la aplicación.
 */
function mostrarComparacionReferenciaMiRetiroSeguro(resumenActual) {
  const contenedor = document.getElementById(
    "resultado-comparacion-referencia",
  );

  if (!contenedor) {
    return;
  }

  const simulacion = obtenerSimulacion();
  const referencia = simulacion.referencia_mi_retiro_seguro;
  const resumenAcreditado = obtenerResumenAcreditadoReferenciaGuardado();
  const resumenComparado = resumenAcreditado || resumenActual;

  if (!referencia || !resumenComparado) {
    contenedor.classList.add("d-none");
    return;
  }

  const actual = montoActualComparable(
    resumenComparado,
    referencia.naturaleza_prestacion,
  );

  document.getElementById(
    "resultado-referencia-pdf-monto",
  ).textContent = formatearMoneda(referencia.monto_estimado_prestacion);

  document.getElementById(
    "resultado-referencia-actual-monto",
  ).textContent = actual == null ? "—" : formatearMoneda(actual);

  const mismaPersona = obtenerInconsistenciasReferencia(referencia)
    .filter((mensaje) => !mensaje.includes("sistema"))
    .length === 0;
  const mismoSistema = (
    referencia.sistema_elegido !== "NO_IDENTIFICADO"
    && referencia.sistema_elegido === resumenComparado.sistema
  );
  const mismaEdad = (
    referencia.edad_retiro_elegida != null
    && Number(referencia.edad_retiro_elegida) === Number(resumenComparado.edad_retiro_anios)
  );
  const mismoTipo = actual != null;

  const comparable = mismaPersona && mismoSistema && mismaEdad && mismoTipo;

  const diferenciaElemento = document.getElementById(
    "resultado-referencia-diferencia",
  );
  const estado = document.getElementById(
    "resultado-referencia-estado-comparacion",
  );

  if (comparable) {
    const diferencia = Number(actual) - Number(referencia.monto_estimado_prestacion);
    diferenciaElemento.textContent = formatearDiferenciaReferencia(diferencia);
    estado.className = "alert alert-info mb-0 mt-3";
    estado.textContent = resumenAcreditado
      ? (
        "La diferencia compara el comprobante con el cálculo propio que usa "
        + "solo la información actualmente acreditada. Si el documento corresponde "
        + "a una fotografía anterior, ambos valores todavía pueden diferir."
      )
      : (
        "La diferencia usa el resultado disponible de la simulación. Recalcula "
        + "la prestación para generar también la fotografía acreditada propia."
      );
  } else {
    diferenciaElemento.textContent = "No comparable";
    estado.className = "alert alert-warning mb-0 mt-3";

    const motivos = [];
    if (!mismaPersona) motivos.push("datos personales distintos");
    if (!mismoSistema) motivos.push("sistema distinto");
    if (!mismaEdad) motivos.push("edad de retiro distinta");
    if (!mismoTipo) motivos.push("naturaleza de prestación distinta o sin monto actual");

    estado.textContent = (
      "La referencia se muestra, pero no se calcula una diferencia directa porque "
      + motivos.join(", ")
      + "."
    );
  }

  document.getElementById(
    "resultado-referencia-contexto",
  ).textContent = (
    `${referencia.sistema_elegido_nombre} · `
    + `${referencia.edad_retiro_elegida ?? "—"} años · `
    + `comprobante ${formatearFechaIsoReferencia(referencia.fecha_comprobante)}`
  );

  contenedor.classList.remove("d-none");
}


function prepararComparacionReferenciaMiRetiroGuardada() {
  const simulacion = obtenerSimulacion();
  const sistema = simulacion.persona?.sistema;

  let resultado = null;
  if (sistema === "SEBD") {
    resultado = simulacion.resultado_sebd_normal;
  } else if (sistema === "MIXTO") {
    resultado = simulacion.resultado_mixto;
  } else if (sistema === "SUCGS") {
    resultado = simulacion.resultado_sucgs;
  }

  if (resultado?.resumen_unificado) {
    mostrarComparacionReferenciaMiRetiroSeguro(
      resultado.resumen_unificado,
    );
  }
}


document.addEventListener("DOMContentLoaded", () => {
  const botonAnalizar = document.getElementById(
    "btn-analizar-referencia-mi-retiro",
  );
  const botonQuitar = document.getElementById(
    "btn-quitar-referencia-mi-retiro",
  );

  if (!botonAnalizar || !botonQuitar) {
    return;
  }

  botonAnalizar.addEventListener("click", analizarReferenciaMiRetiro);
  botonQuitar.addEventListener("click", quitarReferenciaMiRetiro);

  const simulacion = obtenerSimulacion();
  if (simulacion.referencia_mi_retiro_seguro) {
    mostrarReferenciaMiRetiro(simulacion.referencia_mi_retiro_seguro);
  }
});
