#!/usr/bin/env node
import {createHash} from "node:crypto";
import {createReadStream} from "node:fs";
import {writeFile} from "node:fs/promises";
import {createRequire} from "node:module";

const [url, outputPath] = process.argv.slice(2);
if (!url || !outputPath) throw new Error("usage: run-browser-acceptance.mjs <url> <output>");

const require = createRequire(import.meta.url);
const {chromium} = require("/home/vrondelli/.nvm/versions/node/v22.12.0/lib/node_modules/playwright");
const executablePath = chromium.executablePath();
const executableHash = createHash("sha256");
for await (const chunk of createReadStream(executablePath)) executableHash.update(chunk);

const browser = await chromium.launch({headless: true});
const page = await browser.newPage();
const consoleErrors = [];
const consoleWarnings = [];
const pageErrors = [];
const requests = [];
page.on("console", (message) => {
  if (message.type() === "error") consoleErrors.push(message.text());
  if (message.type() === "warning") consoleWarnings.push(message.text());
});
page.on("pageerror", (error) => pageErrors.push(String(error)));
page.on("request", (request) => requests.push(request.url()));

await page.goto(url, {waitUntil: "networkidle"});
await page.waitForFunction(() => window.__intentRouteWitness?.case_count === 6);
const witness = await page.evaluate(() => window.__intentRouteWitness);
const renderedStatus = await page.locator("#status").textContent();
const externalRequests = requests.filter((requestUrl) =>
  !requestUrl.startsWith("http://127.0.0.1:4179/") && !requestUrl.startsWith("data:")
);
const report = {
  schema: "intent-route.generated-browser-acceptance@1",
  status: witness.status === "pass" && witness.case_count === 6 && witness.passed === 6 &&
    consoleErrors.length === 0 && consoleWarnings.length === 0 && pageErrors.length === 0 &&
    externalRequests.length === 0 ? "pass" : "fail",
  url,
  browser: {
    name: "chromium",
    version: browser.version(),
    executable_path: executablePath,
    executable_sha256: executableHash.digest("hex")
  },
  witness,
  rendered_status: renderedStatus,
  console_errors: consoleErrors,
  console_warnings: consoleWarnings,
  page_errors: pageErrors,
  request_count: requests.length,
  external_requests: externalRequests,
  authority_effect: "none",
  claim_ceiling: "generated Codex wrapper browser portability in this recorded Chromium binary only"
};
await browser.close();
await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
process.stdout.write(`${JSON.stringify({schema: report.schema, status: report.status, cases: witness.case_count, passed: witness.passed, external_requests: externalRequests.length})}\n`);
if (report.status !== "pass") process.exitCode = 1;
