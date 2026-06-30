---
node_type: spec
is_session: false
status: candidate
boundary: INTERNAL — Mint is intended-not-shipped; foundry/moat are candidate
created: 2026-06-29
owner_next: sigil-development
authored_by: invoke (mode=define)
lineage:
  - refine run: development/refinement-runs/20260629T0000Z-cav2-mint-feature/RESULT.md
  - review: mint-design-plan-review (ledger; FIX verdict — fixes applied here)
note: Paths are repo-root-relative from domainspec-core/.
---

# Mint — SPEC (define)

## Purpose
**Mint** is a planned cav2-native capability that **mints a new domain-specialized repository**
from the cav2 framework: it composes the doc-tree scaffolder (`domainspec-new-repo`) and then
**casts the cav2 authority spine** (authority kinds, definitions tower, constitutions, promotion
lifecycle — the MOLD) onto a specific domain/research/project. Precedent (hand-done):
`resonantos-economy-research`.

## Contract — what a mint produces
A new repo containing:
1. the framework **partition/doc tree** + a clone-safe framework attach (from `domainspec-new-repo`);
2. a **domain authority-model** with domain-local authority **kinds** (proposed, owner-ratified — see Gates);
3. a domain **source-spine**, **promotion-policy** (ladder + gates), a domain **constitution**, and a **definitions** skeleton;
4. a **framework crosswalk** (per-concept borrow / block / analogy-only / promotion-candidate);
5. a **signed decision-gate record** (minting is a governance act, not a file drop);
6. (deferred) a cav2 **import surface** for two-way adopt-back.

## Inputs
| input | meaning |
|---|---|
| `domain` | the target domain/research/project name |
| `target-repo-path` | where the minted repo is created (sibling of domainspec-core) |
| `--source <framework-path>` | the framework half to attach (cav2 + DomainSpec + Arcanum) |
| `--attach submodule\|copy\|symlink` | clone-safe attach mode (default submodule) |

## Outputs (owned by the minted repo)
The minted repo's `authority/`, `definitions/`, `constitutions/`, `RELATED-FRAMEWORK-CROSSWALK.md`,
plus an `authority/decisions/<date>-mint.md` signed record. Mint itself remains the *authoring*
capability; the minted artifacts belong to the new repo's lifecycle.

## Boundaries / Gates (load-bearing)
- **D49 owner-gate (corrected per review C1).** A mint **proposes** the domain's authority kinds; the
  **cav2 authority owner ratifies**. The domain gets its *own* kinds table (a domain-local authority
  artifact); this is **not** a change to cav2's closed D49 enumeration (`authority/AUTHORITY-MODEL.md`).
- **Public/private (`BLK-CAV2-PUBLIC-PRIVATE-001`).** A mint that emits a *public-attached* repo is
  **blocked** until the public/private boundary is resolved. Arcanum is public; cav2/DomainSpec/Saturn private.
- **claim ≤ proof.** Mint is **intended-not-shipped**; it is *one casting organ* of the machine-map
  foundry, not the foundry. No stage may assume Saturn/the foundry/the moat is shipped.

## Inheritance / localization boundary (meta vs object)
A mint gives a domain repo a **base to grow on its own**: it **inherits the cav2 meta-authority
machinery** (the *how*) and **localizes the object authority** (the *what*). cav2 is **harvested
precedent**, not a governing parent (per `resonantos .../decisions/2026-06-29-method-authority-localized.md`).

| Inherited — the MOLD (how authority is made) | Localized — the casting (what this domain holds) |
|---|---|
| authority-lifecycle (`CAV2-D48`); the closure **rule** (`CAV2-D49`) applied to the domain's *own* table; non-collapse (D22/D29); claim ≤ proof (D38); build-from-owned (C17); the promotion-policy structure + source-movement + the Authority-Kinds-table **format** | the domain's own **kind rows**, definitions, constitution rules, source families, decisions |

- **Boundary test:** defines *how* authority is made → **inherit**; *what* authority the domain holds → **localize**.
- **Seed, don't bind:** the domain's tables are **seeded** from cav2's (a starting point) but owner-authored thereafter.
- **Circularity guardrail (machine-map `two-system-5s-recursion-boundary`):** never inherit cav2's *object* kinds as a governing base — that re-fuses meta and object (the mold becomes a casting of itself). claim ≤ proof: the two-System-5 grounding is a **candidate analogy, not a repo-cited fact** (open AUTHORITY-MAP/GOVERNANCE-ATTENUATION contradiction).

## Glossary
- **mint** — to cast the cav2 authority spine onto a domain, producing a new domain-specialized repo (a *casting* from the MOLD).
- **authority spine** — authority kinds + definitions tower + constitutions + promotion lifecycle (D48).
- **domain-local kinds table** — a minted repo's own authority-kinds enumeration; distinct from cav2's D49 enumeration.
- **scaffold half** — the ~30% doc-tree produced by `domainspec-new-repo`.
- **authority-casting half** — the ~70% governance act Mint owns (rough, by directory count — see RESULT/miner).

## Provenance
Design resolved by refine run `20260629T0000Z-cav2-mint-feature`; justification **re-grounded** here
per the `mint-design-plan-review` FIX verdict (the D49-alter and two-System-5 legs were cracked — see
ARCHITECTURE-BUNDLE §Re-grounded justification).
