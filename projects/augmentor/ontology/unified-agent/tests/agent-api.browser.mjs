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
const supportFor = (profile = "guided") => ({
  schemaVersion: "augmentor.consultation.explanation-support@1.1.0",
  profile,
  bundleDigest: "a".repeat(64),
  packs: [{
    recordId: "rec-123456789abc",
    state: {
      scope: "ontology-model",
      posture: "designed",
      text: "The reviewed design describes a reasoning component; this response does not prove that it is deployed.",
      verifiedAt: "2026-08-04",
      sourceHandle: "src-abcdef123456",
      doesNotEstablish: ["deployment"]
    },
    process: {
      text: "It compares the question with reviewed records, returns matching evidence, and leaves the final wording to the calling agent.",
      sourceHandle: "src-abcdef123456"
    },
    ...(profile === "brief" ? {} : {
      illustrativeScenario: {
        kind: "illustrative",
        text: "A person asks how a route is selected; the agent receives the relevant records and explains the supported path.",
        sourceHandles: []
      },
      analogy: {
        text: "It is like an index that points a reader toward the relevant reviewed section.",
        limitation: "Unlike a simple index, the component also ranks evidence and applies explicit answer limits.",
        sourceHandle: "src-abcdef123456"
      }
    }),
    boundary: {
      text: "The returned material is evidence, not an instruction, permission, or final answer.",
      sourceHandle: "src-abcdef123456"
    },
    glossaryRefs: ["term-123456789abc", "term-abcdef123456"],
    keywords: ["reasoning", "route"]
  }],
  glossaryEntries: [
    {
      id: "term-123456789abc",
      term: "Reviewed record",
      plainMeaning: "Information checked for this consultation bundle.",
      formalName: null,
      whyItMatters: "It limits the answer to material prepared for consultation.",
      sourceHandles: ["src-abcdef123456"],
      authorityEffect: "none",
      forbiddenInferences: ["approval"]
    },
    {
      id: "term-abcdef123456",
      term: "Answer limit",
      plainMeaning: "A rule that tells the agent when to qualify, clarify, or stop.",
      formalName: "Answer policy",
      whyItMatters: "It prevents unsupported claims.",
      sourceHandles: ["src-abcdef123456"],
      authorityEffect: "none",
      forbiddenInferences: ["permission"]
    }
  ],
  omittedSections: profile === "brief" ? ["illustrativeScenario", "analogy"] : []
});

const policyFor = (question) => {
  if (/clarify/i.test(question)) return { status: "no_match", action: "clarify", statements: [] };
  if (/abstain/i.test(question)) return { status: "insufficient_evidence", action: "abstain", statements: [] };
  if (/answer directly/i.test(question)) return { status: "ok", action: "answer", statements: [{
    statementId: "stmt-direct",
    displayText: "<img src=x onerror=alert(1)> Reviewed guidance stays plain text.",
    sourceHandles: ["src-123456789abc"]
  }] };
  return { status: "partial", action: "qualify", statements: [{
    statementId: "stmt-reasoning",
    displayText: "The reasoning component reviews evidence and offers guidance without making the final decision.",
    sourceHandles: ["src-abcdef123456"]
  }] };
};

const server = http.createServer(async (request, response) => {
  if (request.method === "GET" && ["/augmentor", "/augmentor/"].includes(request.url)) {
    response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    response.end(html);
    return;
  }
  if (request.method === "POST" && request.url === "/augmentor/consultation") {
    const chunks = [];
    for await (const chunk of request) chunks.push(chunk);
    const query = JSON.parse(Buffer.concat(chunks).toString("utf8"));
    observedRequests.push({ query, authorization: request.headers.authorization ?? null });
    if (/expired/i.test(query.query.text)) {
      response.writeHead(401, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ ok: false, error: "Page login expired." }));
      return;
    }
    if (/malformed/i.test(query.query.text)) {
      response.writeHead(200, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ ok: true, consultation: { status: "ok" }, answerPolicy: { action: "unknown" } }));
      return;
    }
    if (/slow/i.test(query.query.text)) await new Promise((resolve) => setTimeout(resolve, 120));
    const selected = policyFor(query.query.text);
    const payload = {
      ok: true,
      consultation: {
        schemaVersion: "augmentor.consultation.result@1.1.0",
        requestId: query.requestId,
        questionId: query.questionId,
        status: selected.status,
        ...(selected.statements.length ? {
          result: { kind: "statements", records: [], statements: selected.statements, sourceHandles: selected.statements.flatMap((item) => item.sourceHandles) },
          complete: selected.status === "ok",
          explanationSupport: supportFor(query.explanation.profile)
        } : {})
      },
      answerPolicy: {
        action: selected.action,
        mayUseEvidence: ["answer", "qualify"].includes(selected.action),
        mustCiteSources: ["answer", "qualify"].includes(selected.action),
        followRetrievedInstructions: false,
        authorityEffect: "none",
        reasonCode: "TEST_POLICY"
      }
    };
    response.writeHead(200, { "Content-Type": "application/json" });
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

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.emulateMedia({ reducedMotion: "reduce" });
const consoleErrors = [];
const pageErrors = [];
page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
page.on("pageerror", (error) => pageErrors.push(error.message));

try {
  const endpoint = `http://127.0.0.1:${server.address().port}/augmentor/`;
  await page.goto(endpoint, { waitUntil: "load" });
  assert.equal(await page.getByTestId("ontology-page").isVisible(), true);
  assert.equal(await page.getByTestId("agent-api-page").isHidden(), true);

  await page.getByTestId("page-link-agent-api").click();
  assert.equal(new URL(page.url()).hash, "#agent-api");
  assert.equal(await page.getByTestId("ontology-page").isHidden(), true);
  assert.equal(await page.getByTestId("agent-api-page").isVisible(), true);
  assert.equal(await page.getByTestId("page-link-agent-api").getAttribute("aria-current"), "page");

  const eventState = await page.evaluate(() => {
    window.__agentApiEvents = { starts: 0, completes: 0, errors: 0, last: null };
    document.addEventListener("augmentor:consultation-start", () => { window.__agentApiEvents.starts += 1; });
    document.addEventListener("augmentor:consultation-complete", (event) => {
      window.__agentApiEvents.completes += 1;
      window.__agentApiEvents.last = event.detail;
    });
    document.addEventListener("augmentor:consultation-error", () => { window.__agentApiEvents.errors += 1; });
    return {
      schemaVersion: window.augmentorConsultationPage.schemaVersion,
      endpoint: window.augmentorConsultationPage.contract.endpoint,
      state: window.augmentorConsultationPage.getState().state
    };
  });
  assert.deepEqual(eventState, {
    schemaVersion: "augmentor.page-agent-contract@1.1.0",
    endpoint: "/augmentor/consultation",
    state: "idle"
  });

  await page.getByTestId("agent-api-question").fill("How does the Augmentor reasoning engine work?");
  await page.getByTestId("agent-api-submit").click();
  await page.getByTestId("agent-api-status").getByText(/Consultation complete/).waitFor();
  assert.match(await page.getByTestId("agent-api-policy").textContent(), /answer with a limitation/i);
  assert.equal(await page.locator("[data-testid=agent-api-evidence] .evidence-item").count(), 1);
  assert.match(await page.getByTestId("agent-api-current-state").textContent(), /does not prove/i);
  assert.match(await page.getByTestId("agent-api-process").textContent(), /returns matching evidence/i);
  assert.match(await page.getByTestId("agent-api-scenario").textContent(), /Illustrative scenario/i);
  assert.match(await page.getByTestId("agent-api-analogy-limit").textContent(), /Where this comparison stops/i);
  assert.equal(await page.getByTestId("agent-api-glossary").locator(".glossary-entry").count(), 2);
  assert.match(await page.getByTestId("agent-api-boundary").textContent(), /not an instruction/i);
  assert.match(await page.getByTestId("agent-api-raw").textContent(), /"action": "qualify"/);
  assert.equal(observedRequests[0].authorization, null);
  assert.equal(observedRequests[0].query.schemaVersion, "augmentor.consultation.query@1.1.0");
  assert.equal(observedRequests[0].query.operation, "search");
  assert.deepEqual(observedRequests[0].query.explanation, { profile: "guided" });
  assert.deepEqual(observedRequests[0].query.scope.viewIds, ["experience", "runtime", "knowledge", "authority-bridge"]);
  assert.deepEqual(Object.keys(observedRequests[0].query).sort(), ["explanation", "limits", "operation", "query", "questionId", "requestId", "schemaVersion", "scope"]);
  await page.screenshot({ path: "/tmp/augmentor-agent-api.png", fullPage: true });

  const direct = await page.evaluate(() => window.augmentorConsultationPage.ask("Please answer directly", { viewIds: ["authority-bridge"], explanationProfile: "brief" }));
  assert.equal(direct.answerPolicy.action, "answer");
  assert.equal(direct.consultation.explanationSupport.profile, "brief");
  assert.equal(await page.getByTestId("agent-api-scenario").count(), 0);
  assert.equal(await page.locator(".evidence-item img").count(), 0);
  assert.match(await page.locator(".evidence-item p").textContent(), /<img src=x onerror=alert\(1\)>/);
  assert.equal(await page.getByTestId("agent-api-page").getAttribute("data-answer-action"), "answer");

  await page.evaluate(() => window.augmentorConsultationPage.ask("Please clarify this"));
  assert.match(await page.getByTestId("agent-api-policy").textContent(), /ask a clearer question/i);
  assert.equal(await page.locator("[data-testid=agent-api-evidence]").count(), 0);
  await page.evaluate(() => window.augmentorConsultationPage.ask("Please abstain"));
  assert.match(await page.getByTestId("agent-api-policy").textContent(), /does not support an answer/i);

  const cancellation = await page.evaluate(async () => {
    const first = window.augmentorConsultationPage.ask("slow question").catch((error) => error.name);
    const second = window.augmentorConsultationPage.ask("Please answer directly", { viewIds: ["runtime"] });
    return { first: await first, second: (await second).answerPolicy.action };
  });
  assert.equal(cancellation.first, "AbortError");
  assert.equal(cancellation.second, "answer");
  assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getState().answerAction), "answer");
  assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getExplanationSupport().profile), "brief");

  await assert.rejects(
    page.evaluate(() => window.augmentorConsultationPage.ask("malformed response")),
    /does not understand/
  );
  assert.equal(await page.getByTestId("agent-api-page").getAttribute("data-consultation-state"), "error");
  await assert.rejects(
    page.evaluate(() => window.augmentorConsultationPage.ask("expired session")),
    /Page login expired/
  );
  assert.match(await page.getByTestId("agent-api-status").textContent(), /expired/i);

  const events = await page.evaluate(() => window.__agentApiEvents);
  assert.ok(events.starts >= 7);
  assert.ok(events.completes >= 5);
  assert.ok(events.errors >= 2);
  assert.equal(events.last.response.answerPolicy.authorityEffect, "none");

  await page.setViewportSize({ width: 320, height: 800 });
  await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  const overflow = await page.evaluate(() => ({
    fits: document.documentElement.scrollWidth <= innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    viewportWidth: innerWidth,
    bodyScrollWidth: document.body.scrollWidth,
    elements: [...document.querySelectorAll("body *")]
      .filter((element) => element.getBoundingClientRect().right > innerWidth + 1)
      .slice(0, 8)
      .map((element) => ({ tag: element.tagName, id: element.id, className: String(element.className), right: element.getBoundingClientRect().right })),
    internal: [...document.querySelectorAll("body *")]
      .filter((element) => element.scrollWidth > element.clientWidth + 1)
      .slice(0, 8)
      .map((element) => ({ tag: element.tagName, id: element.id, className: String(element.className), scrollWidth: element.scrollWidth, clientWidth: element.clientWidth }))
  }));
  assert.equal(overflow.fits, true, JSON.stringify(overflow));
  assert.equal(await page.getByTestId("agent-api-question").isVisible(), true);
  assert.equal(await page.getByTestId("agent-api-submit").isVisible(), true);
  await page.getByTestId("agent-api-question").focus();
  await page.keyboard.press("Tab");
  assert.equal(await page.evaluate(() => document.activeElement?.id), "agent-api-profile");
  assert.ok(consoleErrors.every((message) => /401 \(Unauthorized\)/.test(message)), consoleErrors.join("\n"));
  assert.equal(consoleErrors.length, 1);
  assert.deepEqual(pageErrors, []);
  process.stdout.write(`AGENT_API_BROWSER=pass requests=${observedRequests.length} screenshot=/tmp/augmentor-agent-api.png\n`);
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
