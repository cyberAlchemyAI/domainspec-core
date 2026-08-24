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
const receiptPath = path.join(receiptRoot, "view-atlas-browser-receipt.json");
const overviewScreenshotPath = path.join(
  receiptRoot,
  "view-atlas-overview.png",
);
const portalScreenshotPath = path.join(
  receiptRoot,
  "view-atlas-portal.png",
);
const atlasPath = path.join(packageRoot, "BUSINESS-VIEW-ATLAS.html");

const artifactPaths = {
  atlas: "BUSINESS-VIEW-ATLAS.html",
  atlas_catalog: "authoring/view-atlas-catalog.mjs",
  projection: "scripts/view-atlas-projection.mjs",
  renderer: "scripts/render-view-atlas.mjs",
  generator: "scripts/generate-views.mjs",
  coverage_receipt: "receipts/view-atlas-coverage-receipt.json",
  profile: "profile.json",
  relations: "relations/relations.json",
  business_view: "views/business.json",
};

async function sha256File(absolutePath) {
  const digest = createHash("sha256");
  for await (const chunk of createReadStream(absolutePath)) {
    digest.update(chunk);
  }
  return digest.digest("hex");
}

function contentType(absolutePath) {
  return absolutePath.endsWith(".html")
    ? "text/html; charset=utf-8"
    : "application/octet-stream";
}

async function startServer(requestLog) {
  const server = http.createServer(async (request, response) => {
    const requestUrl = new URL(request.url, "http://127.0.0.1");
    requestLog.push(requestUrl.pathname);
    if (requestUrl.pathname !== "/BUSINESS-VIEW-ATLAS.html") {
      response.writeHead(404, { "content-type": "text/plain" });
      response.end("not found");
      return;
    }
    const content = await readFile(atlasPath);
    response.writeHead(200, {
      "cache-control": "no-store",
      "content-type": contentType(atlasPath),
      "x-content-type-options": "nosniff",
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

const assertions = [];
function check(id, condition, detail) {
  assertions.push({ id, status: condition ? "pass" : "fail", detail });
  if (!condition) throw new Error(`${id}: ${detail}`);
}

const startedAt = new Date().toISOString();
await mkdir(receiptRoot, { recursive: true });
const artifacts = await artifactEvidence();
const coverageReceipt = JSON.parse(
  await readFile(
    path.join(packageRoot, "receipts/view-atlas-coverage-receipt.json"),
    "utf8",
  ),
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
let browser = null;
let browserVersion = null;
let terminalStatus = "fail";
let failure = null;
const consoleErrors = [];
const pageErrors = [];

function watchPage(page) {
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));
}

try {
  check(
    "coverage-precondition",
    coverageReceipt.status === "pass" &&
      coverageReceipt.coverage.node_count === 237 &&
      coverageReceipt.coverage.relation_count === 231,
    "the exact deterministic coverage receipt passes before browser execution",
  );
  browser = await chromium.launch({ headless: true });
  browserVersion = browser.version();

  const desktopContext = await browser.newContext({
    viewport: { width: 1365, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: true,
  });
  const desktopPage = await desktopContext.newPage();
  watchPage(desktopPage);
  await desktopPage.goto(
    `${server.origin}/BUSINESS-VIEW-ATLAS.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "desktop-exact-structure",
    (await desktopPage.locator("[data-lens-id]").count()) === 6 &&
      (await desktopPage.locator("[data-concept-id]").count()) === 237 &&
      (await desktopPage.locator("[data-relation-id]").count()) === 231,
    "desktop DOM contains six lenses, 237 nodes, and 231 relations",
  );
  check(
    "desktop-overview-default",
    (await desktopPage.locator("#atlas-overview").isVisible()) &&
      (await desktopPage.locator(".atlas-lens:visible").count()) === 0,
    "enhanced default shows the six-lens overview without a selected lens",
  );
  await desktopPage.screenshot({
    path: overviewScreenshotPath,
    fullPage: true,
  });

  await desktopPage
    .locator('a[href="#lens-participants-boundaries"]')
    .first()
    .click();
  check(
    "lens-activation",
    (await desktopPage.locator(".atlas-lens:visible").count()) === 1 &&
      (await desktopPage.locator("#lens-participants-boundaries").isVisible()),
    "ordinary lens anchor activates exactly one editorial lens",
  );

  await desktopPage.locator('a[href="#atlas-overview"]').first().click();
  check(
    "overview-recovery",
    (await desktopPage.locator("#atlas-overview").isVisible()) &&
      (await desktopPage.locator(".atlas-lens:visible").count()) === 0,
    "ordinary overview anchor restores the search and six-lens overview",
  );
  await desktopPage.locator("#atlas-search").fill("Runner");
  const runnerResult = desktopPage.locator(
    '#atlas-search-results a[href="#node-body-war.business.actor.runner"]',
  );
  check(
    "search-exact-runner",
    (await runnerResult.count()) === 1,
    "search returns the one canonical Runner target",
  );
  await runnerResult.click();
  check(
    "search-focus-transfer",
    (await desktopPage.evaluate(() => document.activeElement?.id)) ===
      "node-body-war.business.actor.runner",
    "search navigation focuses the canonical Runner node",
  );

  const portal = desktopPage.locator(
    "#relation-body-war\\.relation\\.provider-belongs-runner",
  );
  check(
    "portal-original-direction",
    (await portal.getByText("Original direction", { exact: false }).count()) >
      0 &&
      (await portal.textContent()).includes("participants-boundaries") &&
      (await portal.textContent()).includes("business-objects"),
    "the portal exposes its original source-lens to target-lens direction",
  );
  await portal
    .getByRole("link", { name: "Open target endpoint", exact: true })
    .click();
  check(
    "portal-target-lens",
    await desktopPage.locator("#lens-business-objects").isVisible(),
    "portal activation reveals the other endpoint's core lens",
  );
  check(
    "portal-target-focus",
    (await desktopPage.evaluate(() => document.activeElement?.id)) ===
      "node-body-war.business.entity.provider-account",
    "portal activation focuses the exact target endpoint",
  );
  check(
    "portal-visible-target-geometry",
    (await desktopPage
      .locator("#node-body-war\\.business\\.entity\\.provider-account")
      .evaluate((element) => getComputedStyle(element).boxShadow)) !== "none",
    "the fragment target has visible non-color selection geometry",
  );
  await desktopPage.screenshot({
    path: portalScreenshotPath,
    fullPage: true,
  });
  await desktopPage.goBack({ waitUntil: "networkidle" });
  check(
    "history-recovery",
    (await desktopPage.evaluate(() => document.activeElement?.id)) ===
      "node-body-war.business.actor.runner",
    "Back restores and focuses the prior canonical node location",
  );

  const fragmentIntegrity = await desktopPage.evaluate(() => {
    const ids = new Map();
    for (const element of document.querySelectorAll("[id]")) {
      ids.set(element.id, (ids.get(element.id) ?? 0) + 1);
    }
    const fragments = [...document.querySelectorAll('a[href^="#"]')].map(
      (anchor) => anchor.getAttribute("href").slice(1),
    );
    return {
      duplicateIds: [...ids.entries()].filter(([, count]) => count !== 1),
      missingFragments: fragments.filter((fragment) => ids.get(fragment) !== 1),
    };
  });
  check(
    "fragment-integrity",
    fragmentIntegrity.duplicateIds.length === 0 &&
      fragmentIntegrity.missingFragments.length === 0,
    "all ordinary fragment links resolve to exactly one target",
  );
  await desktopContext.close();

  const noJsContext = await browser.newContext({
    viewport: { width: 1365, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: false,
  });
  const noJsPage = await noJsContext.newPage();
  watchPage(noJsPage);
  await noJsPage.goto(
    `${server.origin}/BUSINESS-VIEW-ATLAS.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "native-no-js-complete",
    (await noJsPage.locator(".atlas-lens:visible").count()) === 6 &&
      (await noJsPage.locator("[data-concept-id]:visible").count()) === 237 &&
      (await noJsPage.locator("[data-relation-id]:visible").count()) === 231,
    "all lenses, nodes, and relations remain visible without JavaScript",
  );
  check(
    "native-no-js-links",
    (await noJsPage.locator('a[href^="#node-"]').count()) > 400,
    "ordinary endpoint links remain available without JavaScript",
  );
  await noJsContext.close();

  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    javaScriptEnabled: true,
  });
  const mobilePage = await mobileContext.newPage();
  watchPage(mobilePage);
  await mobilePage.goto(
    `${server.origin}/BUSINESS-VIEW-ATLAS.html`,
    { waitUntil: "networkidle" },
  );
  const mobileWidths = await mobilePage.evaluate(() => ({
    scroll: document.documentElement.scrollWidth,
    client: document.documentElement.clientWidth,
  }));
  check(
    "mobile-no-horizontal-document-overflow",
    mobileWidths.scroll <= mobileWidths.client,
    `390px viewport has ${mobileWidths.scroll}px scroll width and ${mobileWidths.client}px client width`,
  );
  await mobileContext.close();

  const reducedContext = await browser.newContext({
    viewport: { width: 1365, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: true,
    reducedMotion: "reduce",
  });
  const reducedPage = await reducedContext.newPage();
  watchPage(reducedPage);
  await reducedPage.goto(
    `${server.origin}/BUSINESS-VIEW-ATLAS.html`,
    { waitUntil: "networkidle" },
  );
  check(
    "reduced-motion",
    (await reducedPage
      .locator("html")
      .evaluate((element) => getComputedStyle(element).scrollBehavior)) ===
      "auto",
    "reduced motion disables smooth scrolling",
  );
  await reducedPage.emulateMedia({ media: "print", reducedMotion: "reduce" });
  check(
    "print-all-lenses",
    await reducedPage
      .locator(".atlas-lens")
      .evaluateAll((elements) =>
        elements.every(
          (element) => getComputedStyle(element).display !== "none",
        ),
      ),
    "print mode exposes all six lenses",
  );
  check(
    "print-search-hidden",
    (await reducedPage
      .locator(".search")
      .evaluate((element) => getComputedStyle(element).display)) === "none",
    "print mode hides the interactive search control",
  );
  await reducedContext.close();

  check(
    "browser-errors",
    consoleErrors.length === 0 && pageErrors.length === 0,
    `zero console errors and page errors (${consoleErrors.length}/${pageErrors.length})`,
  );
  check(
    "runtime-isolation",
    requestLog.every(
      (requestPath) => requestPath === "/BUSINESS-VIEW-ATLAS.html",
    ),
    "loopback server served only the exact atlas path",
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

const screenshots = {};
for (const [id, absolutePath] of [
  ["overview", overviewScreenshotPath],
  ["portal", portalScreenshotPath],
]) {
  try {
    const metadata = await stat(absolutePath);
    screenshots[id] = {
      path: path.relative(packageRoot, absolutePath),
      sha256: await sha256File(absolutePath),
      size_bytes: metadata.size,
    };
  } catch {
    screenshots[id] = null;
  }
}

const receipt = {
  schema_version: "body-war-view-atlas-browser-receipt/v1",
  status: terminalStatus,
  started_at: startedAt,
  completed_at: new Date().toISOString(),
  artifacts,
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
      { width: 1365, height: 900, device_pixel_ratio: 1 },
      { width: 390, height: 844, device_pixel_ratio: 2 }
    ],
    modes: ["javascript", "no-javascript", "reduced-motion", "print"],
    isolation:
      "fresh incognito context per mode; loopback random-port server; exact atlas path only; server and browser closed at completion",
  },
  request_paths: [...new Set(requestLog)].sort(),
  assertions,
  console_errors: consoleErrors,
  page_errors: pageErrors,
  screenshots,
  failure,
  human_comprehension_state: "not-run",
  accessibility_conformance_state: "not-claimed",
  authority_effect: "none",
  release_admission: "not-granted",
  claim_ceiling:
    "Pinned browser structure and interaction evidence only; no human comprehension, accessibility conformance, ontology promotion, release, deployment, or production evidence.",
};

await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`);
process.stdout.write(
  `view atlas browser validation ${terminalStatus}: ${assertions.filter((assertion) => assertion.status === "pass").length}/${assertions.length} assertions passed\n`,
);
if (terminalStatus !== "pass") process.exitCode = 1;
