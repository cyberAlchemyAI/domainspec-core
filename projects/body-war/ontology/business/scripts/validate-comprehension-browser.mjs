import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { createReadStream } from "node:fs";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { fileURLToPath } from "node:url";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const receiptRoot = path.join(packageRoot, "receipts");
const receiptPath = path.join(
  receiptRoot,
  "comprehension-browser-receipt.json",
);
const taskScreenshotPath = path.join(
  receiptRoot,
  "comprehension-browser-task.png",
);
const journeyScreenshotPath = path.join(
  receiptRoot,
  "comprehension-browser-journey.png",
);

const artifactPaths = {
  task: "BUSINESS-COMPREHENSION-TASK.html",
  stimulus: "BUSINESS-JOURNEY-EXPERIMENT.html",
  task_catalog: "authoring/comprehension-task-catalog.mjs",
  task_generator: "scripts/generate-comprehension-task.mjs",
  stimulus_catalog: "authoring/view-catalog.mjs",
  stimulus_generator: "scripts/generate-views.mjs",
  profile: "profile.json",
  residue: "residue.json",
  relations: "relations/relations.json",
  node_manifest: "nodes/manifest.json",
};

async function sha256File(absolutePath) {
  const digest = createHash("sha256");
  for await (const chunk of createReadStream(absolutePath)) {
    digest.update(chunk);
  }
  return digest.digest("hex");
}

function canonicalize(value) {
  if (Array.isArray(value)) {
    return value.map(canonicalize);
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((key) => [key, canonicalize(value[key])]),
    );
  }
  return value;
}

function canonicalDigest(value) {
  return createHash("sha256")
    .update(JSON.stringify(canonicalize(value)))
    .digest("hex");
}

function contentType(absolutePath) {
  if (absolutePath.endsWith(".html")) return "text/html; charset=utf-8";
  if (absolutePath.endsWith(".png")) return "image/png";
  return "application/octet-stream";
}

async function startServer(requestLog) {
  const allowed = new Set([
    "/BUSINESS-COMPREHENSION-TASK.html",
    "/BUSINESS-JOURNEY-EXPERIMENT.html",
  ]);
  const server = http.createServer(async (request, response) => {
    const requestUrl = new URL(request.url, "http://127.0.0.1");
    requestLog.push(requestUrl.pathname);
    if (!allowed.has(requestUrl.pathname)) {
      response.writeHead(404, { "content-type": "text/plain" });
      response.end("not found");
      return;
    }
    const absolutePath = path.join(
      packageRoot,
      requestUrl.pathname.slice(1),
    );
    const content = await readFile(absolutePath);
    response.writeHead(200, {
      "cache-control": "no-store",
      "content-type": contentType(absolutePath),
    });
    response.end(content);
  });
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address();
  return {
    origin: `http://127.0.0.1:${address.port}`,
    close: () =>
      new Promise((resolve, reject) =>
        server.close((error) => (error ? reject(error) : resolve())),
      ),
  };
}

const assertions = [];
function check(id, condition, detail) {
  const status = condition ? "pass" : "fail";
  assertions.push({ id, status, detail });
  if (!condition) throw new Error(`${id}: ${detail}`);
}

async function artifactEvidence() {
  return Object.fromEntries(
    await Promise.all(
      Object.entries(artifactPaths).map(async ([id, relativePath]) => {
        const absolutePath = path.join(packageRoot, relativePath);
        const metadata = await stat(absolutePath);
        return [
          id,
          {
            path: `projects/body-war/ontology/business/${relativePath}`,
            sha256: await sha256File(absolutePath),
            size_bytes: metadata.size,
          },
        ];
      }),
    ),
  );
}

const startedAt = new Date().toISOString();
await mkdir(receiptRoot, { recursive: true });
const artifacts = await artifactEvidence();
const taskModule = await import(
  pathToFileURL(
    path.join(packageRoot, "authoring/comprehension-task-catalog.mjs"),
  ).href
);
const task = taskModule.comprehensionTask;
const protocol = JSON.parse(
  await readFile(
    path.join(packageRoot, "review/comprehension-protocol.json"),
    "utf8",
  ),
);
const taskHtml = await readFile(
  path.join(packageRoot, artifactPaths.task),
  "utf8",
);

const globalNodeModules = execFileSync("npm", ["root", "-g"], {
  encoding: "utf8",
}).trim();
const playwrightRoot =
  process.env.PLAYWRIGHT_MODULE_PATH ??
  path.join(globalNodeModules, "playwright");
const playwrightPackage = JSON.parse(
  await readFile(path.join(playwrightRoot, "package.json"), "utf8"),
);
const { chromium } = await import(
  pathToFileURL(path.join(playwrightRoot, "index.mjs")).href
);
const executablePath = chromium.executablePath();
const revisionMatch = executablePath.match(/chromium-(\d+)/);
const requestLog = [];
const server = await startServer(requestLog);
let browser;
let terminalStatus = "fail";
let failure = null;
let browserVersion = null;

try {
  check("task-loci-count", task.loci.length === 6, "six learner loci");
  check(
    "matched-arm-fields",
    JSON.stringify(protocol.matched_arms.fields) ===
      JSON.stringify(["task", "loci", "prompt", "stimulus"]),
    "task, loci, prompt, and stimulus are the matched-arm identity fields",
  );
  for (const marker of protocol.learner_deny_markers) {
    check(
      `negative-leakage:${marker}`,
      !taskHtml.includes(marker),
      `${marker} is absent from learner bytes`,
    );
  }

  browser = await chromium.launch({ headless: true });
  browserVersion = browser.version();

  const taskContext = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: true,
  });
  const taskPage = await taskContext.newPage();
  await taskPage.goto(
    `${server.origin}/BUSINESS-COMPREHENSION-TASK.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "task-stimulus-only",
    (await taskPage.locator('[data-locus]').count()) === 6,
    "all six task loci load without reviewer resources",
  );
  check(
    "task-stimulus-link",
    (await taskPage
      .locator('.stimulus a')
      .getAttribute("href")) === "BUSINESS-JOURNEY-EXPERIMENT.html",
    "task points to the exact journey stimulus",
  );
  await taskPage.screenshot({
    path: taskScreenshotPath,
    fullPage: true,
  });
  await taskContext.close();

  const journeyContext = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: true,
  });
  const journeyPage = await journeyContext.newPage();
  await journeyPage.goto(
    `${server.origin}/BUSINESS-JOURNEY-EXPERIMENT.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "js-progressive-tabs",
    (await journeyPage.locator('[role="tab"]').count()) === 2 &&
      (await journeyPage.locator('[role="tabpanel"]').count()) === 2,
    "ordinary links are enhanced into two tabs and panels",
  );
  check(
    "js-single-visible-story",
    (await journeyPage.locator('.story-panel:visible').count()) === 1,
    "one story is visible after enhancement",
  );
  const firstTab = journeyPage.locator('[role="tab"]').first();
  await firstTab.focus();
  await firstTab.press("ArrowRight");
  check(
    "keyboard-tab-navigation",
    (await journeyPage
      .locator('[role="tab"]')
      .nth(1)
      .getAttribute("aria-selected")) === "true" &&
      (await journeyPage
        .locator('#story-activity-to-territory-preview')
        .isVisible()),
    "ArrowRight selects and reveals the second story",
  );
  await journeyPage.locator("#ontology-detail-toggle").check();
  check(
    "detail-toggle",
    await journeyPage
      .locator('details.ontology-details')
      .first()
      .evaluate((element) => element.open),
    "ontology details can be expanded",
  );
  for (const text of [
    "Blocked — owner decision required",
    "Explicitly does not promote",
    "Projection only",
    "Relation owner",
    "Blocking owner",
    "Next gate",
    "status: candidate-local",
    "authority_effect: none",
    "release_admission: not-granted",
  ]) {
    check(
      `visible-authority:${text}`,
      (await journeyPage.getByText(text, { exact: true }).count()) > 0,
      `${text} exists in the rendered stimulus`,
    );
  }
  await journeyPage.screenshot({
    path: journeyScreenshotPath,
    fullPage: true,
  });
  await journeyContext.close();

  const noJsContext = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: false,
  });
  const noJsPage = await noJsContext.newPage();
  await noJsPage.goto(
    `${server.origin}/BUSINESS-JOURNEY-EXPERIMENT.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "native-no-js-stories",
    (await noJsPage.locator('.story-panel:visible').count()) === 2,
    "both complete stories are visible without JavaScript",
  );
  check(
    "native-no-js-links",
    (await noJsPage.locator('a.story-tab').count()) === 2,
    "ordinary story links exist without JavaScript",
  );
  await noJsContext.close();

  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    javaScriptEnabled: true,
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(
    `${server.origin}/BUSINESS-JOURNEY-EXPERIMENT.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "responsive-relation-layout",
    (await mobilePage
      .locator(".relation-reading")
      .first()
      .evaluate(
        (element) =>
          getComputedStyle(element).gridTemplateColumns.split(" ").length ===
          1,
      )),
    "relation sentence collapses to one column at 390 CSS pixels",
  );
  await mobileContext.close();

  const reducedContext = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
  });
  const reducedPage = await reducedContext.newPage();
  await reducedPage.goto(
    `${server.origin}/BUSINESS-JOURNEY-EXPERIMENT.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "reduced-motion",
    (await reducedPage
      .locator("html")
      .evaluate((element) => getComputedStyle(element).scrollBehavior)) ===
      "auto",
    "reduced-motion disables smooth scrolling",
  );
  await reducedPage.emulateMedia({ media: "print", reducedMotion: "reduce" });
  check(
    "print-all-stories",
    await reducedPage
      .locator(".story-panel")
      .evaluateAll((elements) =>
        elements.every(
          (element) => getComputedStyle(element).display !== "none",
        ),
      ),
    "print mode exposes both stories",
  );
  check(
    "print-controls-hidden",
    (await reducedPage
      .locator(".control-deck")
      .evaluate((element) => getComputedStyle(element).display)) === "none",
    "print mode hides interaction controls",
  );
  await reducedContext.close();

  check(
    "runtime-isolation",
    requestLog.every((requestPath) =>
      [
        "/BUSINESS-COMPREHENSION-TASK.html",
        "/BUSINESS-JOURNEY-EXPERIMENT.html",
      ].includes(requestPath),
    ),
    "loopback server served only the exact task and stimulus",
  );
  terminalStatus = "pass";
} catch (error) {
  failure = {
    name: error.name,
    message: error.message,
    stack: error.stack,
  };
} finally {
  if (browser) await browser.close();
  await server.close();
}

const screenshotArtifacts = {};
for (const [id, absolutePath] of [
  ["task", taskScreenshotPath],
  ["journey", journeyScreenshotPath],
]) {
  try {
    const metadata = await stat(absolutePath);
    screenshotArtifacts[id] = {
      path: path.relative(packageRoot, absolutePath),
      sha256: await sha256File(absolutePath),
      size_bytes: metadata.size,
    };
  } catch {
    screenshotArtifacts[id] = null;
  }
}

const receipt = {
  schema_version: "body-war-comprehension-browser-receipt/v1",
  status: terminalStatus,
  started_at: startedAt,
  completed_at: new Date().toISOString(),
  artifacts,
  instrument_identity: {
    task_id: task.task_id,
    task_digest: canonicalDigest(task),
    loci_digest: canonicalDigest(task.loci),
    prompt_digest: canonicalDigest(task.prompt),
    stimulus_contract_digest: canonicalDigest(task.stimulus),
    matched_arm_identity: "byte-identical",
  },
  runtime: {
    node: process.version,
    playwright_version: playwrightPackage.version,
    playwright_module_path: playwrightRoot,
    browser_name: "chromium",
    browser_version: browserVersion,
    browser_revision: revisionMatch?.[1] ?? null,
    executable_path: executablePath,
    executable_sha256: await sha256File(executablePath),
    viewport_modes: [
      { width: 1280, height: 900, device_pixel_ratio: 1 },
      { width: 390, height: 844, device_pixel_ratio: 2 }
    ],
    modes: [
      "javascript",
      "no-javascript",
      "reduced-motion",
      "print"
    ],
    isolation:
      "fresh incognito browser context per mode; loopback random-port server; only exact task and stimulus paths admitted",
  },
  request_paths: [...new Set(requestLog)].sort(),
  assertions,
  screenshots: screenshotArtifacts,
  failure,
  agent_pretest_state: "not-run",
  human_witness_state: "not-authorized",
  claim_ceiling:
    "Pinned browser structure and interaction evidence only; no human comprehension, score correctness, ontology authority, promotion, release, or production evidence.",
};

await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
process.stdout.write(
  `comprehension browser validation ${terminalStatus}: ${assertions.filter((assertion) => assertion.status === "pass").length}/${assertions.length} assertions passed\n`,
);
if (terminalStatus !== "pass") process.exitCode = 1;

