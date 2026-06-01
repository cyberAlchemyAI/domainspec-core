# Spec card — pipeline.logician.fabricated_org_ner_gate

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_1_*.md` — Logician POST-gate battery; Law 5 (Applicant Brings Substance)
**Spec-card version:** v1
**Round:** post-v0.1 (v0.2 roadmap)
**Priority:** v0.2
**Origin:** SSI Booster reference review 2026-05-06 (see `pipeline/roadmap/explorations/ssi_booster_reference_review.md`)

---

## Purpose

Deterministic Logician POST-gate that catches fabricated organization names in Scribe drafts. Complements the existing Law 5 verbatim-substring gate (which catches fabricated credentials/data) by targeting a specific failure mode: invented partnerships and collaborations that name real-sounding organizations not present in PROJECT_CONTEXT.md.

**Example catch:** Scribe drafts "in partnership with Penn State Extension" but Penn State Extension is not listed in the client's PROJECT_CONTEXT.md partners, collaborators, or org fields. Gate fires `F-LOGICIAN-FABRICATED-ORG` and blocks promotion.

## Architecture

### Drop point

Logician POST-gate, fires after Scribe output, before Editor intake. Runs in the existing Logician gate battery alongside Law 1-5 gates.

### Pipeline

1. **Extract:** spaCy NER (`en_core_web_sm` or `en_core_web_md`) extracts all `ORG` entities from Scribe draft text.
2. **Normalize:** lowercase + whitespace-collapse both extracted ORGs and PROJECT_CONTEXT org names.
3. **Allowlist build:** parse PROJECT_CONTEXT.md for all organization names — partners, collaborators, fiscal sponsors, applicant org, sub-awardees, any named org field. Union with the applicant's own org name and any RFA-issuing agency names (funder is always a valid ORG mention).
4. **Set-membership check:** each extracted ORG must appear in the allowlist (fuzzy threshold: Levenshtein ratio >= 0.85 to handle minor spelling variants).
5. **Verdict:** if any ORG entity fails membership, gate returns `FAIL` with failure code `F-LOGICIAN-FABRICATED-ORG` and lists each ungrounded org with its sentence context.

### Properties

- **Deterministic:** yes — spaCy NER is a fixed model, set-membership is boolean. Zero LLM tokens.
- **Fail-closed:** unmatched ORG = FAIL. Operator can override via M13 bypass (audited).
- **False-positive handling:** operator adds legitimate orgs to PROJECT_CONTEXT.md allowlist fields, re-runs gate. No silent suppression.

## Failure codes

| Code | Trigger | Severity | Reason tag |
|---|---|---|---|
| `F-LOGICIAN-FABRICATED-ORG` | ORG entity extracted from Scribe draft not found in PROJECT_CONTEXT.md allowlist | HIGH | `law5_fabricated_partnership` |

## Public API

- `check_fabricated_orgs(draft_text: str, project_context_path: Path) -> GateResult` — returns PASS/FAIL with list of ungrounded ORGs
- `extract_org_entities(text: str) -> list[str]` — spaCy NER ORG extraction
- `build_org_allowlist(project_context_path: Path, rfa_path: Path | None) -> set[str]` — normalized allowlist from PROJECT_CONTEXT + RFA issuer

## Data structures

```python
@dataclass(frozen=True)
class FabricatedOrgFinding:
    org_name: str           # as extracted by NER
    sentence_context: str   # surrounding sentence
    nearest_match: str | None  # closest allowlist entry if ratio > 0.5
    match_ratio: float      # Levenshtein ratio to nearest

@dataclass(frozen=True)
class FabricatedOrgGateResult:
    gate_id: str = "F-LOGICIAN-FABRICATED-ORG"
    verdict: Literal["PASS", "FAIL"]
    findings: tuple[FabricatedOrgFinding, ...] = ()
    org_count_extracted: int = 0
    org_count_ungrounded: int = 0
```

## Dependencies

- `spacy` + `en_core_web_sm` (or `_md`) — NER extraction
- `python-Levenshtein` or `rapidfuzz` — fuzzy matching
- Existing Logician gate battery interface (gate registration, GateResult protocol)
- PROJECT_CONTEXT.md parser (existing)

## Test surface

### Failure-code tests
- Draft with fabricated org → `F-LOGICIAN-FABRICATED-ORG` fires
- Draft with only PROJECT_CONTEXT orgs → PASS
- Draft with minor misspelling of real org (ratio >= 0.85) → PASS (fuzzy match)
- Draft with no ORG entities → PASS (vacuously true)

### Edge cases
- ORG entity that is a substring of an allowlist entry (e.g., "Penn State" vs "Penn State Extension")
- Common generic orgs (e.g., "USDA") — handled by RFA-issuer allowlist inclusion
- Multiple fabricated orgs in one draft — all reported

## Interaction with existing gates

- **Law 5 verbatim-substring gate:** checks for fabricated credentials/data as literal strings. This gate covers the complementary case of fabricated *organizations* via NER. Both fire independently; both must PASS for promotion.
- **Law 1 RFA-is-truth gate:** validates claims against RFA. This gate validates org names against PROJECT_CONTEXT. Orthogonal scopes.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| spaCy NER misses an org mention | Acceptable — gate catches common patterns; verbatim-substring gate covers others. Not a security boundary. |
| spaCy NER over-extracts (flags non-org text as ORG) | Fuzzy match + operator review on FAIL. False positives are operator-visible, not silent. |
| M1 Mac Mini spaCy performance | `en_core_web_sm` is ~11MB, loads in <1s, NER runs in ms. No concern. |

## Done definition

- [ ] spaCy NER extraction works on sample Scribe drafts
- [ ] Allowlist parser handles all PROJECT_CONTEXT org field patterns
- [ ] Fuzzy matching catches minor spelling variants without false-passing fabricated orgs
- [ ] Gate registered in Logician POST-gate battery
- [ ] Failure code `F-LOGICIAN-FABRICATED-ORG` documented in gate registry
- [ ] Tests green: fabricated org caught, real org passed, edge cases handled
- [ ] Dev hardware (M1 Mac Mini 8GB) runs gate in <2s on typical draft
