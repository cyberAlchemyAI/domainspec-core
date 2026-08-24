import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const playwrightModuleRoot = process.argv[2];
if (!playwrightModuleRoot) {
  throw new Error("Pass the absolute global Playwright module path as argument 1");
}

const require = createRequire(import.meta.url);
const { chromium } = require(playwrightModuleRoot);
const htmlPath = path.resolve(fileURLToPath(new URL("../ontology-visualization.html", import.meta.url)));
const explanationPath = path.resolve(fileURLToPath(new URL("../explanations/beginner.json", import.meta.url)));
const screenshotPath = "/tmp/augmentor-unified-agent-ontology.png";
const explanations = JSON.parse(await readFile(explanationPath, "utf8"));
const renderedAnalogy = ({ text, limitation }) =>
  `${text} Where this comparison stops: ${limitation}`;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
let zoomContext;
const consoleErrors = [];
const pageErrors = [];
const externalRequests = [];

page.on("console", (message) => {
  if (message.type() === "error") consoleErrors.push(message.text());
});
page.on("pageerror", (error) => pageErrors.push(error.message));
page.on("request", (request) => {
  if (/^https?:/i.test(request.url())) externalRequests.push(request.url());
});

try {
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });

  assert.equal(await page.locator("#stat-nodes").textContent(), "22");
  assert.equal(await page.locator("#stat-relations").textContent(), "28");
  assert.equal(await page.locator("#stat-views").textContent(), "5");
  assert.equal(await page.locator("#stat-residue").textContent(), "7");
  assert.equal(await page.getByTestId("body-view-button").getAttribute("aria-pressed"), "true");
  assert.equal(await page.getByTestId("technical-view-button").getAttribute("aria-pressed"), "false");
  assert.equal(await page.getByTestId("body-view").isVisible(), true);
  assert.equal(await page.getByTestId("technical-view").isHidden(), true);
  assert.equal(await page.getByTestId("robot-core-controls").locator(".robot-core-button").count(), 10);
  assert.equal(await page.getByTestId("robot-consultation-card").count(), 1);
  assert.equal(await page.locator("#body-region-controls, #body-inspector, #body-status-legend, #sdk-seam-wrap").count(), 0);
  assert.match(await page.locator("#claim-ceiling-copy").textContent(), /Authority effect: none/);
  assert.match(await page.locator("#claim-ceiling-copy").getAttribute("title"), /no working routing/);

  const theme = await page.evaluate(() => {
    const root = getComputedStyle(document.documentElement);
    return {
      canvas: root.getPropertyValue("--canvas").trim(),
      surface: root.getPropertyValue("--surface").trim(),
      ink: root.getPropertyValue("--ink").trim(),
      accent: root.getPropertyValue("--accent").trim(),
      line: root.getPropertyValue("--line").trim(),
      bodyBackgroundImage: getComputedStyle(document.body).backgroundImage,
      graphBackgroundImage: getComputedStyle(document.querySelector(".graph-scroll")).backgroundImage
    };
  });
  assert.deepEqual(theme, {
    canvas: "#fbfbfd",
    surface: "#ffffff",
    ink: "#18181b",
    accent: "#5b5bd6",
    line: "#e8e8ed",
    bodyBackgroundImage: "none",
    graphBackgroundImage: "none"
  });

  const initialHash = new URL(page.url()).hash;
  const workCore = page.getByTestId("robot-core-work-spine");
  await workCore.click();
  assert.equal(await workCore.getAttribute("aria-expanded"), "true");
  assert.equal(await page.locator("#robot-card-heading").textContent(), "Approved work");
  await page.keyboard.press("Escape");
  assert.equal(await workCore.getAttribute("aria-expanded"), null);

  await page.getByTestId("technical-view-button").click();
  assert.equal(await page.getByTestId("technical-view").isVisible(), true);
  assert.equal(await page.getByTestId("body-view").isHidden(), true);
  assert.equal(new URL(page.url()).hash, initialHash);
  assert.equal(await page.locator("#explanation-lenses button").count(), 6);
  assert.deepEqual(await page.locator("#explanation-lenses button").allTextContents(), [
    "What it means",
    "What exists today",
    "How it works",
    "Show an example",
    "Compare it to something familiar",
    "What it cannot do"
  ]);
  assert.equal(await page.locator('#view-tabs [role="tab"]').count(), 0);
  assert.equal(await page.locator("#view-tabs .tab[aria-pressed]").count(), 6);
  assert.equal(await page.locator("#lane-explanations .lane-card").count(), 4);
  assert.equal(await page.locator("#proposed-explanation-modes .proposed-mode").count(), 4);
  await page.locator(".proposed-modes summary").click();
  assert.ok(await page.locator('[data-mode-id="guided_walkthrough"]').isVisible());
  assert.match(
    await page.getByTestId("lane-card-experience").textContent(),
    new RegExp(explanations.lanes.experience.plain_meaning.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
  );
  const desktopPresentation = await page.evaluate(() => ({
    titleFontSize: Number.parseFloat(getComputedStyle(document.querySelector("h1")).fontSize),
    guideTop: Math.round(document.querySelector(".beginner-guide").getBoundingClientRect().top),
    titleFontFamily: getComputedStyle(document.querySelector("h1")).fontFamily
  }));
  assert.ok(desktopPresentation.titleFontSize >= 48 && desktopPresentation.titleFontSize <= 64);
  assert.ok(desktopPresentation.guideTop < 560);
  assert.match(desktopPresentation.titleFontFamily, /Inter|system-ui/);

  await page.getByTestId("explanation-lens-process_view").click();
  assert.equal(
    await page.getByTestId("explanation-lens-process_view").getAttribute("aria-pressed"),
    "true"
  );
  assert.match(
    await page.getByTestId("lane-card-experience").textContent(),
    new RegExp(explanations.lanes.experience.process_view.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"))
  );

  await page.getByTestId("graph-node-augmentor_interface").click();
  assert.equal(await page.locator(".inspector-title").textContent(), "One place to talk");
  assert.equal(
    await page.getByTestId("selected-beginner-explanation").locator("p").textContent(),
    explanations.nodes["aug.concept.augmentor_interface"].process_view
  );
  await page.getByTestId("explanation-lens-analogy").click();
  assert.equal(
    await page.getByTestId("selected-beginner-explanation").locator("p").textContent(),
    renderedAnalogy(explanations.nodes["aug.concept.augmentor_interface"].analogy)
  );

  const authorityLane = page.getByTestId("graph-lane-authority");
  await authorityLane.focus();
  await page.keyboard.press("Enter");
  assert.match(await page.locator(".inspector-title").textContent(), /Who can decide/);
  assert.equal(
    await page.getByTestId("selected-beginner-explanation").locator("p").textContent(),
    renderedAnalogy(explanations.lanes.authority.analogy)
  );
  await page.keyboard.press("Escape");

  const viewCounts = {
    experience: "11 nodes · 9 relations",
    runtime: "12 nodes · 13 relations",
    knowledge: "7 nodes · 7 relations",
    "authority-bridge": "9 nodes · 7 relations",
    "intent-route": "13 nodes · 14 relations"
  };
  for (const [view, count] of Object.entries(viewCounts)) {
    await page.getByTestId(`view-${view}`).click();
    assert.equal(await page.locator("#visible-count").textContent(), count);
  }

  await page.getByTestId("view-intent-route").click();
  await page.getByTestId("graph-node-route_disposition").click();
  assert.equal(await page.locator(".inspector-title").textContent(), "Route finder result");
  assert.equal(await page.getByTestId("technical-record").getAttribute("open"), null);
  assert.match(await page.getByTestId("technical-record").locator("summary").textContent(), /RouteDisposition/);
  await page.keyboard.press("Escape");
  await page.locator('[data-sequence-id="AUG-INTENT-RESOLVE"]').click();
  assert.equal(await page.locator(".sequence-number").count(), 4);

  await page.locator("#reset-filters").click();
  await page.locator("#ontology-search").fill("aug.concept.context_snapshot");
  assert.equal(await page.locator("#visible-count").textContent(), "1 nodes · 0 relations");
  await page.locator("#ontology-search").fill("Saved starting information");
  assert.equal(await page.locator("#visible-count").textContent(), "1 nodes · 0 relations");
  await page.locator("#ontology-search").fill("dispatch-spec");
  assert.notEqual(await page.locator("#visible-count").textContent(), "0 nodes · 0 relations");
  await page.locator("#reset-filters").click();

  const node = page.getByTestId("graph-node-conversation_thread");
  await node.focus();
  await page.keyboard.press("Enter");
  assert.equal(await page.locator(".inspector-title").textContent(), "Saved conversation");
  await page.keyboard.press("Escape");
  assert.match(await page.locator(".inspector-title").textContent(), /Choose something to explore/);

  const relation = page.getByTestId("graph-relation-augmentor_presents_thread");
  await relation.focus();
  await page.keyboard.press("Space");
  assert.match(await page.locator(".beginner-explanation").textContent(), /One place to talk shows Saved conversation/);
  await page.keyboard.press("Escape");

  await page.locator('[data-sequence-id="AUG-EXP-ORDINARY"]').click();
  assert.equal(await page.locator(".sequence-number").count(), 6);

  await page.locator("#reset-filters").click();
  assert.equal(await page.locator("[data-testid='linear-list'] [data-kind='node']").count(), 22);
  assert.equal(await page.locator("[data-testid='linear-list'] [data-kind='relation']").count(), 28);

  await page.getByTestId("body-view-button").click();
  await page.setViewportSize({ width: 320, height: 800 });
  assert.equal(await page.getByTestId("body-view").isVisible(), true);
  assert.equal(await page.getByTestId("robot-core-controls").locator(".robot-core-button").count(), 10);
  assert.equal(
    await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
    true
  );
  assert.ok(await page.getByTestId("robot-core-heart").isVisible());
  assert.ok(await page.getByTestId("robot-core-addon-sdk").isVisible());

  await page.getByTestId("technical-view-button").click();
  const mobileLens = page.getByTestId("explanation-lens-plain_meaning");
  await mobileLens.scrollIntoViewIfNeeded();
  await mobileLens.focus();
  await page.keyboard.press("Shift+Tab");
  await page.keyboard.press("Tab");
  assert.ok(await page.locator("#ontology-search").isVisible());
  assert.ok(await page.getByTestId("explanation-lens-plain_meaning").isVisible());
  assert.ok(await page.getByTestId("lane-card-experience").isVisible());
  assert.ok(await page.getByTestId("ontology-inspector").isVisible());
  assert.equal(
    await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
    true
  );
  assert.ok(await page.locator(".beginner-guide").evaluate(
    (element) => element.getBoundingClientRect().top < 760
  ));
  assert.equal(await page.locator(".claim-ceiling").evaluate(
    (element) => getComputedStyle(element).position
  ), "static");
  assert.equal(await mobileLens.evaluate((element) => {
    const bounds = element.getBoundingClientRect();
    const hit = document.elementFromPoint(bounds.left + bounds.width / 2, bounds.top + bounds.height / 2);
    return element === hit || element.contains(hit);
  }), true);
  assert.equal(await mobileLens.evaluate(
    (element) => getComputedStyle(element).outlineStyle
  ), "solid");

  await page.emulateMedia({ reducedMotion: "reduce" });
  const transitionDuration = await page.locator("button").first().evaluate(
    (element) => getComputedStyle(element).transitionDuration
  );
  assert.match(transitionDuration, /0\.01ms|0s|1e-05s/);

  zoomContext = await browser.newContext({ viewport: { width: 720, height: 500 }, deviceScaleFactor: 2 });
  const zoomPage = await zoomContext.newPage();
  await zoomPage.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
  assert.equal(await zoomPage.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
  assert.ok(await zoomPage.getByTestId("robot-core-face").isVisible());
  assert.ok(await zoomPage.getByTestId("robot-core-addon-sdk").isVisible());
  await zoomPage.screenshot({ path: "/tmp/augmentor-unified-agent-ontology-zoom-200.png", fullPage: true });
  await zoomContext.close();
  zoomContext = null;

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.getByTestId("body-view-button").click();
  await page.screenshot({ path: screenshotPath, fullPage: true });

  assert.deepEqual(consoleErrors, []);
  assert.deepEqual(pageErrors, []);
  assert.deepEqual(externalRequests, []);
  process.stdout.write(`BROWSER_VISUALIZATION=pass screenshot=${screenshotPath}\n`);
} finally {
  if (zoomContext) await zoomContext.close();
  await browser.close();
}
