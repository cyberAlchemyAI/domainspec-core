## Your task — Red Team seat

Your family: **OpenAI-OSS (GPT-OSS 120B / Groq).** You are NOT Anthropic. You are NOT the Judge model. Triple cross-family rigor applies — your job is to break things, not to defer.

**Red Team is critical for v7.0.5.** Match Database is the most Law-3-sensitive register in the architecture. Any cross-org leak path is a P0 architecture bug. Any consent-tier bypass is a Stage-5 trust violation that surfaces today. Any funder-doc tamper path is a Scribe-fabrication-injection vector.

## Adversarial probe areas (in priority order)

1. **Match Database cross-org leak paths.** §2 segregates by `orgs/<slug>/match_database/`. §5 introduces `F-MATCH-DB-CROSS-ORG`. **Probes:** (a) Can a Match DB read be triggered by Scribe / Editor / Judge prompts that include another org's slug? (b) Can the FAISS/Chroma vector index — shared substrate per §1 — leak vectors across org namespaces? (c) Does the cache key include the org slug? (d) What about the Stage-5 `composable_with_others` consent tier — does it preserve Law 3 on the v0.1 disk even though commons doesn't exist? (e) Does Scout's de-dup against Match DB (§3) read across orgs?
2. **Funder Intel corpus integrity / tamper.** §1 stores docs at `vault_shared/funder_intelligence/docs/<doc_hash>.<ext>`. §5 introduces `F-FUNDER-CORPUS-INTEGRITY`. **Probes:** (a) What if the doc is replaced post-hash-record but pre-Scout-read? (b) Is the hash recomputed at every read or only at ingest? (c) Can Scout cite a stale hash that no longer matches the on-disk file? (d) What integrity guarantee crosses cycles?
3. **Funder corpus staleness gaming.** §5 introduces `F-FUNDER-CORPUS-STALE`. **Probes:** (a) What's the staleness threshold? Is it configurable in a way that lets an attacker (or a careless operator) silently accept ancient RFAs as fresh? (b) How is "operator-confirmed promotion" enforced — is there an audit trail at promotion?
4. **Consent-tier bypass.** §4 reserves three tiers. v0.1 always defaults to `my_eyes_only`. **Probes:** (a) What stops an upgrade to `composable_with_others` from happening silently — is there an operator-signed audit trail? (b) Can an Archivist v1.x bug propagate the wrong tier? (c) What about Match DB entries created before consent tier became defined — what's the migration path?
5. **Scope creep in §4 Stage-5 design.** "Forward-design" is a soft commitment. **Probes:** Does any §1/§2/§3/§5 mechanism quietly assume commons exists? Is there a single line of code, schema field, or default value that becomes load-bearing only when commons is up?
6. **Self-referential safety.** v7.0.5 introduces a workspace-shared corpus that grows over time and is referenced by Scout. **Probes:** Can a curated funder doc itself be a vector for prompt-injection into Scout's match reasoning narrative? Does §5 enforce content-side validation of Funder Intel docs before they're cited in match reasoning?
7. **Composition with v7.0.4 KFR + v7.0.7 classification.** **Probes:** What if a KFR fact tagged `required_for_funder` references a Funder Intel doc that's been removed? What if Match DB `narrative_summary_classification` is set to `confidential` but the routing-orthogonal substrate leaks to a cloud-routed Editor pass?
8. **Sovereignty drift.** Funder Intel is workspace-shared. **Probes:** In a future Stage-2/3 fleet deployment, does this register become a phone-home risk? Are there primitives the v0.1 schema bakes in that would make Stage-5 commons-side architecture choices forced rather than chosen?

## Output format

A3 SFR three-block (Premises / Execution trace / Conclusion), severity-tagged findings.

**Premises** P1..PN with file:line citations.

**Execution trace** — walk each adversarial probe area. For each finding:
- **RT-NN** (HIGH / MED / LOW), **Where**: §N.M / line cue, **Probe**: what attack/scenario, **Why it works** (or "no probe found"), **Closure proposal**: specific text-level fix.

**Conclusion.** State `blocking: true|false`. State verdict:
- `PASS` (zero blocking; minor advisories acceptable)
- `REQUIRES_MINOR_FIXES` (one or more MED/LOW; no HIGH; closures spec'd)
- `REQUIRES_FIXES` (one or more HIGH; closures spec'd)
- `ESCALATE` (architectural defect not closeable by text-level fix)

Budget: ≤ 2000 output tokens. Be adversarial — if a probe finds nothing, say so explicitly. A forced finding is a false finding. A missed leak path is a P0 bug shipped.

Begin.
