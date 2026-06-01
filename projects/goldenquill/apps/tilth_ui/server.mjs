import { createServer } from "node:http";
import { readFile, readdir, stat } from "node:fs/promises";
import { createReadStream } from "node:fs";
import { extname, join, normalize, relative, isAbsolute } from "node:path";
import { fileURLToPath } from "node:url";
import { buildLocalProjection } from "./src/read-model/projection.mjs";
import { handleCommand } from "./src/read-model/commands.mjs";
import { handleOpenClawRequest } from "./src/openclaw.mjs";

const root = fileURLToPath(new URL(".", import.meta.url));
const port = Number(process.env.PORT || 4173);
const activeStitchDirName = "stitch_tilth_os_institutional_shell 4";
const activeStitchUrlRoot = `/${encodeURIComponent(activeStitchDirName)}`;
const latestStitchEntry = `${activeStitchUrlRoot}/scout_mission_control_functional_openclaw_interface/code.html`;
const stitchScreenPrefix = `${activeStitchUrlRoot}/`;
const retiredStitchScreens = new Set(["card_matrix_institutional_identity_topology"]);

const stitchNavRoutes = {
  "home": "tilth_os_appshell_institutional_workstation",
  "scout profile": "scout_about_me",
  "scout-about": "scout_about_me",
  "scout": "scout_mission_control_functional_openclaw_interface",
  "upload": "portal_staging_autonomous_upload_console",
  "application/cyc_09f82a": "module_mapper_rfa_decomposition_requirements_4",
  "eligibility/cyc_09f82a": "eligibility_gates_fail_closed_protocol_3",
  "drafting/cyc_09f82a": "scribe_drafting_unified_execution_canvas",
  "budget/cyc_09f82a": "budget_allocator_validator_fiscal_compliance_grid",
  "judge/cyc_09f82a": "judge_scoring_multi_variable_forensic_decomposition",
  "red-team/cyc_09f82a": "red_team_review_adversarial_probe_trace_5",
  "sign-off/cyc_09f82a": "final_packet_authorization_ready_for_authorization",
  "audit/cyc_09f82a": "audit_trail_forensic_amendment_ledger",
  "intake": "evidence_intake_forensic_identity_governance_mapping",
  "quarantine": "logician_eligibility_fail_closed_state",
  "sync": "portal_staging_hardened_beneficiary_command_sync",
  "portal-staging/cyc_09f82a": "portal_staging_manual_review_interlock_hardened"
};

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".woff2": "font/woff2",
};

const localOnlyCsp = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline'",
  "font-src 'self' data:",
  "img-src 'self' data:",
  "connect-src 'self'",
].join("; ");

function safePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?")[0]);
  const normalized = normalize(decoded).replace(/^(\.\.[/\\])+/, "");
  const target = join(root, normalized === "/" ? "index.html" : normalized);
  const rel = relative(root, target);
  if (rel.startsWith("..") || isAbsolute(rel)) {
    throw new Error("Directory traversal detected");
  }
  return target;
}

function htmlEsc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[char]);
}

function writeJson(res, statusCode, value) {
  const body = JSON.stringify(value, null, 2);
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
    "Cache-Control": "no-store",
    "Content-Security-Policy": localOnlyCsp,
  });
  res.end(body);
}

async function readJsonBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const text = Buffer.concat(chunks).toString("utf8");
  if (!text.trim()) return {};
  return JSON.parse(text);
}

function screenLabel(name) {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function stitchPath(screenName) {
  return `${stitchScreenPrefix}${encodeURIComponent(screenName)}/code.html`;
}

async function serveFile(res, filePath) {
  const fileStat = await stat(filePath);
  if (!fileStat.isFile()) throw new Error("not a file");
  res.writeHead(200, {
    "Content-Type": types[extname(filePath)] || "application/octet-stream",
    "Content-Length": fileStat.size,
    "Content-Security-Policy": localOnlyCsp,
  });
  createReadStream(filePath).pipe(res);
}

function stitchHydrationScript() {
  // Hydration JS lives at assets/stitch-hydration.js as a static file so it can
  // be lint-scanned by scripts/doctrine-lint.mjs. The inline bootstrap only
  // injects the server-side route table — the doctrine-bearing logic is in the
  // external file.
  const routesJson = JSON.stringify(stitchNavRoutes);
  const prefixJson = JSON.stringify(stitchScreenPrefix);
  return `
<script id="golden-quill-local-stitch-hydration-config">window.__GQ_ROUTES=${routesJson};window.__GQ_STITCH_PREFIX=${prefixJson};</script>
<script src="/assets/stitch-hydration.js" id="golden-quill-local-stitch-hydration"></script>`;
}

async function serveHydratedStitchScreen(res, filePath) {
  const html = await readFile(filePath, "utf8");
  const script = stitchHydrationScript();
  const hydrated = html.includes("</body>")
    ? html.replace("</body>", `${script}</body>`)
    : `${html}${script}`;

  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": Buffer.byteLength(hydrated),
    "Cache-Control": "no-store",
    "Content-Security-Policy": localOnlyCsp,
  });
  res.end(hydrated);
}

async function serveStitchIndex(res) {
  const stitchRoot = join(root, activeStitchDirName);
  const entries = await readdir(stitchRoot, { withFileTypes: true });
  const screens = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (retiredStitchScreens.has(entry.name)) continue;
    const codePath = join(stitchRoot, entry.name, "code.html");
    try {
      const fileStat = await stat(codePath);
      screens.push({
        name: entry.name,
        size: fileStat.size,
        mtime: fileStat.mtime,
      });
    } catch {
      // Some folders may be notes/assets rather than runnable screens.
    }
  }

  screens.sort((left, right) => left.name.localeCompare(right.name));

  const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Golden Quill Stitch Screens</title>
  <style>
    :root { color-scheme: dark; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #07111f; color: #eef4ff; }
    body { margin: 0; padding: 24px; }
    header { max-width: 1120px; margin: 0 auto 24px; border: 1px solid #344256; padding: 20px; background: #0d1828; }
    h1 { margin: 0 0 8px; font: 700 24px system-ui, sans-serif; }
    p { color: #bcc7d8; margin: 0; }
    .actions { margin-top: 18px; display: flex; gap: 10px; flex-wrap: wrap; }
    a { color: inherit; text-decoration: none; }
    .button, .screen { border: 1px solid #344256; background: #101d2f; }
    .button { padding: 10px 12px; display: inline-block; }
    main { max-width: 1120px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px; }
    .screen { padding: 12px; min-height: 84px; }
    .screen strong { display: block; font: 650 14px system-ui, sans-serif; margin-bottom: 8px; }
    .screen span { color: #95a3b8; font-size: 11px; display: block; }
  </style>
</head>
<body>
  <header>
    <h1>Golden Quill / Tilth Stitch Shell</h1>
    <p>Newest generated screen set in <code>apps/tilth_ui/${htmlEsc(activeStitchDirName)}</code>.</p>
    <div class="actions">
      <a class="button" href="${latestStitchEntry}">Scout Mission Control</a>
      <a class="button" href="${stitchPath(stitchNavRoutes.home)}">App Shell (current)</a>
      <a class="button" href="/">Integrated Prototype (legacy)</a>
    </div>
  </header>
  <main>
    ${screens.map((screen) => `
      <a class="screen" href="${stitchPath(screen.name)}">
        <strong>${htmlEsc(screenLabel(screen.name))}</strong>
        <span>${htmlEsc(screen.mtime.toLocaleString())}</span>
        <span>${Math.round(screen.size / 1024)} KB</span>
      </a>`).join("")}
  </main>
</body>
</html>`;

  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "Content-Length": Buffer.byteLength(html),
    "Cache-Control": "no-store",
    "Content-Security-Policy": localOnlyCsp,
  });
  res.end(html);
}

createServer(async (req, res) => {
  const urlPath = (req.url || "/").split("?")[0];
  const method = req.method || "GET";

  if (method === "GET" && urlPath === "/api/projections/current") {
    try {
      const projection = await buildLocalProjection();
      writeJson(res, 200, projection.ui);
    } catch (err) {
      writeJson(res, 500, {
        status: "rejected",
        reason: "Projection build failed.",
        detail: String(err?.message || err),
      });
    }
    return;
  }

  if (method === "POST" && urlPath === "/api/commands") {
    try {
      const command = await readJsonBody(req);
      const result = await handleCommand(command);
      writeJson(res, result.status === "rejected" ? 400 : 202, {
        status: result.status,
        command_type: result.command_type,
        command_result: result.command_result,
        reason: result.reason,
        events: result.events,
        projection: result.projection,
      });
    } catch (err) {
      writeJson(res, 400, {
        status: "rejected",
        reason: "Command body could not be parsed or handled.",
        detail: String(err?.message || err),
      });
    }
    return;
  }

  if (method === "GET" && urlPath === "/api/openclaw/status") {
    const result = await handleOpenClawRequest({ action: "status" });
    writeJson(res, result.ok === false ? 502 : 200, result);
    return;
  }

  if (method === "POST" && urlPath === "/api/openclaw/run") {
    try {
      const request = await readJsonBody(req);
      const result = await handleOpenClawRequest(request);
      writeJson(res, result.ok === false ? 502 : 200, result);
    } catch (err) {
      writeJson(res, 400, {
        ok: false,
        reason: "OpenClaw request body could not be parsed or handled.",
        detail: String(err?.message || err),
      });
    }
    return;
  }

  if (method === "GET" && urlPath === "/api/routes") {
    writeJson(res, 200, Object.keys(stitchNavRoutes).map(k => `/${k}`));
    return;
  }

  const retiredCardEntry = stitchPath("card_matrix_institutional_identity_topology");
  if (urlPath === "/" || urlPath === "/home") {
    try {
      await serveHydratedStitchScreen(res, join(root, activeStitchDirName, stitchNavRoutes.home, "code.html"));
      return;
    } catch (e) {
      // Fallback below
      console.error("Error serving home screen", e);
    }
  }
  if (urlPath === "/cards" || urlPath === retiredCardEntry || urlPath === "/newest") {
    res.writeHead(302, { Location: latestStitchEntry, "Cache-Control": "no-store" });
    res.end();
    return;
  }
  if (urlPath === "/stitch") {
    await serveStitchIndex(res);
    return;
  }

  if (urlPath.startsWith(stitchScreenPrefix) && urlPath.endsWith("/code.html")) {
    const target = safePath(req.url || "/");
    try {
      await serveHydratedStitchScreen(res, target);
      return;
    } catch {
      // Fall back
    }
  }

  const routeKey = decodeURIComponent(urlPath.split("/")[1]);
  if (routeKey && stitchNavRoutes[routeKey]) {
    try {
      await serveHydratedStitchScreen(res, join(root, activeStitchDirName, stitchNavRoutes[routeKey], "code.html"));
      return;
    } catch (e) {
      // Fall back
      console.error("Error serving stitched screen", e);
    }
  }

  const target = safePath(req.url || "/");
  try {
    await serveFile(res, target);
    return;
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("404 Not Found - Legacy UI has been removed.");
  }
}).listen(port, "127.0.0.1", () => {
  console.log(`Golden Quill Tilth UI running at http://127.0.0.1:${port}`);
});
