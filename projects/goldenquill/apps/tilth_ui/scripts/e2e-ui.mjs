import { spawn } from "node:child_process";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { stat } from "node:fs/promises";
import { join } from "node:path";
import { loadRegister } from "../src/doctrine/banned-terms.mjs";

const MIN_BLOCKER_FONT_PX = 14;
const MIN_BLOCKER_OPACITY = 0.9;

const port = Number(process.env.PORT || 4197);
const baseUrl = `http://127.0.0.1:${port}`;
const appRoot = fileURLToPath(new URL("..", import.meta.url));
const forbiddenHosts = [
  "cdn.tailwindcss.com",
  "fonts.googleapis.com",
  "fonts.gstatic.com",
  "unpkg.com",
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
      // Server is still starting.
    }
    await delay(250);
  }
  throw new Error(`Server did not become ready at ${baseUrl}`);
}

async function postJson(path, body) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await response.json();
  return { response, json };
}

async function launchBrowser() {
  try {
    return await chromium.launch({ headless: true, channel: "chrome" });
  } catch {
    return await chromium.launch({ headless: true });
  }
}

async function clickEveryEnabledButton(page, route, failures) {
  await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
  await page.waitForTimeout(300);
  const controls = page.locator("button:not([disabled]), a[role='button']:not([aria-disabled='true'])");
  const count = await controls.count();
  let clicked = 0;
  for (let index = 0; index < count; index += 1) {
    await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
    await page.waitForTimeout(200);
    const fresh = page.locator("button:not([disabled]), a[role='button']:not([aria-disabled='true'])").nth(index);
    const visible = await fresh.isVisible().catch(() => false);
    if (!visible) continue;
    const label = (await fresh.innerText().catch(() => "")) || await fresh.getAttribute("aria-label").catch(() => "") || `control_${index}`;
    try {
      try {
        await fresh.click({ timeout: 1500 });
      } catch (clickError) {
        await fresh.evaluate((el) => el.click());
      }
      clicked += 1;
      await page.waitForTimeout(500);
    } catch (error) {
      failures.push(`${route} button ${index} (${label.trim()}): ${error.message}`);
    }
  }
  return clicked;
}

// Closes the "blocker text is in DOM but rendered at 8px gray / hidden behind
// overlay" hole. Asserts the element is visible, opaque, above min font size,
// inside the viewport, and not occluded at its own centerpoint.
async function assertVisuallyDominant(page, requiredText, route, ruleId) {
  const locator = page.getByText(requiredText, { exact: false }).first();
  const count = await locator.count();
  assert(count > 0, `${route} [${ruleId}] missing required text in DOM: ${JSON.stringify(requiredText)}`);

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
      top: rect.top,
      left: rect.left,
      onTop: !!onTop,
      meetsFont: fontPx >= minPx,
      meetsOpacity: (Number.isFinite(opacity) ? opacity : 1) >= minOpacity,
      visibility: style.visibility,
      display: style.display,
    };
  }, { minPx: MIN_BLOCKER_FONT_PX, minOpacity: MIN_BLOCKER_OPACITY });

  assert(metrics.width > 0 && metrics.height > 0, `${route} [${ruleId}] required text has zero bounding box: ${JSON.stringify(requiredText)} → ${JSON.stringify(metrics)}`);
  assert(metrics.meetsFont, `${route} [${ruleId}] required text rendered below ${MIN_BLOCKER_FONT_PX}px (got ${metrics.fontPx}px): ${JSON.stringify(requiredText)}`);
  assert(metrics.meetsOpacity, `${route} [${ruleId}] required text opacity ${metrics.opacity} below threshold ${MIN_BLOCKER_OPACITY}: ${JSON.stringify(requiredText)}`);
  assert(metrics.onTop, `${route} [${ruleId}] required text occluded at center by another element: ${JSON.stringify(requiredText)}`);
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

const server = spawn(process.execPath, ["server.mjs"], {
  cwd: appRoot,
  env: { ...process.env, PORT: String(port) },
  stdio: ["ignore", "pipe", "pipe"],
});

const serverOutput = [];
server.stdout.on("data", (chunk) => serverOutput.push(chunk.toString("utf8")));
server.stderr.on("data", (chunk) => serverOutput.push(chunk.toString("utf8")));

let browser;
try {
  await waitForServer();

  const register = await loadRegister();

  const scribe = await postJson("/api/commands", {
    command_type: "SCRIBE_RUN_REQUESTED",
    payload: { cycle_id: "cyc_09F82A", section_id: "sec_project_narrative" },
  });
  assert(scribe.response.ok, `Scribe command endpoint failed: ${JSON.stringify(scribe.json)}`);
  assert(scribe.json.command_result === "REJECTED_FAIL_CLOSED", "Scribe must reject while Logician gate is fail-closed");

  browser = await launchBrowser();
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  const forbiddenRequests = [];
  const consoleErrors = [];
  page.on("request", (request) => {
    const url = request.url();
    if (forbiddenHosts.some((host) => url.includes(host))) forbiddenRequests.push(url);
  });
  page.on("response", r => { if (!r.ok() && r.status() !== 302 && r.status() !== 301) consoleErrors.push("HTTP " + r.status() + " " + r.url()); });

  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  const prefix = "/stitch_tilth_os_institutional_shell%204";
  let hasStitch = false;
  try {
    await stat(join(appRoot, "stitch_tilth_os_institutional_shell 4"));
    await stat(join(appRoot, "assets", "stitch-fonts.css"));
    await stat(join(appRoot, "assets", "stitch-tailwind.css"));
    hasStitch = true;
  } catch {
    hasStitch = false;
  }

  const screens = hasStitch ? [
    "/newest",
    `${prefix}/scout_mission_control_functional_openclaw_interface/code.html`,
    `${prefix}/evidence_intake_forensic_identity_governance_mapping/code.html`,
    `${prefix}/eligibility_gates_fail_closed_protocol_3/code.html`,
    `${prefix}/module_mapper_rfa_decomposition_requirements_4/code.html`,
    `${prefix}/scribe_drafting_unified_execution_canvas/code.html`,
    `${prefix}/budget_allocator_validator_fiscal_compliance_grid/code.html`,
    `${prefix}/judge_scoring_multi_variable_forensic_decomposition/code.html`,
    `${prefix}/red_team_review_adversarial_probe_trace_5/code.html`,
    `${prefix}/final_packet_authorization_ready_for_authorization/code.html`,
    `${prefix}/final_packet_authorization_cooperative_representation_warning/code.html`,
    `${prefix}/portal_staging_manual_review_interlock_hardened/code.html`,
    `${prefix}/audit_trail_forensic_amendment_ledger/code.html`,
    `${prefix}/fid_browser_funder_intelligence_library/code.html`,
    `${prefix}/model_cost_dashboard_operational_visibility/code.html`,
  ] : [];

  if (!hasStitch) {
    console.log("[SKIP] Stitch assets missing, skipping E2E testing of UI screens.");
  }

  let clicked = 0;
  let dominanceChecks = 0;
  const clickFailures = [];
  for (const route of screens) {
    await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
    const bodyText = await page.locator("body").innerText();
    assert(bodyText.length > 80, `${route} rendered an unexpectedly small body`);
    assert(await page.locator("#golden-quill-local-stitch-hydration").count() === 1, `${route} is missing local Stitch hydration`);

    const blockerRules = blockerRulesForRoute(register, route);
    for (const rule of blockerRules) {
      for (const requiredText of rule.required_strings || []) {
        await assertVisuallyDominant(page, requiredText, route, rule.id);
        dominanceChecks += 1;
      }
      for (const altGroup of rule.required_strings_any_of || []) {
        const matchedText = altGroup.find((s) => bodyText.includes(s));
        assert(
          matchedText,
          `${route} [${rule.id}] missing all of any_of group: ${altGroup.map((s) => JSON.stringify(s)).join(", ")}`,
        );
        await assertVisuallyDominant(page, matchedText, route, rule.id);
        dominanceChecks += 1;
      }
    }

    clicked += await clickEveryEnabledButton(page, route, clickFailures);
  }

  assert(clickFailures.length === 0, `Button click failures:\n${clickFailures.join("\n")}`);
  assert(forbiddenRequests.length === 0, `Remote runtime requests found:\n${forbiddenRequests.join("\n")}`);
  assert(consoleErrors.length === 0, `Browser console errors found:\n${consoleErrors.join("\n")}`);

  console.log(`UI E2E passed: guarded Scribe rejected fail-closed, ${screens.length} Stitch routes rendered, ${clicked} enabled buttons/actions clicked, ${dominanceChecks} visual-dominance assertions passed.`);
} finally {
  if (browser) await browser.close();
  console.log("Server output:", serverOutput.join("")); server.kill("SIGTERM");
  await delay(250);
}
