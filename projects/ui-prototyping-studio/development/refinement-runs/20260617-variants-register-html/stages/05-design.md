---
id: design-variants-register-html
run_id: 20260617-variants-register-html
step_id: s5-s8 (x-ray + tournament + dialectic + toy-game, consolidated)
capability_ref: distill+invoke+interrogation (inline)
updatedAt: 2026-06-17
---

# Design — variants register HTML ingestion

## §1 X-ray: where variant HTML flows (and where it dead-ends today)

```
TODAY (broken):
  studio variants generate|register <sid>
     -> generateVariants() [STUB]
        -> PrototypeVariant{ htmlArtifactRef: "/artifacts/.../a.html" }   ← DANGLING path, no body, no data-od-id
        -> store.saveVariants()
  ArtifactContentPort (readHtml/stageHtml/commitHtml)  ← EXISTS, used only by two-gate-apply; variants never enter it.
  => readHtml(htmlArtifactRef) === null. No real HTML anywhere. preview/annotate/mutation/M2 all starve.

TARGET (bridge the seam):
  studio variants register <sid> --label A --file a.html   (Claude Code wrote a.html with data-od-id)
     -> registerVariants({label, html})
        -> canonicalizeHtml(html)            [M0c, deterministic]
        -> VALIDATE data-od-id presence      [new server-side gate]  --reject--> OD_ID_MISSING
        -> stageHtml(canonical) -> commitHtml -> committedRef   [M0b, content-addressed]
        -> PrototypeVariant{ htmlArtifactRef: committedRef }
        -> store.saveVariants()
  => readHtml(htmlArtifactRef) returns real canonical HTML. preview/annotate/mutation/M2 all work.
```

**Finding:** the capability is a **bridge between two existing, disconnected pieces** (variant metadata ↔
the M0b content port), with M0c canonicalization and a new `data-od-id` gate in the middle. M0b + M0c +
the `PrototypeVariant.htmlArtifactRef` field all already exist — so this is wiring + one validation, not
new substrate.

## §2 Tournament — the ingestion interface

| Option | Shape | agent-ergonomics | determinism | scope-fit | verdict |
|--------|-------|------------------|-------------|-----------|---------|
| **A** | `register <sid> --label X --file path` (repeat per variant) | high — agent writes each HTML with the Write tool, then registers | high (file content hashed) | minimal (matches existing flag style) | **WINNER** |
| B | `register <sid> --from <dir>` (a.html/b.html/c.html) | high but implicit label↔file mapping | high | small convenience layer over A | **runner-up (optional sugar)** |
| C | stdin pipe (HTML or JSON per call) | medium — fiddly quoting for large HTML | high | new input mode | rejected (ergonomics) |
| D | manifest file (label→path+meta) | low — extra artifact for 1–3 variants | high | over-engineered | rejected (bloat) |

**Pareto pick: A** (`--label X --file path`, repeatable), with **B as optional sugar** later. Rationale:
A composes with the existing `parse()` flag style, is deterministic (file → canonical hash), and is the
minimal change. B is pure convenience over A; C/D add surface for no MVP gain.

## §3 Dialectic — who owns `data-od-id`?

- **P1 (agent-autonomy):** the SKILL already makes stamping the agent's duty; trust it (documentary only).
- **P2 (core-control):** the core must **validate `data-od-id` presence at register time** and **reject**
  HTML without it.

**Resolution — BOTH, and this is the *good mirror* of F2.** The agent stamps (SKILL duty, Quality bar M2)
**and** the core validates presence server-side and rejects (`OD_ID_MISSING`). The enforcement-honesty
principle (this session's #1 framework gap) says: don't claim a guarantee the core can't enforce — but
*do* enforce the ones it can. Unlike **identity** (F2, structurally unenforceable → documentary-only),
**`data-od-id` presence is structurally checkable**, so the core *should* own it as a real hard gate. This
turns M2 from a documentary Quality-bar line into an enforced admission check.

- **Convergence criterion:** a `register` call whose canonical HTML has **zero** `data-od-id` attributes
  (MVP coarse gate) → REJECT `OD_ID_MISSING`; HTML with ≥1 → admit. Residue: "annotatable component"
  is coarsely defined (≥1 od-id) for MVP; a per-component requirement (every structural element carries
  one) is a follow-up (`GAP-OD-ID-GRANULARITY`).

## §4 Toy-game (falsification before planning)

| Case | Input | Expected |
|------|-------|----------|
| GOOD | `<div data-od-id="card.root"><button data-od-id="cta.primary">Go</button></div>` | admit; `readHtml(ref)` returns canonical HTML; M2 pass |
| BAD  | `<div><button>Go</button></div>` (no od-id) | REJECT `OD_ID_MISSING`; nothing staged/committed |
| IDEMPOTENT | register the GOOD html twice | same committed hash (M0b idempotent-by-hash) |

This falsifies "the gate fires" and "registration is deterministic" cheaply, before building. It mirrors
the M1/C-1 fixture style (GOOD/BAD pairs).
