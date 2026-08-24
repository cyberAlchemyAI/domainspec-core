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
  if (request.url === "/unexpected") {
    response.writeHead(200, { "Content-Type": "application/json" });
    response.end(JSON.stringify({ ok: false, error: "redirect target" }));
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
    if (/forbidden/i.test(query.query.text)) {
      response.writeHead(403, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ ok: false, error: "Forbidden." }));
      return;
    }
    if (/network failure/i.test(query.query.text)) {
      request.socket.destroy();
      return;
    }
    if (/redirect/i.test(query.query.text)) {
      response.writeHead(302, { Location: "/unexpected" });
      response.end();
      return;
    }
    if (/route unavailable/i.test(query.query.text)) {
      response.writeHead(405, { "Content-Type": "text/html; charset=utf-8" });
      response.end("<h1>Method Not Allowed</h1>");
      return;
    }
    if (/server failure/i.test(query.query.text)) {
      response.writeHead(500, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ ok: false, error: "Temporary failure." }));
      return;
    }
    if (/html success/i.test(query.query.text)) {
      response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      response.end("<h1>Not an API response</h1>");
      return;
    }
    if (/malformed json/i.test(query.query.text)) {
      response.writeHead(200, { "Content-Type": "application/json" });
      response.end("{");
      return;
    }
    if (/schema invalid/i.test(query.query.text)) {
      response.writeHead(200, { "Content-Type": "application/json" });
      response.end(JSON.stringify({ ok: true, consultation: { status: "ok" }, answerPolicy: { action: "unknown" } }));
      return;
    }
    if (/slow/i.test(query.query.text)) await new Promise((resolve) => setTimeout(resolve, 120));
    const selected = policyFor(query.query.text);
    const focused = query.schemaVersion === "augmentor.consultation.query@1.2.0" && query.focus;
    const resolvedFocus = focused ? {
      kind: "anatomy-region",
      id: /forged focus/i.test(query.query.text) ? "brain-source" : query.focus.id,
      mappingVersion: "robot-anatomy@1.0.0",
      mappingDigest: "b".repeat(64),
      effectiveViewIds: query.scope.viewIds
    } : null;
    const payload = {
      ok: true,
      consultation: {
        schemaVersion: focused ? "augmentor.consultation.result@1.2.0" : "augmentor.consultation.result@1.1.0",
        requestId: query.requestId,
        questionId: query.questionId,
        status: selected.status,
        ...(resolvedFocus ? { resolvedFocus } : {}),
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
    if (/privacy leak/i.test(query.query.text)) payload.consultation.principal = "principal-private-user";
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
  assert.equal(await page.getByTestId("agent-api-features").locator(".api-feature").count(), 3);
  assert.equal(await page.getByTestId("agent-api-scope-options").getAttribute("open"), null);
  assert.equal(await page.getByTestId("agent-api-integration").getAttribute("open"), null);
  assert.equal(await page.locator(".api-guide-card").count(), 0);

  const eventState = await page.evaluate(() => {
    window.__agentApiEvents = { starts: 0, completes: 0, errors: 0, cancels: 0, last: null, lastStart: null, lastError: null };
    document.addEventListener("augmentor:consultation-start", (event) => {
      window.__agentApiEvents.starts += 1;
      window.__agentApiEvents.lastStart = event.detail;
    });
    document.addEventListener("augmentor:consultation-complete", (event) => {
      window.__agentApiEvents.completes += 1;
      window.__agentApiEvents.last = event.detail;
    });
    document.addEventListener("augmentor:consultation-error", (event) => {
      window.__agentApiEvents.errors += 1;
      window.__agentApiEvents.lastError = event.detail;
    });
    document.addEventListener("augmentor:consultation-cancel", () => { window.__agentApiEvents.cancels += 1; });
    const publicState = window.augmentorConsultationPage.getState();
    return {
      schemaVersion: window.augmentorConsultationPage.schemaVersion,
      endpoint: window.augmentorConsultationPage.contract.endpoint,
      state: publicState.state,
      publicKeys: Object.keys(publicState).sort()
    };
  });
  assert.deepEqual(eventState, {
    schemaVersion: "augmentor.page-agent-contract@1.2.0",
    endpoint: "/augmentor/consultation",
    state: "idle",
    publicKeys: ["answerAction", "errorCode", "presentationScope", "requestId", "requestedFocus", "result", "selection", "selectionEpoch", "state"]
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
  assert.equal(await page.getByTestId("agent-api-more-context").getAttribute("open"), null);
  assert.match(await page.getByTestId("agent-api-raw").textContent(), /"action": "qualify"/);
  assert.equal(observedRequests[0].authorization, null);
  assert.equal(observedRequests[0].query.schemaVersion, "augmentor.consultation.query@1.1.0");
  assert.equal(Object.hasOwn(observedRequests[0].query.query, "kind"), false);
  assert.equal(observedRequests[0].query.operation, "search");
  assert.deepEqual(observedRequests[0].query.explanation, { profile: "guided" });
  assert.deepEqual(observedRequests[0].query.scope.viewIds, ["experience", "runtime", "knowledge", "authority-bridge"]);
  assert.deepEqual(Object.keys(observedRequests[0].query).sort(), ["explanation", "limits", "operation", "query", "questionId", "requestId", "schemaVersion", "scope"]);
  assert.equal(Object.hasOwn(observedRequests[0].query, "focus"), false);
  assert.doesNotMatch(JSON.stringify(await page.evaluate(() => window.augmentorConsultationPage.getState())), /How does the Augmentor/i);
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

  const previewState = await page.evaluate(() => {
    window.augmentorConsultationPage.clearSelection();
    window.augmentorConsultationPage.previewRegion("brain-context");
    return window.augmentorConsultationPage.getState();
  });
  assert.equal(previewState.selection.previewRegionId, "brain-context");
  assert.equal(previewState.selection.pinnedRegionId, null);
  assert.equal(previewState.selection.activeRegionId, "brain-context");
  assert.ok(previewState.selectionEpoch > 0);

  const focused = await page.evaluate(async () => {
    const result = await window.augmentorConsultationPage.ask("Explain the selected work path", {
      focus: { kind: "anatomy-region", id: "work-spine", provenance: "ignored-by-page" },
      viewIds: ["runtime"]
    });
    return {
      result,
      state: window.augmentorConsultationPage.getState(),
      lastStart: window.__agentApiEvents.lastStart,
      raw: document.querySelector("[data-testid=agent-api-raw]").textContent
    };
  });
  const focusedRequest = observedRequests.at(-1).query;
  assert.equal(focusedRequest.schemaVersion, "augmentor.consultation.query@1.2.0");
  assert.equal(Object.hasOwn(focusedRequest.query, "kind"), false);
  assert.deepEqual(focusedRequest.focus, { kind: "anatomy-region", id: "work-spine" });
  assert.equal(Object.hasOwn(focusedRequest.focus, "provenance"), false);
  assert.equal(focused.result.consultation.schemaVersion, "augmentor.consultation.result@1.2.0");
  assert.equal(focused.result.consultation.resolvedFocus.id, "work-spine");
  assert.equal(focused.state.selection.pinnedRegionId, "work-spine");
  assert.equal(focused.state.requestedFocus.id, "work-spine");
  assert.equal(focused.state.presentationScope, "region-scoped");
  assert.equal(focused.lastStart.focus.id, "work-spine");
  assert.equal(focused.lastStart.state, "loading");
  assert.doesNotMatch(JSON.stringify(focused.state), /Explain the selected work path|mappingDigest|mappingVersion/i);
  assert.doesNotMatch(focused.raw, /mappingDigest|mappingVersion|Explain the selected work path/i);

  await assert.rejects(
    page.evaluate(() => window.augmentorConsultationPage.selectRegion("not-on-this-page")),
    /Choose a region shown on this Augmentor page/
  );

  await page.evaluate(() => window.augmentorConsultationPage.ask("General request while a region remains pinned"));
  const generalAfterFocus = observedRequests.at(-1).query;
  assert.equal(generalAfterFocus.schemaVersion, "augmentor.consultation.query@1.1.0");
  assert.equal(Object.hasOwn(generalAfterFocus, "focus"), false);
  assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getState().selection.pinnedRegionId), "work-spine");
  assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getState().presentationScope), "general-not-region-scoped");

  const cancellation = await page.evaluate(async () => {
    const first = window.augmentorConsultationPage.ask("slow question").catch((error) => error.name);
    const second = window.augmentorConsultationPage.ask("Please answer directly", { viewIds: ["runtime"] });
    return { first: await first, second: (await second).answerPolicy.action };
  });
  assert.equal(cancellation.first, "AbortError");
  assert.equal(cancellation.second, "answer");
  assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getState().answerAction), "answer");
  assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getExplanationSupport().profile), "brief");

  const selectionCancellation = await page.evaluate(async () => {
    const pending = window.augmentorConsultationPage.ask("slow focused selection", {
      focus: { kind: "anatomy-region", id: "work-spine" },
      viewIds: ["runtime"]
    }).catch((error) => error.name);
    await new Promise((resolve) => setTimeout(resolve, 20));
    window.augmentorConsultationPage.selectRegion("brain-source");
    return { outcome: await pending, state: window.augmentorConsultationPage.getState() };
  });
  assert.equal(selectionCancellation.outcome, "AbortError");
  assert.equal(selectionCancellation.state.state, "idle");
  assert.equal(selectionCancellation.state.selection.pinnedRegionId, "brain-source");
  assert.equal(selectionCancellation.state.errorCode, null);

  const explicitCancellation = await page.evaluate(async () => {
    const pending = window.augmentorConsultationPage.ask("slow explicit cancel", {
      focus: { kind: "anatomy-region", id: "work-spine" },
      viewIds: ["runtime"]
    }).catch((error) => error.name);
    await new Promise((resolve) => setTimeout(resolve, 20));
    const cancelled = window.augmentorConsultationPage.cancel();
    return { cancelled, outcome: await pending, state: window.augmentorConsultationPage.getState() };
  });
  assert.equal(explicitCancellation.cancelled, true);
  assert.equal(explicitCancellation.outcome, "AbortError");
  assert.equal(explicitCancellation.state.state, "idle");
  assert.equal(explicitCancellation.state.selection.pinnedRegionId, "work-spine");
  assert.equal(explicitCancellation.state.errorCode, null);

  const assertPageError = async (question, expectedCode, messagePattern, options = {}) => {
    await assert.rejects(
      page.evaluate(({ question: value, options: askOptions }) => window.augmentorConsultationPage.ask(value, askOptions), { question, options }),
      messagePattern
    );
    assert.equal(await page.evaluate(() => window.augmentorConsultationPage.getState().errorCode), expectedCode);
    assert.equal(await page.getByTestId("agent-api-page").getAttribute("data-consultation-state"), "error");
  };

  await assertPageError("network failure", "disconnected", /could not be reached/i);
  await assertPageError("redirect response", "protocol-error", /redirected/i);
  await assertPageError("expired session", "authentication-required", /expired/i);
  await assertPageError("forbidden request", "access-denied", /not allowed/i);
  await assertPageError("route unavailable", "disconnected-route-unavailable", /not connected/i);
  await assertPageError("server failure", "service-error", /HTTP 500/i);
  await assertPageError("html success", "protocol-error", /content type/i);
  await assertPageError("malformed json", "protocol-error", /unreadable JSON/i);
  await assertPageError("schema invalid", "protocol-error", /does not understand/i);
  await assertPageError("forged focus", "protocol-error", /selected region/i, {
    focus: { kind: "anatomy-region", id: "work-spine" },
    viewIds: ["runtime"]
  });
  await assertPageError("privacy leak", "protocol-error", /must not expose/i, {
    focus: { kind: "anatomy-region", id: "work-spine" },
    viewIds: ["runtime"]
  });
  assert.equal(await page.getByTestId("agent-api-raw").textContent(), "No usable response.");

  const events = await page.evaluate(() => window.__agentApiEvents);
  assert.ok(events.starts >= 18);
  assert.ok(events.completes >= 7);
  assert.ok(events.errors >= 11);
  assert.ok(events.cancels >= 3);
  assert.equal(events.last.answerAction, "answer");
  assert.equal(events.lastError.errorCode, "protocol-error");
  assert.doesNotMatch(JSON.stringify(events), /General request while|slow focused|mappingDigest|mappingVersion|principal-private-user/i);

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
  await page.screenshot({ path: "/tmp/augmentor-agent-api-mobile.png", fullPage: true });
  assert.ok(consoleErrors.every((message) => /Failed to load resource|401|403|405|500|ERR_EMPTY_RESPONSE/i.test(message)), consoleErrors.join("\n"));
  assert.doesNotMatch(consoleErrors.join("\n"), /principal-private-user|mappingDigest|\/home\//i);
  assert.deepEqual(pageErrors, []);
  process.stdout.write(`AGENT_API_BROWSER=pass requests=${observedRequests.length} screenshots=/tmp/augmentor-agent-api.png,/tmp/augmentor-agent-api-mobile.png\n`);
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
