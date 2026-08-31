import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const playwrightRoot = process.env.WORKSPACE_PLAYWRIGHT_ROOT
  ?? "/home/vrondelli/.nvm/versions/node/v22.12.0/lib/node_modules/playwright";
const chromiumExecutable = process.env.WORKSPACE_CHROMIUM_EXECUTABLE
  ?? "/home/vrondelli/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome";
const baseUrl = process.env.WORKSPACE_BASE_URL ?? "http://127.0.0.1:4187";
const outputRoot = process.env.WORKSPACE_BROWSER_OUTPUT ?? "/tmp/cyberalchemy-workspace-browser-acceptance";
const { chromium } = require(playwrightRoot);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const browser = await chromium.launch({ headless: true, executablePath: chromiumExecutable });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
const consoleErrors = [];
const pageErrors = [];
const requests = [];
const httpErrors = [];
page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
page.on("pageerror", (error) => pageErrors.push(error.message));
page.on("request", (request) => requests.push(request.url()));
page.on("response", (response) => { if (response.status() >= 400) httpErrors.push(`${response.status()} ${response.url()}`); });

await page.goto(baseUrl, { waitUntil: "networkidle" });
assert(await page.getByRole("heading", { name: /Understand the system/ }).isVisible(), "Workspace heading missing");
for (const collection of ["Definitions", "Products", "Projects", "Ontologies"]) {
  assert(await page.getByRole("button", { name: new RegExp(collection) }).isVisible(), `${collection} navigation missing`);
}
assert(await page.getByText("Projection, not authority.").isVisible(), "claim ceiling missing");

await page.getByRole("button", { name: /Definitions/ }).click();
const search = page.getByLabel("Search Definitions");
await search.fill("construction invariant");
const definitionRecord = page.locator(".record-list button").filter({ hasText: "DomainSpec-Governed Construction Invariant" });
assert(await definitionRecord.count() === 1, "D65 search result missing or ambiguous");
await definitionRecord.click();
assert(await page.locator(".record-detail .record-id", { hasText: "CAV2-D65" }).isVisible(), "definition identity missing");
assert(await page.getByText("Claim ceiling", { exact: true }).isVisible(), "claim detail missing");
assert(await page.getByText("Provenance", { exact: true }).isVisible(), "provenance detail missing");

await page.getByRole("button", { name: /Ontologies/ }).click();
const blockedOntology = page.locator(".record-list button").filter({ hasText: "cav2.durable-storage.business" });
assert(await blockedOntology.count() === 1, "blocked Durable Storage ontology is not visible");
await blockedOntology.click();
assert(await page.locator(".record-detail .status", { hasText: "registered-blocked" }).isVisible(), "blocked ontology status is hidden");
assert(await page.getByText(/Catalog visibility and currentness do not imply ontology acceptance/).isVisible(), "ontology authority boundary missing");

await page.getByRole("button", { name: /Projects/ }).click();
const essaysRecord = page.locator(".record-list button").filter({ hasText: "Essays" });
assert(await essaysRecord.count() === 1, "Essays Project entry missing or ambiguous");
await essaysRecord.click();
await page.getByRole("link", { name: /Open project Essays/ }).click();
assert(page.url().endsWith("#/projects/CA2-PROJECT-ESSAYS"), "Essays Project route did not open");
assert(await page.getByText("Project surface").isVisible(), "Project surface marker missing");
assert(await page.getByText("This is a navigation surface, not an invocation.").isVisible(), "Project authority boundary missing");
assert(await page.getByText("Essays Project owner", { exact: true }).isVisible(), "Essays ownership was not preserved");

const forbiddenControl = page.getByRole("button", { name: /create|update|delete|accept|register|publish|edit ontology/i });
assert(await forbiddenControl.count() === 0, "mutating control exposed");
await page.evaluate(() => {
  if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
});
await page.keyboard.press("Tab");
const focusStyle = await page.locator(":focus").evaluate((element) => {
  const style = getComputedStyle(element);
  return { outlineStyle: style.outlineStyle, outlineWidth: style.outlineWidth };
});
assert(focusStyle.outlineStyle !== "none" && focusStyle.outlineWidth !== "0px", "keyboard focus is not visible");

await page.screenshot({ path: `${outputRoot}-desktop.png`, fullPage: true });
await page.setViewportSize({ width: 390, height: 844 });
await page.screenshot({ path: `${outputRoot}-mobile.png`, fullPage: true });
const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
assert(overflow <= 1, `narrow layout has ${overflow}px horizontal overflow`);

const nonLocalRequests = requests.filter((url) => !url.startsWith(baseUrl));
assert(nonLocalRequests.length === 0, `unexpected non-local requests: ${nonLocalRequests.join(", ")}`);
assert(pageErrors.length === 0, `page errors: ${pageErrors.join(" | ")}`);
assert(consoleErrors.length === 0, `console errors: ${consoleErrors.join(" | ")}`);
assert(httpErrors.length === 0, `HTTP errors: ${httpErrors.join(" | ")}`);

console.log(JSON.stringify({
  status: "PASS",
  url: baseUrl,
  playwrightVersion: require(`${playwrightRoot}/package.json`).version,
  checks: {
    fourTypedCollections: "PASS",
    searchAndDefinitionDetail: "PASS",
    provenanceAndClaimCeiling: "PASS",
    blockedOntologyVisibility: "PASS",
    essaysProjectNavigation: "PASS",
    ownershipBoundary: "PASS",
    noMutatingControls: "PASS",
    keyboardFocus: "PASS",
    narrowViewportNoOverflow: "PASS",
    noNonLocalRequests: "PASS",
    consoleAndPageErrors: "PASS"
  },
  screenshots: [`${outputRoot}-desktop.png`, `${outputRoot}-mobile.png`],
}, null, 2));

await browser.close();
