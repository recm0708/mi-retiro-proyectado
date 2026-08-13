"use strict";

/* ============================================================
   Mi Retiro Proyectado
   Importación revisable de documentos oficiales
   ============================================================ */

let borradorImportacionComprobante = null;
let borradorImportacionFichaDigital = null;

const MESES_IMPORTACION = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
];


function obtenerModalBootstrap(id) {
  const elemento = document.getElementById(id);
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
// Comprobante de Mi Retiro Seguro
// ============================================================

function crearFilaPreviewComprobante(registro) {
  const fila = document.createElement("tr");
  fila.dataset.tipoOriginal = registro.tipo;

  const aplicar = document.createElement("input");
  aplicar.type = "checkbox";
  aplicar.className = "form-check-input preview-comprobante-aplicar";
  aplicar.checked = registro.tipo === "HISTORICO";
  aplicar.setAttribute("aria-label", `Pasar ${registro.anio} al historial real`);

  const anio = document.createElement("input");
  anio.type = "number";
  anio.min = "1900";
  anio.max = "2200";
  anio.step = "1";
  anio.className = "form-control form-control-sm preview-comprobante-anio";
  anio.value = registro.anio;
  anio.setAttribute("aria-label", `Año detectado ${registro.anio}`);

  const edad = document.createElement("input");
  edad.type = "number";
  edad.min = "0";
  edad.max = "150";
  edad.step = "1";
  edad.className = "form-control form-control-sm preview-comprobante-edad";
  edad.value = registro.edad;
  edad.setAttribute("aria-label", `Edad detectada para ${registro.anio}`);

  const tipo = document.createElement("select");
  tipo.className = "form-select form-select-sm preview-comprobante-tipo";
  tipo.innerHTML = `
    <option value="HISTORICO">Histórico</option>
    <option value="HISTORICO_PROYECTADO">Histórico + proyectado</option>
    <option value="PROYECTADO">Proyectado</option>
  `;
  tipo.value = registro.tipo;
  tipo.setAttribute("aria-label", `Tipo de registro ${registro.anio}`);

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

  [aplicar, anio, edad, tipo, salarioGrupo, cuotas].forEach((control) => {
    const celda = document.createElement("td");
    celda.appendChild(control);
    fila.appendChild(celda);
  });

  tipo.addEventListener("change", () => {
    if (tipo.value === "PROYECTADO") aplicar.checked = false;
  });

  return fila;
}


function renderizarPreviewComprobante(referencia) {
  borradorImportacionComprobante = structuredClone(referencia);

  document.getElementById("preview-comprobante-fecha-nacimiento").value = referencia.fecha_nacimiento || "";
  document.getElementById("preview-comprobante-sexo").value = referencia.sexo || "";
  document.getElementById("preview-comprobante-fecha-ingreso").value = referencia.fecha_ingreso_css || "";
  document.getElementById("preview-comprobante-sistema").value = referencia.sistema_elegido || "NO_IDENTIFICADO";
  document.getElementById("preview-comprobante-cuotas").value = referencia.cuotas_historicas ?? "";
  document.getElementById("preview-comprobante-edad-retiro").value = referencia.edad_retiro_elegida ?? "";
  const campoMontoReferencia = document.getElementById("preview-comprobante-monto");
  campoMontoReferencia.value = formatearNumeroMonetario(
    referencia.monto_estimado_prestacion ?? 0,
  );
  configurarCampoMonetario(campoMontoReferencia);
  document.getElementById("preview-comprobante-fecha").value = referencia.fecha_comprobante || "";
  document.getElementById("preview-comprobante-prestacion").value = referencia.prestacion_esperada || "";

  const cuerpo = document.getElementById("preview-comprobante-registros");
  cuerpo.replaceChildren();
  (referencia.registros || []).forEach((registro) => {
    cuerpo.appendChild(crearFilaPreviewComprobante(registro));
  });
  document.getElementById("preview-comprobante-registros-contador").textContent = `${(referencia.registros || []).length} registros`;

  const advertencias = document.getElementById("advertencias-import-comprobante");
  const mensajes = Array.isArray(referencia.advertencias) ? referencia.advertencias : [];
  advertencias.textContent = mensajes.join(" ");
  advertencias.classList.toggle("d-none", mensajes.length === 0);

  obtenerModalBootstrap("modal-import-comprobante").show();
}


async function analizarComprobanteImportacion() {
  ocultarEstadoImportacion("estado-comprobante-importacion");
  const input = document.getElementById("import-comprobante-pdf");
  const archivo = input.files?.[0];

  if (!archivo) {
    mostrarEstadoImportacion("estado-comprobante-importacion", "Selecciona primero el comprobante PDF.", "danger");
    return;
  }

  const boton = document.getElementById("btn-analizar-comprobante-importacion");
  boton.disabled = true;
  boton.textContent = "Analizando…";

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

    renderizarPreviewComprobante(contenido);
  } catch {
    mostrarEstadoImportacion("estado-comprobante-importacion", "No fue posible comunicarse con el servidor.", "danger");
  } finally {
    boton.disabled = false;
    boton.textContent = "Analizar comprobante";
  }
}


function leerRegistrosPreviewComprobante() {
  return Array.from(document.querySelectorAll("#preview-comprobante-registros tr")).map((fila) => ({
    aplicar_historial: fila.querySelector(".preview-comprobante-aplicar").checked,
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

  const registrosPreview = leerRegistrosPreviewComprobante();
  const sistema = document.getElementById("preview-comprobante-sistema").value;
  const prestacion = document.getElementById("preview-comprobante-prestacion").value.trim();

  const referencia = {
    ...borradorImportacionComprobante,
    fecha_nacimiento: document.getElementById("preview-comprobante-fecha-nacimiento").value || null,
    sexo: document.getElementById("preview-comprobante-sexo").value || null,
    fecha_ingreso_css: document.getElementById("preview-comprobante-fecha-ingreso").value || null,
    sistema_elegido: sistema,
    sistema_elegido_nombre: textoSistemaImportado(sistema),
    cuotas_historicas: Number(document.getElementById("preview-comprobante-cuotas").value || 0),
    edad_retiro_elegida: Number(document.getElementById("preview-comprobante-edad-retiro").value || 0) || null,
    monto_estimado_prestacion: obtenerValorMonetario(
      document.getElementById("preview-comprobante-monto").value || 0,
    ),
    fecha_comprobante: document.getElementById("preview-comprobante-fecha").value || null,
    prestacion_esperada: prestacion || null,
    naturaleza_prestacion: naturalezaPrestacionImportada(prestacion),
    registros: registrosPreview.map(({ aplicar_historial, ...registro }) => registro),
  };

  const simulacion = obtenerSimulacion();
  simulacion.referencia_mi_retiro_seguro = referencia;
  simulacion.importacion_comprobante_confirmada = true;

  simulacion.persona = {
    ...simulacion.persona,
    ...(referencia.fecha_nacimiento ? { fecha_nacimiento: referencia.fecha_nacimiento } : {}),
    ...(referencia.sexo ? { sexo: referencia.sexo } : {}),
    ...(referencia.fecha_ingreso_css ? { fecha_ingreso_css: referencia.fecha_ingreso_css } : {}),
    ...(sistema !== "NO_IDENTIFICADO" ? { sistema } : {}),
  };

  const registroActual = registrosPreview.find((registro) => (
    registro.anio === ANIO_ACTUAL && registro.tipo !== "PROYECTADO"
  ));

  simulacion.cuotas = {
    ...simulacion.cuotas,
    ...(referencia.cuotas_historicas != null ? { cuotas_totales: referencia.cuotas_historicas } : {}),
    ...(registroActual ? { cuotas_anio_actual: registroActual.cuotas } : {}),
  };

  const reales = registrosPreview.filter((registro) => registro.aplicar_historial);
  if (reales.length > 0) {
    const anioInicio = Math.min(...reales.map((registro) => registro.anio));
    simulacion.modo_historial = "MANUAL";
    simulacion.historial_anio_inicio_temporal = anioInicio;
    simulacion.historial = {
      anio_inicio: anioInicio,
      anio_fin: ANIO_ACTUAL,
      cuotas_totales_referencia: referencia.cuotas_historicas || 0,
      registros: reales.map((registro) => ({
        anio: registro.anio,
        cuotas: registro.cuotas,
        salario_cotizado: registro.salario_anual,
      })),
    };
  }

  invalidarResultadosPorImportacion(simulacion);
  guardarSimulacion(simulacion);

  restaurarDatosPersonales(simulacion);
  restaurarDatosCuotas(simulacion);
  if (typeof inicializarHistorialSalarial === "function") inicializarHistorialSalarial();

  mostrarEstadoImportacion(
    "estado-comprobante-importacion",
    `Datos confirmados: ${textoSistemaImportado(sistema)} · ${referencia.cuotas_historicas ?? "—"} cuotas · referencia ${formatearMoneda(referencia.monto_estimado_prestacion)}. Completa manualmente los campos que el documento no puede determinar.`,
    "success",
  );
  document.getElementById("btn-quitar-comprobante-importacion").classList.remove("d-none");
  obtenerModalBootstrap("modal-import-comprobante").hide();

  if (typeof prepararComparacionReferenciaMiRetiroGuardada === "function") {
    prepararComparacionReferenciaMiRetiroGuardada();
  }
}


function quitarComprobanteImportacion() {
  const simulacion = obtenerSimulacion();
  simulacion.referencia_mi_retiro_seguro = null;
  simulacion.importacion_comprobante_confirmada = false;
  guardarSimulacion(simulacion);
  document.getElementById("import-comprobante-pdf").value = "";
  ocultarEstadoImportacion("estado-comprobante-importacion");
  document.getElementById("btn-quitar-comprobante-importacion").classList.add("d-none");
}


// ============================================================
// Ficha Digital
// ============================================================

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

  const cuota = document.createElement("input");
  cuota.type = "checkbox";
  cuota.className = "form-check-input preview-ficha-cuota";
  cuota.setAttribute("aria-label", `Cuota acreditada de ${MESES_IMPORTACION[registro.mes - 1]} ${registro.anio}`);

  const controles = esMasReciente
    ? (() => {
        const nota = document.createElement("small");
        nota.className = "d-block text-warning mt-1";
        nota.textContent = "Revisa si este mes está completo o parcial.";
        const contenedor = document.createElement("div");
        contenedor.append(estado, nota);
        return [mes, salarioGrupo, contenedor, cuota];
      })()
    : [mes, salarioGrupo, estado, cuota];

  controles.forEach((control) => {
    const celda = document.createElement("td");
    celda.appendChild(control);
    fila.appendChild(celda);
  });

  return fila;
}


function renderizarPreviewFichaDigital(resumen) {
  borradorImportacionFichaDigital = structuredClone(resumen);
  const cuerpo = document.getElementById("preview-ficha-digital-registros");
  cuerpo.replaceChildren();

  const registros = (resumen.registros || []).filter(
    (registro) => registro.anio === ANIO_ACTUAL,
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

  obtenerModalBootstrap("modal-import-ficha-digital").show();
}


async function analizarFichaDigitalImportacion() {
  ocultarEstadoImportacion("estado-ficha-digital-importacion");
  const input = document.getElementById("import-ficha-digital-pdf");
  const archivo = input.files?.[0];

  if (!archivo) {
    mostrarEstadoImportacion("estado-ficha-digital-importacion", "Selecciona primero la Ficha Digital en PDF.", "danger");
    return;
  }

  const boton = document.getElementById("btn-analizar-ficha-digital-importacion");
  boton.disabled = true;
  boton.textContent = "Analizando…";

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

    renderizarPreviewFichaDigital(contenido);
  } catch {
    mostrarEstadoImportacion("estado-ficha-digital-importacion", "No fue posible comunicarse con el servidor.", "danger");
  } finally {
    boton.disabled = false;
    boton.textContent = "Analizar Ficha Digital";
  }
}


function leerRegistrosPreviewFicha() {
  return Array.from(document.querySelectorAll("#preview-ficha-digital-registros tr")).map((fila) => ({
    anio: Number(fila.dataset.anio || ANIO_ACTUAL),
    mes: Number(fila.querySelector(".preview-ficha-mes").value),
    salario: obtenerValorMonetario(
      fila.querySelector(".preview-ficha-salario").value || 0,
    ),
    estado: fila.querySelector(".preview-ficha-estado").value,
    cuota_acreditada: fila.querySelector(".preview-ficha-cuota").checked,
  }));
}


function confirmarFichaDigitalImportacion() {
  if (!borradorImportacionFichaDigital) return;

  const registros = leerRegistrosPreviewFicha().filter(
    (registro) => registro.anio === ANIO_ACTUAL,
  );
  const actuales = registros;
  const simulacion = obtenerSimulacion();

  simulacion.ficha_digital_importada = {
    registros,
    anio_mas_reciente: borradorImportacionFichaDigital.anio_mas_reciente,
    mes_mas_reciente: borradorImportacionFichaDigital.mes_mas_reciente,
    advertencias: borradorImportacionFichaDigital.advertencias || [],
  };
  simulacion.importacion_ficha_digital_confirmada = true;

  if (actuales.length > 0) {
    const cuotasConfirmadas = actuales.filter((registro) => registro.cuota_acreditada).length;
    simulacion.cuotas = {
      ...simulacion.cuotas,
      cuotas_anio_actual: cuotasConfirmadas,
    };

    simulacion.detalle_anio_actual_habilitado = true;
    simulacion.detalle_anio_actual = {
      anio: ANIO_ACTUAL,
      modo_captura: "MENSUAL",
      cuotas_anio_actual_referencia: Number(simulacion.cuotas?.cuotas_anio_actual || 0),
      registros: actuales.map((registro) => ({
        mes: registro.mes,
        cuota_acreditada: registro.cuota_acreditada,
        estado: registro.estado,
        salario_mensual: registro.estado === "SIN_INFORMACION" ? null : registro.salario,
        primera_quincena: null,
        segunda_quincena: null,
      })),
    };
  }

  invalidarResultadosPorImportacion(simulacion);
  guardarSimulacion(simulacion);

  restaurarDatosCuotas(simulacion);
  if (typeof restaurarDetalleAnioActual === "function") restaurarDetalleAnioActual();

  const cuotasMarcadas = actuales.filter((registro) => registro.cuota_acreditada).length;
  mostrarEstadoImportacion(
    "estado-ficha-digital-importacion",
    `Ficha Digital confirmada: ${actuales.length} salarios del año ${ANIO_ACTUAL} y ${cuotasMarcadas} cuotas marcadas como acreditadas. Revisa y valida el detalle en el Paso 3.`,
    "success",
  );
  document.getElementById("btn-quitar-ficha-digital-importacion").classList.remove("d-none");
  obtenerModalBootstrap("modal-import-ficha-digital").hide();
}


function quitarFichaDigitalImportacion() {
  const simulacion = obtenerSimulacion();
  simulacion.ficha_digital_importada = null;
  simulacion.importacion_ficha_digital_confirmada = false;
  simulacion.detalle_anio_actual_habilitado = false;
  simulacion.detalle_anio_actual = null;
  simulacion.resumen_detalle_anio_actual = null;
  guardarSimulacion(simulacion);

  document.getElementById("import-ficha-digital-pdf").value = "";
  ocultarEstadoImportacion("estado-ficha-digital-importacion");
  document.getElementById("btn-quitar-ficha-digital-importacion").classList.add("d-none");
  if (typeof restaurarDetalleAnioActual === "function") restaurarDetalleAnioActual();
}


function restaurarResumenImportaciones() {
  const simulacion = obtenerSimulacion();

  if (simulacion.referencia_mi_retiro_seguro && simulacion.importacion_comprobante_confirmada) {
    const ref = simulacion.referencia_mi_retiro_seguro;
    mostrarEstadoImportacion(
      "estado-comprobante-importacion",
      `Comprobante confirmado: ${textoSistemaImportado(ref.sistema_elegido)} · ${ref.cuotas_historicas ?? "—"} cuotas · referencia ${formatearMoneda(ref.monto_estimado_prestacion)}.`,
      "success",
    );
    document.getElementById("btn-quitar-comprobante-importacion").classList.remove("d-none");
  }

  if (simulacion.ficha_digital_importada && simulacion.importacion_ficha_digital_confirmada) {
    const registros = simulacion.ficha_digital_importada.registros || [];
    const actuales = registros.filter((registro) => registro.anio === ANIO_ACTUAL);
    mostrarEstadoImportacion(
      "estado-ficha-digital-importacion",
      `Ficha Digital confirmada: ${actuales.length} salarios del año ${ANIO_ACTUAL}.`,
      "success",
    );
    document.getElementById("btn-quitar-ficha-digital-importacion").classList.remove("d-none");
  }
}


document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btn-analizar-comprobante-importacion")?.addEventListener("click", analizarComprobanteImportacion);
  document.getElementById("btn-confirmar-import-comprobante")?.addEventListener("click", confirmarComprobanteImportacion);
  document.getElementById("btn-quitar-comprobante-importacion")?.addEventListener("click", quitarComprobanteImportacion);

  document.getElementById("btn-analizar-ficha-digital-importacion")?.addEventListener("click", analizarFichaDigitalImportacion);
  document.getElementById("btn-confirmar-import-ficha")?.addEventListener("click", confirmarFichaDigitalImportacion);
  document.getElementById("btn-quitar-ficha-digital-importacion")?.addEventListener("click", quitarFichaDigitalImportacion);

  restaurarResumenImportaciones();
});
