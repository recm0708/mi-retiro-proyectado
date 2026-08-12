"use strict";

/* ============================================================
   UX.4.1 — Accesibilidad semántica y ayudas contextuales
   ============================================================ */

const AYUDAS_CONTEXTUALES = {
  sistema: {
    titulo: "Sistema previsional",
    texto: "Si no conoces tu sistema, selecciona “No sé cuál tengo”. La aplicación puede continuar sin obligarte a elegir una categoría que no puedas confirmar.",
  },
  cuotas_totales: {
    titulo: "Cuotas acreditadas",
    texto: "Ingresa únicamente las cuotas que ya aparecen acreditadas por la CSS. No sumes aquí cuotas futuras ni meses que todavía no figuren en tu historial.",
  },
  cuotas_anio_actual: {
    titulo: "Cuotas del año actual",
    texto: "Este valor forma parte del total de cuotas acreditadas. Se usa para separar lo ya registrado este año de lo que todavía proyectas aportar.",
  },
  cuotas_esperadas_cierre_anio: {
    titulo: "Cierre esperado del año",
    texto: "Indica cuántas cuotas esperas completar en total durante el año actual, entre 0 y 12. No es una cantidad adicional al total ya informado.",
  },
  cuotas_esperadas_por_anio: {
    titulo: "Densidad futura de cotización",
    texto: "Representa cuántos meses por año esperas seguir cotizando a partir del próximo año. Usa 12 si prevés cotizar todos los meses.",
  },
  modo_historial: {
    titulo: "Cómo proporcionar el historial",
    texto: "El historial anual permite cálculos más completos. Si solo conoces tu salario actual podrás continuar, pero algunas prestaciones pueden quedar incompletas por falta de información histórica.",
  },
  historial_anio_inicio: {
    titulo: "Año inicial del historial",
    texto: "Usa el primer año que deseas registrar dentro de tu historial de cuotas y salarios. Puedes corregirlo si la fecha de ingreso indicada anteriormente no coincide con tu primer registro útil.",
  },
  monto_salario: {
    titulo: "Salario actual",
    texto: "Ingresa el monto vigente que deseas usar como punto de partida para proyectar salarios futuros. No escribas aquí el acumulado salarial del año.",
  },
  periodicidad_salario: {
    titulo: "Periodicidad del salario",
    texto: "Selecciona la forma en que está expresado el monto anterior. La aplicación calculará equivalentes sin cambiar el valor original que ingresaste.",
  },
  proyeccion_anio_fin: {
    titulo: "Horizonte de proyección",
    texto: "El año final debe alcanzar, como mínimo, las fechas de retiro que quieras comparar. Si luego eliges una fecha más lejana, podrás volver y ampliar este horizonte.",
  },
  modalidad_proyeccion: {
    titulo: "Método de proyección",
    texto: "Puedes mantener el salario actual, aplicar una variación anual, indicar un salario futuro conocido o comparar varias tasas. Todos estos valores son escenarios, no registros reales.",
  },
  porcentaje_anual: {
    titulo: "Variación anual",
    texto: "Indica el cambio porcentual que quieres aplicar cada año. Puede ser positivo, cero o negativo y se utiliza únicamente para construir la proyección seleccionada.",
  },
  escenarios_porcentajes: {
    titulo: "Escenarios porcentuales",
    texto: "Escribe varias tasas separadas por comas para comparar trayectorias salariales alternativas sin modificar tu historial real.",
  },
  fecha_corte_retiro: {
    titulo: "Fecha de evaluación",
    texto: "Es la fecha desde la que se evalúan tu edad y los escenarios. Normalmente corresponde al día en que realizas la simulación; no es tu fecha de retiro.",
  },
  ultimo_mes_cuotas: {
    titulo: "Último mes acreditado",
    texto: "Selecciona el último mes que ya figura acreditado por la CSS. Este dato marca hasta dónde llega tu historial real y no debe confundirse con una fecha futura de retiro.",
  },
  fecha_retiro_personalizada: {
    titulo: "Fecha personalizada de retiro",
    texto: "Úsala solo si deseas comparar una fecha distinta de los escenarios predefinidos. La aplicación evaluará esa fecha con las mismas reglas de edad, cuotas y cobertura salarial.",
  },
};

const CAPTIONS_TABLAS = [
  ["history-table", "Historial anual de cuotas y salarios reportados"],
  ["projection-table", "Proyección salarial por año"],
  ["timeline-table", "Línea temporal de historial y proyección"],
  ["retirement-table", "Escenarios de retiro comparados"],
  ["comparison-table", "Comparación de escenarios previsionales"],
  ["results-table", "Detalle del resultado previsional"],
];

let ultimoPanelWizardVisible = null;
let focoInvalidoProgramado = false;

function obtenerEtiquetaControl(control) {
  const etiqueta = document.querySelector(`label[for="${control.id}"]`);
  if (etiqueta) {
    return etiqueta.textContent.replace(/\s+/g, " ").trim();
  }
  return control.getAttribute("aria-label") || control.name || "campo";
}

function anunciarAccesibilidad(mensaje) {
  const region = document.getElementById("a11y-global-status");
  if (!region) {
    return;
  }

  region.textContent = "";
  window.setTimeout(() => {
    region.textContent = mensaje;
  }, 20);
}

function agregarDescripcion(control, idDescripcion) {
  const actuales = (control.getAttribute("aria-describedby") || "")
    .split(/\s+/)
    .filter(Boolean);

  if (!actuales.includes(idDescripcion)) {
    actuales.push(idDescripcion);
    control.setAttribute("aria-describedby", actuales.join(" "));
  }
}

function obtenerMensajeValidacionControl(control) {
  const etiqueta = obtenerEtiquetaControl(control);

  if (control.validity?.valueMissing) {
    return `Completa el campo ${etiqueta}.`;
  }

  if (control.validity?.rangeUnderflow) {
    return `${etiqueta} debe ser igual o mayor que ${control.min}.`;
  }

  if (control.validity?.rangeOverflow) {
    return `${etiqueta} debe ser igual o menor que ${control.max}.`;
  }

  if (control.validity?.stepMismatch) {
    return `Revisa el valor indicado en ${etiqueta}.`;
  }

  return control.validationMessage || `Revisa el campo ${etiqueta}.`;
}


function asegurarErrorDeCampo(control) {
  if (!control.id) {
    return null;
  }

  const idError = `a11y-error-${control.id}`;
  let error = document.getElementById(idError);

  if (!error) {
    error = document.createElement("span");
    error.id = idError;
    error.className = "a11y-field-error";

    const grupo = control.closest(".input-group");
    const referencia = grupo || control;
    referencia.insertAdjacentElement("afterend", error);
  }

  error.textContent = obtenerMensajeValidacionControl(control);
  control.setAttribute("aria-errormessage", idError);
  return error;
}


function limpiarErrorDeCampo(control) {
  if (!control.id) {
    control.removeAttribute("aria-errormessage");
    return;
  }

  const idError = control.getAttribute("aria-errormessage");
  control.removeAttribute("aria-errormessage");

  if (idError?.startsWith("a11y-error-")) {
    document.getElementById(idError)?.remove();
  }
}


function elementoVisible(elemento) {
  return Boolean(
    elemento
    && !elemento.hidden
    && !elemento.classList.contains("d-none")
    && elemento.textContent.trim(),
  );
}


function prepararEstadoVisibilidadMensaje(elemento) {
  const visible = elementoVisible(elemento);
  const teniaEstado = elemento.dataset.a11yVisible !== undefined;
  const estabaVisible = elemento.dataset.a11yVisible === "true";

  elemento.dataset.a11yVisible = String(visible);

  if (
    teniaEstado
    && visible
    && !estabaVisible
    && !focoInvalidoProgramado
  ) {
    window.setTimeout(() => {
      const activo = document.activeElement;
      if (activo?.getAttribute("aria-invalid") === "true") {
        return;
      }

      elemento.focus({ preventScroll: false });
    }, 0);
  }
}

function vincularAyudasDeFormulario() {
  document
    .querySelectorAll("input, select, textarea")
    .forEach((control) => {
      if (!control.id) {
        return;
      }

      let contenedor = control.parentElement;
      if (contenedor?.classList.contains("input-group")) {
        contenedor = contenedor.parentElement;
      }

      let ayuda = contenedor?.querySelector(":scope > .form-text") || null;

      if (!ayuda) {
        const siguiente = control.parentElement?.nextElementSibling;
        if (siguiente?.classList.contains("form-text")) {
          ayuda = siguiente;
        }
      }

      if (!ayuda) {
        return;
      }

      if (!ayuda.id) {
        ayuda.id = `ayuda-${control.id}`;
      }

      agregarDescripcion(control, ayuda.id);
    });
}

function cerrarAyudasContextuales(excepto = null) {
  document
    .querySelectorAll(".context-help-trigger[aria-expanded='true']")
    .forEach((boton) => {
      if (boton === excepto) {
        return;
      }

      boton.setAttribute("aria-expanded", "false");
      const panel = document.getElementById(
        boton.getAttribute("aria-controls"),
      );

      if (panel) {
        panel.hidden = true;
      }
    });
}


function abrirAyudaContextual(boton, panel) {
  cerrarAyudasContextuales(boton);
  boton.setAttribute("aria-expanded", "true");
  panel.hidden = false;
}


function cerrarAyudaContextualSiCorresponde(
  contenedor,
  boton,
  panel,
) {
  window.setTimeout(() => {
    const mantienePuntero = contenedor.matches(":hover");
    const mantieneFoco = document.activeElement === boton;

    if (!mantienePuntero && !mantieneFoco) {
      boton.setAttribute("aria-expanded", "false");
      panel.hidden = true;
    }
  }, 0);
}


function prepararAyudasContextuales() {
  Object.entries(AYUDAS_CONTEXTUALES).forEach(([idControl, ayuda]) => {
    const control = document.getElementById(idControl);
    const etiqueta = document.querySelector(`label[for="${idControl}"]`);

    if (!control || !etiqueta || document.getElementById(`ayuda-contextual-${idControl}`)) {
      return;
    }

    const contenedor = document.createElement("div");
    contenedor.className = "context-help-heading";
    etiqueta.parentNode.insertBefore(contenedor, etiqueta);
    contenedor.appendChild(etiqueta);

    const boton = document.createElement("button");
    boton.type = "button";
    boton.className = "context-help-trigger";
    boton.textContent = "?";
    boton.setAttribute("aria-label", `Ayuda sobre ${ayuda.titulo}`);
    boton.setAttribute("aria-expanded", "false");
    boton.setAttribute("aria-controls", `ayuda-contextual-${idControl}`);
    contenedor.appendChild(boton);

    const panel = document.createElement("div");
    panel.id = `ayuda-contextual-${idControl}`;
    panel.className = "context-help-panel";
    panel.setAttribute("role", "tooltip");
    panel.hidden = true;
    panel.innerHTML = `<strong>${ayuda.titulo}</strong><p>${ayuda.texto}</p>`;
    contenedor.appendChild(panel);

    agregarDescripcion(
      boton,
      panel.id,
    );

    const abrir = () => {
      abrirAyudaContextual(
        boton,
        panel,
      );
    };

    const cerrar = () => {
      cerrarAyudaContextualSiCorresponde(
        contenedor,
        boton,
        panel,
      );
    };

    contenedor.addEventListener(
      "mouseenter",
      abrir,
    );

    contenedor.addEventListener(
      "mouseleave",
      cerrar,
    );

    boton.addEventListener(
      "focus",
      abrir,
    );

    boton.addEventListener(
      "blur",
      cerrar,
    );

    // En equipos táctiles el clic queda como alternativa; en PC no es
    // necesario hacer clic porque el tooltip aparece con hover o foco.
    boton.addEventListener(
      "click",
      abrir,
    );
  });
}

function prepararMensajesDinamicos() {
  document.querySelectorAll(".alert-danger, [id^='error-'], #comparador-error").forEach((elemento) => {
    elemento.setAttribute("role", "alert");
    elemento.removeAttribute("aria-live");
    elemento.setAttribute("aria-atomic", "true");
    elemento.setAttribute("tabindex", "-1");

    if (!elemento.classList.contains("a11y-message-focus")) {
      elemento.classList.add("a11y-message-focus");
    }

    prepararEstadoVisibilidadMensaje(elemento);
  });

  document.querySelectorAll(".alert-warning").forEach((elemento) => {
    if (elemento.getAttribute("role") === "alert") {
      elemento.removeAttribute("aria-live");
    } else {
      elemento.setAttribute("role", "status");
      elemento.setAttribute("aria-live", "polite");
    }

    elemento.setAttribute("aria-atomic", "true");
  });
}

function prepararValidacionAccesible() {
  document.querySelectorAll("form").forEach((formulario) => {
    if (formulario.dataset.a11yValidation === "ready") {
      return;
    }

    formulario.dataset.a11yValidation = "ready";

    formulario.addEventListener("invalid", (evento) => {
      const control = evento.target;

      // UX.4.3: la retroalimentación visual se controla de forma local para
      // evitar depender de globos nativos inconsistentes entre navegadores.
      evento.preventDefault();

      control.setAttribute("aria-invalid", "true");
      asegurarErrorDeCampo(control);

      if (!focoInvalidoProgramado) {
        focoInvalidoProgramado = true;
        const etiqueta = obtenerEtiquetaControl(control);
        window.setTimeout(() => {
          control.focus({ preventScroll: false });
          anunciarAccesibilidad(`Revisa el campo ${etiqueta}.`);
          focoInvalidoProgramado = false;
        }, 0);
      }
    }, true);

    const limpiarSiValido = (evento) => {
      const control = evento.target;
      if (control.validity?.valid === true) {
        control.removeAttribute("aria-invalid");
        limpiarErrorDeCampo(control);
      }
    };

    formulario.addEventListener("input", limpiarSiValido);
    formulario.addEventListener("change", limpiarSiValido);

    formulario.addEventListener("reset", () => {
      window.setTimeout(() => {
        formulario.querySelectorAll("[aria-invalid='true']").forEach((control) => {
          control.removeAttribute("aria-invalid");
          limpiarErrorDeCampo(control);
        });
      }, 0);
    });
  });
}

function prepararSemanticaWizard(enfocarCambio = false) {
  const progreso = document.querySelector(".wizard-steps");
  if (progreso) {
    progreso.setAttribute("role", "navigation");
    progreso.setAttribute("aria-label", "Progreso de la simulación");
  }

  document.querySelectorAll(".wizard-line").forEach((linea) => {
    linea.setAttribute("aria-hidden", "true");
  });

  let panelVisible = null;

  document.querySelectorAll(".wizard-panel[data-panel]").forEach((panel) => {
    const numero = panel.dataset.panel;
    const idPanel = `wizard-panel-${numero}`;
    panel.id = panel.id || idPanel;
    panel.setAttribute("role", "region");

    const titulo = panel.querySelector("h2");
    if (titulo) {
      titulo.id = titulo.id || `wizard-panel-${numero}-titulo`;
      titulo.setAttribute("tabindex", "-1");
      panel.setAttribute("aria-labelledby", titulo.id);
    }

    const oculto = panel.classList.contains("d-none");
    panel.setAttribute("aria-hidden", String(oculto));

    if (!oculto) {
      panelVisible = panel;
    }

    const botonPaso = document.querySelector(`.wizard-step[data-step="${numero}"]`);
    if (botonPaso) {
      botonPaso.setAttribute("aria-controls", panel.id);
    }
  });

  if (!panelVisible) {
    return;
  }

  if (enfocarCambio && ultimoPanelWizardVisible && ultimoPanelWizardVisible !== panelVisible.id) {
    const titulo = panelVisible.querySelector("h2");
    titulo?.focus({ preventScroll: false });
    anunciarAccesibilidad(`Paso ${panelVisible.dataset.panel} de 6. ${titulo?.textContent.trim() || ""}`);
  }

  ultimoPanelWizardVisible = panelVisible.id;
}

function prepararCaptionsTablas() {
  document.querySelectorAll("table").forEach((tabla) => {
    if (tabla.querySelector(":scope > caption")) {
      return;
    }

    const configuracion = CAPTIONS_TABLAS.find(([clase]) => tabla.classList.contains(clase));
    if (!configuracion) {
      return;
    }

    const caption = document.createElement("caption");
    caption.className = "visually-hidden";
    caption.textContent = configuracion[1];
    tabla.prepend(caption);
  });
}

function prepararContenedoresDesplazables() {
  document
    .querySelectorAll(".table-responsive, .history-table-wrapper, .timeline-table-wrapper, .retirement-table-wrapper, .comparison-table-wrapper")
    .forEach((contenedor) => {
      const tieneDesbordamiento = contenedor.scrollWidth > contenedor.clientWidth + 1;

      if (tieneDesbordamiento) {
        contenedor.tabIndex = 0;

        if (!contenedor.classList.contains("table-scroll-focus")) {
          contenedor.classList.add("table-scroll-focus");
        }

        contenedor.setAttribute("aria-label", "Tabla desplazable horizontalmente");
      } else if (contenedor.classList.contains("table-scroll-focus")) {
        contenedor.removeAttribute("tabindex");
        contenedor.classList.remove("table-scroll-focus");
        contenedor.removeAttribute("aria-label");
      }
    });
}

function prepararEnlacesExternos() {
  document.querySelectorAll("a[target='_blank']").forEach((enlace) => {
    if (enlace.dataset.a11yExternal === "ready") {
      return;
    }

    const aviso = document.createElement("span");
    aviso.className = "visually-hidden";
    aviso.textContent = " (abre en una pestaña nueva)";
    enlace.appendChild(aviso);
    enlace.dataset.a11yExternal = "ready";
  });
}

function sincronizarAccesibilidadDinamica() {
  vincularAyudasDeFormulario();
  prepararAyudasContextuales();
  prepararMensajesDinamicos();
  prepararCaptionsTablas();
  prepararContenedoresDesplazables();
  prepararEnlacesExternos();
}

document.addEventListener("DOMContentLoaded", () => {
  sincronizarAccesibilidadDinamica();
  prepararValidacionAccesible();
  prepararSemanticaWizard(false);

  const observador = new MutationObserver((cambios) => {
    const cambioPanel = cambios.some((cambio) => (
      cambio.type === "attributes"
      && cambio.target.classList?.contains("wizard-panel")
    ));

    sincronizarAccesibilidadDinamica();
    prepararValidacionAccesible();
    prepararSemanticaWizard(cambioPanel);
  });

  observador.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ["class"],
  });

  document.addEventListener("pointerdown", (evento) => {
    if (!evento.target.closest(".context-help-heading")) {
      cerrarAyudasContextuales();
    }
  });

  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape") {
      cerrarAyudasContextuales();
    }
  });

  window.addEventListener("resize", prepararContenedoresDesplazables);
});
