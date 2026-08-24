# Stage 08 — Critic Repair and Distill

Status: `repair-authored; planned witnesses not executed`

## Review result

Both independent critics returned `BLOCK` on the reviewed draft. The review
dispatch itself closed as `resolved`: the attacks completed, but the reviewed
target did not pass unchanged.

- The authority critic exposed an absent neutral-projection allowlist,
  caller-substitutable ownership, a derived-graph second writer, spoofable
  snapshot/provenance bindings, route/grant ambiguity, semantic upcast risk,
  and premature transport selection.
- The episode-integrity critic exposed duplicate supersession spelling,
  canonical-vocabulary conflict, mutable Task/VersionContext meaning, open
  status algebra, incomplete digest/recovery/revocation rules, and reducer
  versioning gaps.

The repairs are incorporated into [API-CONTRACT.md](../API-CONTRACT.md) and
[06-design.md](06-design.md). No critic was rerun because the confirmed
strategy capped the loop at one. The parent therefore performed a bounded
closure check against every persisted finding and converted the repairs into
explicit planned falsifiers.

## Repair map

| Finding family | Contract repair | Planned falsifier |
| --- | --- | --- |
| projection leakage | closed allowlist, manifest, view grant, leakage report | inject owner, path, policy, or prompt-role fields and require rejection |
| privilege confusion | disjoint route audiences; authorization before target parsing | send an append body through a read grant and require zero journal delta |
| episode hijack | immutable principal/workspace/vault/delegation binding | probe foreign episode ID and require opaque denial |
| mutable context | one-time Task/VersionContext dereference and inert snapshots/digests | mutate the source handles after open and require byte-stable replay |
| derived second writer | isolated episode overlay with closed record kinds | require zero canonical graph node/relation writes |
| supersession ambiguity | only `open_episode` plus overlay-only reference | reject second spelling and cycles; emit no `AKV-REL-022` |
| evidence rebinding | producer and target bindings resolved before append | cross-attempt, cross-task, revoked, or forged handles append nothing |
| ambiguous commit | atomic event/idempotency boundary and scoped recovery handle | crash before/after commit and recover deterministically |
| semantic upcast | semantic-effect-none receipts and no automatic Lesson | close an episode and require zero Task or Lesson semantic delta |
| reducer drift | version-keyed snapshots, exact order, digest chain, quarantine | gap/fork/shuffle/version drift fails closed |

## Distill unit check

The smallest coherent implementation unit is not one endpoint. It is the
contract-closed chain:

`neutral projection + command/event schemas + transition oracle + atomic journal + deterministic reducer + isolated overlay + capability adapters`.

Splitting below that boundary would leave either an ungoverned writer, an
unverifiable receipt, or a read model whose source semantics cannot be proven.
Transport and deployment split cleanly and remain deferred. Lesson review also
splits cleanly because the append route has no transition into verified Lesson.

Verdict: `pass for normal Plan at the authored contract level`, conditional on
the deterministic Design selection receipt. Runtime evidence remains
`planned_not_executed`.

