"use strict";


/* ============================================================
   Entrada y formato monetario
   ============================================================ */

/*
 * Los campos monetarios aceptan punto como separador decimal y
 * muestran coma como separador de miles. La interfaz limita la
 * edición a dos decimales; el backend vuelve a validar la precisión.
 */


/**
 * Elimina separadores visuales y limita la parte decimal.
 *
 * @param {string} texto Texto introducido por el Asegurado(a).
 * @param {boolean} permitirNegativo Permite signo negativo.
 * @returns {string} Texto numérico normalizado.
 */
function normalizarEntradaDecimal(
  texto,
  permitirNegativo = false,
) {
  let valor = String(
    texto ?? "",
  ).trim();

  const negativo = (
    permitirNegativo
    && valor.startsWith("-")
  );

  valor = valor
    .replace(/,/g, "")
    .replace(/[^\d.]/g, "");

  const partes = valor.split(".");
  const entero = partes.shift() || "";

  let decimales = partes.join("");
  decimales = decimales.slice(0, 2);

  let resultado = entero;

  if (
    valor.includes(".")
    && (
      decimales !== ""
      || valor.endsWith(".")
    )
  ) {
    resultado += `.${decimales}`;
  }

  if (negativo && resultado !== "") {
    resultado = `-${resultado}`;
  }

  return resultado;
}


/**
 * Convierte un texto monetario visible en número.
 *
 * @param {string|number} valor Valor editable o guardado.
 * @returns {number} Valor numérico.
 */
function obtenerValorMonetario(valor) {
  const texto = normalizarEntradaDecimal(
    String(valor ?? ""),
    false,
  );

  return Number(texto);
}


/**
 * Formatea un número con separador de miles y dos decimales.
 *
 * @param {string|number} valor Valor monetario.
 * @returns {string} Número sin prefijo de moneda.
 */
function formatearNumeroMonetario(valor) {
  const numero = obtenerValorMonetario(
    valor,
  );

  if (!Number.isFinite(numero)) {
    return "";
  }

  return numero.toLocaleString(
    "en-US",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
  );
}


/**
 * Configura un input monetario para edición segura.
 *
 * Durante la edición se retiran las comas para no interferir con
 * el cursor. Al salir del campo se muestran miles y centavos.
 *
 * @param {HTMLInputElement} input Campo que se configurará.
 */
function configurarCampoMonetario(input) {
  if (
    !input
    || input.dataset.moneyConfigured === "true"
  ) {
    return;
  }

  input.dataset.moneyConfigured = "true";
  input.inputMode = "decimal";
  input.autocomplete = "off";

  input.addEventListener(
    "focus",
    () => {
      input.value = normalizarEntradaDecimal(
        input.value,
      );
    },
  );

  input.addEventListener(
    "input",
    () => {
      const normalizado = normalizarEntradaDecimal(
        input.value,
      );

      if (input.value !== normalizado) {
        input.value = normalizado;
      }
    },
  );

  input.addEventListener(
    "blur",
    () => {
      if (input.value.trim() === "") {
        return;
      }

      input.value = formatearNumeroMonetario(
        input.value,
      );
    },
  );

  if (input.value.trim() !== "") {
    input.value = formatearNumeroMonetario(
      input.value,
    );
  }
}


/**
 * Configura los campos monetarios estáticos encontrados.
 *
 * @param {ParentNode} raiz Contenedor donde se buscarán campos.
 */
function configurarCamposMonetarios(
  raiz = document,
) {
  raiz
    .querySelectorAll(".money-input")
    .forEach(
      configurarCampoMonetario,
    );
}


/**
 * Limita un input decimal genérico a dos posiciones.
 *
 * @param {HTMLInputElement} input Campo porcentual u otro decimal.
 * @param {boolean} permitirNegativo Permite valores negativos.
 */
function configurarCampoDecimal(
  input,
  permitirNegativo = false,
) {
  if (
    !input
    || input.dataset.decimalConfigured === "true"
  ) {
    return;
  }

  input.dataset.decimalConfigured = "true";
  input.inputMode = "decimal";

  input.addEventListener(
    "input",
    () => {
      const normalizado = normalizarEntradaDecimal(
        input.value,
        permitirNegativo,
      );

      if (input.value !== normalizado) {
        input.value = normalizado;
      }
    },
  );
}


document.addEventListener(
  "DOMContentLoaded",
  () => {
    configurarCamposMonetarios();
  },
);
