#!/usr/bin/env python3
"""
Council audit pass — takes the Logician JSON + the author-manifest + Josh's raw
concerns, dispatches to Editor / Judge / Red Team (three non-Anthropic families)
for independent review of the bedrock work done today.

Cross-family rigor: the bedrock work was authored by Anthropic (me). Under the
rule in SKELETON.md ("Authored-by-Anthropic code is NEVER reviewed by an
Anthropic-family seat"), Scribe is NOT used here — Editor drafts the narrative,
Judge scores, Red Team challenges. The final synthesis that goes to Josh is
written by the session agent with explicit citations to the three passes.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline" / "orchestrator"))
from router import _dispatch, load_config, get_seat_config  # type: ignore

WORKSPACE = Path("/Users/goldenquill/Downloads/GoldenQuill")
AUDIT = WORKSPACE / "pipeline" / "validation" / "bedrock_audit_2026-04-15"
LOGICIAN_JSON = AUDIT / "02_logician_audit.json"
assert LOGICIAN_JSON.exists(), f"missing: {LOGICIAN_JSON}"

logician = json.loads(LOGICIAN_JSON.read_text())

# -------------------------------------------------------------------------
# Author manifest — what I (Anthropic / the bedrock author) claim I did.
# Declared honestly so reviewers can challenge against actual filesystem state.
# -------------------------------------------------------------------------
AUTHOR_MANIFEST = """
AUTHOR MANIFEST — what the bedrock author (Anthropic, session 2026-04-14/15)
claims they did:

Phase 1 (consolidate):
  - Stopped OpenClaw LaunchAgent (`launchctl unload`).
  - Snapshotted /Users/goldenquill/.openclaw/agents/tilth-workspace/ to
    /Users/goldenquill/.openclaw/agents/_snapshot_tilth-workspace_2026-04-14/.
  - Renamed /Users/goldenquill/Downloads/GoldenQuill/ (v1) to
    /Users/goldenquill/Downloads/_archive_GoldenQuill_pre-bedrock_2026-04-14/.
  - Renamed /Users/goldenquill/Downloads/GoldenQuill_v2/ (v2) to
    /Users/goldenquill/Downloads/GoldenQuill/ (now canonical).
  - Restored HeartbeatQAfiles/ from archive.

Phase 2 (harvest):
  - Copied 39+ files from _snapshot_ to canonical: logician/logician.py (40KB),
    pipeline/orchestrator/{router.py,routing.yaml,logician_consensus.py},
    pipeline/orchestrator/seats/{scout,editor,judge,red_team}.py,
    pipeline/scout/scan_golden_quill.py + databases/*.csv,
    pipeline/rubrics/vapg_fy26.json, skills/{editor,logician,sentinel}/,
    live radar MD files, validation history, agent self-analysis memory.
  - run_log.json: snapshot (3.7KB real data) overwrote canonical (125B stub).

Phase 2.5 (identity):
  - Created /Users/goldenquill/Downloads/GoldenQuill/IDENTITY.md (was only in
    HeartbeatQAfiles/ before; snapshot's IDENTITY.md said "four-seat council"
    — rewrote to five-seat with Editor included).

Phase 3 (repoint daemon):
  - Backed up openclaw.json to openclaw.json.bak.2026-04-15.
  - Stopped daemon, edited agents.list[0].workspace from
    "/Users/goldenquill/.openclaw/agents/tilth-workspace" to
    "/Users/goldenquill/Downloads/GoldenQuill", reloaded daemon.
  - Daemon came back on 127.0.0.1:18789 (HTTP 200), tilth pointer confirmed.
  - Verified seats: all five callable via router.py --check.

Mistake-and-revert:
  - Began "reconciling" scout from ollama/mistral:7b → groq/moonshotai/kimi-k2
    based on assumption that 8GB Mac couldn't load 7B locally. Wrong: ollama
    0.20.6 is installed and serving, mistral:7b (4.4GB) and qwen2.5:7b (4.7GB)
    are on disk, M1 unified memory + demand-load handles the burst. Josh
    caught it; author reverted all three files (routing.yaml, router.yaml,
    SKELETON.md) and saved a feedback memory about not assuming hardware.

Just-now:
  - Created MEMORY.md at canonical root (topology gate flagged it missing).
  - Wrote tools/_bedrock_audit.py (this audit's deterministic runner).

WHAT IS EXPLICITLY NOT CLAIMED:
  - No end-to-end pipeline run yet against a real RFA.
  - No cleanup of the stale-path entries in run_log.json.
  - No update to logician/gates/topology_gate.py's WORKSPACE_ROOT_OK
    allowlist to include the harvested identity files (IDENTITY, HEARTBEAT,
    TOOLS, SKELETON, FOUNDATION_README, state/, sessions/, _private/).
  - No removal or archival of the old ~/.openclaw/agents/tilth-workspace/
    directory.
  - No update of hardcoded /Users/goldenquill/ paths in the 25 tool script
    locations the audit flagged.
"""

JOSH_RAW_CONCERNS = """
JOSH'S STATED CONCERNS (verbatim):

"We had A LOT of issues. Its concerning.  we need a thorough audit that is
 also run through openclaw."

"seriously though, we had 5 versions of claude argue a point. The thesis team
 was being by-passed. The list of failure points can go on and on at this
 juncture. Then the bombed first rebuild."

Concern vectors to address:
  (A) Multiple Claude instances argued a point without quorum / tie-break.
  (B) The "thesis team" (deterministic gates, Five Laws enforcement) was being
      bypassed by LLM seats.
  (C) The v2 "first rebuild" bombed — shipped incomplete, missing the
      orchestrator / seats / logician engine / rubric / databases.

Josh wants the audit to produce not just a defect list but MECHANISM findings:
why each failure class happened and what structural safeguards prevent recurrence.
"""

# -------------------------------------------------------------------------
# Common input pack for all three seats
# -------------------------------------------------------------------------
COMMON_CTX = f"""
You are reviewing a bedrock-consolidation pass performed on the Golden Quill
workspace on 2026-04-14/15 by an Anthropic-family agent (Claude).

Three non-Anthropic seats are reviewing this work independently (you are one
of them). Your pass will be combined with the others and surfaced to the
operator (Josh). Cross-family rigor rules apply: do not defer to the
Anthropic author; your job is to find what the Anthropic author missed,
rationalized, or got wrong.

Ground every claim in the Logician JSON or the author manifest. If you invent
findings, you fail your own job.

--- LOGICIAN DETERMINISTIC AUDIT (findings, truncated) ---
{json.dumps({
    'summary': logician['summary'],
    'topology_errors': [v for v in logician['checks']['topology_gate'].get('violations', []) if v.get('severity') == 'ERROR'],
    'topology_warns': [v for v in logician['checks']['topology_gate'].get('violations', []) if v.get('severity') == 'WARN'],
    'routing_consistency': logician['checks']['routing_consistency'],
    'hardcoded_paths_sample': logician['checks']['hardcoded_paths_in_tools'].get('findings', [])[:10],
    'hardcoded_paths_count': logician['checks']['hardcoded_paths_in_tools'].get('finding_count'),
    'run_log_hygiene': {
        'total_runs': logician['checks']['run_log_path_hygiene'].get('total_runs'),
        'stale': logician['checks']['run_log_path_hygiene'].get('stale_path_runs'),
        'canonical': logician['checks']['run_log_path_hygiene'].get('canonical_path_runs'),
    },
    'openclaw_pointer': logician['checks']['openclaw_pointer_alignment'],
    'admin_risk_status': logician['checks']['admin_risk_identity_scan'].get('status'),
    'seat_count_coherence': logician['checks']['seat_count_doc_coherence'].get('status'),
    'recent_touches_summary': {
        'count_48h': logician['checks']['recent_touches_fingerprint'].get('touched_count'),
    },
}, indent=2)}
--- END LOGICIAN JSON ---

{AUTHOR_MANIFEST}

{JOSH_RAW_CONCERNS}
"""

# -------------------------------------------------------------------------
# Prompts for each seat
# -------------------------------------------------------------------------
EDITOR_PROMPT = f"""{COMMON_CTX}

YOUR JOB (Editor seat — clarity + draft the audit narrative):

Write a plain-language audit narrative from the above findings. Structure:

1. Bottom line: what is the state of the workspace after bedrock?
2. What the author did right (specific, cited to manifest / Logician).
3. What the author did wrong or incomplete (specific, cited to Logician
   findings or manifest's "WHAT IS NOT CLAIMED" section).
4. The three mechanism questions Josh raised, each addressed concretely:
   - Why were 5 Claudes arguing without a tie-break mechanism?
   - Why was the thesis team (gates / Five Laws enforcement) bypassed?
   - Why did the v2 rebuild ship incomplete?
5. Open questions the author did not answer.

Requirements:
- Cite specific files, line numbers, or Logician check names for every claim.
- No corporate hedging. Call spades spades.
- 400-800 words. Markdown with headers.
- Do NOT score or rate — that's the Judge's job. Just narrate.
"""

JUDGE_PROMPT = f"""{COMMON_CTX}

YOUR JOB (Judge seat — score against the Five Operating Laws):

The Five Operating Laws are non-negotiable. Score the bedrock work against
each one on a 0-20 scale (so max 100). The scale:
  0  = severe violation
  5  = violation with partial mitigation
  10 = no clear violation but weak adherence
  15 = strong adherence with minor gaps
  20 = exemplary

Laws:
  Law 1: RFA is the source of truth. (N/A for bedrock if no active grant —
         but evaluate whether the work respected existing source-of-truth
         documents, e.g., SKELETON, SOUL, lessons.md.)
  Law 2: No boundary drift. (Did the bedrock work expand scope beyond what
         was asked? Did it silently introduce new structures?)
  Law 3: Org isolation. (Did cross-client data leak? Was PROJECT_CONTEXT
         discipline respected? N/A if no client work was touched.)
  Law 4: Apolitical sector language + admin-risk term scanning.
         (Were flagged terms silently rewritten? See admin_risk check status.)
  Law 5: Applicant brings the substance. (Did the author invent facts,
         constraints, or data that weren't provided? The reverted
         ollama-won't-work-on-8GB episode is the strongest data point here.)

Output:
  Return a JSON object with:
    {{"scores": {{"law_1": N, "law_2": N, "law_3": N, "law_4": N, "law_5": N}},
     "reasoning": {{"law_1": "...", "law_2": "...", ...}},
     "total": N,
     "verdict": "PASS" | "FAIL" | "NEEDS_REVISION",
     "threshold_note": "PASS ≥ 80; FAIL < 50; NEEDS_REVISION between.",
     "critical_flag": "..."}}

- Put nothing before or after the JSON. Do not wrap it in markdown code fences.
- Cite at least one Logician check or manifest item per law in your reasoning.
"""

RED_TEAM_PROMPT = f"""{COMMON_CTX}

YOUR JOB (Red Team — adversarial challenge of the Anthropic author's work):

You are explicitly tasked with finding what the Anthropic author missed,
rationalized, or got wrong. Be skeptical of the manifest. Cross-check it
against the Logician findings and the workspace reality.

Produce a challenge memo with:

1. **Unclaimed damage.** What changed state in the workspace that is NOT
   in the author's manifest? Use the 'recent_touches_fingerprint' count
   (touched_count in the last 48h) to argue.

2. **Confident-but-wrong patterns.** The author admits one: the Ollama
   reconciliation. Are there others visible in the touches, the
   routing_consistency check, or the manifest? Name them.

3. **Unaddressed mechanism failures.** The author acknowledges Josh's three
   mechanism concerns but did NOT propose structural safeguards. What
   concrete code changes would actually prevent recurrence? Name at least
   three, each a file path + one-line description.

4. **Hidden drift the Logician missed.** The Logician runs discrete checks;
   what structural drift is it blind to? (Hint: the routing mismatches, the
   stale run_log paths, the `agentDir` vs `workspace` separation, the old
   tilth-workspace directory still on disk, the gate's own allowlist.)

5. **One sentence to Josh.** If Josh reads only your first line, what is
   the single most important thing he should know about today's bedrock work?

Requirements:
- 300-700 words. Markdown with headers.
- Cite Logician check names or manifest items for every claim.
- Do NOT be polite. Be correct.
"""

# -------------------------------------------------------------------------
# Run the three seats
# -------------------------------------------------------------------------
def call(seat_name: str, prompt: str) -> dict:
    cfg = load_config()
    sc = get_seat_config(seat_name)
    provider_cfg = cfg["providers"][sc["provider"]]
    messages = [{"role": "user", "content": prompt}]
    return _dispatch(provider_cfg, sc, messages, system=None)

print("[1/3] Editor drafting audit narrative (Llama 3.3 70B)...", file=sys.stderr)
editor_resp = call("editor", EDITOR_PROMPT)
(AUDIT / "03_editor_audit_draft.md").write_text(
    f"# Editor Audit Draft\n\n"
    f"_Model: {editor_resp['family']}/{editor_resp['model']}_\n\n"
    f"{editor_resp['content']}\n"
)
print(f"    wrote 03_editor_audit_draft.md ({len(editor_resp['content'])} chars)", file=sys.stderr)

print("[2/3] Judge scoring against Five Laws (Qwen 3 32B)...", file=sys.stderr)
judge_resp = call("judge", JUDGE_PROMPT)
# Strip <think> tags if Qwen reasoning mode included them
raw = judge_resp["content"]
# Judge may wrap with markdown fences; strip for clean JSON.
cleaned = raw.strip()
if cleaned.startswith("```"):
    cleaned = cleaned.split("```", 2)[1]
    if cleaned.startswith("json"):
        cleaned = cleaned[4:]
    cleaned = cleaned.rsplit("```", 1)[0].strip()
# Qwen sometimes includes a <think>...</think> prefix. Strip it.
import re as _re
cleaned = _re.sub(r"<think>.*?</think>\s*", "", cleaned, flags=_re.DOTALL)
try:
    judge_json = json.loads(cleaned)
    (AUDIT / "04_judge_score.json").write_text(json.dumps({
        "model": f"{judge_resp['family']}/{judge_resp['model']}",
        "score": judge_json,
    }, indent=2))
    print(f"    wrote 04_judge_score.json  total={judge_json.get('total')}  verdict={judge_json.get('verdict')}", file=sys.stderr)
except Exception as e:
    # Save raw for forensics
    (AUDIT / "04_judge_score_RAW.txt").write_text(raw)
    print(f"    WARN: judge output not parseable as JSON ({e}); raw saved", file=sys.stderr)

print("[3/3] Red Team challenging the Anthropic author (GPT-OSS 120B)...", file=sys.stderr)
redteam_resp = call("red_team", RED_TEAM_PROMPT)
(AUDIT / "05_red_team_challenge.md").write_text(
    f"# Red Team Challenge\n\n"
    f"_Model: {redteam_resp['family']}/{redteam_resp['model']}_\n\n"
    f"{redteam_resp['content']}\n"
)
print(f"    wrote 05_red_team_challenge.md ({len(redteam_resp['content'])} chars)", file=sys.stderr)

print("\nCouncil pass complete.", file=sys.stderr)
