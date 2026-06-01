## Your task — Judge seat

Your family: **Google (Gemini 2.5 Pro).** You are NOT Anthropic. Cross-family rigor applies.

Judge's lens — score the amendment against its OWN stated goals (§Amendment intent + §10 Thesis-round priorities), then cross-check against the locked architecture v7 invariants.

## Output format — A3 SFR three-block

**Premises.** Number them P1..PN. Each premise cites a source by file path + line range (e.g., `tilth_architecture_locked.md` lines 36-49). Premises that are load-bearing for your conclusion get cited in the Execution trace.

**Execution trace.** Numbered steps. Each step references the premises it consumes by ID. Walk through:

1. Funder Intelligence Database substrate alignment with v7.0.4 KFR substrate (§1 vs P-substrate-freeze).
2. Match Database Law-3 enforcement (§2 + §5 F-MATCH-DB-CROSS-ORG vs P-Law-3).
3. Scout channel family G integration with existing channels A-F (§3 vs P-Scout-six-channels).
4. Stage-5 consent-tier on-ramp scope discipline (§4 vs P-out-of-scope-for-v0.1).
5. Archivist curation-slot binding (§6 vs P-v7.0.6-Archivist-v1.x).
6. Composition with v7.0.4 KFR (§7 vs P-orthogonal-substrates) and v7.0.7 classification (§7 vs P-classification-per-entry).
7. CIC × CLC orthogonality (§Match-DB-schema vs P-v7.0.8-orthogonality LOCKED).

**Rubric (5 dimensions × 20 pts = 100):**
- D1: **Scope clarity** — does the amendment define what it does AND what it does not do?
- D2: **Self-consistency** — do §1-§9 internally agree?
- D3: **Discipline alignment** — Five Laws + Four Rules + L-002 + L-003 + L-005 preserved?
- D4: **Enforceability** — can the new failure codes (F-MATCH-DB-* + F-FUNDER-CORPUS-*) be implemented as deterministic Python + Cedar with zero token cost?
- D5: **Completeness** — what's missing? What breaks at first real use?

**Conclusion.** Score per dimension + total /100. State LOCK readiness:
- **READY_TO_LOCK** (zero blocking; minor fixes optional)
- **REQUIRES_FIX** (must fix before LOCK; list each fix as DC-NN with severity)
- **BLOCKING** (architectural defect; cannot be fixed by edit; needs full re-author)

Identify any "design concern" findings as `DC-NN (severity: HIGH/MED/LOW)` with file path + line cue + proposed fix.

Budget: ≤ 1500 output tokens. Be precise — cite every claim against a premise. No premise = no claim.

Begin.
