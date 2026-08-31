# Validation Matrix

## Required Evidence

| Area | Positive controls | Negative controls | Required claim |
| --- | --- | --- | --- |
| Material state | Empty proposal retains its deferred meaning; nonempty staged candidate uses the W0-accepted distinct non-authorizing outcome; exact apply-approved material retains its ready meaning. | Invalid mode/state/version pair; staged candidate with approval; empty staged candidate; apply material without exact approval; unknown candidate token treated as approved; single-axis or single-verdict consumer; staged receipt consumed as mutation-ready. | Candidate bytes can be validated without apply authority, existing meanings do not drift, and legacy consumers fail closed. |
| Material integrity | Exact sources, outputs, targets, dependencies, mirrors, owners, and publication classes agree. | Missing/stale/empty output; path or symlink escape; owner/publication escape; missing dependency; mirror drift; extra/missing target. | `pass` binds the exact declared bytes and full target inventory. |
| JSON postimage | Valid JSON and JSON Pointer assertions pass. | Invalid JSON; missing pointer; wrong equals/not-equals/absent result; declared kind mismatch. | JSON semantics are evaluated only as declared. |
| YAML-file postimage | A YAML path explicitly declared `utf8-text` passes literal assertions. If structural YAML is selected, its pinned safe parser/version and JSON-compatible subset also pass. | Filename-based inference; unowned parser; parser/version drift; custom tag or non-JSON-compatible value; wrong assertion; kind mismatch. | YAML is never parsed as JSON, and structural parsing is never added implicitly. |
| Markdown/text postimage | UTF-8 literal equals/contains/not-contains assertions pass. | Invalid UTF-8; missing literal; forbidden literal present; incompatible operator; hygiene failure. | Text lifecycle wording is evaluated without JSON parsing. |
| Requested effect | Base request, manifest, and eligibility digest represent the same canonical effect; the separately reachable late regression passes against the v3 representation. | Missing base effect; target, owner, write ceiling, allowed/forbidden effect, or lifecycle state differs; non-canonical set-like order; recomputed request digest over a tampered embedded effect. | Owner request emission and later validation are bound to the frozen effect by canonical replay. |
| Stage graph | All independent reachable stages run; dependents wait for declared predecessors. | Unknown dependency; cycle; later stage falsely PASS after upstream block; reachable stage omitted. | Every declared stage has a truthful result. |
| Exit propagation | First nonzero status is returned while later reachable blockers are retained. | Later success or cleanup masks the first failure; early break hides another independent failure. | Complete blocker set and correct process status coexist. |
| Actual material consumer | Real validator consumes the exact package and filesystem transition twice and emits deterministic isolated receipts. | `--help`; different valid package; stale package; target/ref mismatch; create/present or update/absent mismatch; plan-baseline drift; zero exit/no receipt; invalid receipt. | Consumer presence and equal output bytes cannot substitute for validation of the authorized transition. |
| Full lifecycle | Synthetic JSON/Markdown/YAML-file candidate crosses proposal, staged closure, independent review, and request emission twice byte-stably on canonical bytes; the existing Task Session live-entry fixture consumes the v3 request graph through its declared wrapper. | Any recorded negative blocks before request emission; request replay after executable drift blocks; a stale fixture filename or incomplete downstream dependency set fails. | The smallest complete no-effect vertical slice works and remains consumable at the actual downstream test boundary. |
| Generated packaging/parity | A separate authorized sync makes canonical and generated Codex/Claude Invoke surfaces byte-equivalent. | Direct generated edit, unrelated generated replacement, or stale generated file. | Packaging is a declared mutation after canonical verification, and runtime packages project the reviewed behavior. |
| Private/public boundary | All public fixtures are synthetic and contain no Body War prose/data. | Private path/content copied into public Arcanum package. | The repair is reusable without leaking private project material. |

## Body War Revalidation Boundary

After the canonical repair is separately accepted and installed, the Body War
continuation may regenerate its material-package receipt, closure manifest, closure
receipt, independent review, and owner request against the repaired executable refs.
That private rehearsal must preserve the existing candidate postimage digests or
treat any changed postimage as a new candidate.

It still must report these separate gaps as `not_evaluable` until their own contracts
exist:

- exact WPRA task/SWU target paths and validation contracts;
- Implementation Readiness selection/admission evidence;
- Strava credentials and live provider evidence;
- deployment receipt;
- privacy-owner decision;
- geometry and scoring work.

Passing this matrix cannot supply those facts.
