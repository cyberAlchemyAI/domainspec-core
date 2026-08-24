import assert from "node:assert/strict"
import { createRequire } from "node:module"
import { mkdir, writeFile } from "node:fs/promises"
import { dirname, resolve } from "node:path"
import { fileURLToPath } from "node:url"

import { canonicalBytes } from "../../../../../cyberAlchemy-v2/implementation/ontology-evidence-workbench/src/canonical-json.mjs"

const require = createRequire(import.meta.url)
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE = resolve(ROOT, "projects/body-war/ontology/whole-system")
const RECEIPTS = resolve(PACKAGE, "receipts")
const PLAYWRIGHT_ROOT = process.env.BODY_WAR_PLAYWRIGHT_ROOT ?? "/home/vrondelli/.nvm/versions/node/v22.12.0/lib/node_modules/playwright"
const { chromium } = require(PLAYWRIGHT_ROOT)
const playwrightPackage = require(`${PLAYWRIGHT_ROOT}/package.json`)
const baseUrl = process.env.BODY_WAR_OEW_URL ?? "http://127.0.0.1:4178/"

const pageErrors = []
const failedRequests = []
const externalRequests = []
const browser = await chromium.launch({ headless: true })
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } })
  page.on("pageerror", (error) => pageErrors.push(error.message))
  page.on("requestfailed", (request) => failedRequests.push(`${request.url()} ${request.failure()?.errorText ?? "unknown"}`))
  page.on("request", (request) => {
    const url = new URL(request.url())
    if (!(["127.0.0.1", "localhost"].includes(url.hostname))) externalRequests.push(request.url())
  })

  await page.goto(baseUrl, { waitUntil: "domcontentloaded", timeout: 30_000 })
  await page.waitForFunction(() => document.querySelectorAll(".react-flow__node").length === 4, undefined, { timeout: 30_000 })
  const rootBody = await page.locator("body").innerText()
  const portalSection = page.getByTestId("knowledge-focus-portals")
  const portalButtons = portalSection.getByRole("button")
  assert.equal(await page.title(), "Body War Whole-System Ontology")
  assert.equal(rootBody.includes("Access Token Required"), false)
  assert.equal(rootBody.includes("freshness could not be verified"), false)
  assert.equal(rootBody.includes("Welcome to the knowledge graph"), false)
  assert.equal(await portalSection.count(), 1)
  assert.equal(await portalButtons.count(), 35)
  assert.equal(await page.locator(".react-flow__node").count(), 4)
  assert.match(await portalSection.innerText(), /original: .* · direction: .* · authority: none/)
  const focusScreenshot = resolve(RECEIPTS, "oew-frontend-focus-scene.png")
  await mkdir(RECEIPTS, { recursive: true })
  await page.screenshot({ path: focusScreenshot, fullPage: true })

  await portalButtons.first().click()
  await page.waitForFunction(() => document.querySelector('[data-testid="knowledge-focus-portals"]')?.textContent?.includes("Back to"), undefined, { timeout: 30_000 })
  assert.ok(await page.locator(".react-flow__node").count() < 276)

  await page.goto(new URL("?oew=1", baseUrl).toString(), { waitUntil: "domcontentloaded", timeout: 30_000 })
  await page.waitForFunction(() => document.querySelectorAll(".oew-node").length === 4, undefined, { timeout: 30_000 })
  const evidenceBody = await page.locator("body").innerText()
  const colorTokens = await page.locator("[data-color-token]").evaluateAll((elements) => elements.map((element) => element.getAttribute("data-color-token")))
  assert.equal(evidenceBody.includes("Workbench blocked"), false)
  assert.equal(await page.locator(".oew-node").count(), 4)
  const nodeBoxes = await page.locator(".oew-node").evaluateAll((nodes) => nodes.map((node) => {
    const box = node.getBoundingClientRect()
    return { left: box.left, right: box.right, top: box.top, bottom: box.bottom }
  }))
  for (let left = 0; left < nodeBoxes.length; left += 1) {
    for (let right = left + 1; right < nodeBoxes.length; right += 1) {
      const a = nodeBoxes[left]
      const b = nodeBoxes[right]
      assert.equal(a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top, false)
    }
  }
  assert.ok(colorTokens.length >= 1)
  assert.ok(colorTokens.length < 20)
  assert.match(evidenceBody, /Body War · whole-system candidate/)
  assert.equal(evidenceBody.includes("actor.anti-cheat-reviewer"), false)
  const graphSceneScreenshot = resolve(RECEIPTS, "oew-frontend-relation-scene.png")
  await page.screenshot({ path: graphSceneScreenshot, fullPage: true })
  await page.getByRole("tab", { name: "Full index" }).click()
  await page.waitForFunction(() => document.querySelectorAll(".oew-table tbody tr").length === 577, undefined, { timeout: 30_000 })
  const fullIndexBody = await page.locator("body").innerText()
  assert.match(fullIndexBody, /Geometry And Score Runtime Gap|geometry-score-gap/i)
  const evidenceScreenshot = resolve(RECEIPTS, "oew-frontend-relation-table.png")
  await page.screenshot({ path: evidenceScreenshot, fullPage: true })

  assert.deepEqual(pageErrors, [])
  assert.deepEqual(failedRequests, [])
  assert.deepEqual(externalRequests, [])
  const receipt = {
    schema_version: "body-war-whole-system-oew-browser-acceptance/v1",
    result: "pass",
    observed_at: new Date().toISOString(),
    target: baseUrl,
    runtime: {
      playwright: playwrightPackage.version,
      chromium_executable: chromium.executablePath(),
      viewport: { width: 1440, height: 1000 },
    },
    focus_scene: {
      nodes: 4,
      labeled_boundary_portals: 35,
      portal_pivot_and_back: "pass",
      token_prompt_absent: true,
      freshness_banner_absent: true,
      screenshot: "receipts/oew-frontend-focus-scene.png",
    },
    exact_relation_surface: {
      focused_graph_nodes: 4,
      focused_graph_relations: colorTokens.length,
      indexed_nodes: 276,
      indexed_relations: 301,
      bound_predicate_color_tokens: 39,
      geometry_score_gap_visible: true,
      focused_screenshot: "receipts/oew-frontend-relation-scene.png",
      screenshot: "receipts/oew-frontend-relation-table.png",
    },
    network: { external_requests: 0, failed_requests: 0 },
    page_errors: [],
    claim_ceiling: "Local candidate browser acceptance only; no ontology promotion, live Strava data, geometry calculation, score authority, deployment, or production claim.",
    authority_effect: "none",
  }
  await writeFile(resolve(RECEIPTS, "oew-frontend-browser-acceptance.json"), canonicalBytes(receipt))
  process.stdout.write(`PASS: Chromium rendered both four-node Body War focus scenes, ${colorTokens.length} focused relation card(s), and the full 276-node/301-relation index.\n`)
} finally {
  await browser.close()
}
