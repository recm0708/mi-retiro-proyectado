"use strict";

/*
 * Mi Retiro Proyectado — Gestión de apariencia.
 *
 * Propósito: Aplica Sistema, Claro, Oscuro y Alto contraste y conserva la preferencia visual independiente de la simulación.
 * Alcance: La clave de tema en localStorage no forma parte de datos previsionales ni de consentimiento.
 */

(() => {

  const STORAGE_KEY = "miRetiroProyectado.tema";
  const VALID_THEMES = new Set(["system", "light", "dark", "contrast"]);
  const mediaDark = window.matchMedia("(prefers-color-scheme: dark)");

  const THEME_LABELS = {
    system: "Sistema",
    light: "Claro",
    dark: "Oscuro",
    contrast: "Contraste",
  };

  function readPreference() {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      return VALID_THEMES.has(saved) ? saved : "system";
    } catch {
      return "system";
    }
  }

  function resolveBootstrapTheme(preference) {
    if (preference === "contrast") {
      return "dark";
    }

    if (preference === "system") {
      return mediaDark.matches ? "dark" : "light";
    }

    return preference;
  }

  function applyTheme(preference) {
    const normalized = VALID_THEMES.has(preference)
      ? preference
      : "system";

    const bootstrapTheme = resolveBootstrapTheme(normalized);
    const root = document.documentElement;

    root.setAttribute("data-app-theme", normalized);
    root.setAttribute("data-bs-theme", bootstrapTheme);
    root.style.colorScheme = bootstrapTheme;

    return normalized;
  }

  function savePreference(preference) {
    try {
      window.localStorage.setItem(STORAGE_KEY, preference);
    } catch {
      // La aplicación continúa funcionando si el navegador bloquea storage.
    }
  }

  function updateControls(preference) {
    const trigger = document.getElementById("menu-apariencia");
    const triggerLabel = document.getElementById("theme-trigger-label");
    const legacySelector = document.getElementById("selector-tema");

    if (trigger) {
      trigger.dataset.themeCurrent = preference;
      trigger.setAttribute(
        "aria-label",
        `Cambiar apariencia. Tema actual: ${THEME_LABELS[preference]}`,
      );
    }

    if (triggerLabel) {
      triggerLabel.textContent = THEME_LABELS[preference];
    }

    document.querySelectorAll("[data-theme-choice]").forEach((button) => {
      const selected = button.dataset.themeChoice === preference;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-pressed", selected ? "true" : "false");
    });

    // Compatibilidad defensiva con plantillas anteriores durante actualizaciones.
    if (legacySelector) {
      legacySelector.value = preference;
    }
  }

  function selectTheme(preference) {
    const normalized = applyTheme(preference);
    savePreference(normalized);
    updateControls(normalized);
    return normalized;
  }

  const initialPreference = applyTheme(readPreference());

  document.addEventListener("DOMContentLoaded", () => {
    updateControls(initialPreference);

    document.querySelectorAll("[data-theme-choice]").forEach((button) => {
      button.addEventListener("click", () => {
        selectTheme(button.dataset.themeChoice);
      });
    });

    const legacySelector = document.getElementById("selector-tema");
    if (legacySelector) {
      legacySelector.addEventListener("change", () => {
        selectTheme(legacySelector.value);
      });
    }
  });

  mediaDark.addEventListener("change", () => {
    if (readPreference() === "system") {
      applyTheme("system");
      updateControls("system");
    }
  });
})();
