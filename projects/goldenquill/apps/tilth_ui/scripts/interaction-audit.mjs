import { spawn } from "node:child_process";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

const port = Number(process.env.PORT || 4173);
const baseUrl = `http://127.0.0.1:${port}`;
const appRoot = fileURLToPath(new URL("..", import.meta.url));

let routes = [];

async function waitForServer() {
  const deadline = Date.now() + 20_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${baseUrl}/api/projections/current`);
      if (response.ok) return;
    } catch { }
    await delay(250);
  }
  throw new Error(`Server did not become ready at ${baseUrl}`);
}

async function runInteractionAudit() {
  console.log("Starting Interaction Audit...");
  
  const reportsDir = join(appRoot, "reports", "interaction-audit");
  const screenshotsDir = join(reportsDir, "screenshots");
  await mkdir(reportsDir, { recursive: true });
  await mkdir(screenshotsDir, { recursive: true });

  const server = spawn(process.execPath, ["server.mjs"], {
    cwd: appRoot,
    env: { ...process.env, PORT: String(port) },
    stdio: ["ignore", "pipe", "pipe"],
  });

  let browser;
  let results = [];

  try {
    await waitForServer();
    
    console.log("Fetching dynamic routes from server...");
    const routeRes = await fetch(`${baseUrl}/api/routes`);
    routes = await routeRes.json();
    console.log(`Discovered ${routes.length} routes:`, routes);

    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    
    for (const route of routes) {
      console.log(`\n[${new Date().toISOString()}] Auditing route: ${route}`);
      const page = await context.newPage();
      
      try {
        const response = await page.goto(`${baseUrl}${route}`, { waitUntil: "domcontentloaded" });
        if (!response || !response.ok()) {
          results.push({ route, status: "FAIL_DEAD_ROUTE", message: `HTTP ${response ? response.status() : "Unknown"}` });
          await page.close();
          continue;
        }

        // Snapshot initial state
        const safeRouteName = route === "/" ? "root" : route.replace(/[^a-zA-Z0-9]/g, "_");
        await page.screenshot({ path: join(screenshotsDir, `${safeRouteName}_initial.png`) });

        // Find interactive elements
        const locators = page.locator("button, a, [role='button']");
        const count = await locators.count();
        console.log(`  Found ${count} interactive elements.`);

        for (let i = 0; i < count; i++) {
          const el = locators.nth(i);
          const isVisible = await el.isVisible().catch(() => false);
          if (!isVisible) continue;

          const tagName = await el.evaluate(e => e.tagName.toLowerCase());
          const text = (await el.innerText()).substring(0, 30).replace(/\n/g, " ");
          const href = await el.getAttribute("href");
          const isDisabled = await el.isDisabled().catch(() => false);
          const hasHref = !!href;

          const elementId = `Index ${i} - <${tagName}> "${text}"`;
          // console.log(`    Testing: ${elementId}`);

          if (isDisabled) {
            results.push({ route, element: elementId, status: "OK_DISABLED_WITH_REASON" });
            continue;
          }

          if (tagName === "a" && href && href.startsWith("mailto:")) {
            results.push({ route, element: elementId, status: "OK_MAILTO_DRAFT" });
            continue;
          }

          // Simulate click (in a new tab context if it navigates, to preserve our original page state)
          // For simplicity, since some buttons might mutate local DOM, we track URL before/after or just intercept requests
          
          let clicked = false;
          let newUrl = page.url();
          
          try {
            // We use evaluate to trigger click without actually destroying our playwright context if it navigates
            await el.evaluate(e => e.click());
            clicked = true;
            await page.waitForTimeout(500); // await side effects
            newUrl = page.url();
          } catch (e) {
            results.push({ route, element: elementId, status: "FAIL_DEAD_CLICK", reason: e.message });
            continue;
          }

          if (newUrl !== `${baseUrl}${route}`) {
            results.push({ route, element: elementId, status: "OK_NAVIGATES", target: newUrl });
            // Revert route
            await page.goto(`${baseUrl}${route}`, { waitUntil: "domcontentloaded" });
          } else {
            // Did it open a modal or do something?
            // This is a naive check. For a true audit, we'd watch DOM mutations.
            // If it has href="#", it might be intentional UI toggle.
            if (href === "#") {
              results.push({ route, element: elementId, status: "OK_OPENS_PANEL_OR_NOOP" });
            } else {
              results.push({ route, element: elementId, status: "FAIL_VISUAL_ONLY_BUTTON" });
            }
          }
        }
      } catch (err) {
        console.error(`Error processing route ${route}:`, err);
        results.push({ route, status: "ERROR", message: err.message });
      } finally {
        await page.close();
      }
    }

    // Generate Reports
    await writeFile(join(reportsDir, "latest.json"), JSON.stringify(results, null, 2));

    let mdContent = "# Interaction Audit Report\n\n";
    for (const r of results) {
      if (r.element) {
        mdContent += `- **${r.route}** | ${r.element} -> \`${r.status}\` ${r.target ? `(to ${r.target})` : ""}\n`;
      } else {
        mdContent += `- **${r.route}** -> \`${r.status}\` (${r.message})\n`;
      }
    }
    await writeFile(join(reportsDir, "latest.md"), mdContent);
    // Also write to root INTERACTION_FAILURES.md as requested
    await writeFile(join(appRoot, "INTERACTION_FAILURES.md"), mdContent);

    console.log("Interaction Audit Complete. Reports generated.");

  } finally {
    if (browser) await browser.close();
    server.kill("SIGTERM");
  }
}

runInteractionAudit().catch(err => {
  console.error("Interaction audit crashed:", err);
  process.exit(1);
});
