# Stage 05 — Distill (coherent unit selection)

- Capability: `distill` · Mode: `standard`
- Status: **pass**

## Selected coherent unit (SCU)

**"Hover-prefill → click-capture → governed-apply, per element."**

The smallest unit that delivers the operator's Figma feel *without* breaking the studio's identity: the user hovers any element to see its real properties (observed), clicks to capture an intent against it, the comment persists and drains via the existing CLI cycle, the agent synthesizes a candidate, and the honest diff stays honest because unattributed/theme changes surface in the existing `null` bucket as a "visual-only" row.

## Pareto criteria (value ÷ cost)

| Capability | User value | Build cost | Keep in MVP? |
| --- | --- | --- | --- |
| Hover pre-fill from `getComputedStyle` (F2b) | High (the "Figma" feel) | Low (~25 LOC, one file, reuses message listener) | **Yes** |
| `null`-bucket "visual-only" diff row (F5) | High (dissolves the diff-lies tension) | Low (~10 LOC, bucket already exists) | **Yes** |
| In-page CSS expand/collapse + URL view-state (F4a) | Med-High (candidate readability) | Low-Med (~15 LOC + CSS + URL state) | **Yes** |
| Reuse immediate `/comment` + `listPendingComments` (F3a) | (table stakes) | ~0 (already built) | **Yes** |
| Comment-capture on untagged elements (odId:null) | Med | Low to capture | **Yes (capture only)** |
| Untagged-element **apply** (mint handle survives M1 fence) (F1a full) | Med | **High (fence redesign)** | **No — deferred** |
| Routed `/full/<label>` (F4b) | Low (vs CSS) | Med | No |
| Optimistic-local + server-sync (F3c) | Low (vs working sync) | Med | No |

## Rejected alternatives (recorded)

- **Pure annotate-any-element-and-apply (F1a).** Rejected for MVP: minted handles fail the M1 admission fence; making them survive is a fence redesign, not an MVP edit.
- **Computed-style as *canonical* (F2b unlabeled).** Rejected: pre-fill must be labelled *observed*, not canonical, to keep provenance honest (R2).
- **New "theme/global" change-class in the domain model (F5a/F5b).** Rejected vs surfacing the existing `null` bucket: less code, no model/test churn, already attributable.

## Recomposition target

This SCU recomposes into the full vision by later (1) making minted handles survive the fence (untagged apply), (2) optional routed full view, (3) optional descriptor/DNA-based extraction — each an independent follow-on, none required for the MVP loop to close.

## distill-frame → handed to s06 Design
