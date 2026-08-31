"use strict";

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";


const BASE_URL = (
  process.env.MRP_VISUAL_BASE_URL
  || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

const OUTPUT_DIR = (
  process.env.VISUAL_A11Y_OUTPUT
  || path.join(
    os.tmpdir(),
    "mrp-visual-a11y",
  )
);

const STRICT_A11Y = (
  process.env.MRP_A11Y_STRICT === "1"
);

const STORAGE_KEY = "miRetiroProyectado.tema";

const ROUTES = [
  "/",
  "/simulacion",
  "/comparar",
  "/como-se-calcula",
  "/metodologia",
  "/dev",
];

const SCENARIOS = [
  {
    name: "mobile-light",
    width: 360,
    height: 800,
    theme: "light",
  },
  {
    name: "tablet-dark",
    width: 768,
    height: 1024,
    theme: "dark",
  },
  {
    name: "desktop-contrast",
    width: 1440,
    height: 900,
    theme: "contrast",
  },
];


function slug(value) {
  if (value === "/") {
    return "inicio";
  }

  return value
    .replace(/^\/+/, "")
    .replace(/[^a-zA-Z0-9_-]+/g, "-")
    .replace(/-+/g, "-");
}


function ensureOutputDirectories() {
  fs.mkdirSync(
    OUTPUT_DIR,
    {
      recursive: true,
    },
  );

  fs.mkdirSync(
    path.join(
      OUTPUT_DIR,
      "screenshots",
    ),
    {
      recursive: true,
    },
  );
}


function markdownReport(report) {
  const lines = [
    "# Visual & Accessibility Baseline",
    "",
    `- **Resultado operativo:** \`${report.operationalResult.toUpperCase()}\``,
    `- **Modo axe:** \`${report.strictA11y ? "strict" : "informativo"}\``,
    `- **Páginas evaluadas:** \`${report.results.length}\``,
    `- **Violaciones axe:** \`${report.totalViolations}\``,
    `- **Errores operativos:** \`${report.operationalErrors.length}\``,
    "",
    "## Escenarios",
    "",
  ];

  for (const item of report.results) {
    lines.push(
      `- \`${item.scenario}\` — \`${item.route}\`: `
      + `${item.violations} violaciones, HTTP ${item.status}.`,
    );
  }

  if (report.operationalErrors.length) {
    lines.push(
      "",
      "## Errores operativos",
      "",
    );

    for (const error of report.operationalErrors) {
      lines.push(
        `- ${error}`,
      );
    }
  }

  return `${lines.join("\n")}\n`;
}


async function analyzePage(
  browser,
  scenario,
  route,
) {
  const context = await browser.newContext({
    viewport: {
      width: scenario.width,
      height: scenario.height,
    },
  });

  await context.addInitScript(
    ({ key, theme }) => {
      window.localStorage.setItem(
        key,
        theme,
      );
    },
    {
      key: STORAGE_KEY,
      theme: scenario.theme,
    },
  );

  const page = await context.newPage();

  const consoleErrors = [];
  const pageErrors = [];

  page.on(
    "console",
    (message) => {
      if (message.type() === "error") {
        consoleErrors.push(
          message.text(),
        );
      }
    },
  );

  page.on(
    "pageerror",
    (error) => {
      pageErrors.push(
        String(error),
      );
    },
  );

  const response = await page.goto(
    `${BASE_URL}${route}`,
    {
      waitUntil: "domcontentloaded",
      timeout: 30000,
    },
  );

  if (!response) {
    throw new Error(
      `${route}: navegación sin respuesta HTTP.`,
    );
  }

  const status = response.status();

  if (status < 200 || status >= 400) {
    throw new Error(
      `${route}: HTTP ${status}.`,
    );
  }

  await page.waitForLoadState(
    "networkidle",
    {
      timeout: 8000,
    },
  ).catch(
    () => {},
  );

  const appliedTheme = await page.evaluate(
    () => (
      document.documentElement
        .getAttribute("data-app-theme")
    ),
  );

  if (appliedTheme !== scenario.theme) {
    throw new Error(
      `${route}: tema esperado ${scenario.theme}, `
      + `obtenido ${appliedTheme}.`,
    );
  }

  const axe = await new AxeBuilder({
    page,
  })
    .withTags([
      "wcag2a",
      "wcag2aa",
      "wcag21a",
      "wcag21aa",
      "wcag22a",
      "wcag22aa",
    ])
    .analyze();

  const screenshotName = (
    `${scenario.name}--${slug(route)}.png`
  );

  await page.screenshot({
    path: path.join(
      OUTPUT_DIR,
      "screenshots",
      screenshotName,
    ),
    fullPage: true,
  });

  const result = {
    scenario: scenario.name,
    route,
    theme: scenario.theme,
    viewport: {
      width: scenario.width,
      height: scenario.height,
    },
    status,
    violations: axe.violations.length,
    violationDetails: axe.violations.map(
      (violation) => ({
        id: violation.id,
        impact: violation.impact,
        description: violation.description,
        nodes: violation.nodes.length,
      }),
    ),
    consoleErrors,
    pageErrors,
    screenshot: screenshotName,
  };

  await context.close();

  return result;
}


async function main() {
  ensureOutputDirectories();

  const browser = await chromium.launch({
    headless: true,
  });

  const results = [];
  const operationalErrors = [];

  try {
    for (const scenario of SCENARIOS) {
      for (const route of ROUTES) {
        process.stdout.write(
          `[visual-a11y] ${scenario.name} ${route} ... `,
        );

        try {
          const result = await analyzePage(
            browser,
            scenario,
            route,
          );

          results.push(
            result,
          );

          console.log(
            `OK (${result.violations} axe)`,
          );
        } catch (error) {
          const message = (
            `${scenario.name} ${route}: ${String(error)}`
          );

          operationalErrors.push(
            message,
          );

          console.log(
            "FAIL",
          );

          console.error(
            `[visual-a11y] ${message}`,
          );
        }
      }
    }
  } finally {
    await browser.close();
  }

  const totalViolations = results.reduce(
    (total, item) => (
      total + item.violations
    ),
    0,
  );

  const report = {
    schemaVersion: 1,
    strictA11y: STRICT_A11Y,
    baseUrl: BASE_URL,
    scenarios: SCENARIOS,
    routes: ROUTES,
    evaluated: results.length,
    totalViolations,
    operationalResult: (
      operationalErrors.length
        ? "fail"
        : "pass"
    ),
    operationalErrors,
    results,
  };

  fs.writeFileSync(
    path.join(
      OUTPUT_DIR,
      "accessibility-report.json",
    ),
    `${JSON.stringify(report, null, 2)}\n`,
    "utf8",
  );

  fs.writeFileSync(
    path.join(
      OUTPUT_DIR,
      "summary.md",
    ),
    markdownReport(report),
    "utf8",
  );

  console.log();
  console.log(
    `[visual-a11y] Evaluadas: ${results.length}`,
  );

  console.log(
    `[visual-a11y] Violaciones axe: ${totalViolations}`,
  );

  console.log(
    `[visual-a11y] Errores operativos: ${operationalErrors.length}`,
  );

  if (operationalErrors.length) {
    process.exitCode = 2;
    return;
  }

  if (
    STRICT_A11Y
    && totalViolations > 0
  ) {
    process.exitCode = 1;
  }
}


main().catch(
  (error) => {
    console.error(
      `[visual-a11y] ERROR FATAL: ${String(error)}`,
    );

    process.exitCode = 2;
  },
);
