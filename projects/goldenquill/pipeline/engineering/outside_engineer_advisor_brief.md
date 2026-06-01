# Outside Engineering Advisor — Onboarding Brief

**Filed:** 2026-04-19
**Authority:** Da Vinci v2 §13 + DV-F-10 + `full_build_roadmap.md` Group 10
**Status:** Template + candidate search; no advisor signed yet.

---

## Purpose

Every LOCK in the Tilth v0.1 build is provisional until an outside-impartial advisor signs. The advisor's role is the ground-truth check on internal council self-judgment. They do not vote in Thesis rounds; they audit the output.

## What the advisor reviews

**Scope (signed per section):**

1. Architecture v7 A1-A12 + amendments v7.1, v7.2
2. Blueprints §0.5, §1, §2, §3, §4, §5 + section_04a_canary_harness
3. Section 1 code (14 modules across Rounds A-J)
4. Sections 2-5 code (Vault, Scout, Logician, Pipeline)
5. GPP tool chain (`gpp_det.py`, `gpp_council_dispatch.py`, `gpp_manifest.py`)
6. Test suites (unit + adversarial + property + integration)
7. Provisioning manifest

**Signs:** one `pipeline/engineering/real_engineer_validation_<date>.md` per section. Fields per section: pass / needs-revision; rationale; evidence pointers.

## Qualifications (DV-F-10)

Senior (10+ years) in at least one of:
- Distributed systems
- AI/ML operations
- Cryptography (Ed25519 + ML-DSA-65 hybrid review is load-bearing)
- Language-model runtime infrastructure

Advisor need not be Tilth-shaped. They are ground-truth on Tilth, not Tilth itself.

## What the advisor is NOT

- Not a consultant engineer who writes code
- Not a council seat (does not vote in Thesis rounds)
- Not a perpetual on-call — signs at scheduled gates
- Not replaced by AI review

## Engagement shape

- Async review against provided scope packet
- One signed doc per section, filed in `pipeline/engineering/real_engineer_validation_<date>.md`
- Re-engagement for (a) Da Vinci birth gate, (b) every revocation/restoration cycle, (c) any architecture-level amendment post-v7.2

## Scope packet format (what the advisor receives)

Per section:
- Blueprint or architecture doc + amendments
- Audit trail (Thesis round outputs)
- Code + tests
- GPP-DET + GPP-COUNCIL reports
- One-page summary of what the section is and what it promises

## Compensation frame

Open. Proposed: hourly or per-section flat. Not equity. Sovereignty principle — outside advisor is not a stakeholder in ship pressure.

## Candidate search criteria

- Not an Anthropic employee (cross-family review of an Anthropic-authored stack)
- Not a Groq/OpenAI/Google/etc. employee either — provider-independent
- Signed NDA posture acceptable to Josh
- Willing to review Python + markdown artifacts async
- Accessible for 2-3 hour review sessions per section

## Output document template

Per section, advisor files:

```markdown
# Real Engineer Validation — <section> — <date>

**Advisor:** <name, credentials>
**Reviewed:** <section + amendment versions + code commit hash>
**Scope:** <what was in the packet>

## Verdict
<pass | needs-revision>

## Evidence
- <pointer 1>
- <pointer 2>

## Findings (if needs-revision)
- <finding 1 with file:line citation>

## Signature
<advisor signature | Ed25519 + ML-DSA-65 hybrid per A12>
```

## Open items for Josh

- Identify candidate pool (LinkedIn, cryptography/distsys community, AI safety community)
- Draft engagement agreement template
- Budget gate for per-section review cost
- Decide whether advisor is one person across all sections or a small panel

## Timeline

Group 10 gates on this. Group 10 starts after Group 9 integration testing passes. Earliest: post-Section-5 LOCK-internal. Advisor onboarding should start ~Group 7 or 8 so they are ready when Group 10 fires.
