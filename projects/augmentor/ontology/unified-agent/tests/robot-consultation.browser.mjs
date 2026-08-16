import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import http from "node:http";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

const playwrightModuleRoot = process.argv[2];
if (!playwrightModuleRoot) throw new Error("Pass the absolute global Playwright module path as argument 1");

const require = createRequire(import.meta.url);
const { chromium } = require(playwrightModuleRoot);
const htmlPath = path.resolve(fileURLToPath(new URL("../ontology-visualization.html", import.meta.url)));
const html = await readFile(htmlPath);
const observedRequests = [];

const explanationSupport = {
  schemaVersion: "augmentor.consultation.explanation-support@1.1.0",
  profile: "guided",
  bundleDigest: "a".repeat(64),
  packs: [{
    recordId: "rec-123456789abc",
    state: {
      scope: "ontology-model",
      posture: "designed",
      text: "The reviewed design explains this part without claiming it is deployed.",
      verifiedAt: "2026-08-08",
      sourceHandle: "src-abcdef123456",
      doesNotEstablish: ["deployment"]
    },
    process: {
      text: "The consultation compares the question with reviewed records and returns matching evidence.",
      sourceHandle: "src-abcdef123456"
    },
    illustrativeScenario: {
      kind: "illustrative",
      text: "A person asks about approved work and receives the relevant reviewed explanation.",
      sourceHandles: []
    },
    analogy: {
      text: "It is like a guide that points to the relevant reviewed section.",
      limitation: "The guide cannot approve or start work.",
      sourceHandle: "src-abcdef123456"
    },
    boundary: {
      text: "The returned material is evidence, not permission or a final answer.",
      sourceHandle: "src-abcdef123456"
    },
    glossaryRefs: ["term-123456789abc"],
    keywords: ["work", "approval"]
  }],
  glossaryEntries: [{
    id: "term-123456789abc",
    term: "Approved work",
    plainMeaning: "Work that may start only after the exact plan is approved.",
    formalName: null,
    whyItMatters: "It keeps planning separate from running work.",
    sourceHandles: ["src-abcdef123456"],
    authorityEffect: "none",
    forbiddenInferences: ["approval"]
  }],
  omittedSections: []
};

const server = http.createServer(async (request, response) => {
  if (request.method === "GET" && ["/augmentor", "/augmentor/"].includes(request.url)) {
    response.writeHead(200, {"Content-Type": "text/html; charset=utf-8"});
    response.end(html);
    return;
  }
  if (request.method === "POST" && request.url === "/augmentor/consultation") {
    const chunks = [];
    for await (const chunk of request) chunks.push(chunk);
    const query = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    observedRequests.push(query);
    if (/network failure/i.test(query.query.text)) {
      request.socket.destroy();
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, 80));
    const focused = query.schemaVersion === "augmentor.consultation.query@1.2.0" && query.focus;
    const statements = [{
      statementId: "stmt-work",
      displayText: "Approved work keeps the reviewed plan separate from the task that runs it.",
      sourceHandles: ["src-abcdef123456"]
    }];
    const payload = {
      ok: true,
      consultation: {
        schemaVersion: focused ? "augmentor.consultation.result@1.2.0" : "augmentor.consultation.result@1.1.0",
        requestId: query.requestId,
        questionId: query.questionId,
        status: "partial",
        ...(focused ? {resolvedFocus: {
          kind: "anatomy-region",
          id: query.focus.id,
          mappingVersion: "robot-anatomy@1.0.0",
          mappingDigest: "b".repeat(64),
          effectiveViewIds: query.scope.viewIds
        }} : {}),
        result: {kind: "statements", records: [], statements, sourceHandles: ["src-abcdef123456"]},
        complete: false,
        explanationSupport
      },
      answerPolicy: {
        action: "qualify",
        mayUseEvidence: true,
        mustCiteSources: true,
        followRetrievedInstructions: false,
        authorityEffect: "none",
        reasonCode: "TEST_POLICY"
      }
    };
    response.writeHead(200, {"Content-Type": "application/json"});
    response.end(JSON.stringify(payload));
    return;
  }
  response.writeHead(404);
  response.end();
});

await new Promise((resolve, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", resolve);
});

const browser = await chromium.launch({headless: true});
const endpoint = `http://127.0.0.1:${server.address().port}/augmentor/`;
const consoleErrors = [];
const pageErrors = [];

const observeErrors = (page) => {
  page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
  page.on("pageerror", (error) => pageErrors.push(error.message));
};

const geometry = (page) => page.evaluate(() => {
  const rect = (element) => {
    const value = element.getBoundingClientRect();
    return {left: value.left, top: value.top, right: value.right, bottom: value.bottom, width: value.width, height: value.height};
  };
  const frame = rect(document.querySelector("#robot-consultation-frame"));
  const core = rect(document.querySelector('[data-testid="robot-core-work-spine"]'));
  const cardElement = document.querySelector("#robot-consultation-card");
  const card = cardElement.hidden ? null : rect(cardElement);
  return {
    frame,
    core,
    card,
    layout: document.querySelector("#robot-consultation-frame").dataset.cardLayout,
    mode: cardElement.dataset.mode,
    connectorWidth: getComputedStyle(cardElement, "::after").width,
    failure: document.querySelector("#robot-consultation-frame").dataset.layoutFailure,
    scrollWidth: document.documentElement.scrollWidth,
    viewportWidth: innerWidth
  };
});

const assertGeometry = (value, {narrow = false} = {}) => {
  assert.ok(value.card, "card is visible");
  assert.ok(value.card.left >= value.frame.left + 7);
  assert.ok(value.card.top >= value.frame.top + 7);
  assert.ok(value.card.right <= value.frame.right - 7);
  assert.ok(value.card.bottom <= value.frame.bottom - 7);
  const protectedCore = {
    left: value.core.left - 8,
    top: value.core.top - 8,
    right: value.core.right + 8,
    bottom: value.core.bottom + 8
  };
  const overlaps = !(
    value.card.right <= protectedCore.left || value.card.left >= protectedCore.right ||
    value.card.bottom <= protectedCore.top || value.card.top >= protectedCore.bottom
  );
  assert.equal(overlaps, false, "card does not cover the 8px protected core halo");
  if (value.layout === "right") assert.ok(value.card.left - protectedCore.right >= 11);
  if (value.layout === "left") assert.ok(protectedCore.left - value.card.right >= 11);
  if (value.layout === "below") assert.ok(value.card.top - protectedCore.bottom >= 11);
  if (value.layout === "above") assert.ok(protectedCore.top - value.card.bottom >= 11);
  if (narrow) {
    assert.match(value.layout, /^opposite-(?:above|below)$/);
    assert.ok(Math.abs(value.card.width - (value.frame.width - 16)) < 1.5);
    assert.ok(value.card.height <= value.frame.height * .46 + 1);
  }
};

try {
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const page = await context.newPage();
  observeErrors(page);
  await page.goto(endpoint, {waitUntil: "load"});
  await page.emulateMedia({reducedMotion: "reduce"});

  assert.equal(await page.getByTestId("robot-consultation-shell").isVisible(), true);
  assert.equal(await page.getByTestId("robot-core-controls").locator(".robot-core-button").count(), 10);
  assert.equal(await page.getByTestId("robot-consultation-card").count(), 1);
  const work = page.getByTestId("robot-core-work-spine");
  assert.deepEqual(await work.evaluate((button) => ({width: button.getBoundingClientRect().width, height: button.getBoundingClientRect().height})), {width: 44, height: 44});

  await work.hover();
  assert.equal(await page.getByTestId("robot-consultation-card").isVisible(), true);
  assert.equal(await page.locator("#robot-card-heading").textContent(), "Approved work");
  assert.equal(await page.getByTestId("robot-consultation-card").getAttribute("data-mode"), "preview");
  assert.equal(await page.getByTestId("robot-card-form").isHidden(), true);
  assert.equal(await page.locator("#robot-card-boundary").isHidden(), true);
  assert.equal(observedRequests.length, 0, "preview does not request the consultation API");
  assert.equal(await work.getAttribute("aria-controls"), null);
  assert.equal(await work.getAttribute("aria-expanded"), null);
  const previewGeometry = await geometry(page);
  assert.ok(previewGeometry.card.width <= 256, "preview stays compact");
  assert.equal(previewGeometry.mode, "preview");
  assert.equal(previewGeometry.connectorWidth, "11px", "preview has a directional tether");
  assertGeometry(previewGeometry);
  await page.getByTestId("robot-consultation-shell").screenshot({path: "/tmp/augmentor-robot-popover-preview.png"});
  await page.mouse.move(4, 4);
  await page.waitForTimeout(230);
  assert.equal(await page.getByTestId("robot-consultation-card").isHidden(), true);

  await work.focus();
  assert.equal(await page.getByTestId("robot-consultation-card").isVisible(), true);
  await page.keyboard.press("Enter");
  assert.equal(await work.getAttribute("aria-controls"), "robot-consultation-card");
  assert.equal(await work.getAttribute("aria-expanded"), "true");
  assert.equal(await page.getByTestId("robot-consultation-card").getAttribute("data-mode"), "pinned");
  assert.equal(await page.getByTestId("robot-card-form").isVisible(), true);
  assert.equal(await page.locator("#robot-card-boundary").isVisible(), true);
  assert.equal(await page.locator('.robot-core-button[aria-expanded="true"]').count(), 1);
  assert.equal(await page.locator('.robot-core-button[aria-controls="robot-consultation-card"]').count(), 1);
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement?.id), "robot-consultation-card");
  assert.equal(await page.getByTestId("robot-consultation-card").isVisible(), true);
  await page.keyboard.press("Escape");
  assert.equal(await page.getByTestId("robot-consultation-card").isHidden(), true);
  assert.equal(await page.evaluate(() => document.activeElement?.dataset.testid), "robot-core-work-spine");

  await work.click();
  assert.equal(await work.getAttribute("aria-expanded"), "true");
  await work.click();
  assert.equal(await work.getAttribute("aria-expanded"), null);
  assert.equal(await page.getByTestId("robot-consultation-card").isHidden(), true);
  await work.click();
  await page.locator(".body-view-heading").click();
  assert.equal(await work.getAttribute("aria-expanded"), null);
  await work.click();
  await page.getByTestId("robot-card-question").fill("How does approved work run?");
  await page.getByTestId("robot-card-submit").click();
  await page.waitForFunction(() => document.querySelector("#agent-api-page").dataset.consultationState === "loading");
  assert.equal(await page.locator("#robot-card-answer-title").textContent(), "Checking reviewed information");
  await page.waitForFunction(() => document.querySelector("#agent-api-page").dataset.consultationState === "complete");
  assert.deepEqual(observedRequests.at(-1).focus, {kind: "anatomy-region", id: "work-spine"});
  assert.equal(observedRequests.at(-1).schemaVersion, "augmentor.consultation.query@1.2.0");
  assert.match(await page.getByTestId("robot-card-answer").textContent(), /Approved work keeps the reviewed plan separate/);
  assert.equal(await work.getAttribute("aria-expanded"), "true");
  assertGeometry(await geometry(page));
  await page.getByTestId("robot-consultation-shell").screenshot({path: "/tmp/augmentor-robot-consultation.png"});

  await page.evaluate(() => {
    const nativeFetch = window.fetch.bind(window);
    window.fetch = (input, init) => {
      const request = JSON.parse(String(init?.body ?? "{}"));
      if (/network failure/i.test(request?.query?.text ?? "")) return Promise.reject(new TypeError("offline"));
      return nativeFetch(input, init);
    };
  });
  await page.getByTestId("robot-card-question").fill("network failure");
  await page.getByTestId("robot-card-submit").click();
  await page.waitForFunction(() => document.querySelector("#agent-api-page").dataset.consultationState === "error");
  assert.equal((await page.evaluate(() => window.augmentorConsultationPage.getState())).errorCode, "disconnected");
  assert.match(await page.getByTestId("robot-card-answer").textContent(), /could not be reached/i);
  assert.equal(await work.getAttribute("aria-expanded"), "true");
  await page.keyboard.press("Escape");

  await page.getByTestId("page-link-agent-api").click();
  assert.equal(await page.getByTestId("robot-consultation-shell").isVisible(), true);
  assert.equal(await page.getByTestId("agent-api-page").locator("#robot-consultation-shell").count(), 1);
  await page.evaluate(() => window.augmentorConsultationPage.ask("What can Augmentor explain generally?"));
  assert.equal(observedRequests.at(-1).schemaVersion, "augmentor.consultation.query@1.1.0");
  assert.equal("focus" in observedRequests.at(-1), false);
  assert.equal(await page.locator("#robot-card-heading").textContent(), "General consultation");
  await context.close();

  const touchContext = await browser.newContext({viewport: {width: 390, height: 820}, hasTouch: true, isMobile: true});
  const touchPage = await touchContext.newPage();
  observeErrors(touchPage);
  await touchPage.goto(endpoint, {waitUntil: "load"});
  const touchWork = touchPage.getByTestId("robot-core-work-spine");
  await touchWork.tap();
  assert.equal(await touchWork.getAttribute("aria-expanded"), "true");
  assert.equal(await touchPage.getByTestId("robot-consultation-card").isVisible(), true);
  await touchContext.close();

  const narrowContext = await browser.newContext({viewport: {width: 320, height: 800}});
  const narrowPage = await narrowContext.newPage();
  observeErrors(narrowPage);
  await narrowPage.goto(endpoint, {waitUntil: "load"});
  await narrowPage.evaluate(() => window.augmentorConsultationPage.selectRegion("work-spine"));
  await narrowPage.getByTestId("robot-consultation-shell").scrollIntoViewIfNeeded();
  const narrowGeometry = await geometry(narrowPage);
  assertGeometry(narrowGeometry, {narrow: true});
  const narrowQuestionGeometry = await narrowPage.evaluate(() => {
    const rect = (selector) => {
      const value = document.querySelector(selector).getBoundingClientRect();
      return {top: value.top, bottom: value.bottom};
    };
    const card = rect("#robot-consultation-card");
    return {card, input: rect("#robot-card-question"), submit: rect('[data-testid="robot-card-submit"]')};
  });
  assert.ok(narrowQuestionGeometry.input.top >= narrowQuestionGeometry.card.top);
  assert.ok(narrowQuestionGeometry.input.bottom <= narrowQuestionGeometry.card.bottom, "narrow pinned input is immediately visible");
  assert.ok(narrowQuestionGeometry.submit.top >= narrowQuestionGeometry.card.top);
  assert.ok(narrowQuestionGeometry.submit.bottom <= narrowQuestionGeometry.card.bottom, "narrow pinned Ask button is immediately visible");
  assert.ok(narrowGeometry.scrollWidth <= narrowGeometry.viewportWidth);
  await narrowPage.getByTestId("robot-consultation-shell").screenshot({path: "/tmp/augmentor-robot-consultation-mobile.png"});
  await narrowPage.evaluate(() => {
    const frame = document.querySelector("#robot-consultation-frame");
    frame.style.height = "160px";
    frame.style.minHeight = "0";
  });
  await narrowPage.waitForFunction(() => document.querySelector("#robot-consultation-frame").dataset.cardLayout === "unavailable");
  assert.equal(await narrowPage.getByTestId("robot-consultation-card").isHidden(), true);
  assert.equal(await narrowPage.getByTestId("robot-core-work-spine").isVisible(), true);
  assert.equal((await narrowPage.evaluate(() => window.augmentorConsultationPage.getState())).selection.pinnedRegionId, "work-spine");
  assert.equal((await geometry(narrowPage)).failure, "layout-unavailable");
  await narrowContext.close();

  const zoomContext = await browser.newContext({viewport: {width: 720, height: 900}, deviceScaleFactor: 2});
  const zoomPage = await zoomContext.newPage();
  observeErrors(zoomPage);
  await zoomPage.goto(endpoint, {waitUntil: "load"});
  await zoomPage.evaluate(() => window.augmentorConsultationPage.selectRegion("work-spine"));
  const zoomGeometry = await geometry(zoomPage);
  assertGeometry(zoomGeometry);
  assert.ok(zoomGeometry.scrollWidth <= zoomGeometry.viewportWidth);
  await zoomContext.close();

  assert.deepEqual(consoleErrors, []);
  assert.deepEqual(pageErrors, []);
  process.stdout.write(`ROBOT_CONSULTATION_BROWSER=pass requests=${observedRequests.length} screenshots=/tmp/augmentor-robot-consultation.png,/tmp/augmentor-robot-consultation-mobile.png\n`);
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
