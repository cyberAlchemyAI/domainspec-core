import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const DEFAULT_STAGING_DIR = fileURLToPath(new URL("../../../../pipeline/funder_intelligence/_staging/gold/", import.meta.url));

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];

    if (quoted) {
      if (char === '"' && next === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
      continue;
    }

    if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else if (char !== "\r") {
      field += char;
    }
  }

  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }

  const headers = rows.shift() || [];
  return rows
    .filter((items) => items.some((item) => String(item || "").trim()))
    .map((items) => Object.fromEntries(headers.map((header, i) => [header, items[i] ?? ""])));
}

async function readCsv(stagingDir, name) {
  return parseCsv(await readFile(`${stagingDir}/${name}`, "utf8"));
}

async function readManifest(stagingDir) {
  try {
    return JSON.parse(await readFile(`${stagingDir}/manifest.json`, "utf8"));
  } catch {
    return [];
  }
}

function parseMoneyToken(token) {
  const cleaned = String(token || "").replace(/[$,\s]/g, "").toLowerCase();
  const match = cleaned.match(/(\d+(?:\.\d+)?)(k|m)?/);
  if (!match) return null;
  const base = Number(match[1]);
  if (!Number.isFinite(base)) return null;
  const multiplier = match[2] === "m" ? 1_000_000 : match[2] === "k" ? 1_000 : 1;
  return Math.round(base * multiplier);
}

export function estimateAwardValue(awardRange) {
  const text = String(awardRange || "");
  const tokens = text.match(/\$?\d[\d,]*(?:\.\d+)?\s*[kKmM]?/g) || [];
  const values = tokens.map(parseMoneyToken).filter((value) => Number.isFinite(value));
  if (!values.length) {
    return {
      amount: 0,
      value_basis: "No defensible award amount in staging row.",
    };
  }
  const amount = Math.max(...values);
  return {
    amount,
    value_basis: `Source award-range value parsed from "${text}". This is an opportunity size signal, not guaranteed funding.`,
  };
}

function compactText(...parts) {
  return parts
    .map((part) => String(part || "").trim())
    .filter(Boolean)
    .join(" / ");
}

function rowHasDiscoverySignal(program) {
  return Boolean(
    program.program_name ||
    program.normalized_program_name ||
    program.award_range ||
    program.deadline ||
    program.apply_url ||
    program.topics
  );
}

function verificationStateFor({ program, funder, brokenUrl, liveVerification }) {
  if (liveVerification?.source_url && liveVerification?.fetched_at && liveVerification?.content_hash) {
    return liveVerification.fit_state === "VERIFIED_FIT" ? "VERIFIED_FIT" : "LIVE_SOURCE_VERIFIED";
  }
  if (brokenUrl) return "VERIFICATION_FAILED";
  if (program.apply_url || funder.primary_url) return "UNVERIFIED";
  return "SOURCE_URL_NEEDED";
}

function sourceBackingTierFor({ program, funder, brokenUrl, liveVerification }) {
  if (liveVerification?.fit_state === "VERIFIED_FIT" && liveVerification?.source_url && liveVerification?.content_hash) {
    return "VERIFIED_FIT";
  }
  if (brokenUrl) return "BROKEN_URL_REVIEW";
  if (program.award_range || program.deadline || program.provenance_edges || funder.provenance_edges) {
    return "STAGING_SOURCE_QUALIFIED";
  }
  return "STAGING_NEEDS_REVIEW";
}

function nextActionFor({ program, funder, brokenUrl, verificationState }) {
  if (verificationState === "VERIFIED_FIT") return "Live source evidence exists; operator can review gates before drafting.";
  if (brokenUrl) return `Live-check or repair URL before fit elevation: ${brokenUrl.status || "needs review"}.`;
  if (program.apply_url || funder.primary_url) return "VERIFY live source before any fit elevation.";
  return "Find a live source URL before VERIFY can run.";
}

function sortPrograms(programs) {
  return [...programs].sort((left, right) => {
    const leftAward = estimateAwardValue(left.award_range).amount;
    const rightAward = estimateAwardValue(right.award_range).amount;
    const leftSignal = (left.apply_url ? 2 : 0) + (left.deadline ? 1 : 0) + (leftAward ? 1 : 0);
    const rightSignal = (right.apply_url ? 2 : 0) + (right.deadline ? 1 : 0) + (rightAward ? 1 : 0);
    return rightSignal - leftSignal || rightAward - leftAward || String(left.program_id).localeCompare(String(right.program_id));
  });
}

export async function buildScoutProjection({
  stagingDir = DEFAULT_STAGING_DIR,
  liveVerificationEvents = [],
  maxCandidates = 10,
} = {}) {
  let funders, programs, cycles, searchSeeds, brokenUrls, manifest;
  let isFallback = false;

  try {
    [funders, programs, cycles, searchSeeds, brokenUrls, manifest] = await Promise.all([
      readCsv(stagingDir, "funders.csv"),
      readCsv(stagingDir, "programs.csv"),
      readCsv(stagingDir, "opportunity_cycles.csv"),
      readCsv(stagingDir, "search_seeds.csv"),
      readCsv(stagingDir, "broken_url_queue.csv"),
      readManifest(stagingDir),
    ]);
  } catch (error) {
    if (error.code === "ENOENT") {
      isFallback = true;
      funders = [{ funder_id: "DEMO_F1", name: "Demo Foundation" }];
      programs = [{
        program_id: "DEMO_P1",
        funder_id: "DEMO_F1",
        program_name: "Demo Grant",
        award_range: "$50k - $100k",
        apply_url: "https://demo.example.com",
        deadline: "2026-12-31"
      }];
      cycles = [{ program_id: "DEMO_P1", deadline: "2026-12-31" }];
      searchSeeds = [];
      brokenUrls = [];
      manifest = { status: "STAGING_UNAVAILABLE_FALLBACK" };
    } else {
      throw error;
    }
  }

  const fundersById = new Map(funders.map((funder) => [funder.funder_id, funder]));
  const cyclesByProgram = new Map(cycles.map((cycle) => [cycle.program_id, cycle]));
  const brokenByProgram = new Map(brokenUrls.filter((row) => row.program_id).map((row) => [row.program_id, row]));
  const brokenByFunder = new Map(brokenUrls.filter((row) => row.funder_id).map((row) => [row.funder_id, row]));
  const liveByCandidate = new Map(liveVerificationEvents.map((event) => [event.payload?.candidate_id || event.payload?.program_id, event.payload || {}]));

  const candidates = sortPrograms(programs.filter(rowHasDiscoverySignal))
    .slice(0, maxCandidates)
    .map((program, index) => {
      const funder = fundersById.get(program.funder_id) || {};
      const cycle = cyclesByProgram.get(program.program_id) || {};
      const brokenUrl = brokenByProgram.get(program.program_id) || brokenByFunder.get(program.funder_id);
      const liveVerification = liveByCandidate.get(program.program_id);
      const award = estimateAwardValue(program.award_range);
      const verification_state = verificationStateFor({ program, funder, brokenUrl, liveVerification });
      const source_backing_tier = sourceBackingTierFor({ program, funder, brokenUrl, liveVerification });
      const stage = source_backing_tier === "VERIFIED_FIT"
          ? "VERIFIED_FIT"
          : brokenUrl
            ? "VERIFYING"
          : index < 3
            ? "ADDED_FROM_STAGING"
            : "TRACKING";

      return {
        opportunity_id: program.program_id,
        program_id: program.program_id,
        funder_id: program.funder_id,
        title: program.program_name || program.normalized_program_name || funder.name || "Unnamed funding program",
        funder: funder.name || funder.normalized_name || "Unknown funder",
        program_code: program.program_id,
        deadline: cycle.deadline || program.deadline || "",
        opening_date: cycle.opening_date || program.opening_date || "",
        source_url: program.apply_url || funder.primary_url || "",
        source_url_status: brokenUrl?.status || (program.apply_url || funder.primary_url ? "NEEDS_LIVE_CHECK" : "MISSING"),
        stage,
        estimated_value: award.amount,
        value_basis: award.value_basis,
        source_backing_tier,
        verification_state,
        source_backing_note: compactText(program.certainty, program.provenance_edges ? "provenance present" : "", funder.source_asset_ids ? "source assets present" : ""),
        next_action: nextActionFor({ program, funder, brokenUrl, verificationState: verification_state }),
        topics: program.topics || funder.topics || "",
      };
    });

  const verified = candidates.filter((candidate) => candidate.source_backing_tier === "VERIFIED_FIT");
  const total_tracked_value = candidates.reduce((sum, candidate) => sum + Number(candidate.estimated_value || 0), 0);
  const newly_added_value = candidates
    .filter((candidate) => candidate.stage === "ADDED_FROM_STAGING")
    .reduce((sum, candidate) => sum + Number(candidate.estimated_value || 0), 0);
  const blocked_value = candidates
    .filter((candidate) => candidate.verification_state !== "VERIFIED_FIT")
    .reduce((sum, candidate) => sum + Number(candidate.estimated_value || 0), 0);

  return {
    projection_type: "ScoutProjection",
    generated_from: isFallback ? "DEMO_FALLBACK" : "pipeline/funder_intelligence/_staging/gold",
    manifest,
    counts: {
      funders: funders.length,
      programs: programs.length,
      opportunity_cycles: cycles.length,
      search_seeds: searchSeeds.length,
      broken_url_queue: brokenUrls.length,
      candidates_visible: candidates.length,
    },
    totals: {
      total_tracked_value,
      verified_fit_value: verified.reduce((sum, candidate) => sum + Number(candidate.estimated_value || 0), 0),
      newly_added_value,
      blocked_value,
      opportunities_found: programs.length,
      opportunities_added: candidates.filter((candidate) => candidate.stage === "ADDED_FROM_STAGING").length,
      opportunities_tracking: cycles.length,
      verified_fit_count: verified.length,
      next_deadline_days: "?",
      display_note: `${programs.length} staging program rows loaded read-only; visible values are source-qualified estimates, never guaranteed awards.`,
    },
    candidates,
  };
}

export { DEFAULT_STAGING_DIR };
