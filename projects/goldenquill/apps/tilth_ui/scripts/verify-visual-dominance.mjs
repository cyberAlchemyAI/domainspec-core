// Closes the "blocker text is in the DOM but rendered at 8px gray / collapsed /
// occluded by an overlay" hole that string-match HTML scanning cannot catch.
//
// For each route with a per-route blocker rule in
// src/doctrine/banned-terms.json (required_blocker_copy register), this script
// loads the route in a headless Chromium and asserts the required strings are:
//   - present and visible (display + visibility + opacity)
//   - rendered at >= MIN_BLOCKER_FONT_PX
//   - have a non-zero bounding box
//   - not occluded at their own centerpoint by some other element on top
//
// Runs as a separate gate (not folded into e2e-ui.mjs) so it stays
// independently auditable and survives parallel edits to e2e-ui.mjs.
//
// Exits 0 on full pass, 1 on any failure.

import { spawn } from "node:child_process";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import { stat } from "node:fs/promises";
import { join } from "node:path";
import { chromium } from "playwright";
import { loadRegister } from "../src/doctrine/banned-terms.mjs";

const MIN_BLOCKER_FONT_PX = 14;
const MIN_BLOCKER_OPACITY = 0.9;

const port = Number(process.env.PORT || 4199);
const baseUrl = `http://127.0.0.1:${port}`;
const appRoot = fileURLToPath(new URL("..", import.meta.url));

// Routes the gate exercises. Each one carries at least one substring that
// matches a per-route rule in src/doctrine/banned-terms.json.
const CANDIDATE_ROUTES = [
  "/stitch_tilth_os_institutional_shell%203/final_packet_authorization_cooperative_representation_warning/code.html",
  "/stitch_tilth_os_institutional_shell%203/final_packet_authorization_hardened_beneficiary_identity_lock/code.html",
  "/stitch_tilth_os_institutional_shell%203/eligibility_gates_fail_closed_protocol_1/code.html",
  "/stitch_tilth_os_institutional_shell%203/eligibility_gates_fail_closed_protocol_2/code.html",
  "/stitch_tilth_os_institutional_shell%203/eligibility_gates_fail_closed_state/code.html",
  "/stitch_tilth_os_institutional_shell%203/logician_eligibility_gates_fail_closed_logic/code.html",
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function waitForServer() {
  const deadline = Date.now() + 20_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${baseUrl}/api/projections/current`);
      if (response.ok) return;
    } catch {
      // server still starting
    }
    await delay(250);
  }
  throw new Error(`Server did not become ready at ${baseUrl}`);
}

async function launchBrowser() {
  try {
    return await chromium.launch({ headless: true, channel: "chrome" });
  } catch {
    return await chromium.launch({ headless: true });
  }
}

function blockerRulesForRoute(register, route) {
  const group = register.registers.required_blocker_copy;
  if (!group) return [];
  return group.entries.filter((entry) => {
    const inRoute = entry.route_match_any.some((m) => route.includes(m));
    if (!inRoute) return false;
    const inState = entry.state_match_any.some((m) => route.includes(m));
    if (!inState) return false;
    const excluded = (entry.state_exclude_any || []).some((m) => route.includes(m));
    return !excluded;
  });
}

async function assertVisuallyDominant(page, requiredText, route, ruleId) {
  const locator = page.getByText(requiredText, { exact: false }).first();
  const count = await locator.count();
  assert(count > 0, `${route} [${ruleId}] required text missing from DOM: ${JSON.stringify(requiredText)}`);

  const visible = await locator.isVisible().catch(() => false);
  assert(visible, `${route} [${ruleId}] required text not visible (display/visibility/opacity collapsed): ${JSON.stringify(requiredText)}`);

  const metrics = await locator.evaluate((el, { minPx, minOpacity }) => {
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const fontPx = parseFloat(style.fontSize) || 0;
    const opacity = parseFloat(style.opacity);
    const cx = Math.round(rect.left + rect.width / 2);
    const cy = Math.round(rect.top + rect.height / 2);
    const topEl = document.elementFromPoint(cx, cy);
    const onTop = topEl === el || (topEl && el.contains(topEl)) || (topEl && topEl.contains(el));
    return {
      fontPx,
      opacity: Number.isFinite(opacity) ? opacity : 1,
      width: rect.width,
      height: rect.height,
      onTop: !!onTop,
      meetsFont: fontPx >= minPx,
      meetsOpacity: (Number.isFinite(opacity) ? opacity : 1) >= minOpacity,
    };
  }, { minPx: MIN_BLOCKER_FONT_PX, minOpacity: MIN_BLOCKER_OPACITY });

  assert(metrics.width > 0 && metrics.height > 0, `${route} [${ruleId}] required text has zero bounding box: ${JSON.stringify(requiredText)} → ${JSON.stringify(metrics)}`);
  assert(metrics.meetsFont, `${route} [${ruleId}] required text rendered below ${MIN_BLOCKER_FONT_PX}px (got ${metrics.fontPx}px): ${JSON.stringify(requiredText)}`);
  assert(metrics.meetsOpacity, `${route} [${ruleId}] required text opacity ${metrics.opacity} below threshold ${MIN_BLOCKER_OPACITY}: ${JSON.stringify(requiredText)}`);
  assert(metrics.onTop, `${route} [${ruleId}] required text occluded at center by another element: ${JSON.stringify(requiredText)}`);
}

async function ensureStitchAssets() {
  try {
    await stat(join(appRoot, "stitch_tilth_os_institutional_shell 3"));
    await stat(join(appRoot, "assets", "stitch-fonts.css"));
    await stat(join(appRoot, "assets", "stitch-tailwind.css"));
    return true;
  } catch {
    return false;
  }
}

const server = spawn(process.execPath, ["server.mjs"], {
  cwd: appRoot,
  env: { ...process.env, PORT: String(port) },
  stdio: ["ignore", "pipe", "pipe"],
});

let browser;
try {
  await waitForServer();

  if (!(await ensureStitchAssets())) {
    console.log("[SKIP] Stitch assets missing — verify:visual-dominance skipped.");
    process.exit(0);
  }

  const register = await loadRegister();
  browser = await launchBrowser();
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });

  let routesExercised = 0;
  let assertionsRun = 0;
  for (const route of CANDIDATE_ROUTES) {
    const rules = blockerRulesForRoute(register, route);
    if (rules.length === 0) continue;
    routesExercised += 1;

    const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "domcontentloaded" });
    if (!response || !response.ok()) {
      throw new Error(`Route ${route} returned HTTP ${response ? response.status() : "no-response"}`);
    }

    for (const rule of rules) {
      for (const requiredText of rule.required_strings || []) {
        await assertVisuallyDominant(page, requiredText, route, rule.id);
        assertionsRun += 1;
      }
      for (const altGroup of rule.required_strings_any_of || []) {
        const bodyText = await page.locator("body").innerText();
        const matchedText = altGroup.find((s) => bodyText.includes(s));
        assert(
          matchedText,
          `${route} [${rule.id}] none of any_of group present in body: ${altGroup.map((s) => JSON.stringify(s)).join(", ")}`,
        );
        await assertVisuallyDominant(page, matchedText, route, rule.id);
        assertionsRun += 1;
      }
    }
  }

  if (routesExercised === 0) {
    console.log("[SKIP] No CANDIDATE_ROUTES matched any blocker rules — register or route list out of sync.");
    process.exit(0);
  }
  console.log(`Visual-dominance gate PASSED: ${routesExercised} routes, ${assertionsRun} assertions.`);
} finally {
  if (browser) await browser.close();
  server.kill("SIGTERM");
  await delay(250);
}
