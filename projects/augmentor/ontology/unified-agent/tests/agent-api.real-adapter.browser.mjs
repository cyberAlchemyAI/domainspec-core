import assert from "node:assert/strict";
import { cp, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import http from "node:http";
import { createRequire } from "node:module";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const playwrightModuleRoot = process.argv[2];
const resonantWorkspaceRoot = process.argv[3];
if (!playwrightModuleRoot) throw new Error("Pass the absolute global Playwright module path as argument 1.");
if (!resonantWorkspaceRoot) throw new Error("Pass the absolute ResonantOS 2.0.0-alpha checkout path as argument 2.");

const require = createRequire(import.meta.url);
const { chromium } = require(playwrightModuleRoot);
const testDirectory = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.resolve(testDirectory, "../ontology-visualization.html");
const consumerRoot = path.resolve(testDirectory, "../development/consultation-api/generated/consumer");
const adapterModulePath = path.join(
  path.resolve(resonantWorkspaceRoot),
  "browser-first/host/run-augmentor-consultation-deployment.mjs"
);
const {
  DEPLOYMENT_PRINCIPAL_HEADER,
  startAugmentorConsultationDeploymentServer,
} = await import(pathToFileURL(adapterModulePath).href);

const TRUSTED_PRINCIPAL = "augmentor";
const CONSULTATION_ACCESS_HEADER = "x-resonantos-consultation-key";
const html = await readFile(htmlPath);
const proxyObservations = [];

const listenLoopback = (server) => new Promise((resolve, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", () => {
    server.off("error", reject);
    resolve();
  });
});

const closeServer = async (server) => {
  if (!server?.listening) return;
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
};

const readBody = async (request) => {
  const chunks = [];
  for await (const chunk of request) chunks.push(chunk);
  return Buffer.concat(chunks);
};

const identityHeaders = (headers) => ({
  authorization: headers.authorization ?? null,
  consultationKey: headers[CONSULTATION_ACCESS_HEADER] ?? null,
  principal: headers[DEPLOYMENT_PRINCIPAL_HEADER] ?? null,
});

const forwardedIdentity = Object.freeze({
  authorization: null,
  consultationKey: null,
  principal: TRUSTED_PRINCIPAL,
});

function writeJson(response, status, payload) {
  const body = Buffer.from(JSON.stringify(payload));
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": body.length,
    "Cache-Control": "private, no-store",
    "X-Content-Type-Options": "nosniff",
  });
  response.end(body);
}

function createSameOriginProxy(adapterEndpoint) {
  return http.createServer(async (request, response) => {
    const pathname = new URL(request.url ?? "/", "http://augmentor.local").pathname;
    if (request.method === "GET" && ["/augmentor", "/augmentor/"].includes(pathname)) {
      response.writeHead(200, {
        "Content-Type": "text/html; charset=utf-8",
        "Content-Length": html.length,
        "Cache-Control": "no-store",
      });
      response.end(html);
      return;
    }
    if (request.method !== "POST" || pathname !== "/augmentor/consultation") {
      writeJson(response, 404, { ok: false, error: "Not found." });
      return;
    }
    try {
      const body = await readBody(request);
      const inboundIdentity = identityHeaders(request.headers);
      proxyObservations.push({
        inboundIdentity,
        forwardedIdentity: { ...forwardedIdentity },
        query: JSON.parse(body.toString("utf8")),
      });
      // This test-only proxy deliberately forwards neither caller credentials nor a caller principal.
      const upstream = await fetch(`${adapterEndpoint}/augmentor/consultation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          [DEPLOYMENT_PRINCIPAL_HEADER]: TRUSTED_PRINCIPAL,
        },
        body,
      });
      const upstreamBody = Buffer.from(await upstream.arrayBuffer());
      response.writeHead(upstream.status, {
        "Content-Type": upstream.headers.get("content-type") ?? "application/json; charset=utf-8",
        "Content-Length": upstreamBody.length,
        "Cache-Control": "private, no-store",
        "X-Content-Type-Options": "nosniff",
      });
      response.end(upstreamBody);
    } catch (error) {
      writeJson(response, 502, { ok: false, error: "Test proxy could not reach the local consultation adapter." });
    }
  });
}

const temporaryRoot = await mkdtemp(path.join(os.tmpdir(), "augmentor-real-adapter-"));
const screenshots = {
  general: path.join(os.tmpdir(), "augmentor-agent-api-real-adapter-general.png"),
  focused: path.join(os.tmpdir(), "augmentor-agent-api-real-adapter-work-spine.png"),
};
let adapterServer;
let proxyServer;
let browser;

try {
  adapterServer = await startAugmentorConsultationDeploymentServer({
    projectionRoot: consumerRoot,
    trustedPrincipal: TRUSTED_PRINCIPAL,
    port: 0,
  });
  assert.equal(adapterServer.address().address, "127.0.0.1");
  const adapterEndpoint = `http://127.0.0.1:${adapterServer.address().port}`;

  proxyServer = createSameOriginProxy(adapterEndpoint);
  await listenLoopback(proxyServer);
  assert.equal(proxyServer.address().address, "127.0.0.1");
  const proxyEndpoint = `http://127.0.0.1:${proxyServer.address().port}`;

  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.emulateMedia({ reducedMotion: "reduce" });
  const consoleErrors = [];
  const pageErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(error.message));

  await page.goto(`${proxyEndpoint}/augmentor/#agent-api`, { waitUntil: "load" });
  assert.equal(await page.getByTestId("agent-api-page").isVisible(), true);

  await page.getByTestId("agent-api-question").fill("What is a saved conversation?");
  await page.getByTestId("agent-api-submit").click();
  await page.waitForFunction(() => document.querySelector("#agent-api-page")?.dataset.consultationState === "complete");
  const generalState = await page.evaluate(() => window.augmentorConsultationPage.getState());
  assert.equal(generalState.state, "complete");
  assert.ok(generalState.result?.statementCount > 0, "general consultation must return usable evidence");
  assert.ok(["answer", "qualify"].includes(generalState.answerAction));
  assert.ok(await page.getByTestId("agent-api-evidence").locator(".evidence-item").count() > 0);
  await page.screenshot({ path: screenshots.general, fullPage: true });

  assert.equal(proxyObservations.length, 1);
  const generalRequest = proxyObservations[0];
  assert.equal(generalRequest.query.schemaVersion, "augmentor.consultation.query@1.1.0");
  assert.equal(Object.hasOwn(generalRequest.query.query, "kind"), false);
  assert.equal(Object.hasOwn(generalRequest.query, "focus"), false);
  assert.deepEqual(generalRequest.inboundIdentity, {
    authorization: null,
    consultationKey: null,
    principal: null,
  });
  assert.deepEqual(generalRequest.forwardedIdentity, forwardedIdentity);

  const directWithoutPrincipal = await fetch(`${adapterEndpoint}/augmentor/consultation`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
  });
  assert.equal(directWithoutPrincipal.status, 401);

  const hostileProxyRequest = await fetch(`${proxyEndpoint}/augmentor/consultation`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer caller-supplied-value",
      "X-ResonantOS-Consultation-Key": "caller-supplied-key",
      "X-ResonantOS-Consultation-Principal": "caller-supplied-principal",
    },
    body: JSON.stringify(generalRequest.query),
  });
  assert.equal(hostileProxyRequest.status, 200);
  assert.equal((await hostileProxyRequest.json()).ok, true);
  const hostileObservation = proxyObservations.at(-1);
  assert.deepEqual(hostileObservation.inboundIdentity, {
    authorization: "Bearer caller-supplied-value",
    consultationKey: "caller-supplied-key",
    principal: "caller-supplied-principal",
  });
  assert.deepEqual(hostileObservation.forwardedIdentity, forwardedIdentity);

  const workCore = page.getByTestId("robot-core-work-spine");
  await workCore.click();
  assert.equal(await workCore.getAttribute("aria-expanded"), "true");
  assert.equal(await page.locator("#robot-card-heading").textContent(), "Approved work");
  assert.match(
    await page.locator("#robot-card-boundary").textContent(),
    /A plan, approved work instructions, a running task, and its completion check are different things\./
  );
  assert.equal(await page.getByTestId("robot-consultation-card").getAttribute("data-mode"), "pinned");
  await page.getByTestId("robot-card-question").fill(
    "How do a work plan, approval, one running task, and the final completion check fit together?"
  );
  await page.getByTestId("robot-card-submit").click();
  await page.waitForFunction(() => document.querySelector("#agent-api-page")?.dataset.consultationState === "complete");
  const focusedResponse = JSON.parse(await page.getByTestId("agent-api-raw").textContent());
  assert.equal(focusedResponse.consultation.schemaVersion, "augmentor.consultation.result@1.2.0");
  assert.equal(focusedResponse.consultation.resolvedFocus.id, "work-spine");
  assert.ok(await page.getByTestId("robot-card-answer").textContent());
  await page.screenshot({ path: screenshots.focused, fullPage: true });

  const focusedRequest = proxyObservations.at(-1).query;
  assert.equal(focusedRequest.schemaVersion, "augmentor.consultation.query@1.2.0");
  assert.equal(Object.hasOwn(focusedRequest.query, "kind"), false);
  assert.deepEqual(focusedRequest.focus, { kind: "anatomy-region", id: "work-spine" });

  const mismatchedBundleRoot = path.join(temporaryRoot, "manifest-map-mismatch");
  await cp(consumerRoot, mismatchedBundleRoot, { recursive: true });
  const manifestPath = path.join(mismatchedBundleRoot, "projection-manifest.json");
  const mismatchedManifest = JSON.parse(await readFile(manifestPath, "utf8"));
  mismatchedManifest.anatomyFocusMapDigest = "0".repeat(64);
  await writeFile(manifestPath, `${JSON.stringify(mismatchedManifest, null, 2)}\n`);
  const mismatchedServer = await startAugmentorConsultationDeploymentServer({
    projectionRoot: mismatchedBundleRoot,
    trustedPrincipal: TRUSTED_PRINCIPAL,
    port: 0,
  });
  try {
    const rejectedBundle = await fetch(
      `http://127.0.0.1:${mismatchedServer.address().port}/augmentor/consultation`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          [DEPLOYMENT_PRINCIPAL_HEADER]: TRUSTED_PRINCIPAL,
        },
        body: JSON.stringify(focusedRequest),
      }
    );
    assert.equal(rejectedBundle.status, 200);
    const rejectedPayload = await rejectedBundle.json();
    assert.equal(rejectedPayload.ok, true);
    assert.equal(rejectedPayload.consultation.status, "temporary_failure");
    assert.equal(rejectedPayload.consultation.reasonCode, "DEPENDENCY_UNAVAILABLE");
    assert.equal(rejectedPayload.answerPolicy.action, "abstain");
    assert.equal(rejectedPayload.answerPolicy.mayUseEvidence, false);
  } finally {
    await closeServer(mismatchedServer);
  }

  assert.deepEqual(consoleErrors, [], consoleErrors.join("\n"));
  assert.deepEqual(pageErrors, [], pageErrors.join("\n"));
  process.stdout.write(
    `AGENT_API_REAL_ADAPTER_BROWSER=pass general=usable focus=work-spine proxyRequests=${proxyObservations.length} screenshots=${screenshots.general},${screenshots.focused}\n`
  );
} finally {
  await browser?.close();
  await closeServer(proxyServer);
  await closeServer(adapterServer);
  await rm(temporaryRoot, { recursive: true, force: true });
}
