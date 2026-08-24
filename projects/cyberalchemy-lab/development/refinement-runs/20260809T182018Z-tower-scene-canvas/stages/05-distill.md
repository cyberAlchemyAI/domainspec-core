# 05 — Distill selected vertical slice

## Selected unit

**One locked synthetic tower, three evidence scenes, two named axes.**

Input is the existing L0 read model. Output is a new, local **Tower Scene Manifest** consumed by the page. The manifest has one tower descriptor (`tower:toy`) and three evidence-progression scenes. It may also carry a separately namespaced Tower System atlas whose non-realized entries are always unavailable explanatory panels.

## Minimum scene descriptor

```text
TowerSceneDescriptor {
  tower_id, title, semantic_axis, level_id, scene_kind,
  evidence_state, implementation_status, source_refs,
  claim_ceiling, content, unavailable_reason,
  interaction_contract: "read-only", reduced_motion_mode
}
```

## Negative control / toy game

Create a manifest entry that omits `source_refs` or has `semantic_axis: "bare-L1"`. The loader must reject it, and the page must render its unavailable state rather than a live-looking scene. This prevents visual polish from silently becoming a semantic claim.

## Recomposition path

The same manifest supports later towers only after a new locked projection exists per tower. It does not itself select, ingest, promote, or validate those towers.
