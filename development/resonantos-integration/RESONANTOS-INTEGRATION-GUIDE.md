---
tags: [resonantos, living-archive, cyberalchemy, integration-guide, governance]
node_type: guide
status: candidate
created: 2026-06-24
audience: resonantOS engineer (Living Archive)
boundary: scrubbed-for-external-teammate
---

# CyberAlchemy ↔ Living Archive — Integration Guide

*Audience: a resonantOS engineer who will wire this up. Practical and concrete.*

## What this is

**CyberAlchemy is the governance layer for your Living Archive's write side.** It is
**not** a replacement for the Living Archive. Your archive owns the *map* — "what's
here, what's still true, how confident, how useful." CyberAlchemy owns the *decision* —
"may the archive **rely** on this? who decided? is it promoted?"

Think of it as: the Living Archive remembers everything; CyberAlchemy decides what's
allowed to govern future work. The read path stays entirely yours. The write/decision
path is where we plug in.

## What CyberAlchemy is, and how it relates

- **Living Archive vs governance layer.** The Living Archive is the memory substrate and
  owns the map. CyberAlchemy owns the **governed store** (the write target) plus the
  **decisions** about it. We deliberately do *not* duplicate your fact-over-time
  machinery — validity windows, supersession, per-edge confidence/utility, contradiction
  resolution. Those stay yours; we read them, we don't rebuild them.
- **Capture vs governed-write.** *Capture* = recording evidence. Everything captured enters
  as `status: candidate` and never short-circuits into something trusted. *Governed-write*
  = promoting a candidate into something the system relies on. These are two distinct steps,
  and the gap between them is the whole point.
- **Promotion / Review Queue.** Promotion is explicit, owner-routed, and gated. It is
  **default-deny**: anything not explicitly enumerated stays blocked until a decision adds
  it. Your **Review Queue** *is* this promotion ladder — we map onto it, we don't add a
  parallel one.
- **Authority-triage front door.** Every intake passes one question — "does writing this
  govern future work?" — and routes to the **narrowest responsible owner**.
- **Scope-tags.** Each record carries exactly one scope: `user-memory`,
  `project-instructions`, `runtime-rules`, or `knowledge-store`. The queue reads per scope.
  One intake port spans many substrates by **tagging**, never by melting them together.
- **Saturn & DomainSpec.** CyberAlchemy is the authority spine under two further efforts —
  **Saturn** (a convergence loop closing intent↔reality with evidence) and **DomainSpec**
  (a typed-intent layer). Both are **intended, not shipped** — please treat them as
  direction, not as available product. Posture throughout: AI augments human work, it does
  not replace it.

## Wiring section — the exact hooks to attach to

Everything below already exists in your manifest/SDK. The honest exception is called out.

**Capabilities** (from `public/addons/living-archive.json`):
- `archive-read` (`shared`, hard-stop) — read scopes `active-memory/context`,
  `system-memory/context`.
- `memory-provider` (`scope:"system"`, hard-stop) — the system provider slot.
- `archive-intake-write` (`scope:"intake-only"`, hard-stop) — **the governed-write seam**;
  `intakeWriteScopes: ["Memory/INTAKE"]`, `canRequestIngest:true`,
  `canWriteKnowledgePages:false`.

**Surfaces:**
- `living-archive-workspace` (page) — read/lookup + provider management.
- `living-archive-review` (panel, "Review Queue") — the promotion gate surface.

**MCP tools** (`examples/living-archive-mcp.mjs`):
- READ → `living_archive_search`, `living_archive_read`. We attach **capture** and
  **lookup** here. No governance needed on this side.
- GOVERNED-WRITE IN → `living_archive_write_intake` (lands in `INTAKE/mcp/*`),
  `living_archive_request_ingest` (queues into `INTAKE/review-queue/`). Intake-only by
  contract — it physically cannot write trusted pages, which is exactly the property we want.
- PROMOTION GATE → `living_archive_decide_review` (action enum **approve / reject /
  escalate**), `living_archive_promote_review_artifact` (the only MCP path to trusted
  knowledge writes).

**Honest gap — the piece to IMPLEMENT.** In the example code, the portable service
**returns HTTP 501** for `process-ingest-request`, `decide-review`, and
`promote-review-artifact` ("Trusted wiki writes require Strategist-owned ingest/review
inside the desktop host"), and policy pins `canWriteKnowledgePages:false`. The contract,
tool name, proxy boundary, and 501 reason string are **yours** (already shipped) — what
CyberAlchemy supplies is only the **trusted-write provider *body* behind your named
`promote_review_artifact` seam**, not a parallel promotion path. The read + intake +
review-queue seam is built and tested; the promotion executor is the host-side body we
implement behind that 501 boundary. We are not claiming a turnkey drop-in.

**Concrete round-trip:**
1. **Intake** — agent calls `living_archive_write_intake` (or `request_ingest`); record
   lands in `INTAKE/*` with `status: candidate`, scope-tag stamped.
2. **Review** — record appears in the `living-archive-review` Review Queue
   (`living_archive_review_queue`).
3. **Decide** — owner calls `living_archive_decide_review` → **approve / reject /
   escalate**.
4. **Promote** — on approve, `living_archive_promote_review_artifact` runs the host-side
   trusted-write provider (the piece we implement) → fact enters trusted memory.
5. **Lookup** — `living_archive_search` / `living_archive_read` now return the promoted
   fact through your existing read path.

## Scope-tag discipline + lifecycle mapping

Every intake carries exactly one scope-tag (`user-memory` / `project-instructions` /
`runtime-rules` / `knowledge-store`); the queue reads per scope and never melts them.

The candidate → review → promote lifecycle maps **directly** onto your Review Queue plus
the `decide_review` enum:

| cav2 lifecycle stage | Living Archive mechanism |
|---|---|
| `candidate` (captured, not relied on) | record in `INTAKE/*` / Review Queue |
| review (owner-routed, gated) | `living-archive-review` panel + `decide_review` |
| approve | promote → trusted write |
| reject | record stays candidate / dropped |
| escalate | route to narrower/higher owner |

Default-deny holds: nothing reaches trusted memory without an explicit approve.

## Install / dogfood path + first slice

Smallest-first. Recommended **first slice: a read-only observer/meter** — attach only to
`living_archive_search`/`read` and the `living-archive-workspace` page, and *measure*
intake/lookup traffic. No writes, no promotion, no host provider needed yet. This proves
the seam and produces the governed-run data with zero risk.

Then, in order: (1) wire `write_intake` + `request_ingest` with scope-tagging; (2) surface
candidates in the Review Queue and exercise `decide_review`; (3) implement the host-side
promotion provider behind `promote_review_artifact`. Running resonantOS as the first host
is itself the dogfood: the governed runs it generates are the data we use to build the SDK.

## Boundary note

This guide describes the governance model only. It intentionally omits internal mechanics
(engine internals, layer maps, the capture harness's internals) — ask if you need
something it doesn't cover, and we'll scope what can be shared.
