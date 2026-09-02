import { createHash } from "node:crypto";
import { mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const WORKSPACE_ID = "local-essay-workspace";
const PROPOSAL_A_TEXT = "# Persisted proposal A\n\nA proposal staged, saved, and accepted through the real Tauri ledger.";
const PROPOSAL_A_REQUEST_ID = "wdio-record-proposal-a";
const PROPOSAL_A_ID = "wdio-proposal-a";
const PROPOSAL_B_TEXT = "# Persisted proposal B\n\nA second proposal staged and saved before an external ledger rejection.";
const PROPOSAL_B_REQUEST_ID = "wdio-record-proposal-b";
const PROPOSAL_B_ID = "wdio-proposal-b";
const PROPOSAL_B_REJECT_REQUEST_ID = "wdio-reject-proposal-b";
const FIXED_DEADLINE_UNIX_MS = 4_102_444_800_000;
const ARTIFACT_DIRECTORY = process.env.WORKSPACE_WDIO_OUTPUT ?? "/tmp/cav2-workspace-tauri-smoke";

function screenshotDigest(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

async function invokeInWebView(command, args) {
  return browser.tauri.execute(
    async ({ core }, commandName, commandArgs) => {
      if (typeof core?.invoke !== "function") throw new Error("TAURI_INVOKE_UNAVAILABLE");
      return core.invoke(commandName, commandArgs);
    },
    command,
    args,
  );
}

function proposalCommand({ requestId, proposalId, sourceRevision, text }) {
  const operationId = `wdio-proposal-${proposalId}`;
  const command = {
    command: "record-proposal",
    request_id: requestId,
    workspace_id: WORKSPACE_ID,
    proposal_id: proposalId,
    source_revision: sourceRevision,
    context: {
      context_id: `wdio-context-${proposalId}`,
      purpose: operationId,
      provenance: ["wdio:real-tauri-slice-3"],
      sufficiency: "sufficient",
      authority_ceiling: "proposal-only",
      inferred: false,
      confidence_basis_points: null,
      conflicts: [],
      correction_ref: null,
      rejected: false,
    },
    operation_id: operationId,
    target_artifact: "essay.md",
    target_region: "body",
    text,
    rationale: "Exercise the proposal-to-writer-save handoff.",
    uncertainty: "Candidate smoke evidence only.",
    validation_diagnostics: ["wdio-real-ipc"],
    deadline_unix_ms: FIXED_DEADLINE_UNIX_MS,
  };
  if (command.context.purpose !== command.operation_id) {
    throw new Error("WDIO_PROPOSAL_PURPOSE_OPERATION_MISMATCH");
  }
  return command;
}

function rejectProposalBCommand() {
  return {
    command: "reject-proposal",
    request_id: PROPOSAL_B_REJECT_REQUEST_ID,
    workspace_id: WORKSPACE_ID,
    proposal_id: PROPOSAL_B_ID,
    expected_revision: 1,
    reason: "Deterministic WDIO terminal-conflict fixture.",
    deadline_unix_ms: FIXED_DEADLINE_UNIX_MS,
  };
}

async function openProjectOwnedEssays() {
  const explore = await $('button[aria-label="Explore workspace"]');
  await explore.waitForClickable();
  await explore.click();
  await expect($('//*[normalize-space()="Explore the system."]')).toBeDisplayed();

  const essaysRecord = await $('//*[contains(@class,"record-list")]//button[contains(.,"CA2-PROJECT-ESSAYS")]');
  await essaysRecord.waitForClickable();
  await essaysRecord.click();
  const openOwned = await $("button*=Open owned capability");
  await openOwned.waitForClickable();
  await openOwned.click();
  await expect($(".ownership-strip")).toHaveText(expect.stringContaining("Essays-owned action plane"));
}

async function createPreparedStudio() {
  const setupHeading = await $('//*[normalize-space()="Begin with intent, not a blank page."]');
  if (await setupHeading.isExisting()) {
    const createStudio = await $("button=Create local studio");
    await createStudio.waitForClickable();
    await createStudio.click();
  }
  await expect($('//*[normalize-space()="Ontology as a Product Practice"]')).toBeDisplayed();

  const acceptIntent = await $("button=Accept intent");
  if (await acceptIntent.isExisting()) {
    await acceptIntent.waitForClickable();
    await acceptIntent.click();
  }
  const generatePlan = await $("button=Generate & accept local plan");
  if (await generatePlan.isExisting()) {
    await generatePlan.waitForClickable();
    await generatePlan.click();
  }
  await expect($('//*[normalize-space()="Composition plan"]')).toBeDisplayed();
  await expect($("[data-testid=milkdown-editor]")).toBeDisplayed();
}

async function resetScrollToTop() {
  await browser.execute(() => window.scrollTo(0, 0));
  await browser.waitUntil(
    async () => await browser.execute(() => window.scrollY) === 0,
    { timeout: 5_000, timeoutMsg: "WebView did not reset to the top surface" },
  );
}

async function lifecycleRailGeometry() {
  return browser.execute(() => {
    const stageRail = document.querySelector(".stage-rail");
    const appRail = document.querySelector(".app-rail");
    if (!stageRail || !appRail) throw new Error("MOBILE_LIFECYCLE_GEOMETRY_UNAVAILABLE");
    const rect = (element) => {
      const bounds = element.getBoundingClientRect();
      return { left: bounds.left, right: bounds.right, top: bounds.top, bottom: bounds.bottom };
    };
    const items = Array.from(stageRail.querySelectorAll(":scope > li"));
    const labels = items.map((item) => item.querySelector(":scope > span:last-child"));
    if (labels.some((label) => !label)) throw new Error("MOBILE_LIFECYCLE_LABEL_UNAVAILABLE");
    return {
      clientWidth: stageRail.clientWidth,
      scrollWidth: stageRail.scrollWidth,
      rail: rect(stageRail),
      items: items.map(rect),
      labels: labels.map((label) => rect(label)),
      viewportWidth: window.innerWidth,
      appRailTop: appRail.getBoundingClientRect().top,
    };
  });
}

function expectLifecycleRailGeometry(geometry) {
  expect(geometry.items).toHaveLength(5);
  expect(geometry.labels).toHaveLength(5);
  expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.clientWidth + 1);
  for (const bounds of [...geometry.items, ...geometry.labels]) {
    expect(bounds.left).toBeGreaterThanOrEqual(geometry.rail.left - 1);
    expect(bounds.right).toBeLessThanOrEqual(geometry.rail.right + 1);
    expect(bounds.left).toBeGreaterThanOrEqual(-1);
    expect(bounds.right).toBeLessThanOrEqual(geometry.viewportWidth + 1);
  }
  expect(geometry.rail.bottom).toBeLessThanOrEqual(geometry.appRailTop + 1);
}

async function essaysDesktopGeometry() {
  return browser.execute(() => {
    const plane = document.querySelector(".essays-owned-plane");
    const dock = document.querySelector(".agent-dock");
    if (!plane || !dock) throw new Error("DESKTOP_ESSAYS_GEOMETRY_UNAVAILABLE");
    const findExact = (selector, text) => Array.from(document.querySelectorAll(selector))
      .find((element) => element.textContent?.trim() === text);
    const targets = [
      ["review panel", document.querySelector(".review-panel")],
      ["Editorial review heading", document.querySelector("#review-heading")],
      ["Open editorial review button", findExact("button", "Open editorial review")],
      ["Residue & export heading", document.querySelector("#residue-heading")],
      ["Validate current revision button", findExact("button", "Validate current revision")],
      ["Export reviewable package button", findExact("button", "Export reviewable package")],
    ];
    if (targets.some(([, element]) => !element)) throw new Error("DESKTOP_ESSAYS_TARGET_UNAVAILABLE");
    const rect = (element) => {
      const bounds = element.getBoundingClientRect();
      return { left: bounds.left, right: bounds.right, top: bounds.top, bottom: bounds.bottom };
    };
    return {
      plane: rect(plane),
      dock: rect(dock),
      planeClientWidth: plane.clientWidth,
      planeScrollWidth: plane.scrollWidth,
      documentClientWidth: document.documentElement.clientWidth,
      documentScrollWidth: document.documentElement.scrollWidth,
      targets: targets.map(([name, element]) => ({ name, contained: plane.contains(element), bounds: rect(element) })),
    };
  });
}

function expectEssaysDesktopGeometry(geometry) {
  expect(geometry.plane.right).toBeLessThanOrEqual(geometry.dock.left + 1);
  expect(geometry.planeScrollWidth).toBeLessThanOrEqual(geometry.planeClientWidth + 1);
  expect(geometry.documentScrollWidth).toBeLessThanOrEqual(geometry.documentClientWidth + 1);
  expect(geometry.targets).toHaveLength(6);
  for (const target of geometry.targets) {
    expect(target.contained).toBe(true);
    expect(target.bounds.left).toBeGreaterThanOrEqual(geometry.plane.left - 1);
    expect(target.bounds.right).toBeLessThanOrEqual(geometry.plane.right + 1);
    expect(target.bounds.top).toBeGreaterThanOrEqual(geometry.plane.top - 1);
    expect(target.bounds.bottom).toBeLessThanOrEqual(geometry.plane.bottom + 1);
    expect(target.bounds.right).toBeLessThanOrEqual(geometry.dock.left + 1);
  }
}

async function inspectOntology(screenshots) {
  const ontologyRail = await $('button[aria-label="Open Ontology"]');
  await ontologyRail.waitForClickable();
  await ontologyRail.click();
  await expect($('//*[normalize-space()="Follow meaning through its relations."]')).toBeDisplayed();

  const portal = await $('button[aria-label="Focus Essays, Project Entry, proposed"]');
  await portal.waitForClickable();
  await portal.click();
  await expect($("[data-testid=portal-scope]")).toHaveText(expect.stringContaining("Essays"));

  const coordination = await $('button*=coordination');
  await coordination.waitForClickable();
  await coordination.click();
  await expect($("[data-testid=portal-scope]")).toHaveText(expect.stringContaining("Choose a node as a portal."));

  const coordinatesEdge = await $('.react-flow__edge[data-id="WORKSPACE-REL-004"]');
  await coordinatesEdge.waitForDisplayed();
  await expect($(".relation-label[data-relation-type=coordinates]")).toBeDisplayed();

  const survivingEndpoint = await $('.react-flow__node[data-id="CA2-PROJECT-CYBERALCHEMY-WORKSPACE"]');
  await survivingEndpoint.waitForClickable();
  await survivingEndpoint.click();

  const inspect = await $("button=Inspect record & relations");
  await inspect.waitForClickable();
  await inspect.click();
  await expect($("[role=dialog]")).toBeDisplayed();
  await expect($("[aria-label='Textual relationship view']")).toBeDisplayed();

  const path = join(ARTIFACT_DIRECTORY, "ontology-dialog-1280x820.png");
  await browser.saveScreenshot(path);
  screenshots.push({ path, sha256: screenshotDigest(path) });
  const close = await $('button[aria-label="Close ontology detail"]');
  await close.waitForClickable();
  await close.click();
  await $("[role=dialog]").waitForExist({ reverse: true });
}

describe("unified Workspace and Essays Slice 3 through real Tauri IPC", () => {
  it("stages, writer-saves, accepts, and preserves terminal residue across relaunch", async () => {
    mkdirSync(ARTIFACT_DIRECTORY, { recursive: true });
    await browser.setWindowSize(1280, 820);
    await browser.execute(() => {
      window.localStorage.clear();
      window.location.hash = "#/collections/projects";
    });

    await openProjectOwnedEssays();
    await createPreparedStudio();

    const attachLedger = await $("button=Attach ledger");
    await attachLedger.waitForClickable();
    await attachLedger.click();
    await expect($("aside.agent-dock")).toHaveText(expect.stringContaining("Local agent ledger created and attached."));

    const principal = await invokeInWebView("principal_evidence", {});
    expect(principal).toMatchObject({ clientId: "essays-tauri", evidenceKind: "local-process", verifiedHumanIdentity: false });
    expect(principal.principalSubject).toMatch(/^unix:\d+$/);

    const proposalACommand = proposalCommand({ requestId: PROPOSAL_A_REQUEST_ID, proposalId: PROPOSAL_A_ID, sourceRevision: 0, text: PROPOSAL_A_TEXT });
    const proposalReceipt = await invokeInWebView("execute", { command: proposalACommand });
    expect(proposalReceipt).toMatchObject({ request_id: PROPOSAL_A_REQUEST_ID, workspace_id: WORKSPACE_ID, outcome: "accepted", replayed: false, linked_proposal_id: PROPOSAL_A_ID });

    await $("button=Refresh").click();
    const proposalCard = await $("article.agent-proposal");
    await proposalCard.waitForDisplayed();
    await expect(proposalCard).toHaveText(expect.stringContaining(PROPOSAL_A_TEXT));

    const acceptSaved = await $("button=Accept saved draft in ledger");
    expect(await acceptSaved.isEnabled()).toBe(false);
    await $("button=Stage in editor").click();
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("staged-unsaved"));
    expect(await acceptSaved.isEnabled()).toBe(false);

    const saveDraft = await $("button=Save accepted draft");
    await saveDraft.waitForClickable();
    await saveDraft.click();
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("saved-exact"));
    await acceptSaved.waitForEnabled();
    await acceptSaved.click();

    const acceptedText = await $("section.accepted-text");
    await expect(acceptedText).toHaveText(expect.stringContaining("r1"));
    await expect(acceptedText).toHaveText(expect.stringContaining(PROPOSAL_A_TEXT));
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("accepted"));

    const beforeRelaunch = await invokeInWebView("snapshot", { workspaceId: WORKSPACE_ID, cursor: null });
    expect(beforeRelaunch.workspace.accepted_revision).toBe(1);
    expect(beforeRelaunch.workspace.accepted_text).toBe(PROPOSAL_A_TEXT);

    const proposalBCommand = proposalCommand({ requestId: PROPOSAL_B_REQUEST_ID, proposalId: PROPOSAL_B_ID, sourceRevision: 1, text: PROPOSAL_B_TEXT });
    const proposalBReceipt = await invokeInWebView("execute", { command: proposalBCommand });
    expect(proposalBReceipt).toMatchObject({ request_id: PROPOSAL_B_REQUEST_ID, workspace_id: WORKSPACE_ID, outcome: "accepted", replayed: false, linked_proposal_id: PROPOSAL_B_ID });
    await $("button=Refresh").click();
    const proposalBCard = await $(`//article[contains(@class,"agent-proposal")][contains(.,"${PROPOSAL_B_ID}")]`);
    await proposalBCard.waitForDisplayed();
    await proposalBCard.$("button=Stage in editor").click();
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("staged-unsaved"));
    await $("button=Save accepted draft").click();
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("saved-exact"));

    const proposalBRejectReceipt = await invokeInWebView("execute", { command: rejectProposalBCommand() });
    expect(proposalBRejectReceipt).toMatchObject({ request_id: PROPOSAL_B_REJECT_REQUEST_ID, workspace_id: WORKSPACE_ID, outcome: "rejected", replayed: false, linked_proposal_id: PROPOSAL_B_ID });
    const staleUiAccept = await proposalBCard.$("button=Accept saved draft in ledger");
    await staleUiAccept.waitForEnabled();
    await staleUiAccept.click();
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("terminal-conflict"));
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("Acceptance targets exact saved Essays workspace"));

    const conflictSnapshot = await invokeInWebView("snapshot", { workspaceId: WORKSPACE_ID, cursor: null });
    expect(conflictSnapshot.workspace.accepted_revision).toBe(1);
    expect(conflictSnapshot.workspace.accepted_text).toBe(PROPOSAL_A_TEXT);
    expect(conflictSnapshot.proposals.find((proposal) => proposal.proposal_id === PROPOSAL_B_ID)?.status).toBe("rejected");
    const terminalCursor = conflictSnapshot.event_cursor;

    const screenshots = [];
    const essaysPath = join(ARTIFACT_DIRECTORY, "essays-accepted-1280x820.png");
    await browser.saveScreenshot(essaysPath);
    screenshots.push({ path: essaysPath, sha256: screenshotDigest(essaysPath) });

    await resetScrollToTop();
    await expect($(".ownership-strip")).toBeDisplayed();
    await expect($(".essays-root .topbar")).toBeDisplayed();
    await expect($(".stage-rail")).toBeDisplayed();
    await expect($("[data-testid=milkdown-editor]")).toBeDisplayed();
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("terminal-conflict"));
    const desktopEssaysGeometry = await essaysDesktopGeometry();
    expectEssaysDesktopGeometry(desktopEssaysGeometry);
    const essaysTopPath = join(ARTIFACT_DIRECTORY, "essays-top-reset-1280x820.png");
    await browser.saveScreenshot(essaysTopPath);
    screenshots.push({ path: essaysTopPath, sha256: screenshotDigest(essaysTopPath) });

    await inspectOntology(screenshots);

    await browser.reloadSession();
    await browser.setWindowSize(1280, 820);
    const essaysRail = await $('button[aria-label="Open Essays"]');
    await essaysRail.waitForClickable();
    await essaysRail.click();
    await expect($('//*[normalize-space()="Ontology as a Product Practice"]')).toBeDisplayed();
    await $("button=Refresh").click();

    const afterRelaunch = await invokeInWebView("snapshot", { workspaceId: WORKSPACE_ID, cursor: null });
    expect(afterRelaunch.workspace.accepted_revision).toBe(1);
    expect(afterRelaunch.workspace.accepted_text).toBe(PROPOSAL_A_TEXT);
    expect(afterRelaunch.event_cursor).toBe(terminalCursor);
    await expect($("[aria-label='Persisted proposal handoff']")).toHaveText(expect.stringContaining("terminal-conflict"));

    const replayReceipt = await invokeInWebView("execute", { command: proposalACommand });
    expect(replayReceipt.replayed).toBe(true);
    const afterReplay = await invokeInWebView("snapshot", { workspaceId: WORKSPACE_ID, cursor: null });
    expect(afterReplay.event_cursor).toBe(terminalCursor);
    expect(afterReplay.proposals.filter((proposal) => proposal.proposal_id === PROPOSAL_A_ID)).toHaveLength(1);

    const requestedOuterViewport = { width: 390, height: 844 };
    await browser.setWindowSize(requestedOuterViewport.width, requestedOuterViewport.height);
    await resetScrollToTop();
    const measuredInnerViewport = await browser.execute(() => ({ width: window.innerWidth, height: window.innerHeight }));
    expect(measuredInnerViewport.width).toBeGreaterThan(0);
    expect(measuredInnerViewport.height).toBeGreaterThan(0);
    const mobileLifecycleGeometry = await lifecycleRailGeometry();
    expectLifecycleRailGeometry(mobileLifecycleGeometry);
    const essaysMobilePath = join(ARTIFACT_DIRECTORY, "essays-mobile-top-390x844.png");
    await browser.saveScreenshot(essaysMobilePath);
    screenshots.push({ path: essaysMobilePath, sha256: screenshotDigest(essaysMobilePath) });

    process.stdout.write(`${JSON.stringify({
      status: "CANDIDATE_SCREENSHOTS_CAPTURED",
      viewport: { width: 1280, height: 820 },
      requestedOuterViewport,
      measuredInnerViewport,
      desktopEssaysGeometry,
      mobileLifecycleGeometry,
      fixture: "fresh-browser-local-and-temporary-sqlite",
      webview: "actual-tauri-embedded-provider",
      screenshots,
      aestheticAssessment: "not-evaluated",
      authorityEffect: "none",
    })}\n`);
  });
});
