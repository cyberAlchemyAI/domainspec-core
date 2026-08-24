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
const prototypeFastLane = process.argv.slice(2).includes("--prototype-fast-lane");
const unknownArguments = process.argv
  .slice(2)
  .filter((argument) => argument !== "--prototype-fast-lane");
if (unknownArguments.length > 0) {
  throw new Error(
    `unsupported browser validator arguments: ${unknownArguments.join(", ")}`,
  );
}
const receiptRoot = path.join(packageRoot, "receipts");
const receiptPath = path.join(receiptRoot, "view-atlas-browser-receipt.json");
const overviewScreenshotPath = path.join(
  receiptRoot,
  "view-atlas-arrow-overview.png",
);
const mobileRelationScreenshotPath = path.join(
  receiptRoot,
  "view-atlas-arrow-relation-mobile.png",
);
const atlasPath = path.join(packageRoot, "BUSINESS-VIEW-ATLAS.html");
const swu003RevalidationReceiptPath = path.resolve(
  packageRoot,
  "..",
  "..",
  "development",
  "invoke-runs",
  "20260730T062453Z-business-ontology-atlas-arrows",
  "work-pack",
  "closeout",
  "SWU-BWAA-003.revalidation-001.receipt.json",
);

const artifactPaths = {
  atlas: "BUSINESS-VIEW-ATLAS.html",
  atlas_catalog: "authoring/view-atlas-catalog.mjs",
  projection: "scripts/view-atlas-projection.mjs",
  renderer: "scripts/render-view-atlas.mjs",
  browser_validator: "scripts/validate-view-atlas-browser.mjs",
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
const swu003RevalidationReceipt = JSON.parse(
  await readFile(swu003RevalidationReceiptPath, "utf8"),
);
const generatedViewCheck = prototypeFastLane
  ? execFileSync(
      process.execPath,
      [path.join(packageRoot, "scripts/generate-views.mjs"), "--check"],
      { encoding: "utf8", cwd: path.resolve(packageRoot, "../../../..") },
    ).trim()
  : null;
const globalNodeModules = execFileSync("npm", ["root", "-g"], {
  encoding: "utf8",
}).trim();
const playwrightCliPath = execFileSync("which", ["playwright"], {
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
const browserRequests = [];
const failedRequests = [];
const server = await startServer(requestLog);
let browser = null;
let browserVersion = null;
let terminalStatus = "fail";
let failure = null;
const consoleErrors = [];
const pageErrors = [];
let externalRequestUrls = [];
let browserClosed = false;
let serverClosed = false;

function watchPage(page) {
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));
  page.on("request", (request) => browserRequests.push(request.url()));
  page.on("requestfailed", (request) =>
    failedRequests.push({
      url: request.url(),
      error: request.failure()?.errorText ?? "unknown",
    }),
  );
}

try {
  check(
    "coverage-precondition",
    coverageReceipt.status === "pass" &&
      coverageReceipt.coverage.node_count === 237 &&
      coverageReceipt.coverage.relation_count === 231,
    "the exact deterministic coverage receipt passes before browser execution",
  );
  const swu003Atlas = swu003RevalidationReceipt.target_inventory.find(
    (target) =>
      target.path ===
      "projects/body-war/ontology/business/BUSINESS-VIEW-ATLAS.html",
  );
  const governedAtlasBinding =
    swu003RevalidationReceipt.result === "pass" &&
    swu003Atlas?.final_sha256 === artifacts.atlas.sha256;
  check(
    "swu-003-artifact-binding",
    governedAtlasBinding ||
      (prototypeFastLane &&
        generatedViewCheck.includes("business views current:")),
    governedAtlasBinding
      ? "the browser run is bound to the repaired atlas bytes accepted by the SWU-BWAA-003 revalidation receipt"
      : "prototype fast lane binds the browser run to live byte-current generated atlas output while SWU-BWAA-003 lifecycle synchronization is deferred",
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
  const behaviorObjectLane = desktopPage.locator(
    '.semantic-lane[data-flow-source="behavior"][data-flow-target="business-objects"]',
  );
  check(
    "desktop-directed-overview",
    (await desktopPage.locator(".overview-lens-node").count()) === 6 &&
      (await desktopPage.locator(".semantic-lane").count()) === 13 &&
      (await desktopPage
        .locator(".overview-spatial path[data-flow-source]")
        .count()) === 13 &&
      (await behaviorObjectLane.count()) === 1 &&
      (await behaviorObjectLane.textContent()).includes("55 relations"),
    "desktop exposes six linked overview nodes, 13 matching geometry/semantic lanes, and the exact 55-count behavior to business-objects lane",
  );
  await desktopPage.screenshot({
    path: overviewScreenshotPath,
    fullPage: true,
  });

  const predicateBrief = desktopPage
    .locator(".reference-brief--predicate")
    .first();
  await predicateBrief.locator("summary").click();
  check(
    "predicate-brief-click",
    (await predicateBrief.getAttribute("open")) !== null &&
      (await predicateBrief.textContent()).includes("Projection wording") &&
      (await predicateBrief.textContent()).includes(
        "not a canonical predicate definition",
      ),
    "click exposes bounded predicate wording without promoting it to a canonical definition",
  );

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
  await desktopPage.waitForFunction(
    () =>
      document.activeElement?.id === "node-body-war.business.actor.runner",
  );
  check(
    "search-focus-transfer",
    (await desktopPage.evaluate(() => document.activeElement?.id)) ===
      "node-body-war.business.actor.runner",
    "search navigation focuses the canonical Runner node",
  );
  const runnerNode = desktopPage.locator(
    "#node-body-war\\.business\\.actor\\.runner",
  );
  const runnerBrief = runnerNode.locator(".reference-brief--node");
  await runnerBrief.hover();
  const runnerHoverState = await runnerBrief.evaluate((brief) => {
    const content = brief.querySelector(".reference-brief__content");
    const style = getComputedStyle(content);
    return {
      hovered: brief.matches(":hover"),
      open: brief.open,
      display: style.display,
      contentVisibility: style.contentVisibility,
      width: content.getBoundingClientRect().width,
      height: content.getBoundingClientRect().height,
    };
  });
  check(
    "node-brief-hover",
    await runnerBrief.locator(".reference-brief__content").isVisible(),
    `hover exposes the representative node brief: ${JSON.stringify(runnerHoverState)}`,
  );
  await runnerBrief.locator("summary").focus();
  check(
    "node-brief-focus",
    await runnerBrief.locator(".reference-brief__content").isVisible(),
    "keyboard focus exposes the representative node brief",
  );
  await desktopPage.keyboard.press("Enter");
  check(
    "node-brief-keyboard-persistent",
    (await runnerBrief.getAttribute("open")) !== null &&
      (await runnerBrief.textContent()).includes("Concept ID") &&
      (await runnerBrief.textContent()).includes("Outgoing incidence") &&
      (await runnerBrief.textContent()).includes("Source references"),
    "Enter persistently opens exact source-backed node metadata and incidence",
  );

  const portal = desktopPage.locator(
    "#relation-body-war\\.relation\\.provider-belongs-runner",
  );
  const portalArrow = portal.locator(".relation-arrow");
  const arrowOrder = await portalArrow.evaluate((arrow) =>
    [...arrow.children].map((child) => ({
      className: child.className,
      text: child.textContent.trim(),
    })),
  );
  check(
    "exact-relation-arrow-order",
    arrowOrder.length === 3 &&
      arrowOrder[0].className.includes("relation-arrow__source") &&
      arrowOrder[1].className.includes("relation-arrow__predicate") &&
      arrowOrder[2].className.includes("relation-arrow__target") &&
      arrowOrder.every((part) => part.text.length > 0),
    "the representative relation presents non-empty source, predicate, and target in semantic DOM order",
  );
  await portalArrow.locator(".relation-arrow__source").focus();
  check(
    "exact-relation-arrow-focus",
    await portalArrow
      .locator(".relation-arrow__source")
      .evaluate((element) => element === document.activeElement),
    "the exact source endpoint is independently keyboard-focusable",
  );
  const relationBrief = portal.locator(".reference-brief--relation");
  await relationBrief.locator("summary").click();
  check(
    "relation-brief-click",
    (await relationBrief.getAttribute("open")) !== null &&
      (await relationBrief.textContent()).includes("Exact tuple") &&
      (await relationBrief.textContent()).includes("Authority effect") &&
      (await relationBrief.textContent()).includes("Forbidden collapse"),
    "click exposes the exact relation tuple and policy metadata",
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
  await desktopPage.waitForFunction(
    () =>
      document.activeElement?.id ===
      "node-body-war.business.entity.provider-account",
  );
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
  const businessObjectsLensBrief = desktopPage
    .locator("#lens-business-objects .reference-brief--lens")
    .first();
  await businessObjectsLensBrief.locator("summary").click();
  check(
    "lens-brief-click",
    (await businessObjectsLensBrief.getAttribute("open")) !== null &&
      (await businessObjectsLensBrief.textContent()).includes("Question:") &&
      (await businessObjectsLensBrief.textContent()).includes(
        "Directed flows",
      ),
    "click exposes the lens question, counts, and directed flows",
  );
  await desktopPage.goBack({ waitUntil: "networkidle" });
  await desktopPage.waitForFunction(
    () =>
      document.activeElement?.id === "node-body-war.business.actor.runner",
  );
  check(
    "history-recovery",
    (await desktopPage.evaluate(() => document.activeElement?.id)) ===
      "node-body-war.business.actor.runner",
    "Back restores and focuses the prior canonical node location",
  );

  const blockedExamples = await desktopPage.evaluate(() => {
    const result = { recorded: null, missing: null };
    for (const node of document.querySelectorAll(".node-card")) {
      const brief = node.querySelector(".reference-brief--node");
      const statusRow = [...brief.querySelectorAll("dl div")].find(
        (row) => row.querySelector("dt")?.textContent === "Candidate status",
      );
      if (statusRow?.querySelector("dd")?.textContent !== "blocked") continue;
      const heading = [...brief.querySelectorAll("h5")].find(
        (item) => item.textContent === "Blocking questions",
      );
      const questions = heading?.nextElementSibling;
      if (
        questions?.matches("ul") &&
        questions.querySelector("li") &&
        !result.recorded
      ) {
        result.recorded = node.id;
      }
      if (
        questions?.matches("p") &&
        questions.textContent.includes("No blocking question recorded") &&
        !result.missing
      ) {
        result.missing = node.id;
      }
    }
    return result;
  });
  check(
    "blocked-brief-fixtures",
    Boolean(blockedExamples.recorded && blockedExamples.missing),
    "the generated atlas retains both a recorded blocking question and an explicit missing-question example",
  );
  for (const [kind, nodeId] of Object.entries(blockedExamples)) {
    await desktopPage.goto(
      `${server.origin}/BUSINESS-VIEW-ATLAS.html#${nodeId}`,
      { waitUntil: "networkidle" },
    );
    const brief = desktopPage.locator(`[id="${nodeId}"]`).locator(
      ".reference-brief--node",
    );
    await brief.locator("summary").click();
    check(
      `blocked-${kind}-question-visible`,
      await brief
        .locator(
          kind === "recorded"
            ? "h5:text-is('Blocking questions') + ul li"
            : "text=No blocking question recorded",
        )
        .first()
        .isVisible(),
      kind === "recorded"
        ? "a recorded blocking question is visible in the opened node brief"
        : "the source-backed absence of a blocking question is explicitly visible",
    );
  }

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
  check(
    "native-no-js-arrow-and-lane-meaning",
    (await noJsPage.locator(".semantic-lane:visible").count()) === 13 &&
      (await noJsPage.locator(".relation-arrow:visible").count()) === 231,
    "all 13 semantic lanes and 231 exact relation arrows remain readable without JavaScript",
  );
  const noJsBrief = noJsPage
    .locator(".reference-brief--node")
    .first();
  check(
    "native-no-js-brief",
    (await noJsBrief.getAttribute("open")) !== null &&
      (await noJsBrief.locator(".reference-brief__content").isVisible()),
    "static-open native details expose source-backed reference content without JavaScript",
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
  check(
    "mobile-semantic-overview",
    (await mobilePage.locator(".semantic-lane:visible").count()) === 13 &&
      (await mobilePage
        .locator(".overview-spatial")
        .evaluate((element) => getComputedStyle(element).display)) === "none",
    "mobile hides only the compressed spatial map and preserves all 13 semantic lanes",
  );
  await mobilePage.goto(
    `${server.origin}/BUSINESS-VIEW-ATLAS.html#relation-body-war.relation.provider-belongs-runner`,
    { waitUntil: "networkidle" },
  );
  const mobileRelation = mobilePage.locator(
    '[id="relation-body-war.relation.provider-belongs-runner"]',
  );
  const mobileArrowLayout = await mobileRelation
    .locator(".relation-arrow")
    .evaluate((arrow) => {
      const parts = [...arrow.children].map((element) =>
        element.getBoundingClientRect(),
      );
      return {
        stacked:
          parts.length === 3 &&
          parts[0].top < parts[1].top &&
          parts[1].top < parts[2].top,
        scrollWidth: arrow.scrollWidth,
        clientWidth: arrow.clientWidth,
      };
    });
  check(
    "mobile-exact-arrow-stacks",
    mobileArrowLayout.stacked &&
      mobileArrowLayout.scrollWidth <= mobileArrowLayout.clientWidth,
    `mobile exact arrow stacks source, predicate, and target without horizontal loss (${mobileArrowLayout.scrollWidth}/${mobileArrowLayout.clientWidth})`,
  );
  const mobileRelationBrief = mobileRelation.locator(
    ".reference-brief--relation",
  );
  await mobileRelationBrief.locator("summary").click();
  check(
    "mobile-touch-brief",
    (await mobileRelationBrief.getAttribute("open")) !== null &&
      (await mobileRelationBrief.textContent()).includes("Exact tuple"),
    "touch/click persistently exposes the exact relation brief",
  );
  await mobileRelation.screenshot({
    path: mobileRelationScreenshotPath,
  });
  await mobileContext.close();

  const largeTextContext = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    deviceScaleFactor: 1,
    javaScriptEnabled: true,
  });
  const largeTextPage = await largeTextContext.newPage();
  watchPage(largeTextPage);
  await largeTextPage.goto(
    `${server.origin}/BUSINESS-VIEW-ATLAS.html#relation-body-war.relation.provider-belongs-runner`,
    { waitUntil: "networkidle" },
  );
  await largeTextPage.evaluate(() => {
    document.documentElement.style.fontSize = "200%";
  });
  const largeTextBrief = largeTextPage.locator(
    '[id="relation-body-war.relation.provider-belongs-runner"] .reference-brief--relation',
  );
  await largeTextBrief.locator("summary").click();
  const largeTextWidths = await largeTextPage.evaluate(() => ({
    scroll: document.documentElement.scrollWidth,
    client: document.documentElement.clientWidth,
  }));
  check(
    "two-hundred-percent-text",
    (await largeTextBrief.locator(".reference-brief__content").isVisible()) &&
      largeTextWidths.scroll <= largeTextWidths.client,
    `200% root text preserves the opened relation brief without horizontal document loss (${largeTextWidths.scroll}/${largeTextWidths.client})`,
  );
  await largeTextContext.close();

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
  check(
    "print-arrow-lanes-and-briefs",
    (await reducedPage.locator(".semantic-lane:visible").count()) === 13 &&
      (await reducedPage.locator(".relation-arrow:visible").count()) === 231 &&
      (await reducedPage
        .locator(".reference-brief__content:visible")
        .count()) > 0,
    "print retains all semantic lanes, exact arrows, and reference-brief content",
  );
  await reducedContext.close();

  externalRequestUrls = [
    ...new Set(
      browserRequests.filter((requestUrl) => {
        const parsed = new URL(requestUrl);
        return (
          (parsed.protocol === "http:" || parsed.protocol === "https:") &&
          parsed.origin !== server.origin
        );
      }),
    ),
  ].sort();
  check(
    "browser-errors",
    consoleErrors.length === 0 && pageErrors.length === 0,
    `zero console errors and page errors (${consoleErrors.length}/${pageErrors.length})`,
  );
  check(
    "request-errors",
    failedRequests.length === 0,
    `zero failed browser requests (${failedRequests.length})`,
  );
  check(
    "external-network-isolation",
    externalRequestUrls.length === 0,
    `zero external network requests (${externalRequestUrls.length})`,
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
  if (browser) {
    await browser.close();
    browserClosed = true;
  }
  await server.close();
  serverClosed = true;
}

const screenshots = {};
for (const [id, absolutePath] of [
  ["overview", overviewScreenshotPath],
  ["relation_mobile", mobileRelationScreenshotPath],
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
  execution_lane: prototypeFastLane
    ? "candidate-local-prototype-fast-lane"
    : "governed-work-pack",
  artifact_binding:
    swu003RevalidationReceipt.result === "pass" &&
    swu003RevalidationReceipt.target_inventory.find(
      (target) =>
        target.path ===
        "projects/body-war/ontology/business/BUSINESS-VIEW-ATLAS.html",
    )?.final_sha256 === artifacts.atlas.sha256
      ? "swu-bwaa-003-revalidation-receipt"
      : prototypeFastLane
        ? "live-byte-current-generator-check"
        : "failed",
  started_at: startedAt,
  completed_at: new Date().toISOString(),
  artifacts,
  predecessor_revalidation: {
    path: "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/work-pack/closeout/SWU-BWAA-003.revalidation-001.receipt.json",
    sha256: await sha256File(swu003RevalidationReceiptPath),
  },
  runtime: {
    node: process.version,
    playwright_version: playwrightPackage.version,
    playwright_cli_path: playwrightCliPath,
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
    modes: [
      "javascript",
      "no-javascript",
      "mobile",
      "reduced-motion",
      "200-percent-root-text",
      "print",
    ],
    isolation:
      "fresh incognito context per mode; loopback random-port server; exact atlas path only; server and browser closed at completion",
  },
  request_paths: [...new Set(requestLog)].sort(),
  browser_request_urls: [...new Set(browserRequests)].sort(),
  external_request_urls: externalRequestUrls,
  failed_requests: failedRequests,
  teardown: {
    browser_closed: browserClosed,
    loopback_server_closed: serverClosed,
  },
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
