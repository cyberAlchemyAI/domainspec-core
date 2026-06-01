# FID Validators

Per FID Refinement Methodology Discipline 7, each pass adds the recurrence guards needed to keep the patterns it surfaced from re-occurring.

This directory is the canonical home for those validators.

## Roster (LANDED at Pass 1, 2026-05-18)

| Validator | Pattern caught | Pass added | Priority |
|---|---|---|---|
| `no_unquoted_colon_placeholders.py` | YAML parser breaks on `key: <NEEDED — Pillar 2: ...>` (Pass-0 pattern G1) | 1 | high |
| `no_gold_standard_label_remaining.py` | `gold[- ]standard(s?)` rhetoric leak (Pass-0 pattern G3) | 1 | high |
| `gate_dsl_schema_check.py` | gates missing one of `gate_id / gate_type / severity / fail_action / source_required / corpus_ref` per Discipline 3a | 1 | high |
| `gate_taxonomy_consistency.py` | `(gate_type, severity, fail_action)` tuple does not match Discipline 3a.4 matrix | 1 | high |

## Roster (SCOPED for separate dispatch, ACs in this README)

| Validator | Pattern caught | Acceptance criteria |
|---|---|---|
| `no_quoted_scalar_paren_list_items.py` | `- "<scalar>" (<comment>)` list-item syntax (Pass-0 pattern G2) | (a) runs `yaml.safe_load` on every fenced ` ```yaml ` block in `pillar_1_charters/*.md`; (b) returns nonzero exit on any parse failure; (c) outputs the offending file:line:span; (d) round-trip-tested against the Pass-0 fix corpus |
| `artifact_id_matches_filename.py` | charter `artifact_id` field disagrees with filename stem | (a) parses `artifact_id` from header table + §B yaml; (b) compares to `<stem>_charter_v0_DRAFT.md`; (c) reports any mismatch; (d) covers both batch-A (funder-level) and batch-B (program-level) filename conventions |
| `lifecycle_status_valid.py` | `lifecycle / validation_status / runtime_load_status / operator_label` not in canonical enum set per Discipline 8 | (a) reads §B yaml; (b) validates the four-field status block against the Discipline-8 enum; (c) reports any deviation; (d) handles both `draft + pre_corpus_hypothesis` and `draft + source_backed` post-Pillar-2 states |

## Running

From the repo root:

```bash
python3 -m pipeline.funder_intelligence._validators.no_unquoted_colon_placeholders \
    pipeline/funder_intelligence/pillar_1_charters/*.md

python3 -m pipeline.funder_intelligence._validators.no_gold_standard_label_remaining \
    pipeline/funder_intelligence/pillar_1_charters/*.md

python3 -m pipeline.funder_intelligence._validators.gate_dsl_schema_check \
    pipeline/funder_intelligence/pillar_1_charters/*.md

python3 -m pipeline.funder_intelligence._validators.gate_taxonomy_consistency \
    pipeline/funder_intelligence/pillar_1_charters/*.md
```

Each validator:

* Returns **exit 0** on clean run.
* Returns **exit 1** on any finding.
* Prints findings to stdout in `path:line: <finding>` format.
* Is dependency-free (standard library + PyYAML only).

## Pass-1 caveat

Pass 1 introduces `gate_type` + `confidence` + (optional) `pass_1_reconciliation_note` on every existing gate. Gates still carry pre-Pass-1 abbreviated operators (`lte`, `gt`, `eq`, `matches`, etc.). The DSL grammar at Discipline 3a treats those as deprecated aliases; `gate_dsl_schema_check.py` checks structural completeness (presence of required fields) without yet enforcing operator-name canonicalization. A future pass renames operators in place and tightens that validator.
