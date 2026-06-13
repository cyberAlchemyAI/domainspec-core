# TO-JOSH — Founder / Grant Strategy / Deployment Lead

You carry the decisions, staffing, founder content, and capital track. Engineering (Vlad, Koichi) and QA (Victor) are unblocked on everything they can build alone — **the items below are the ones that need you**, ordered by how much downstream work they release.
**Source:** [docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md](docs/strategy/development/node-on-desk-readiness/DISPATCH-VALIDATION.md)

## Agent execution contract — run this first

When Josh asks an agent to "read the artifacts" or handle this handoff, the
agent should treat this file as an executable interface, not a memo.

1. Read `pipeline/SESSION_BOOTSTRAP.md` for project orientation.
2. Read this handoff and the linked source artifacts by path. Do not paste file
   contents into a prompt.
3. Run `$craft state` against the owner ledgers below before asking Josh
   anything. The ledger is the source of truth; `CRAFT.md` is only a view.
4. If the next action needs Josh's judgment, run `$interrogation` for that one
   decision or input lane. Ask one evidence-backed question at a time.
5. After each answer, immediately update the owning artifact: close or amend the
   Craft decision/gap when the answer resolves it, or record residue if it does
   not.
6. If a question belongs to Vlad, Koichi, Victor, legal counsel, or a future
   hire, do not answer for them. Add a routed next action instead.
7. Return a `Craft Result` with the ledgers touched, decisions recorded,
   remaining blockers, and next move.

### Josh-facing Craft scope

Run `$craft state` for these ledgers before starting the interview:

| Scope | Ledger | Why Josh owns the next move |
| --- | --- | --- |
| boundary/canon | `docs/strategy/development/boundary-and-canon/.craft/ledger.yml` | `DEC-BC-POSTURE-VOCAB` and `DEC-BC-UI-BOUNDARY` are governance calls. |
| root promotion governance | `.craft/ledger.yml` | `DEC-OQ4`, `DEC-D2-FLIP`, `DEC-D3-SHARED-GATE`, and `DEC-D4-VERIFY` require owner ratification. |
| staffing/budget | `docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml` | Hours/rates, staffing triggers, and `DEC-SBT-TRIGGER-MODEL` are business decisions. |
| after-acceleration | `docs/strategy/development/after-acceleration-roadmap/.craft/ledger.yml` | Stage-gate thresholds are founder judgment. |
| capital logic | `docs/features/capital-logic-library/.craft/ledger.yml` | Launch cards and domain-expert contracting need Josh's content and staffing calls. |
| sales/legal | `docs/strategy/development/sales-contracting-legal/.craft/ledger.yml` | Sales material, counsel retention, and first-LOI readiness are founder/legal lanes. |
| company ops | `docs/strategy/development/company-operations-finance/.craft/ledger.yml` | Support triage, entity hygiene, Node Care, and validation packet ownership need Josh. |
| white-glove | `docs/strategy/development/white-glove-delivery-node-care/.craft/ledger.yml` | Founder-led service wrapper and later CS handoff need Josh's operating choices. |
| node readiness | `docs/strategy/development/node-on-desk-readiness/.craft/ledger.yml` | Parent readiness depends on Josh-owned RG-1 and RG-X blockers. |

### Interrogation interface for Josh

Use `$interrogation` when a row below needs a selected option or numeric input.
Start with the highest-leverage blocker:

```text
$interrogation docs/strategy/development/boundary-and-canon --mode owner-decision
```

Question shape:

- Context: cite the specific decision ID and source artifact path.
- Why it matters: name downstream nodes unlocked.
- Recommended default: include one when the artifact already gives a safe
  recommendation.
- Risk if unanswered: name the Craft gate that stays blocked.
- Target update: name the ledger decision/gap to close or amend.

## A. Two blocking decisions — ratify these first (highest leverage)

1. **DEC-BC-POSTURE-VOCAB** *(BLOCKING)* → [docs/strategy/development/boundary-and-canon/BUILD-SPEC.md](docs/strategy/development/boundary-and-canon/BUILD-SPEC.md)
   Ratify the 4→3 posture translation table: Unrestricted→**Frontier-Eligible**, Hybrid→**Split-Context Hybrid**, Sovereign→**Local-Only/Sovereign**, Sanitized→**DEPRECATED** (defense-in-depth only). One ratification unblocks Vlad's posture-enforcement build (`GAP-TRB-POSTURE-CANON`) **and** node-readiness canon (`GAP-NOD-CANON-VOCAB`).

2. **DEC-OQ4** *(BLOCKING, P0)* → [.craft/artifacts/BUILD-SPEC.md](.craft/artifacts/BUILD-SPEC.md)
   Ratify the decision-surface shape (Vlad proposes three typed surfaces, rec A). Unblocks the promotion-governance L1 build and the promotion-authority gate.

## B. Other decisions to make
→ specs frame the options; you choose.
- **DEC-BC-UI-BOUNDARY** — operator console phase: (a) v0.1 read-only projection / (b) deferred later-phase / (c) out-of-scope. **Interactive v0.1 UI is not permitted (headless-only locked)** — recommendation is (a) or (b). Resolves `GAP-BC-UI-SCOPE` + `GAP-TRB-UI-PHASE`.
- **DEC-D2-FLIP / DEC-D3-SHARED-GATE / DEC-D4-VERIFY** — ratify Vlad's proposals (D3 needs a **K value**, rec ≥3 orgs; D4 needs the **guardrail-KPI set**). [promotion-governance spec](.craft/artifacts/BUILD-SPEC.md) Part A.
- **DEC-SBT-TRIGGER-MODEL** — pick trigger model A (deployment-count) / B (revenue) / C (hybrid). [docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md](docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md) §3.
- **DEC-AAR-STAGE-GATES** — set the stage-gate threshold values. [docs/strategy/development/after-acceleration-roadmap/BUILD-SPEC.md](docs/strategy/development/after-acceleration-roadmap/BUILD-SPEC.md).

## C. Operator-input — only you can fill (no spec substitutes)
- **Hours & rates** — fill the budget worksheet at [docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md](docs/strategy/development/staffing-budget-and-triggers/BUILD-SPEC.md) §2. This clears the two hard budget blocks (`GAP-NOD-HOURS-RATES`, `GAP-SBT-HOURS-RATES`).
- **Staffing go/no-go:** contract 4 segment domain experts (`GAP-CLL-DOMAIN-EXPERTS`), assign the independent security reviewer (`GAP-QSP-SECURITY-REVIEWER`), retain fractional legal counsel (`GAP-SCL-LEGAL-FIRST-LOI`), set onboarding triggers (`GAP-SBT-ONBOARD-NOW/-LATER`).
- **Capital Logic content:** author/validate the 5 launch cards + capture per-card status (`GAP-CLL-LAUNCH-CARDS`) — the schema is ready in [capital-logic-library spec](docs/features/capital-logic-library/BUILD-SPEC.md).

## D. Founder build — specs ready, your content fills them
- **Company ops** → [docs/strategy/development/company-operations-finance/BUILD-SPEC.md](docs/strategy/development/company-operations-finance/BUILD-SPEC.md): support triage + issue log (`GAP-COF-SUPPORT-TRIAGE`, block), entity hygiene, Node Care cadence, validation packet (with Victor).
- **White-glove service wrapper** → [docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md](docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md): `GAP-WGD-PLAYBOOK` (delta over `docs/white_glove_v0_1_beta.md`).
- **Node-readiness sequence** → [docs/strategy/development/node-on-desk-readiness/BUILD-SPEC.md](docs/strategy/development/node-on-desk-readiness/BUILD-SPEC.md): adopt the RG-1…RG-10 gate ladder (`GAP-NOD-SEQUENCE`).
- **Sales materials** → [docs/strategy/development/sales-contracting-legal/BUILD-SPEC.md](docs/strategy/development/sales-contracting-legal/BUILD-SPEC.md): one-pager / demo / segment framing / pipeline tracker (`GAP-SCL-SALES-MATERIALS`). Every claim must trace to Victor's claims register.
- **After-acceleration sequencing** → adopt the stage-gate structure (`GAP-AAR-SEQUENCING`) and set thresholds (B above).

## E. External-research approvals (rg03)
Approve or defer the consolidated external-research surface (funder refs · hardware SKU sheets · market rates · legal patterns · service/proof patterns). All are public-reference, no protected context. See [docs/strategy/development/RESEARCH-EXECUTION-SYNTHESIS-2026-06-12.md](docs/strategy/development/RESEARCH-EXECUTION-SYNTHESIS-2026-06-12.md). Nothing local-first is waiting on these.

## F. Pilots (later, post-build)
- `GAP-AAR-REPEATABILITY` — done-condition: a non-founder runs an install end-to-end.
- `GAP-AAR-SERVICE-PILOTS` — scoped grant-admin pilots with measured labor + reputational risk before hiring an admin lead.
