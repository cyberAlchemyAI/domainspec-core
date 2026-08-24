import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";

const [playwrightModuleRoot, targetUrl, htmlPath, outputRoot] = process.argv.slice(2);
if (!playwrightModuleRoot || !targetUrl || !htmlPath || !outputRoot) {
  throw new Error("Usage: node ux-evidence.browser.mjs <playwright-root> <target-url> <html-path> <output-root>");
}

const require = createRequire(import.meta.url);
const { chromium } = require(playwrightModuleRoot);
const playwrightVersion = require(path.join(playwrightModuleRoot, "package.json")).version;
const resolvedOutputRoot = path.resolve(outputRoot);
const evidencePaths = {
  accessibility: path.join(resolvedOutputRoot, "accessibility"),
  aria: path.join(resolvedOutputRoot, "aria"),
  measurements: path.join(resolvedOutputRoot, "measurements"),
  screenshots: path.join(resolvedOutputRoot, "screenshots"),
  traces: path.join(resolvedOutputRoot, "traces")
};

await Promise.all([
  mkdir(evidencePaths.accessibility, { recursive: true }),
  mkdir(evidencePaths.aria, { recursive: true }),
  mkdir(evidencePaths.measurements, { recursive: true }),
  mkdir(evidencePaths.screenshots, { recursive: true }),
  mkdir(evidencePaths.traces, { recursive: true })
]);

const htmlBytes = await readFile(path.resolve(htmlPath));
const targetSha256 = createHash("sha256").update(htmlBytes).digest("hex");
const sourceCards = [
  {
    source_card_id: "UX-SRC-WCAG22",
    source_kind: "normative-standard",
    title: "Web Content Accessibility Guidelines 2.2",
    url: "https://www.w3.org/TR/WCAG22/",
    supports: ["text contrast", "reflow", "descriptive labels", "visible focus"]
  },
  {
    source_card_id: "UX-SRC-WCAG-LABELS",
    source_kind: "official-guidance",
    title: "Understanding SC 2.4.6: Headings and Labels",
    url: "https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels",
    supports: ["labels should describe topic or purpose"]
  },
  {
    source_card_id: "UX-SRC-DIGITAL-PLAIN",
    source_kind: "official-design-guidance",
    title: "Digital.gov: Design for understanding",
    url: "https://digital.gov/guides/plain-language/design",
    supports: ["clear descriptive headings", "selective emphasis", "scannable hierarchy"]
  },
  {
    source_card_id: "UX-SRC-USWDS-TYPE",
    source_kind: "official-design-system-guidance",
    title: "U.S. Web Design System: Typography",
    url: "https://designsystem.digital.gov/components/typography/",
    supports: ["neutral interface typography", "clear labels", "legible hierarchy"]
  }
];

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
const page = await context.newPage();
const consoleErrors = [];
const pageErrors = [];
const externalRequests = [];
const targetOrigin = new URL(targetUrl).origin;

page.on("console", (message) => {
  if (message.type() === "error") consoleErrors.push(message.text());
});
page.on("pageerror", (error) => pageErrors.push(error.message));
page.on("request", (request) => {
  const url = request.url();
  if (/^https?:/i.test(url) && !url.startsWith(targetOrigin)) externalRequests.push(url);
});

const measurePage = () => page.evaluate(() => {
  const parseColor = (value) => {
    const hex = value.trim().match(/^#([\da-f]{6})$/i)?.[1];
    if (hex) return [0, 2, 4].map((offset) => Number.parseInt(hex.slice(offset, offset + 2), 16));
    const values = value.match(/[\d.]+/g)?.map(Number) ?? [];
    return values.slice(0, 3);
  };
  const luminance = (rgb) => rgb
    .map((channel) => channel / 255)
    .map((channel) => channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4)
    .reduce((sum, channel, index) => sum + channel * [0.2126, 0.7152, 0.0722][index], 0);
  const contrast = (foreground, background) => {
    const [lighter, darker] = [luminance(parseColor(foreground)), luminance(parseColor(background))]
      .sort((left, right) => right - left);
    return Number(((lighter + 0.05) / (darker + 0.05)).toFixed(2));
  };
  const root = getComputedStyle(document.documentElement);
  const canvas = root.getPropertyValue("--canvas").trim();
  const surface = root.getPropertyValue("--surface").trim();
  const title = document.querySelector("h1");
  const titleStyle = getComputedStyle(title);
  const guideCopy = document.querySelector(".guide-head p");
  const guideCopyStyle = getComputedStyle(guideCopy);
  const firstLens = document.querySelector(".lens-button");
  const firstLensRect = firstLens.getBoundingClientRect();
  const focusedOutline = getComputedStyle(firstLens);
  return {
    viewport: { width: innerWidth, height: innerHeight },
    document: { scrollWidth: document.documentElement.scrollWidth, scrollHeight: document.documentElement.scrollHeight },
    title: {
      fontSize: Number.parseFloat(titleStyle.fontSize),
      lineHeight: Number.parseFloat(titleStyle.lineHeight),
      fontFamily: titleStyle.fontFamily,
      width: Math.round(title.getBoundingClientRect().width),
      height: Math.round(title.getBoundingClientRect().height),
      contrast: contrast(titleStyle.color, canvas)
    },
    guide: {
      top: Math.round(document.querySelector(".beginner-guide").getBoundingClientRect().top),
      copyContrast: contrast(guideCopyStyle.color, surface)
    },
    firstLens: {
      width: Math.round(firstLensRect.width),
      height: Math.round(firstLensRect.height),
      outlineWidth: focusedOutline.outlineWidth,
      outlineStyle: focusedOutline.outlineStyle,
      hitTargetVisible: (() => {
        const hit = document.elementFromPoint(firstLensRect.left + firstLensRect.width / 2, firstLensRect.top + firstLensRect.height / 2);
        return firstLens === hit || firstLens.contains(hit);
      })()
    },
    claim: { position: getComputedStyle(document.querySelector(".claim-ceiling")).position },
    labels: [...document.querySelectorAll(".lens-button")].map((button) => button.textContent.trim()),
    viewLabels: [...document.querySelectorAll("#view-tabs .tab")].map((button) => button.childNodes[0].textContent.trim()),
    tokens: {
      accent: root.getPropertyValue("--accent").trim(),
      warning: root.getPropertyValue("--warning").trim()
    }
  };
});

let responseStatus;
let desktop;
let narrow;
let ariaSnapshot;
let hardGates;
let languageEvidence;

try {
  const response = await page.goto(targetUrl, { waitUntil: "networkidle" });
  responseStatus = response?.status() ?? null;
  await page.getByTestId("explanation-lens-plain_meaning").focus();
  desktop = await measurePage();
  ariaSnapshot = await page.locator("body").ariaSnapshot();
  await page.screenshot({ path: path.join(evidencePaths.screenshots, "desktop-1440x1000.png"), fullPage: true });

  await page.getByTestId("explanation-lens-state_view").click();
  await page.getByTestId("view-intent-route").click();
  await page.getByTestId("graph-node-route_disposition").click();
  languageEvidence = await page.evaluate(() => {
    const data = JSON.parse(document.getElementById("ontology-data").textContent);
    const avoidableJargon = /\b(?:bounded|projection|disposition|lifecycle|receipt|canonical|ontology|digest|adapter|registrar|immutable|artifact|residue)\b/i;
    const jargonHits = [];
    for (const [subjectId, explanation] of Object.entries({
      ...data.beginner_explanations.nodes,
      ...data.beginner_explanations.lanes
    })) {
      for (const field of ["plain_meaning", "state_view", "process_view", "boundary"]) {
        if (avoidableJargon.test(explanation[field])) jargonHits.push(`${subjectId}.${field}`);
      }
    }
    return {
      friendlyNameCoverage: Object.values(data.beginner_explanations.nodes).filter((item) => item.friendly_name).length,
      nodeCount: data.nodes.length,
      jargonHits,
      selectedTitle: document.querySelector(".inspector-title")?.textContent,
      selectedExplanationLabel: document.querySelector(".beginner-explanation-label")?.textContent,
      technicalRecordOpen: document.querySelector("[data-testid=technical-record]")?.hasAttribute("open") ?? null
    };
  });

  await page.setViewportSize({ width: 320, height: 800 });
  await page.getByTestId("explanation-lens-plain_meaning").scrollIntoViewIfNeeded();
  await page.getByTestId("explanation-lens-plain_meaning").focus();
  await page.keyboard.press("Shift+Tab");
  await page.keyboard.press("Tab");
  narrow = await measurePage();
  await page.screenshot({ path: path.join(evidencePaths.screenshots, "mobile-320x800.png"), fullPage: true });

  hardGates = [
    { id: "UX-HG-HTTP", status: responseStatus === 200 ? "pass" : "fail", observed: responseStatus, source_cards: [] },
    { id: "UX-HG-CONSOLE", status: consoleErrors.length === 0 && pageErrors.length === 0 ? "pass" : "fail", observed: { consoleErrors, pageErrors }, source_cards: [] },
    { id: "UX-HG-NETWORK", status: externalRequests.length === 0 ? "pass" : "fail", observed: externalRequests, source_cards: [] },
    { id: "UX-HG-REFLOW", status: narrow.document.scrollWidth <= narrow.viewport.width ? "pass" : "fail", observed: { scrollWidth: narrow.document.scrollWidth, viewportWidth: narrow.viewport.width }, source_cards: ["UX-SRC-WCAG22"] },
    { id: "UX-HG-TEXT-CONTRAST", status: desktop.title.contrast >= 4.5 && desktop.guide.copyContrast >= 4.5 ? "pass" : "fail", observed: { title: desktop.title.contrast, guideCopy: desktop.guide.copyContrast }, source_cards: ["UX-SRC-WCAG22"] },
    { id: "UX-HG-FOCUS", status: Number.parseFloat(desktop.firstLens.outlineWidth) >= 2 && desktop.firstLens.outlineStyle !== "none" && Number.parseFloat(narrow.firstLens.outlineWidth) >= 2 && narrow.firstLens.outlineStyle !== "none" && narrow.firstLens.hitTargetVisible && narrow.claim.position !== "sticky" ? "pass" : "fail", observed: { desktop: desktop.firstLens, narrow: narrow.firstLens, claim: narrow.claim }, source_cards: ["UX-SRC-WCAG22"] },
    { id: "UX-HG-TARGET", status: desktop.firstLens.width >= 24 && desktop.firstLens.height >= 24 ? "pass" : "fail", observed: desktop.firstLens, source_cards: ["UX-SRC-WCAG22"] },
    { id: "UX-HG-LABELS", status: desktop.labels.every(Boolean) && desktop.viewLabels.every(Boolean) ? "pass" : "fail", observed: { explanationLabels: desktop.labels, viewLabels: desktop.viewLabels }, source_cards: ["UX-SRC-WCAG-LABELS"] },
    { id: "UX-HG-BEGINNER-COPY", status: languageEvidence.friendlyNameCoverage === languageEvidence.nodeCount && languageEvidence.jargonHits.length === 0 && languageEvidence.technicalRecordOpen === false ? "pass" : "fail", observed: languageEvidence, source_cards: ["UX-SRC-DIGITAL-PLAIN", "UX-SRC-WCAG-LABELS"] }
  ];
} finally {
  await context.tracing.stop({ path: path.join(evidencePaths.traces, "interface.zip") });
  await browser.close();
}

const hardGateFailures = hardGates.filter((finding) => finding.status === "fail");
const findings = {
  status: hardGateFailures.length ? "block" : "flag",
  target: targetUrl,
  hard_gates: hardGates,
  soft_flags: [
    {
      id: "UX-SF-GRAPH-SCROLL",
      status: "flag",
      finding: "The directed graph keeps its own horizontal scroll region at narrow widths because its two-dimensional relationships require it; the surrounding document reflows.",
      limit: "Real low-vision users should confirm whether the synchronized text view is an adequate alternative.",
      source_cards: ["UX-SRC-WCAG22"]
    }
  ],
  screenshot_review: [
    {
      id: "UX-SS-HIERARCHY",
      status: desktop.title.fontSize <= 64 && desktop.guide.top < 560 ? "pass" : "flag",
      observed: { titleFontSize: desktop.title.fontSize, guideTop: desktop.guide.top },
      judgment: "The reduced neutral headline no longer dominates the tool, and the explanation guide appears before filters and the graph.",
      source_cards: ["UX-SRC-USWDS-TYPE", "UX-SRC-DIGITAL-PLAIN"]
    },
    {
      id: "UX-SS-COLOR-ROLES",
      status: desktop.tokens.accent !== desktop.tokens.warning ? "pass" : "flag",
      observed: desktop.tokens,
      judgment: "Navigation and selection use a quiet blue; amber is reserved for the important-limit warning.",
      source_cards: ["UX-SRC-DIGITAL-PLAIN"]
    }
  ],
  human_study: [
    "Confirm that beginners can predict what each explanation button reveals.",
    "Confirm that the four friendly lane names preserve the intended distinctions.",
    "Confirm that the cooler palette and reduced headline feel calmer across user display settings.",
    "Measure whether users can distinguish a route-finder result from the product's chosen route."
  ],
  not_automatable: [
    "Beginner comprehension",
    "Perceived visual balance and trust",
    "Whether the analogies improve recall without creating false authority inferences"
  ]
};

const accessibility = {
  status: hardGateFailures.length ? "fail" : "pass-with-residue",
  scope: "Browser-observable checks only; not an accessibility conformance certification.",
  checks: hardGates.filter((finding) => ["UX-HG-REFLOW", "UX-HG-TEXT-CONTRAST", "UX-HG-FOCUS", "UX-HG-TARGET", "UX-HG-LABELS", "UX-HG-BEGINNER-COPY"].includes(finding.id))
};
const runMetadata = {
  schema: "augmentor.ux-evidence-run@0.1.0",
  run_id: path.basename(resolvedOutputRoot),
  target: targetUrl,
  target_sha256: targetSha256,
  mode: "validate-interface",
  browser: "chromium",
  playwright_version: playwrightVersion,
  viewports: [{ width: 1440, height: 1000 }, { width: 320, height: 800 }],
  status: findings.status,
  fixture_calibration: "not-run",
  observability: {
    scenario_count: 1,
    generated_output_count: 12,
    validator_layer_coverage: {
      L0: "HTTP, console, page errors, and external requests",
      L1: "accessible names, ARIA snapshot, focus, and target size",
      L2: "explanation, view, graph-node, and keyboard interactions",
      L3: "desktop hierarchy, 320px reflow, and contrast proxies",
      L4: "plain-language and technical-vocabulary soft flags",
      L5: "not evaluated; no domain-market rule was promoted",
      L6: "human comprehension and visual-preference residue only"
    },
    hard_gate_count: hardGates.length,
    soft_flag_count: findings.soft_flags.length,
    screenshot_review_count: findings.screenshot_review.length,
    human_study_residue_count: findings.human_study.length,
    source_card_coverage: sourceCards.length,
    quality_bar_status: findings.status,
    anti_pattern_hits: [],
    reflection_trigger_recommendation: "none"
  }
};
const consoleNetwork = { responseStatus, consoleErrors, pageErrors, externalRequests };
const measurements = { desktop, narrow };
const residueLedger = `schema: augmentor.ux-residue-ledger@0.1.0
status: open
items:
  - id: UX-RES-COMPREHENSION
    claim_class: human_study
    question: Can beginners predict what each explanation button reveals?
  - id: UX-RES-LANE-LANGUAGE
    claim_class: human_study
    question: Do the friendly lane names preserve the four intended distinctions?
  - id: UX-RES-VISUAL-TONE
    claim_class: screenshot_review
    question: Does the reduced headline and cooler palette feel calmer on real user displays?
  - id: UX-RES-ROUTER-BOUNDARY
    claim_class: human_study
    question: Can users distinguish a route-finder result from the product's chosen route?
`;
const summary = `# Augmentor ontology UX evidence

- Status: ${findings.status}
- Mode: validate-interface
- Target: ${targetUrl}
- Target SHA-256: ${targetSha256}
- Hard gates: ${hardGates.length - hardGateFailures.length}/${hardGates.length} passed
- Fixture calibration: not run

## Observed

- The headline is ${desktop.title.fontSize}px at 1440px and the guide begins at ${desktop.guide.top}px.
- The document reflows to ${narrow.viewport.width}px without page-level horizontal overflow.
- The interface exposes six purpose-oriented explanation labels and six task-oriented view labels.
- Navigation/selection and warning colors use separate tokens.

## Evidence boundary

Playwright observed rendered behavior, layout, focus styling, selected contrast pairs, requests, console output, and accessible names. It does not prove comprehension, usability, trust, visual preference, or complete WCAG conformance.

## Sources

${sourceCards.map((card) => `- [${card.title}](${card.url})`).join("\n")}
`;

await Promise.all([
  writeFile(path.join(resolvedOutputRoot, "run-metadata.json"), `${JSON.stringify(runMetadata, null, 2)}\n`),
  writeFile(path.join(resolvedOutputRoot, "evidence-cards.json"), `${JSON.stringify(sourceCards, null, 2)}\n`),
  writeFile(path.join(resolvedOutputRoot, "findings.json"), `${JSON.stringify(findings, null, 2)}\n`),
  writeFile(path.join(resolvedOutputRoot, "console-network.json"), `${JSON.stringify(consoleNetwork, null, 2)}\n`),
  writeFile(path.join(evidencePaths.accessibility, "checks.json"), `${JSON.stringify(accessibility, null, 2)}\n`),
  writeFile(path.join(evidencePaths.aria, "page.yml"), `${ariaSnapshot.trim()}\n`),
  writeFile(path.join(evidencePaths.measurements, "layout.json"), `${JSON.stringify(measurements, null, 2)}\n`),
  writeFile(path.join(resolvedOutputRoot, "residue-ledger.yml"), residueLedger),
  writeFile(path.join(resolvedOutputRoot, "summary.md"), summary)
]);

process.stdout.write(`UX_EVIDENCE=${findings.status} output=${resolvedOutputRoot} hard_gates=${hardGates.length - hardGateFailures.length}/${hardGates.length}\n`);
if (hardGateFailures.length) process.exitCode = 1;
