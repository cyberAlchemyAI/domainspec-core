# LOGICIAN Self-Evaluation — 2026-04-20

**Model:** groq/openai/gpt-oss-120b
**Old:** /Users/goldenquill/Downloads/GoldenQuill/skills/logician/SKILL.md
**New:** /Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/agents/logician_enforcement_agent_v1.md

---

## IMPROVEMENTS (what NEW does better for grant outcomes)  
- **Fail‑closed determinism (Section 5‑7, 7‑8):** NEW makes every gate return `RED BLOCK` on any indeterminate result, eliminating the “soft‑fail” paths that existed in the OLD script where a missing file or ambiguous check could be ignored. This guarantees that illegal content never proceeds downstream.  
- **Cedar policy integrity check (Section 5‑1):** NEW adds a SHA‑256 manifest verification for all policy files before any gate runs. This prevents silent policy drift and ensures the exact rule set that was audited is the one being enforced.  
- **Explicit gate taxonomy & severity mapping (Section 5‑5‑8):** Each gate now has a unique failure code (`F‑KGIE‑INCOMPLETE`, `F‑BOUNDARY‑DRIFT`, etc.) and a clear severity tier. The OLD prompt only listed gates; NEW supplies a machine‑readable taxonomy, which makes downstream automation (e.g., alert routing) reliable.  
- **Revision‑loop counter as a gate (Gate 7, Section 5‑7):** The new version enforces a hard limit of three revision cycles with a dedicated gate, whereas the OLD only described “track cycles” in prose. This prevents endless back‑and‑forth and forces operator intervention before a deadline.  
- **Unified, version‑controlled admin‑risk register (Section 7):** The register is now a YAML file loaded via a hash‑verified manifest, guaranteeing the exact term list used for scanning. The OLD version stored the JSON register on disk without integrity checks, exposing the pipeline to accidental tampering.  
- **Structured JSON gate reports (Section 14):** Every gate outputs a canonical JSON payload, replacing the ad‑hoc JSON snippets in the OLD prompt. This enables deterministic downstream processing, automated dashboards, and reliable audit trails.  

## REGRESSIONS (what OLD did better that NEW lost or weakened)  
- **Human‑readable CLI examples:** The OLD prompt included concrete, copy‑and‑paste bash commands (`python3 … preflight …`) that an operator could run instantly. NEW replaces them with abstract `logician.py` invocations that assume a virtual environment (`.venv/bin/python3`) and a custom `cedarpy` library, raising the barrier for ad‑hoc debugging.  
- **Explicit “what you do NOT do” list:** The OLD prompt enumerated prohibited actions (e.g., “Do not generate text”) in a separate bullet list. NEW embeds the same constraints in prose but they are harder to scan automatically, increasing the risk that a future maintainer misses a restriction.  
- **Less explicit error‑message wording:** OLD gate failures were described with human‑friendly messages like “RED violations: STOP. Surface missing fields to the applicant.” NEW relies on generic `result` fields and failure codes; without a companion human‑readable legend, an operator may need to map codes back to actionable text.  

## MISSING (gaps in both versions)  
- **Policy‑as‑Code for KGIE thresholds:** Both prompts enforce KGIE existence but do not expose configurable thresholds (e.g., how “weak” a geography entry can be before it becomes a YELLOW vs. RED). Without a tunable rule set, the gate cannot be calibrated per funder or grant size.  
- **No audit‑trail linkage to the original RFA version:** Neither version records the RFA hash or version identifier that the gate used for traceability. If the RFA is amended after a gate run, the system cannot prove which version was validated.  
- **Missing integration with the Logician’s own test harness:** The prompts describe a “self‑check” but do not define a reproducible test suite (e.g., a set of synthetic grant files) that can be run automatically on CI to guarantee gate stability after code changes.  

## TENSIONS (tradeoffs where reasonable people would disagree)  
- **Zero‑token enforcement vs. operational flexibility:** NEW’s “model = none” guarantee eliminates token cost but also removes any possibility of using a lightweight LLM for fuzzy checks (e.g., fuzzy address validation). Some engineers may argue that a tiny LLM could reduce false‑positive RED blocks without violating the “zero token” principle if it’s run locally.  
- **Hard failure on missing admin‑risk register (Fail‑Closed) vs. grant‑deadline pressure:** If the register fails to load, the pipeline halts entirely. In a tight deadline, a team might prefer to “warn and continue” rather than stop the entire submission. The current design forces a trade‑off between compliance certainty and time‑to‑submission.  
- **Granular JSON failure codes vs. simplicity for operators:** The detailed taxonomy improves machine routing but makes manual triage harder for non‑technical operators who must learn each code. Simpler “PASS/FAIL” could be more approachable at the cost of losing diagnostic precision.  

## VERDICT: UPGRADE — The new Logician adds deterministic fail‑closed behavior, cryptographic policy integrity, and a formal gate taxonomy, which together raise compliance and auditability dramatically despite a higher operational complexity.  

## TOP 3 CHANGES before deploying NEW as replacement  
1. **Add a human‑readable failure‑code dictionary** (e.g., `F‑KGIE‑INCOMPLETE → “KGIE preflight missing required element”`). Store it alongside the gate JSON outputs so operators can instantly interpret codes without consulting external docs.  
2. **Introduce configurable KGIE severity thresholds** (e.g., a YAML `kgie_thresholds.yaml` mapping each element to `PASS/YELLOW/RED` criteria). This will let the council calibrate the gate per funder or grant size without code changes.  
3. **Persist the RFA hash in every gate report** (`rfa_sha256`) and validate it against the current RFA file on every run. This ties each validation to a specific RFA version, closing the audit‑trail gap identified above.
