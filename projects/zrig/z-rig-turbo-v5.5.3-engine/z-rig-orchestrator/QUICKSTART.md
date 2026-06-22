# Z-Rig Turbo v5.5.3 — Quick Start Guide

**For any OpenClaw session / channel that needs to use the Rig.**

---

## What Is The Z-Rig?

A multi-model orchestration pipeline that dispatches multiple AI agents to build, verify, and red-team code artifacts. It produces higher-quality output than any single model by using independent builders, adversarial verification, and mechanical gate evaluation.

**Stats:** 8,255 lines | 21 modules | 229 tests | 9 runs completed | Spec: v5.5.3

---

## When To Use It

- **Production code** (>3 files or >100 lines)
- **Architecture documents** requiring multi-perspective review
- **Any high-stakes artifact** (patents, legal, deployments)
- **When you want independent verification** — multiple models build the same thing, best output is synthesized

---

## Pipeline Modes

| Mode | When | Builders | Waves | Time |
|------|------|----------|-------|------|
| **MICRO** | Tiny tasks, <2 files, routine | 1 | 3 (M0→M1→M2) | ~2 min |
| **STANDARD** | Most tasks | 3 | 14 (W0→W11) | ~10-20 min |
| **FULL** | High-stakes, irreversible | 3-5 | 16 (adds W6+W7) | ~30-60 min |
| **AUTO** | Let classifier decide | varies | varies | varies |

---

## How To Run

### Step 1: Create task.json
```json
{
  "task_id": "MY-TASK-001",
  "summary": "What you're building",
  "requested_change": "Detailed description of the change",
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "artifact_type": "utility-module",
  "artifact_domain_tags": ["python"],
  "stakes_level": "routine",
  "scope_ambiguity": "none",
  "target_files": ["src/myfile.py", "tests/test_myfile.py"],
  "public_interface_impact": {"changes_public_surface": false},
  "deterministic_verifier": {"kind": "frozen_test_suite", "frozen_before_run": true},
  "reversibility": {"fully_reversible": true},
  "deployment_side_effects": "none",
  "security_relevance": {"is_security_relevant": false}
}
```

### Step 2: Create run_config.json
```json
{
  "run_id": "MY-TASK-001",
  "mode": "AUTO",
  "artifact_type": "utility-module",
  "artifact_domain_tags": ["python"],
  "stakes_level": "routine",
  "scope_ambiguity": "none",
  "deterministic_metric_defined": true,
  "provider_list": ["anthropic", "xai", "openai"],
  "w2_builder_count": 3,
  "w4_verifier_count": 3,
  "w5_squad_count": 2,
  "w9_panel_size": 3,
  "max_rework_cycles": 2
}
```

### Step 3: Classify (optional — see what mode the Rig picks)
```bash
cd ~/.openclaw/workspace/z-rig-orchestrator
PYTHONPATH=src python3 -m zrig classify --task task.json --config run_config.json
```

### Step 4: Run
```bash
PYTHONPATH=src python3 -m zrig run --task task.json --config run_config.json --live
```

The `--live` flag wires real agent dispatch through OpenClaw.

---

## Wave Sequence (STANDARD Mode)

```
W0  → Provider Probe (check model availability)
W1  → Spec/Planning (planners write requirements)
W2  → Build (3 builders write code independently)
W3  → Synthesis (pick best / merge outputs)
W4  → Verification (independent code review)
W5  → Red Team (adversarial attack — try to break it)
W5.5→ Remediation (fix critical findings, if any)
W8  → User Acceptance Testing
W8.5→ FDL Preservation (if needed)
W9  → Final Panel Review (vote: ACCEPT/REVISE/REJECT)
W10 → Deployment (write files)
W11 → Sentinel (post-deploy monitoring)
```

Every wave has a **gate** — a mechanical predicate that must PASS before proceeding. Zero FATALs at W5 to continue.

---

## Gate Results

| Gate | What It Checks |
|------|---------------|
| G0 | ≥3 model families available, registry hash computed |
| G2 | ≥2 builders delivered, family diversity met |
| G3 | Synthesis confidence > threshold, canonical impl exists |
| G4 | No FATAL findings, verification confidence > threshold |
| G5 | Zero unresolved FATALs from red team |
| G9 | Panel majority ACCEPT, no REJECT votes |

---

## Failure Routing

If a gate fails, the Rig doesn't just stop — it routes the failure:
- **REWORK** — retry the same wave
- **RETURN** — go back to an earlier wave
- **ESCALATE** — pause and ask for human input
- **HALT** — stop the pipeline (serious failure)

3 consecutive timeouts → **automatic HALT** (MECH-015 cascade).

---

## Key Files

```
z-rig-orchestrator/
├── src/zrig/
│   ├── pipeline.py        — Async wave state machine
│   ├── gates.py           — Gate predicate evaluation
│   ├── classifier.py      — Mode selection (AUTO/MICRO/STANDARD/FULL)
│   ├── live_executor.py   — Real agent dispatch via bridge
│   ├── wave_prompts.py    — Prompt templates for each wave
│   ├── dispatch.py        — Agent spawning + failover
│   ├── families.py        — Family diversity enforcement
│   ├── residue.py         — Necronomicon Memory Loop
│   ├── metrics.py         — Self-improvement triggers
│   ├── format_utils.py    — Human-readable output
│   ├── run_summary.py     — Terminal run report
│   └── __main__.py        — CLI entry point
├── runs/                  — Run artifacts (manifests, configs)
└── tests/                 — 229 tests
```

---

## Codebase Location

```
~/.openclaw/workspace/z-rig-orchestrator/
```

**Skill:** `~/.openclaw/workspace/skills/z-rig/SKILL.md`

---

## For Analog 6 (Internal)

When a channel asks you to "use the Rig" or "run it through the pipeline":
1. Read the skill: `skills/z-rig/SKILL.md`
2. Create task.json + run_config.json in `runs/HRR-NNN/`
3. Classify → dispatch builders → synthesize → verify → report
4. The `--live` flag handles agent dispatch via OpenClaw bridge

The Rig is a tool. Use it when quality matters more than speed.
